import { useEffect } from 'react'
import { NavLink, Outlet, useLocation } from 'react-router-dom'

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
  const loc = useLocation()
  useEffect(() => { window.scrollTo(0, 0) }, [loc.pathname])

  return (
    <div className="min-h-screen flex flex-col bg-white">
      <header className="no-print sticky top-0 z-40 border-b border-stone-300 bg-white/95 backdrop-blur">
        <div className="max-w-5xl mx-auto px-5 h-16 flex items-center justify-between">
          <NavLink to="/" className="flex items-baseline gap-2 group">
            <span className="font-display text-xl font-bold tracking-tight text-stone-900">MVČP</span>
            <span className="text-xs uppercase tracking-[0.18em] text-stone-600 group-hover:text-stone-900 transition-colors font-semibold">Academy</span>
          </NavLink>
          <nav className="hidden md:flex items-center gap-0.5">
            {NAV.filter(n => n.to !== '/').map(n => (
              <NavLink key={n.to} to={n.to}
                className={({ isActive }) => `px-3.5 py-2 text-[13px] rounded-md transition-colors font-medium ${isActive
                  ? 'text-stone-900 bg-stone-100 font-bold'
                  : 'text-stone-600 hover:text-stone-900 hover:bg-stone-50'}`}>
                {n.label}
              </NavLink>
            ))}
          </nav>
        </div>
        <div className="h-px bg-gradient-to-r from-transparent via-stone-300 to-transparent" />
      </header>

      <main className="flex-1 max-w-3xl w-full mx-auto px-5 py-10 pb-28 md:pb-16">
        <Outlet />
      </main>

      <nav className="no-print md:hidden fixed bottom-0 inset-x-0 z-40 bg-white/98 backdrop-blur border-t border-stone-300"
        style={{ paddingBottom: 'env(safe-area-inset-bottom)' }}>
        <div className="grid grid-cols-5">
          {NAV.slice(0, 5).map(n => (
            <NavLink key={n.to} to={n.to} end={n.to === '/'}
              className={({ isActive }) => `flex flex-col items-center py-2 text-[10.5px] tracking-wide ${isActive ? 'text-stone-900 font-bold' : 'text-stone-500 font-medium'}`}
              style={{ minHeight: 54 }}>
              <span className="text-base leading-none mb-1">{n.icon}</span>{n.label}
            </NavLink>
          ))}
        </div>
      </nav>

      <footer className="no-print hidden md:block py-8 text-center text-xs text-stone-500 tracking-wide font-medium">
        MVČP ACADEMY · izobraževalno orodje · viri: OHCHR · UN · Svet Evrope · brez sledenja
      </footer>
    </div>
  )
}
