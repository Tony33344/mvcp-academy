import { core, comparisons } from '../lib/data'
import Md from '../components/Md'

export default function Learn() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold">📚 Kurikulum — splošno učenje</h1>
        <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
          8 modulov od koncepta do aktualnih dogodkov. Brez izpitnih oznak — za vse, ki jih zanima tema.
        </p>
      </div>

      <section className="space-y-3">
        <h2 className="font-semibold">Moduli</h2>
        {core.map((c, i) => (
          <details key={c.id} className="card">
            <summary className="cursor-pointer font-medium text-sm">
              Modul {i + 1}: {c.title} <span className="text-slate-400">({c.titleEn})</span>
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
                      <tr key={ri} className={ri === 0 ? 'bg-slate-100 dark:bg-slate-800 font-semibold' : ''}>
                        {row.map((cell, ci) => (
                          <td key={ci} className="border border-slate-200 dark:border-slate-700 px-2 py-1.5 align-top">{cell}</td>
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
