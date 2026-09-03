import { useEffect, useRef, useState } from 'react'
import { entities, entityEdges, TOPIC_COLORS, TYPE_NAMES } from '../lib/data'

export default function Graph() {
  const ref = useRef<HTMLDivElement>(null)
  const [typeFilter, setTypeFilter] = useState('all')
  const [selected, setSelected] = useState<{ label: string; facts: string; type: string } | null>(null)
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const networkRef = useRef<any>(null)

  useEffect(() => {
    let cancelled = false
    Promise.all([import('vis-network'), import('vis-data')]).then(([{ Network }, { DataSet }]) => {
      if (cancelled || !ref.current) return
      const filtered = typeFilter === 'all' ? entities : entities.filter(e => e.type === typeFilter)
      const idSet = new Set(filtered.map(e => e.id))
      const nodes = new DataSet(filtered.map(e => ({
        id: e.id, label: e.label.length > 40 ? e.label.slice(0, 38) + '…' : e.label,
        group: e.type, title: e.facts || e.label,
      })))
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const edges = new DataSet(entityEdges
        .filter(e => idSet.has(e.source) && idSet.has(e.target))
        .map(e => ({ from: e.source, to: e.target, dashes: e.authority === 'C' || e.authority === 'D' || e.authority === 'E' })) as any)
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      networkRef.current = new Network(ref.current, { nodes: nodes as any, edges: edges as any }, {
        groups: Object.fromEntries(Object.entries(TOPIC_COLORS).map(([k, c]) => [k, { color: { background: c, border: c } }])),
        physics: { stabilization: { iterations: 150 } },
        interaction: { hover: true },
      })
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      networkRef.current.on('click', (params: any) => {
        const id = params.nodes[0]
        if (!id) { setSelected(null); return }
        const e = entities.find(x => x.id === id)
        if (e) setSelected({ label: e.label, facts: e.facts, type: e.typeSl })
      })
    })
    return () => { cancelled = true; networkRef.current?.destroy?.() }
  }, [typeFilter])

  const types = Array.from(new Set(entities.map(e => e.type)))

  return (
    <div className="space-y-3">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <h1 className="text-xl font-bold">🕸️ Graf znanja</h1>
        <select className="input max-w-[220px] text-sm" value={typeFilter} onChange={e => setTypeFilter(e.target.value)} aria-label="Filter po tipu entitete">
          <option value="all">Vse entitete ({entities.length})</option>
          {types.map(t => <option key={t} value={t}>{TYPE_NAMES[t] ?? t} ({entities.filter(e => e.type === t).length})</option>)}
        </select>
      </div>

      <div className="flex flex-wrap gap-2 text-xs">
        {Object.entries(TYPE_NAMES).map(([k, n]) => (
          <span key={k} className="inline-flex items-center gap-1">
            <span className="inline-block w-3 h-3 rounded-sm" style={{ background: TOPIC_COLORS[k] }} />{n}
          </span>
        ))}
      </div>

      <div ref={ref} className="card !p-0 h-[60vh] min-h-[400px] overflow-hidden" role="img" aria-label="Interaktivni graf znanja MVČP" />

      <details className="card">
        <summary className="cursor-pointer text-sm font-medium">📋 Seznam entitet (dostopna alternativa grafu)</summary>
        <ul className="mt-3 text-sm space-y-1.5 max-h-96 overflow-auto">
          {entities.map(e => (
            <li key={e.id}>
              <button onClick={() => setSelected({ label: e.label, facts: e.facts, type: e.typeSl })} className="text-left hover:underline">
                <span className="inline-block w-2.5 h-2.5 rounded-sm mr-2" style={{ background: TOPIC_COLORS[e.type] }} />
                {e.label}
              </button>
            </li>
          ))}
        </ul>
      </details>

      {selected && (
        <div className="card border-blue-300">
          <div className="flex justify-between items-start">
            <h2 className="font-semibold text-sm">{selected.label}</h2>
            <button onClick={() => setSelected(null)} aria-label="Zapri" className="text-stone-600 hover:text-stone-700 px-2">✕</button>
          </div>
          <div className="text-xs text-stone-600 mb-2">{selected.type}</div>
          <p className="text-sm text-stone-800">{selected.facts || '—'}</p>
        </div>
      )}
    </div>
  )
}
