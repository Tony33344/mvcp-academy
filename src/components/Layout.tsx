import { useEffect, useState } from 'react'
import { NavLink, Outlet, useLocation } from 'react-router-dom'
import { getSetting, setSetting } from '../db/db'

const NAV = [
  { to: '/', label: 'Domov', icon: '⌂' },
  { to: '/exam', label: 'Izpit', icon: '◎' },
  { to: '/learn', label: 'Uči se', icon: '¶' },
  { to: '/practice', label: 'Vadba', icon: '⚡' },
  { to: '/explore', label: 'Graf', icon: '⁂' },
  { to: '/sources', label: 'Viri', icon: '⌘' },
  { to: '/progress', label: 'Napredek', icon: '↑' },
  { to: '/about', label: 'O app', icon: 'ℹ' },
]

export default function Layout() {
  const [dark, setDark] = useState(false)
  const loc = useLocation()

  useEffect(() => {
    getSetting<boolean>('dark', window.matchMedia('(prefers-color-scheme: dark)').matches).then(setDark)
  }, [])
  useEffect(() => {
    document.documentElement.classList.toggle('dark', dark)
  }, [dark])
  useEffect(() => { window.scrollTo(0, 0) }, [loc.pathname])

  return (
    <div className="min-h-screen flex flex-col">
      <header className="no-print sticky top-0 z-40 border-b border-stone-200/80 dark:border-stone-800 bg-[#faf9f6]/90 dark:bg-stone-950/90 backdrop-blur">
        <div className="max-w-5xl mx-auto px-5 h-16 flex items-center justify-between">
          <NavLink to="/" className="flex items-baseline gap-2 group">
            <span className="font-display text-xl font-semibold tracking-tight">MVČP</span>
            <span className="text-xs uppercase tracking-[0.18em] text-stone-500 group-hover:text-stone-700 dark:group-hover:text-stone-300 transition-colors">Academy</span>
          </NavLink>
          <div className="flex items-center gap-1">
            <nav className="hidden md:flex items-center gap-0.5">
              {NAV.filter(n => n.to !== '/').map(n => (
                <NavLink key={n.to} to={n.to}
                  className={({ isActive }) => `px-3.5 py-2 text-[13px] rounded-md transition-colors ${isActive
                    ? 'text-stone-900 dark:text-stone-50 font-medium'
                    : 'text-stone-500 hover:text-stone-900 dark:text-stone-400 dark:hover:text-stone-200'}`}>
                  {n.label}
                </NavLink>
              ))}
            </nav>
            <button aria-label="Preklopi temo" onClick={() => { setDark(!dark); setSetting('dark', !dark) }}
              className="p-2.5 rounded-full hover:bg-stone-100 dark:hover:bg-stone-800 text-base" style={{ minWidth: 44, minHeight: 44 }}>
              {dark ? '☀' : '☾'}
            </button>
          </div>
        </div>
        <div className="h-px bg-gradient-to-r from-transparent via-stone-300 dark:via-stone-700 to-transparent" />
      </header>

      <main className="flex-1 max-w-3xl w-full mx-auto px-5 py-10 pb-28 md:pb-16">
        <Outlet />
      </main>

      <nav className="no-print md:hidden fixed bottom-0 inset-x-0 z-40 bg-[#faf9f6]/95 dark:bg-stone-950/95 backdrop-blur border-t border-stone-200 dark:border-stone-800"
        style={{ paddingBottom: 'env(safe-area-inset-bottom)' }}>
        <div className="grid grid-cols-5">
          {NAV.slice(0, 5).map(n => (
            <NavLink key={n.to} to={n.to} end={n.to === '/'}
              className={({ isActive }) => `flex flex-col items-center py-2 text-[10px] tracking-wide ${isActive ? 'text-stone-900 dark:text-stone-100 font-semibold' : 'text-stone-400'}`}
              style={{ minHeight: 54 }}>
              <span className="text-base leading-none mb-1">{n.icon}</span>{n.label}
            </NavLink>
          ))}
        </div>
      </nav>

      <footer className="no-print hidden md:block py-8 text-center text-xs text-stone-400 tracking-wide">
        MVČP ACADEMY · izobraževalno orodje · viri: OHCHR · UN · Svet Evrope · brez sledenja
      </footer>
    </div>
  )
}
