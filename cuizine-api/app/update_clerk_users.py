import os
import requests
from typing import List, Dict
import json
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv

load_dotenv()

CLERK_SECRET_KEY = os.getenv('CLERK_SECRET_KEY')
BASE_URL = "https://api.clerk.com/v1"

class ClerkBulkManager:
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {CLERK_SECRET_KEY}",
            "Content-Type": "application/json"
        }

    def get_all_users(self) -> List[Dict]:
        """Fetch all users from Clerk"""
        try:
            response = requests.get(
                f"{BASE_URL}/users",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching users: {e}")
            return []

    def update_user_metadata(self, user_id: str, metadata: Dict) -> bool:
        """Update a single user's metadata"""
        try:
            response = requests.patch(
                f"{BASE_URL}/users/{user_id}/metadata",
                headers=self.headers,
                json={"public_metadata": metadata}
            )
            response.raise_for_status()
            print(f"Successfully updated user {user_id}")
            return True
        except Exception as e:
            print(f"Error updating user {user_id}: {e}")
            return False

    def bulk_update_metadata(self, metadata: Dict):
        """Update all users with the same metadata"""
        users = self.get_all_users()
        success_count = 0
        
        print(f"Found {len(users)} users to update")
        
        # Using ThreadPoolExecutor for parallel updates
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [
                executor.submit(self.update_user_metadata, user['id'], metadata)
                for user in users
            ]
            
            for future in futures:
                if future.result():
                    success_count += 1

        print(f"\nUpdate Complete:")
        print(f"Successfully updated: {success_count}/{len(users)} users")
        return success_count

def main():
    # Default metadata for all users
    default_metadata = {
        "subscription_tier": "free",
        "role": "user",
        "recipes_remaining": 5,
        "recipes_generated": 0,
        "subscription_status": "active"
    }
    
    manager = ClerkBulkManager()
    
    # List current users and their metadata first
    print("\nCurrent Users:")
    users = manager.get_all_users()
    for user in users:
        print(f"\nUser ID: {user['id']}")
        print(f"Email: {user.get('email_addresses', [{}])[0].get('email_address', 'No email')}")
        print(f"Current metadata: {json.dumps(user.get('public_metadata', {}), indent=2)}")

    # Confirm before updating
    if input("\nDo you want to update all users with default metadata? (y/n): ").lower() == 'y':
        manager.bulk_update_metadata(default_metadata)
    else:
        print("Update cancelled")

if __name__ == "__main__":
    main()