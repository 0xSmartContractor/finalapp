'use client'

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Sparkles, 
  Clock,
  Brain 
} from 'lucide-react';
import { Button } from '@/components/ui/button';

const recipePurposes = [
  "Quick Weeknight Dinners",
  "Gourmet Date Nights",
  "Healthy Meal Prep",
  "Kid-Friendly Lunches",
  "Vegan Desserts",
  "High-Protein Breakfasts",
  "Gluten-Free Snacks",
  "Keto-Friendly Meals"
];

const FlowingLines = () => (
  <svg
    className="absolute inset-0 w-full h-full opacity-[0.03] pointer-events-none"
    viewBox="0 0 1200 800"
    xmlns="http://www.w3.org/2000/svg"
  >
    {/* SVG paths omitted for brevity */}
  </svg>
);

export default function HeroSection() {
  const [currentPurpose, setCurrentPurpose] = useState(recipePurposes[0]);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentPurpose(prev => {
        const currentIndex = recipePurposes.indexOf(prev);
        return recipePurposes[(currentIndex + 1) % recipePurposes.length];
      });
    }, 3000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-black relative flex flex-col items-center justify-center overflow-hidden">
      <FlowingLines />
      
      <div className="container mx-auto px-4 relative">
        <div className="max-w-5xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex justify-center mb-8"
          >
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-[#111111] border border-[#222222]">
              <span className="w-2 h-2 rounded-full bg-lime-500 animate-pulse" />
              <span className="text-[#FAFAFA] text-sm font-medium tracking-wide">
                NOW IN BETA
              </span>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center mb-16"
          >
            <h1 className="text-5xl sm:text-6xl md:text-7xl font-bold mb-6">
              <span className="text-white">AI-Powered Recipes for</span>
              <br />
              <AnimatePresence mode="wait">
                <motion.div
                  key={currentPurpose}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  transition={{ duration: 0.5 }}
                >
                  <span className="text-transparent bg-clip-text bg-gradient-to-r from-lime-500 via-lime-400 to-emerald-500 leading-[1.4] inline-block">
                    {currentPurpose}
                  </span>
                </motion.div>
              </AnimatePresence>
            </h1>
            <p className="text-xl sm:text-2xl mb-12 text-gray-300">
              Cuizine creates personalized recipes for any purpose, dietary need, or occasion.
              Just tell us what you need.
            </p>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
              className="flex justify-center mb-16"
            >
              <div className="relative group">
                <div className="absolute -inset-0.5 bg-gradient-to-r from-lime-500 to-emerald-500 rounded-lg blur opacity-20 group-hover:opacity-100 transition duration-1000 group-hover:duration-200" />
                <Button className="relative px-8 py-4 bg-lime-500 rounded-lg group-hover:bg-lime-400 transition-colors duration-200">
                  <span className="font-semibold text-black text-lg">
                    Start Creating
                  </span>
                </Button>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.5 }}
              className="grid grid-cols-3 gap-8 max-w-2xl mx-auto"
            >
              {[
                { icon: Sparkles, text: "AI-Powered" },
                { icon: Clock, text: "Quick Generation" },
                { icon: Brain, text: "Personalized" }
              ].map(({ icon: Icon, text }, index) => (
                <div
                  key={index}
                  className="flex flex-col items-center gap-3"
                >
                  <div className="w-12 h-12 rounded-full bg-lime-500/10 flex items-center justify-center">
                    <Icon className="w-6 h-6 text-lime-500" />
                  </div>
                  <span className="text-[#888888] text-sm font-medium">
                    {text}
                  </span>
                </div>
              ))}
            </motion.div>
          </motion.div>
        </div>
      </div>
    </div>
  );
}