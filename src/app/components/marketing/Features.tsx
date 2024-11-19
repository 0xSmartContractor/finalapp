'use client'

import React from 'react'
import { motion } from 'framer-motion'
import { Sparkles, Utensils, Clock, Brain, ChefHat, Users } from 'lucide-react'

const FeatureCard = ({ title, description, icon: Icon, delay }: { 
  title: string, 
  description: string, 
  icon: React.ElementType, 
  delay: number 
}) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    whileInView={{ opacity: 1, y: 0 }}
    viewport={{ once: true }}
    transition={{ duration: 0.5, delay }}
    className="relative group"
  >
    <div className="absolute -inset-0.5 bg-gradient-to-r from-lime-500 to-emerald-500 rounded-2xl blur opacity-0 group-hover:opacity-20 transition duration-1000" />
    <div className="relative bg-[#111111] border border-[#222222] rounded-2xl p-6 hover:border-lime-500/20 transition-colors duration-200">
      <div className="flex items-center gap-4 mb-4">
        <div className="p-2 bg-lime-500/10 rounded-lg">
          <Icon className="h-6 w-6 text-lime-500" />
        </div>
        <h3 className="text-xl font-semibold text-white">{title}</h3>
      </div>
      <p className="text-gray-400">{description}</p>
    </div>
  </motion.div>
)

export default function FeaturesSection() {
  return (
    <section className="relative bg-black pb-24 overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-b from-black via-black to-transparent" />
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_bottom,_var(--tw-gradient-stops))] from-lime-500/10 via-[#111111] to-[#111111]" />

      <div className="container mx-auto px-4 relative z-10 pt-24">
        <div className="max-w-3xl mx-auto text-center mb-12 sm:mb-20">
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-3xl sm:text-4xl md:text-5xl font-bold mb-4 sm:mb-6 text-white"
          >
            Revolutionize Your{' '}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-lime-500 via-lime-400 to-emerald-500">
              Cooking Experience
            </span>
          </motion.h2>
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2 }}
            className="text-base sm:text-lg md:text-xl text-gray-400"
          >
            Discover how Cuizine combines AI technology with culinary expertise to transform your kitchen adventures.
          </motion.p>
        </div>

        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          <FeatureCard
            icon={Brain}
            title="AI Recipe Generation"
            description="Get personalized recipes based on your preferences, dietary restrictions, and available ingredients."
            delay={0.2}
          />
          <FeatureCard
            icon={ChefHat}
            title="Expert Guidance"
            description="Step-by-step instructions with tips from professional chefs to perfect every dish."
            delay={0.3}
          />
          <FeatureCard
            icon={Clock}
            title="Time Management"
            description="Smart cooking timers and prep schedules to help you coordinate multiple dishes effortlessly."
            delay={0.4}
          />
          <FeatureCard
            icon={Users}
            title="Portion Control"
            description="Automatically adjust recipes for any number of servings while maintaining perfect proportions."
            delay={0.5}
          />
          <FeatureCard
            icon={Utensils}
            title="Meal Planning"
            description="Create balanced weekly meal plans with automatic shopping lists and prep instructions."
            delay={0.6}
          />
          <FeatureCard
            icon={Sparkles}
            title="Smart Substitutions"
            description="Intelligent ingredient substitutions based on your pantry and dietary preferences."
            delay={0.7}
          />
        </div>
      </div>
    </section>
  )
}