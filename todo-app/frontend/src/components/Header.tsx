'use client';

import { useAuth } from '@/contexts/AuthContext';
import Link from 'next/link';
import { useRouter } from 'next/navigation';

export default function Header() {
  const { user, signout, isLoading } = useAuth();
  const router = useRouter();

  const handleSignout = async () => {
    await signout();
    router.push('/');
  };

  return (
    <header className="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-gray-200/50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          <Link href="/" className="flex items-center space-x-2">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center">
              <span className="text-white font-bold text-lg">T</span>
            </div>
            <span className="text-xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
              TodoApp
            </span>
          </Link>

          <nav className="hidden md:flex items-center space-x-8">
            <Link 
              href="/" 
              className="text-gray-600 hover:text-indigo-600 transition-colors duration-200"
            >
              Home
            </Link>
            
            {user ? (
              <>
                <Link 
                  href="/dashboard" 
                  className="text-gray-600 hover:text-indigo-600 transition-colors duration-200"
                >
                  Dashboard
                </Link>
                <div className="flex items-center space-x-4">
                  <span className="text-sm text-gray-500 hidden sm:block">
                    {user.email}
                  </span>
                  <button
                    onClick={handleSignout}
                    className="btn btn-outline text-sm px-4 py-2"
                  >
                    Sign Out
                  </button>
                </div>
              </>
            ) : (
              <>
                <Link 
                  href="/signin" 
                  className="text-gray-600 hover:text-indigo-600 transition-colors duration-200"
                >
                  Sign In
                </Link>
                <Link 
                  href="/signup" 
                  className="btn btn-primary text-sm px-4 py-2"
                >
                  Sign Up
                </Link>
              </>
            )}
          </nav>

          {/* Mobile menu button */}
          <div className="md:hidden flex items-center">
            <button className="p-2 rounded-md text-gray-600 hover:text-gray-900 focus:outline-none">
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}