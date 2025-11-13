import { useEffect, useState } from 'react'

export default function App() {
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
    <div className="min-h-screen transition-theme bg-white text-black dark:bg-[#0b0b0f] dark:text-white">
      <header className="flex items-center justify-between px-8 py-5">
        <h1 className="text-2xl font-bold">Payroll Management</h1>
        <button
          className="inline-flex items-center gap-2 px-3 py-2 rounded border border-gray-300 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-900"
          onClick={() => setDark((v) => !v)}
        >
          <span className="inline-block w-4 h-4 rounded-full bg-black dark:bg-white" />
          {dark ? 'Light Mode' : 'Dark Mode'}
        </button>
      </header>
      <main className="px-8">
        <section className="py-24 text-center">
          <h2 className="text-4xl md:text-5xl font-extrabold tracking-tight">
            Manage HR & Payroll End-to-End
          </h2>
          <p className="mt-4 text-gray-600 dark:text-gray-400">
            Onboarding to payouts, reports and insights.
          </p>
          <div className="mt-10 flex gap-4 justify-center">
            <a className="px-5 py-2 rounded bg-indigo-600 text-white" href="#hr">Go to HR</a>
            <a className="px-5 py-2 rounded bg-purple-600 text-white" href="#payroll">Run Payroll</a>
            <a className="px-5 py-2 rounded bg-gray-900 text-white dark:bg-gray-100 dark:text-black" href="#reports">View Reports</a>
          </div>
        </section>
      </main>
    </div>
  )
}

