'use client';

import { useRouter } from "next/navigation";


export default function LoginPage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <h1 className="text-4xl font-bold mb-4">Login Page</h1>
      <p className="text-lg mb-8">Please log in to continue.</p>
      {/* Add your login form here */}
    </div>
  );
}