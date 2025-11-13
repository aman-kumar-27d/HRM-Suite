import { useEffect, useState } from 'react'
import './App.css'
import './index.css'

function App() {
  const [dark, setDark] = useState<boolean>(document.documentElement.classList.contains('dark'))
  useEffect(() => {
    if (dark) {
      document.documentElement.classList.add('dark')
      localStorage.setItem('theme', 'dark')
    } else {
      document.documentElement.classList.remove('dark')
      localStorage.setItem('theme', 'light')
    }
  }, [dark])

  return (
    <div className="min-h-screen bg-white text-black dark:bg-[#0b0b0f] dark:text-white">
      <header className="flex items-center justify-between px-6 py-4">
        <h1 className="text-2xl font-bold">Payroll Management</h1>
        <button
          className="px-3 py-1 rounded border border-gray-300 dark:border-gray-700"
          onClick={() => setDark((v) => !v)}
        >
          {dark ? 'Light Mode' : 'Dark Mode'}
        </button>
      </header>
      <main className="px-6">
        <section className="py-20 text-center">
          <h2 className="text-4xl font-extrabold tracking-tight">
            Manage HR & Payroll End-to-End
          </h2>
          <p className="mt-4 text-gray-600 dark:text-gray-400">
            Onboarding to payouts, reports and insights.
          </p>
          <div className="mt-8 flex gap-4 justify-center">
            <a className="px-5 py-2 rounded bg-blue-600 text-white" href="#hr">Go to HR</a>
            <a className="px-5 py-2 rounded bg-purple-600 text-white" href="#payroll">Run Payroll</a>
            <a className="px-5 py-2 rounded bg-gray-900 text-white dark:bg-gray-100 dark:text-black" href="#reports">View Reports</a>
          </div>
        </section>
      </main>
    </div>
  )
}

export default App
