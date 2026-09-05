import { Link } from 'react-router-dom'
import { core, comparisons } from '../lib/data'
import Md from '../components/Md'

export default function Learn() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold">📚 Kurikulum — splošno učenje</h1>
        <p className="text-sm text-stone-600 mt-1">
          11 modulov od koncepta do aktualnih dogodkov. Brez izpitnih oznak — za vse, ki jih zanima tema.
        </p>
      </div>

      <Link to="/learn/seminars" className="card card-hover !p-5 flex items-center justify-between group">
        <div>
          <div className="kicker mb-1">16 SEMINARSKIH NALOG</div>
          <div className="font-medium text-sm">Seminarske naloge — pogodbe, členi, študentski izdelki, izpitna vprašanja</div>
        </div>
        <span className="text-stone-500 group-hover:translate-x-1 transition-transform">→</span>
      </Link>

      <section className="space-y-3">
        <h2 className="font-semibold">Moduli</h2>
        {core.map((c, i) => (
          <details key={c.id} className="card">
            <summary className="cursor-pointer font-medium text-sm">
              Modul {i + 1}: {c.title} <span className="text-stone-600">({c.titleEn})</span>
            </summary>
            <div className="mt-3"><Md>{c.body}</Md></div>
          </details>
        ))}
      </section>

      <section>
        <h2 className="font-semibold mb-3">Primerjalne tabele ({comparisons.length})</h2>
        <div className="space-y-3">
          {comparisons.map(cmp => (
            <details key={cmp.id} className="card">
              <summary className="cursor-pointer font-medium text-sm">{cmp.title}</summary>
              <div className="overflow-x-auto mt-3">
                <table className="w-full text-xs border-collapse">
                  <tbody>
                    {cmp.rows.map((row, ri) => (
                      <tr key={ri} className={ri === 0 ? 'bg-stone-100 font-semibold' : ''}>
                        {row.map((cell, ci) => (
                          <td key={ci} className="border border-stone-300 px-2 py-1.5 align-top">{cell}</td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </details>
          ))}
        </div>
      </section>
    </div>
  )
}
