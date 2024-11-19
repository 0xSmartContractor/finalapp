'use client'

import { useState } from 'react'
import Link from 'next/link'
import { motion, AnimatePresence } from 'framer-motion'
import { Button } from "@/components/ui/button"
import { Menu, X, ChefHat } from 'lucide-react'
import { useAuth, useClerk, useUser } from '@clerk/nextjs'

export default function Navbar() {
  const { user } = useUser()
  const { openSignIn, openSignUp } = useClerk()
  const [isOpen, setIsOpen] = useState(false)
  const { signOut } = useAuth()

  const navItems = [
    { name: 'Features', href: '#features' },
    { name: 'Pricing', href: '#pricing' },
    { name: 'Recipes', href: '/recipes' },
    { name: 'About', href: '/about-us' },
    { name: 'Store', href: '/store' },
    { name: 'Contact', href: '#contact' },
  ]

  return (
    <nav className="fixed w-full z-50 transition-all duration-300 bg-lime-500/90 backdrop-blur-sm border-b border-[#222222]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex-shrink-0">
            <Link href={user ? "/dashboard" : "/"} className="flex items-center space-x-2 text-[#111111] font-bold text-xl">
              <ChefHat className="w-6 h-6" />
              <span>Cuizine</span>
            </Link>
          </div>
          
          {/* Desktop Nav Links */}
          <div className="hidden md:flex items-center justify-center flex-grow">
            {navItems.map((item) => (
              <Link
                key={item.name}
                href={item.href}
                className="text-[#222222] hover:text-black px-3 py-2 rounded-md text-sm font-semibold transition-colors duration-200"
              >
                {item.name}
              </Link>
            ))}
          </div>

          {/* Sign In / Sign Up Buttons */}
          <div className="hidden md:flex items-center space-x-4">
            {user ? (
              <Button onClick={() => signOut()} className="bg-red-500 hover:bg-red-600 text-white font-semibold">
                Sign Out
              </Button>
            ) : (
              <>
                <Button
                  variant="ghost"
                  className="text-[#222222] hover:text-black font-semibold"
                  onClick={() => openSignIn()}
                >
                  Log in
                </Button>
                <Button
                  className="bg-[#111111] hover:bg-[#222222] text-lime-500 font-semibold"
                  onClick={() => openSignUp()}
                >
                  Sign up
                </Button>
              </>
            )}
          </div>
          
          {/* Mobile Menu Button */}
          <div className="md:hidden">
            <Button 
              variant="ghost" 
              onClick={() => setIsOpen(!isOpen)} 
              aria-label="Toggle menu"
              className="text-[#222222] hover:text-black hover:bg-transparent focus:bg-transparent active:bg-transparent"
            >
              {isOpen ? (
                <X className="h-6 w-6" />
              ) : (
                <Menu className="h-6 w-6" />
              )}
            </Button>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3 }}
            className="md:hidden bg-lime-500/90 backdrop-blur-sm border-t border-[#222222]"
          >
            <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
              {navItems.map((item) => (
                <Link
                  key={item.name}
                  href={item.href}
                  className="text-[#222222] hover:bg-[#111111] hover:text-lime-500 block px-3 py-2 rounded-md text-base font-semibold transition-colors duration-200"
                  onClick={() => setIsOpen(false)}
                >
                  {item.name}
                </Link>
              ))}
              {user ? (
                <Button 
                  onClick={() => {
                    signOut()
                    setIsOpen(false)
                  }} 
                  className="w-full bg-red-500 hover:bg-red-600 text-white font-semibold mt-2"
                >
                  Sign Out
                </Button>
              ) : (
                <>
                  <Button
                    variant="ghost"
                    className="w-full text-[#222222] hover:bg-[#111111] hover:text-lime-500 font-semibold"
                    onClick={() => {
                      setIsOpen(false)
                      openSignIn()
                    }}
                  >
                    Log in
                  </Button>
                  <Button
                    className="w-full bg-[#111111] hover:bg-[#222222] text-lime-500 font-semibold mt-2"
                    onClick={() => {
                      setIsOpen(false)
                      openSignUp()
                    }}
                  >
                    Sign up
                  </Button>
                </>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </nav>
  )
}