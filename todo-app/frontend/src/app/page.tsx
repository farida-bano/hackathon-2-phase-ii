'use client';

import Link from 'next/link';

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div className="text-center lg:text-left">
            <h1 className="text-display gradient-text font-bold">
              Organize Your Life
            </h1>
            <p className="text-body text-gray-600 mt-6 max-w-lg">
              A beautifully designed todo app that helps you stay productive and organized.
              Manage your tasks efficiently with our intuitive interface.
            </p>
            <div className="mt-10 flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
              <Link
                href="/signin"
                className="btn btn-primary py-3 px-8 text-base font-semibold"
              >
                Sign In
              </Link>
              <Link
                href="/signup"
                className="btn btn-secondary py-3 px-8 text-base font-semibold"
              >
                Get Started
              </Link>
            </div>
          </div>

          <div className="relative">
            <div className="absolute -top-6 -right-6 w-64 h-64 bg-purple-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob"></div>
            <div className="absolute -bottom-8 -left-6 w-72 h-72 bg-indigo-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-2000"></div>
            <div className="absolute top-20 left-20 w-60 h-60 bg-pink-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-4000"></div>

            <div className="relative bg-white/20 backdrop-blur-lg rounded-3xl border border-white/30 p-8 card">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-3 h-3 rounded-full bg-red-400"></div>
                <div className="w-3 h-3 rounded-full bg-yellow-400"></div>
                <div className="w-3 h-3 rounded-full bg-green-400"></div>
              </div>

              <div className="space-y-4">
                <div className="flex items-center gap-3 p-3 bg-white/50 rounded-lg">
                  <div className="w-5 h-5 rounded-full border-2 border-gray-300 flex items-center justify-center">
                    <div className="w-2 h-2 rounded-full bg-indigo-500"></div>
                  </div>
                  <span className="text-gray-700">Complete project proposal</span>
                </div>

                <div className="flex items-center gap-3 p-3 bg-white/50 rounded-lg">
                  <div className="w-5 h-5 rounded-full border-2 border-gray-300 flex items-center justify-center">
                    <div className="w-2 h-2 rounded-full bg-indigo-500"></div>
                  </div>
                  <span className="text-gray-700">Schedule team meeting</span>
                </div>

                <div className="flex items-center gap-3 p-3 bg-white/50 rounded-lg">
                  <div className="w-5 h-5 rounded-full border-2 border-indigo-500 flex items-center justify-center bg-indigo-500">
                    <svg className="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M5 13l4 4L19 7"></path>
                    </svg>
                  </div>
                  <span className="text-gray-700 line-through">Review quarterly reports</span>
                </div>
              </div>

              <div className="mt-6 pt-4 border-t border-gray-200/50">
                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium text-gray-600">3 tasks</span>
                  <span className="text-sm font-medium text-gray-600">1 completed</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
