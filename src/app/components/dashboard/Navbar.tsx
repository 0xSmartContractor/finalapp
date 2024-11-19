'use client'

import { useState } from 'react';
import Link from 'next/link';
import { useClerk} from '@clerk/nextjs';
import { Button } from "@/components/ui/button";
import { ChefHat } from 'lucide-react';

export default function DashboardNavbar() {
  const { signOut } = useClerk();
  const [isOpen, setIsOpen] = useState(false);

  const dashboardNavItems = [
    { name: 'Dashboard', href: '/dashboard' },
    { name: 'Recipes', href: '/dashboard/recipes' },
    { name: 'Meal Planning', href: '/dashboard/meal-planning' },
    { name: 'Settings', href: '/dashboard/settings' },
  ];

  return (
    <nav className="fixed w-full z-50 transition-all duration-300 bg-lime-500/90 backdrop-blur-sm border-b border-[#222222]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex-shrink-0">
            <Link href="/dashboard" className="flex items-center space-x-2 text-[#111111] font-bold text-xl">
              <ChefHat className="w-6 h-6" />
              <span>Cuizine</span>
            </Link>
          </div>

          {/* Desktop Nav Links */}
          <div className="hidden md:flex items-center justify-center flex-grow">
            {dashboardNavItems.map((item) => (
              <Link
                key={item.name}
                href={item.href}
                className="text-[#222222] hover:text-black px-3 py-2 rounded-md text-sm font-semibold transition-colors duration-200"
              >
                {item.name}
              </Link>
            ))}
          </div>

          {/* Sign Out Button */}
          <div className="hidden md:flex items-center space-x-4">
            <Button
              onClick={() => signOut()}
              className="bg-[#111111] hover:bg-[#222222] text-lime-500 font-semibold"
            >
              Sign Out
            </Button>
          </div>

          {/* Mobile Menu Button */}
          <div className="md:hidden">
            <Button
              variant="ghost"
              onClick={() => setIsOpen(!isOpen)}
              aria-label="Toggle menu"
              className="text-[#222222] hover:text-black hover:bg-transparent focus:bg-transparent active:bg-transparent"
            >
              <svg
                className="h-6 w-6"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 6h16M4 12h16M4 18h16"
                />
              </svg>
            </Button>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      {isOpen && (
        <div className="md:hidden bg-lime-500/90 backdrop-blur-sm border-t border-[#222222]">
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
            {dashboardNavItems.map((item) => (
              <Link
                key={item.name}
                href={item.href}
                className="text-[#222222] hover:bg-[#111111] hover:text-lime-500 block px-3 py-2 rounded-md text-base font-semibold transition-colors duration-200"
                onClick={() => setIsOpen(false)}
              >
                {item.name}
              </Link>
            ))}
            <Button
              onClick={() => signOut()}
              className="w-full bg-[#111111] hover:bg-[#222222] text-lime-500 font-semibold mt-2"
            >
              Sign Out
            </Button>
          </div>
        </div>
      )}
    </nav>
  );
}