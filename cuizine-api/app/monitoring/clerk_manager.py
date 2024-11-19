import asyncio
import signal
import os
from typing import List, Dict
from datetime import datetime, time
import requests
import logging
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path

# Create necessary directories
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # Gets the project root
LOGS_DIR = BASE_DIR / "logs"
METRICS_DIR = BASE_DIR / "metrics"

LOGS_DIR.mkdir(exist_ok=True)
METRICS_DIR.mkdir(exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOGS_DIR / "clerk_updates.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('clerk_manager')

class ClerkSubscriptionManager:
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {os.getenv('CLERK_SECRET_KEY')}",
            "Content-Type": "application/json"
        }
        self.is_running = False

    def get_all_users(self) -> List[Dict]:
        try:
            response = requests.get(
                "https://api.clerk.com/v1/users",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching users: {e}")
            return []

    def update_user_metadata(self, user: Dict) -> bool:
        try:
            current_metadata = user.get('public_metadata', {})
            subscription_tier = current_metadata.get('subscription_tier', 'free')
            
            new_recipe_count = {
                'free': 5,
                'pro': 100,
                'premium': 100
            }.get(subscription_tier, 5)
            
            new_metadata = {
                **current_metadata,
                'recipes_remaining': new_recipe_count,
                'recipes_generated': 0,
                'last_reset': datetime.utcnow().isoformat()
            }

            response = requests.patch(
                f"https://api.clerk.com/v1/users/{user['id']}/metadata",
                headers=self.headers,
                json={"public_metadata": new_metadata}
            )
            response.raise_for_status()
            logger.info(f"Successfully reset user {user['id']} ({subscription_tier})")
            return True
        except Exception as e:
            logger.error(f"Error updating user {user['id']}: {e}")
            return False

    async def monthly_reset(self):
        """Perform monthly reset of recipe counts"""
        logger.info("Starting monthly reset")
        try:
            users = self.get_all_users()
            
            with ThreadPoolExecutor(max_workers=5) as executor:
                results = list(executor.map(self.update_user_metadata, users))
            
            success_count = sum(1 for r in results if r)
            logger.info(f"Reset complete: Updated {success_count}/{len(users)} users")
            
            # Save reset metrics
            metrics = {
                'timestamp': datetime.utcnow().isoformat(),
                'total_users': len(users),
                'successful_updates': success_count,
                'failed_updates': len(users) - success_count
            }
            
            os.makedirs('metrics', exist_ok=True)
            with open('metrics/last_reset.json', 'w') as f:
                json.dump(metrics, f, indent=2)
                
        except Exception as e:
            logger.error(f"Critical error during reset: {e}")
            raise

    def stop(self):
        """Stop the scheduler"""
        self.is_running = False
        logger.info("Scheduler stopping...")

    async def run_scheduler(self):
        """Run the scheduler with proper shutdown handling"""
        self.is_running = True
        logger.info("Scheduler started")
        
        while self.is_running:
            now = datetime.now()
            
            # Calculate time until next check
            if now.hour == 0 and now.minute == 0 and now.day == 1:
                try:
                    await self.monthly_reset()
                except Exception as e:
                    logger.error(f"Reset failed: {e}")
                # Wait an hour after reset attempt to prevent multiple runs
                await asyncio.sleep(3600)
            else:
                # Calculate time until next check (every minute)
                await asyncio.sleep(60)

async def shutdown(signal, loop, manager):
    """Cleanup tasks tied to the service's shutdown."""
    logger.info(f"Received exit signal {signal.name}...")
    
    manager.stop()
    
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    [task.cancel() for task in tasks]
    
    logger.info(f"Cancelling {len(tasks)} outstanding tasks")
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()

def handle_exception(loop, context):
    msg = context.get("exception", context["message"])
    logger.error(f"Caught exception: {msg}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Clerk Subscription Manager')
    parser.add_argument('--reset-now', action='store_true', help='Run reset immediately')
    parser.add_argument('--schedule', action='store_true', help='Start the scheduler')
    
    args = parser.parse_args()
    manager = ClerkSubscriptionManager()

    if args.reset_now:
        asyncio.run(manager.monthly_reset())
    elif args.schedule:
        loop = asyncio.get_event_loop()
        loop.set_exception_handler(handle_exception)
        
        # Add signal handlers for graceful shutdown
        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(
                sig,
                lambda s=sig: asyncio.create_task(shutdown(s, loop, manager))
            )
        
        try:
            loop.run_until_complete(manager.run_scheduler())
        finally:
            loop.close()
            logger.info("Successfully shutdown the scheduler.")
    else:
        parser.print_help()