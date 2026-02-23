'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function ExpertPage() {
  const router = useRouter();
  const [selectedPlan, setSelectedPlan] = useState<string | null>(null);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    preferredTime: '',
    caseDescription: ''
  });

  const pricingPlans = [
    {
      id: 'ai-professional',
      name: 'AI Professional',
      price: 'Free',
      description: 'AI-powered legal analysis and recommendations',
      features: [
        'Basic clause analysis',
        'Risk assessment',
        'AI recommendations',
        'Document summary',
        'Instant results'
      ],
      badge: 'Most Popular',
      experience: 'AI Assistant'
    },
    {
      id: 'senior-advocate',
      name: 'Senior Advocate Review',
      price: '$299',
      description: 'Expert human legal review with AI assistance',
      features: [
        'Comprehensive legal review',
        'Senior advocate consultation',
        'Detailed risk analysis',
        'Negotiation strategies',
        '24-48 hour turnaround'
      ],
      badge: 'Professional',
      experience: '10+ Years Experience'
    },
    {
      id: 'litigation-strategy',
      name: 'Litigation Strategy Package',
      price: '$999',
      description: 'Complete litigation support and strategy development',
      features: [
        'Full case strategy',
        'Court filing assistance',
        'Expert witness coordination',
        'Document preparation',
        'Priority support'
      ],
      badge: 'Premium',
      experience: '15+ Years Experience'
    }
  ];

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    alert(`Thank you for your interest! We'll contact you soon about the ${selectedPlan} plan.`);
    router.push('/dashboard');
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div className="min-h-screen bg-black text-white">
      {/* Header */}
      <div className="border-b border-green-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-green-400 font-bold text-xl">LexAI Legal Expert</h1>
            </div>
            <button 
              onClick={() => router.push('/dashboard')}
              className="text-green-400 hover:text-green-300 transition-colors"
            >
              ← Back to Dashboard
            </button>
          </div>
        </div>
      </div>

      {/* Hero Section */}
      <div className="bg-gradient-to-b from-gray-900 to-black py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="mb-8">
            <div className="inline-flex items-center px-3 py-1 rounded-full bg-green-900 text-green-400 text-sm font-medium mb-4">
              🏛️ Professional Legal Services
            </div>
            <h1 className="text-4xl font-bold text-white mb-4">
              Expert Legal Counsel at Your Fingertips
            </h1>
            <p className="text-xl text-gray-400 max-w-3xl mx-auto">
              Connect with experienced legal professionals for comprehensive document review, 
              strategic advice, and litigation support.
            </p>
          </div>
          
          <div className="bg-yellow-900 border border-yellow-600 rounded-lg p-4 max-w-2xl mx-auto mb-8">
            <div className="flex items-center">
              <span className="text-yellow-400 text-2xl mr-3">⚠️</span>
              <div className="text-left">
                <h3 className="text-yellow-400 font-semibold mb-1">Coming Soon</h3>
                <p className="text-yellow-200 text-sm">
                  This service is currently in development. Sign up for early access and be the first to know when we launch!
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Pricing Plans */}
      <div className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-white mb-4">Choose Your Legal Service Plan</h2>
            <p className="text-gray-400 text-lg">
              Professional legal expertise tailored to your needs
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {pricingPlans.map((plan) => (
              <div
                key={plan.id}
                className={`bg-gray-900 border rounded-xl p-8 hover:shadow-[0_0_30px_rgba(0,255,136,0.3)] transition-all duration-300 cursor-pointer ${
                  selectedPlan === plan.id 
                    ? 'border-green-400 shadow-[0_0_20px_rgba(0,255,136,0.4)]' 
                    : 'border-green-800 hover:border-green-600'
                }`}
                onClick={() => setSelectedPlan(plan.id)}
              >
                {/* Plan Header */}
                <div className="text-center mb-6">
                  <div className="inline-flex items-center px-3 py-1 rounded-full bg-green-900 text-green-400 text-xs font-medium mb-4">
                    {plan.badge}
                  </div>
                  <h3 className="text-2xl font-bold text-white mb-2">{plan.name}</h3>
                  <div className="text-4xl font-bold text-green-400 mb-2">{plan.price}</div>
                  <p className="text-gray-400 text-sm">{plan.description}</p>
                </div>

                {/* Experience Badge */}
                <div className="bg-black border border-green-800 rounded-lg p-3 mb-6">
                  <div className="flex items-center justify-center">
                    <span className="text-green-400 text-sm font-medium">⭐ {plan.experience}</span>
                  </div>
                </div>

                {/* Features */}
                <div className="space-y-3 mb-8">
                  {plan.features.map((feature, index) => (
                    <div key={index} className="flex items-center">
                      <span className="text-green-400 mr-3">✓</span>
                      <span className="text-gray-300 text-sm">{feature}</span>
                    </div>
                  ))}
                </div>

                {/* Select Button */}
                <button
                  className={`w-full py-3 rounded-lg font-semibold transition-all duration-200 ${
                    selectedPlan === plan.id
                      ? 'bg-green-500 text-black hover:bg-green-400'
                      : 'bg-gray-800 border border-green-800 text-green-400 hover:bg-green-950 hover:border-green-500'
                  }`}
                >
                  {selectedPlan === plan.id ? 'Selected' : 'Select Plan'}
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Scheduling Form */}
      {selectedPlan && (
        <div className="py-16 bg-gray-950">
          <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="bg-black border border-green-800 rounded-xl p-8">
              <h2 className="text-2xl font-bold text-white mb-6">Schedule Your Consultation</h2>
              
              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-green-400 text-sm font-medium mb-2">
                      Full Name
                    </label>
                    <input
                      type="text"
                      name="name"
                      value={formData.name}
                      onChange={handleInputChange}
                      required
                      className="w-full bg-gray-900 border border-green-800 rounded-lg px-4 py-3 text-white placeholder-gray-600 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
                      placeholder="Enter your full name"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-green-400 text-sm font-medium mb-2">
                      Email Address
                    </label>
                    <input
                      type="email"
                      name="email"
                      value={formData.email}
                      onChange={handleInputChange}
                      required
                      className="w-full bg-gray-900 border border-green-800 rounded-lg px-4 py-3 text-white placeholder-gray-600 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
                      placeholder="your@email.com"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-green-400 text-sm font-medium mb-2">
                      Phone Number
                    </label>
                    <input
                      type="tel"
                      name="phone"
                      value={formData.phone}
                      onChange={handleInputChange}
                      required
                      className="w-full bg-gray-900 border border-green-800 rounded-lg px-4 py-3 text-white placeholder-gray-600 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
                      placeholder="+1 (555) 123-4567"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-green-400 text-sm font-medium mb-2">
                      Preferred Consultation Time
                    </label>
                    <select
                      name="preferredTime"
                      value={formData.preferredTime}
                      onChange={handleInputChange}
                      required
                      className="w-full bg-gray-900 border border-green-800 rounded-lg px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
                    >
                      <option value="">Select a time</option>
                      <option value="morning">Morning (9AM - 12PM)</option>
                      <option value="afternoon">Afternoon (12PM - 5PM)</option>
                      <option value="evening">Evening (5PM - 8PM)</option>
                    </select>
                  </div>
                </div>
                
                <div>
                  <label className="block text-green-400 text-sm font-medium mb-2">
                    Case Description
                  </label>
                  <textarea
                    name="caseDescription"
                    value={formData.caseDescription}
                    onChange={handleInputChange}
                    rows={4}
                    className="w-full bg-gray-900 border border-green-800 rounded-lg px-4 py-3 text-white placeholder-gray-600 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
                    placeholder="Briefly describe your legal needs and the documents you'd like reviewed..."
                  />
                </div>
                
                <div className="flex gap-4">
                  <button
                    type="submit"
                    className="flex-1 bg-green-500 text-black py-3 rounded-lg font-semibold hover:bg-green-400 transition-colors duration-200"
                  >
                    Submit Request
                  </button>
                  <button
                    type="button"
                    onClick={() => setSelectedPlan(null)}
                    className="flex-1 bg-gray-800 border border-green-800 text-green-400 py-3 rounded-lg font-semibold hover:bg-green-950 hover:border-green-500 transition-all duration-200"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {/* Footer */}
      <div className="border-t border-green-800 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <p className="text-gray-400 text-sm">
            © 2024 LexAI Legal Expert. Professional legal services powered by AI and human expertise.
          </p>
        </div>
      </div>
    </div>
  );
}
