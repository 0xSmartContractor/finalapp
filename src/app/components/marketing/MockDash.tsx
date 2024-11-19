'use client'

import React, { useState } from 'react'
import { 
  ChefHat, 
  Home, 
  Calendar, 
  Clock, 
  Settings, 
  TrendingUp
} from 'lucide-react'
import { Button } from "@/components/ui/button"

// Default mock data
// const defaultProfile = {
//   display_name: 'Alex Johnson',
//   profile_image_url: '/api/placeholder/150/150',
// }

const allRecipes = [
  {
    id: 'tr1',
    title: "Overnight Oats with Berries",
    meal_type: 'breakfast',
    time: '8:00 AM',
    completed: true,
    description: "A healthy and delicious breakfast option packed with fiber and antioxidants.",
    ingredients: ["Rolled oats", "Milk", "Greek yogurt", "Mixed berries", "Honey", "Chia seeds"],
    instructions: ["Mix oats, milk, yogurt, and chia seeds in a jar.", "Add honey to taste.", "Top with mixed berries.", "Refrigerate overnight.", "Enjoy in the morning!"]
  },
  {
    id: 'tr2',
    title: "Mediterranean Quinoa Bowl",
    meal_type: 'lunch',
    time: '12:30 PM',
    completed: false,
    description: "A nutritious and flavorful lunch bowl inspired by Mediterranean cuisine.",
    ingredients: ["Quinoa", "Cherry tomatoes", "Cucumber", "Kalamata olives", "Feta cheese", "Olive oil", "Lemon juice"],
    instructions: ["Cook quinoa according to package instructions.", "Chop vegetables and mix with cooked quinoa.", "Add olives and crumbled feta cheese.", "Drizzle with olive oil and lemon juice.", "Season with salt and pepper to taste."]
  },
  {
    id: 'tr3',
    title: "Grilled Salmon with Asparagus",
    meal_type: 'dinner',
    time: '7:00 PM',
    completed: false,
    description: "A light and healthy dinner option rich in omega-3 fatty acids.",
    ingredients: ["Salmon fillet", "Asparagus", "Lemon", "Olive oil", "Garlic", "Dill"],
    instructions: ["Preheat grill to medium-high heat.", "Season salmon with olive oil, garlic, and dill.", "Grill salmon for 4-5 minutes per side.", "Grill asparagus for 2-3 minutes.", "Serve with lemon wedges."]
  },
  {
    id: 'tr4',
    title: "Spicy Tofu Stir-Fry",
    meal_type: 'dinner',
    time: '6:30 PM',
    completed: false,
    description: "A vegetarian-friendly stir-fry packed with protein and vegetables.",
    ingredients: ["Firm tofu", "Mixed vegetables", "Soy sauce", "Sriracha", "Sesame oil", "Garlic", "Ginger"],
    instructions: ["Press and cube tofu.", "Stir-fry vegetables in sesame oil.", "Add tofu and sauce mixture.", "Cook until heated through.", "Serve over rice or noodles."]
  },
  {
    id: 'tr5',
    title: "Avocado Toast with Poached Egg",
    meal_type: 'breakfast',
    time: '9:00 AM',
    completed: false,
    description: "A trendy and nutritious breakfast that's quick to prepare.",
    ingredients: ["Whole grain bread", "Ripe avocado", "Eggs", "Cherry tomatoes", "Red pepper flakes", "Salt and pepper"],
    instructions: ["Toast bread and mash avocado on top.", "Poach eggs in simmering water.", "Top toast with poached egg.", "Garnish with sliced tomatoes and seasonings."]
  }
]

const WEEKDAYS = [
  { key: 'mon', label: 'M' },
  { key: 'tue', label: 'T' },
  { key: 'wed', label: 'W' },
  { key: 'thu', label: 'T' },
  { key: 'fri', label: 'F' },
  { key: 'sat', label: 'S' },
  { key: 'sun', label: 'S' }
]

const Dashboard = () => {
  const [todaysRecipes] = useState(allRecipes.slice(0, 3))

  return (
    <div className="w-full min-h-screen bg-black text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <header className="py-4">
          <div className="flex flex-col gap-2 py-2">
            <div className="flex gap-2">
              <div className="w-3 h-3 rounded-full bg-red-500"></div>
              <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
              <div className="w-3 h-3 rounded-full bg-green-500"></div>
            </div>
            <div className="flex items-center gap-2">
              <ChefHat className="h-8 w-8 text-lime-400" />
              <span className="text-2xl font-bold text-lime-400">Cuizine</span>
            </div>
          </div>
        </header>

        <div className="flex flex-col lg:flex-row gap-6">
          {/* Simplified Sidebar */}
          <aside className="lg:w-64 bg-[#1A1A1A] p-4 rounded-xl border border-[#2A2A2A] hidden lg:block">
            <nav className="space-y-2 flex-1">
              {[
                { icon: Home, label: 'Dashboard', active: true },
                { icon: Calendar, label: 'Meal Planner' },
                { icon: Clock, label: 'Recent' },
                { icon: Settings, label: 'Settings' },
              ].map((item, index) => (
                <Button
                  key={index}
                  variant="ghost"
                  className={`w-full justify-start ${
                    item.active
                      ? 'bg-lime-400/10 text-lime-400'
                      : 'hover:bg-[#2A2A2A] text-gray-400'
                  }`}
                >
                  <item.icon className="h-5 w-5 mr-2" />
                  {item.label}
                </Button>
              ))}
            </nav>
          </aside>

          {/* Simplified Main Content */}
          <main className="flex-1">
            {/* Quick Stats */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
              {[
                { label: 'Total Recipes', value: '24', trend: '+4 this week' },
                { label: 'Meal Plans', value: '3', trend: 'Active plans' },
                { label: 'Cooking Streak', value: '7', trend: 'days' },
              ].map((stat, index) => (
                <div
                  key={index}
                  className="bg-[#1A1A1A] rounded-xl border border-[#2A2A2A] p-4"
                >
                  <div className="text-gray-400 text-sm mb-1">{stat.label}</div>
                  <div className="text-2xl font-bold mb-1">{stat.value}</div>
                  <div className="flex items-center gap-1 text-xs text-lime-400">
                    <TrendingUp className="h-3 w-3" />
                    {stat.trend}
                  </div>
                </div>
              ))}
            </div>

            {/* Today's Recipes Preview */}
            <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
              <div className="bg-[#1A1A1A] rounded-xl border border-[#2A2A2A] p-6">
                <h2 className="text-lg font-semibold mb-4">Today&apos;s Recipes</h2>
                <div className="space-y-4">
                  {todaysRecipes.map((recipe) => (
                    <div 
                      key={recipe.id}
                      className="flex items-center justify-between p-3 rounded-lg bg-[#2A2A2A]"
                    >
                      <div>
                        <div className="font-medium">{recipe.title}</div>
                        <div className="text-sm text-gray-400">{recipe.time}</div>
                      </div>
                      <div className={`px-2 py-1 rounded text-xs ${
                        recipe.completed ? 'bg-lime-400/20 text-lime-400' : 'bg-blue-400/20 text-blue-400'
                      }`}>
                        {recipe.completed ? 'Completed' : recipe.meal_type}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Simplified Calendar Preview */}
              <div className="bg-[#1A1A1A] rounded-xl border border-[#2A2A2A] p-6">
                <h2 className="text-lg font-semibold mb-4">Upcoming Meals</h2>
                <div className="grid grid-cols-7 gap-2">
                  {WEEKDAYS.map((day) => (
                    <div key={day.key} className="text-center text-sm text-gray-400">
                      {day.label}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </main>
        </div>
      </div>
    </div>
  )
}

export default Dashboard