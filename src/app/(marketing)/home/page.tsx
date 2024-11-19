/* eslint-disable @next/next/no-img-element */
import React from 'react'
import { motion } from 'framer-motion'
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "../../../components/ui/card"
import { ChevronRight, Star, Check, ArrowRight } from 'lucide-react'

const LandingPage: React.FC = () => {
  return (
    <div className="bg-amber-50 min-h-screen">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-b from-amber-100 to-amber-50 py-20 sm:py-32">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center"
          >
            <h1 className="text-4xl sm:text-6xl font-bold text-amber-900 mb-6">
              Cook Like a Pro with <span className="text-orange-500">AI-Powered Recipes</span>
            </h1>
            <p className="text-xl text-amber-800 mb-8 max-w-2xl mx-auto">
              Cuizine combines artificial intelligence with culinary expertise to transform your cooking experience. Get personalized recipes, meal plans, and expert guidance.
            </p>
            <Button size="lg" className="bg-orange-500 hover:bg-orange-600 text-white">
              Start Cooking Smarter <ChevronRight className="ml-2" />
            </Button>
          </motion.div>
        </div>
        <div className="absolute bottom-0 left-0 right-0 h-20 bg-gradient-to-t from-amber-50 to-transparent"></div>
      </section>

      {/* Features Section */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl sm:text-4xl font-bold text-amber-900 text-center mb-12">
            Revolutionize Your Cooking Experience
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            {[
              { title: "AI Recipe Generation", description: "Get personalized recipes based on your preferences and available ingredients." },
              { title: "Smart Meal Planning", description: "Create balanced weekly meal plans with automatic shopping lists." },
              { title: "Expert Culinary Guidance", description: "Access step-by-step instructions and tips from professional chefs." },
            ].map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
              >
                <Card className="bg-white shadow-lg hover:shadow-xl transition-shadow duration-300">
                  <CardHeader>
                    <CardTitle className="text-xl font-semibold text-amber-900">{feature.title}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-amber-700">{feature.description}</p>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="bg-gradient-to-b from-amber-100 to-amber-50 py-20">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl sm:text-4xl font-bold text-amber-900 text-center mb-12">
            How Cuizine Works
          </h2>
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div>
              <ol className="space-y-6">
                {[
                  "Input your preferences and dietary restrictions",
                  "Our AI generates personalized recipes",
                  "Get a smart shopping list for ingredients",
                  "Follow step-by-step cooking instructions",
                ].map((step, index) => (
                  <li key={index}>
                    <motion.div
                      className="flex items-center space-x-4"
                      initial={{ opacity: 0, x: -20 }}
                      whileInView={{ opacity: 1, x: 0 }}
                      viewport={{ once: true }}
                      transition={{ duration: 0.5, delay: index * 0.1 }}
                    >
                      <span className="flex-shrink-0 w-8 h-8 flex items-center justify-center rounded-full bg-orange-500 text-white font-bold">
                        {index + 1}
                      </span>
                      <span className="text-lg text-amber-800">{step}</span>
                    </motion.div>
                  </li>
                ))}
              </ol>
            </div>
            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5 }}
              className="relative"
            >
              <div className="absolute inset-0 bg-gradient-to-r from-orange-500 to-amber-500 rounded-lg transform rotate-3"></div>
              <img
                src="/placeholder.svg?height=400&width=600"
                alt="Cuizine App Interface"
                className="relative rounded-lg shadow-xl"
              />
            </motion.div>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl sm:text-4xl font-bold text-amber-900 text-center mb-12">
            Choose Your Culinary Journey
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            {[
              { name: "Starter", price: 9, features: ["1000+ recipes", "Basic meal planning", "Shopping list generation"] },
              { name: "Chef", price: 19, features: ["5000+ recipes", "Advanced meal planning", "Nutritional information", "Recipe scaling"], popular: true },
              { name: "Master Chef", price: 29, features: ["Unlimited recipes", "Custom recipe creation", "24/7 chef support", "Inventory management"] },
            ].map((plan, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
              >
                <Card className={`bg-white shadow-lg hover:shadow-xl transition-shadow duration-300 ${plan.popular ? 'border-2 border-orange-500' : ''}`}>
                  <CardHeader>
                    <CardTitle className="text-2xl font-bold text-amber-900">{plan.name}</CardTitle>
                    {plan.popular && <span className="text-orange-500 font-semibold">Most Popular</span>}
                  </CardHeader>
                  <CardContent>
                    <p className="text-3xl font-bold text-amber-900 mb-4">${plan.price}<span className="text-lg font-normal">/mo</span></p>
                    <ul className="space-y-2">
                      {plan.features.map((feature, i) => (
                        <li key={i} className="flex items-center text-amber-700">
                          <Check className="mr-2 h-5 w-5 text-orange-500" />
                          {feature}
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                  <CardFooter>
                    <Button className="w-full bg-orange-500 hover:bg-orange-600 text-white">
                      Get Started
                    </Button>
                  </CardFooter>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="bg-gradient-to-b from-amber-100 to-amber-50 py-20">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl sm:text-4xl font-bold text-amber-900 text-center mb-12">
            What Our Users Say
          </h2>
          <div className="grid md:grid-cols-2 gap-8">
            {[
              { name: "Sarah L.", role: "Home Cook", quote: "Cuizine has transformed my cooking. I'm making restaurant-quality meals at home!" },
              { name: "Mike T.", role: "Busy Professional", quote: "The meal planning feature saves me so much time and stress every week." },
            ].map((testimonial, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
              >
                <Card className="bg-white shadow-lg hover:shadow-xl transition-shadow duration-300">
                  <CardContent className="pt-6">
                    <div className="flex items-center mb-4">
                      {[...Array(5)].map((_, i) => (
                        <Star key={i} className="h-5 w-5 text-yellow-400 fill-current" />
                      ))}
                    </div>
                    <p className="text-amber-800 mb-4">&quot;{testimonial.quote}&quot;</p>
                    <div className="flex items-center">
                      <div className="mr-4 h-12 w-12 rounded-full bg-amber-200 flex items-center justify-center text-amber-800 font-bold text-xl">
                        {testimonial.name[0]}
                      </div>
                      <div>
                        <p className="font-semibold text-amber-900">{testimonial.name}</p>
                        <p className="text-amber-700">{testimonial.role}</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="bg-gradient-to-r from-orange-500 to-amber-500 rounded-lg p-12 text-center">
            <h2 className="text-3xl sm:text-4xl font-bold text-white mb-6">
              Ready to Transform Your Cooking?
            </h2>
            <p className="text-xl text-white mb-8 max-w-2xl mx-auto">
              Join thousands of happy cooks who have revolutionized their kitchen with Cuizine&apos;s AI-powered recipes.
            </p>
            <Button size="lg" className="bg-white text-orange-500 hover:bg-amber-100">
              Start Your Free Trial <ArrowRight className="ml-2" />
            </Button>
          </div>
        </div>
      </section>
    </div>
  )
}

export default LandingPage