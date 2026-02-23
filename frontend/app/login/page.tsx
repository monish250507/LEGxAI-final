'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [isSignUp, setIsSignUp] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    // Basic validation
    if (!email || !password) {
      setError('Please fill in all fields');
      setIsLoading(false);
      return;
    }

    if (password.length < 6) {
      setError('Password must be at least 6 characters');
      setIsLoading(false);
      return;
    }

    try {
      // Mock authentication - accept any valid email/password for demo
      await new Promise(resolve => setTimeout(resolve, 1500)); // Simulate API delay
      
      // Store auth token and user data
      localStorage.setItem('lexai_token', 'mock_token_' + Date.now());
      localStorage.setItem('lexai_user', JSON.stringify({ 
        email, 
        name: email.split('@')[0],
        createdAt: new Date().toISOString()
      }));
      
      // Show success message briefly
      if (isSignUp) {
        alert('Account created successfully! Welcome to LexAI!');
      } else {
        alert('Login successful! Welcome back to LexAI!');
      }
      
      // Redirect to dashboard
      router.push('/dashboard');
    } catch (err) {
      setError(isSignUp ? 'Sign up failed. Please try again.' : 'Login failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-black flex items-center justify-center px-4">
      <div className="max-w-md w-full">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="w-16 h-16 bg-green-500 rounded-xl flex items-center justify-center mx-auto mb-4 hover:shadow-[0_0_30px_rgba(0,255,136,0.6)] transition-all duration-300">
            <span className="text-black font-bold text-2xl">L</span>
          </div>
          <h1 className="text-green-400 font-bold text-2xl mb-2">
            {isSignUp ? 'Create Account' : 'LexAI'}
          </h1>
          <p className="text-gray-500 text-sm">
            {isSignUp ? 'Join the Constitution-Aware Legal AI Platform' : 'Constitution-Aware Legal AI Platform'}
          </p>
        </div>

        {/* Login Form */}
        <div className="bg-gray-900 border border-green-900 rounded-2xl p-8 mb-6">
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Email Field */}
            <div>
              <label htmlFor="email" className="text-green-400 text-sm font-medium mb-2 block">
                Email Address
              </label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-3 bg-black border border-green-800 rounded-lg text-white placeholder-gray-600 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200"
                placeholder="Enter your email"
                required
              />
            </div>

            {/* Password Field */}
            <div>
              <label htmlFor="password" className="text-green-400 text-sm font-medium mb-2 block">
                Password
              </label>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-3 bg-black border border-green-800 rounded-lg text-white placeholder-gray-600 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200"
                placeholder="Enter your password"
                required
              />
            </div>

            {/* Error Message */}
            {error && (
              <div className="bg-red-900/20 border border-red-800 rounded-lg p-3">
                <p className="text-red-400 text-sm">{error}</p>
              </div>
            )}

            {/* Submit Button */}
            <button
              type="submit"
              disabled={isLoading}
              className="w-full h-12 bg-black border border-green-500 text-green-400 rounded-lg font-semibold hover:bg-green-950 hover:text-green-300 hover:shadow-[0_0_25px_rgba(0,255,136,0.4)] transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? (
                <div className="flex items-center justify-center">
                  <div className="w-5 h-5 border-2 border-green-400 border-t-transparent rounded-full animate-spin"></div>
                  <span className="ml-2">{isSignUp ? 'Creating Account...' : 'Authenticating...'}</span>
                </div>
              ) : (
                <span>{isSignUp ? '🚀 Create Account' : '🔐 Secure Login'}</span>
              )}
            </button>
          </form>
        </div>

        {/* Footer */}
        <div className="text-center space-y-3">
          <p className="text-gray-500 text-xs">
            Protected by military-grade encryption
          </p>
          <button 
            className="w-full py-2 text-gray-400 text-sm hover:text-green-400 transition-colors duration-200"
            onClick={() => setIsSignUp(!isSignUp)}
          >
            {isSignUp ? '🔐 Already have an account? Login' : '🚀 New to LexAI? Create Account'}
          </button>
          <button 
            className="w-full py-2 text-gray-400 text-sm hover:text-green-400 transition-colors duration-200"
            onClick={() => window.open('/docs', '_blank')}
          >
            📖 Documentation
          </button>
          {!isSignUp && (
            <button 
              className="w-full py-2 text-gray-400 text-sm hover:text-green-400 transition-colors duration-200"
              onClick={() => alert('Password reset would be implemented here')}
            >
              🆘 Forgot Password?
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
