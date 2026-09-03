import { useEffect, useState } from 'react'
import { flashcards, quiz, topics } from '../lib/data'
import { srsStats } from '../lib/srs'
import { db, exportBackup, importBackup, type TopicMastery } from '../db/db'

export default function Progress() {
  const [stats, setStats] = useState({ total: 0, new: 0, learning: 0, review: 0, due: 0 })
  const [attempts, setAttempts] = useState<{ questionId: string; score: number; points: number; at: number }[]>([])
  const [mastery, setMastery] = useState<TopicMastery[]>([])
  const [msg, setMsg] = useState('')

  useEffect(() => {
    srsStats(flashcards.map(c => c.id)).then(setStats)
    db.quizAttempts.orderBy('at').reverse().limit(50).toArray().then(setAttempts)
    db.topicMastery.toArray().then(setMastery)
  }, [])

  // compute mastery from quiz attempts
  useEffect(() => {
    const byTopic: Record<string, { got: number; max: number }> = {}
    for (const a of attempts) {
      const q = quiz.find(x => x.id === a.questionId)
      if (!q) continue
      for (const t of q.topics) {
        byTopic[t] = byTopic[t] ?? { got: 0, max: 0 }
        byTopic[t].got += a.score; byTopic[t].max += a.points
      }
    }
    ;(async () => {
      for (const [topicId, v] of Object.entries(byTopic)) {
        if (!v.max) continue
        const pct = v.got / v.max
        const level = pct >= 0.7 ? 'green' : pct >= 0.4 ? 'yellow' : 'red'
        await db.topicMastery.put({ topicId, level, updatedAt: Date.now() })
      }
      setMastery(await db.topicMastery.toArray())
    })()
  }, [attempts])

  async function doExport() {
    const json = await exportBackup()
    const blob = new Blob([json], { type: 'application/json' })
    const a = document.createElement('a')
    a.href = URL.createObjectURL(blob)
    a.download = `mvcp-backup-${new Date().toISOString().slice(0, 10)}.json`
    a.click()
    setMsg('Varnostna kopija prenesena.')
  }

  async function doImport(file: File) {
    try {
      await importBackup(await file.text())
      setMsg('Uvoženo. Osveži stran.')
    } catch (e) {
      setMsg('Napaka: ' + (e as Error).message)
    }
  }

  const levelColor = (l: string) => l === 'green' ? 'bg-green-500' : l === 'yellow' ? 'bg-yellow-500' : 'bg-red-500'

  return (
    <div className="space-y-6">
      <h1 className="text-xl font-bold">📈 Napredek</h1>

      <section className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        {[
          { l: 'Kartice', v: `${stats.review + stats.learning}/${stats.total}` },
          { l: 'Zapadle', v: stats.due },
          { l: 'Poskusi vprašanj', v: attempts.length },
          { l: 'Teme ocenjene', v: mastery.length },
        ].map(s => (
          <div key={s.l} className="card text-center">
            <div className="text-xl font-bold text-blue-600">{s.v}</div>
            <div className="text-xs text-stone-600">{s.l}</div>
          </div>
        ))}
      </section>

      <section className="card">
        <h2 className="font-semibold text-sm mb-3">Obvladanje tem (iz kvizov)</h2>
        {mastery.length === 0 ? (
          <p className="text-sm text-stone-600">Še ni podatkov — reši nekaj vprašanj v Vadba → Vprašanja.</p>
        ) : (
          <div className="space-y-2">
            {mastery.map(m => {
              const t = topics.find(x => x.id === m.topicId)
              return (
                <div key={m.topicId} className="flex items-center gap-3">
                  <span className={`inline-block w-3 h-3 rounded-full ${levelColor(m.level)}`} aria-hidden />
                  <span className="text-sm flex-1">{t ? `${t.n}. ${t.title}` : m.topicId}</span>
                  <span className="text-xs text-stone-600 capitalize">{m.level}</span>
                </div>
              )
            })}
          </div>
        )}
        <p className="text-xs text-stone-600 mt-2">🟢 ≥70 % · 🟡 40–70 % · 🔴 &lt;40 % — barva ni edini signal (besedilo + legenda).</p>
      </section>

      <section className="card">
        <h2 className="font-semibold text-sm mb-3">Varnostna kopija (iOS: Safari lahko izbriše podatke)</h2>
        <div className="flex flex-wrap gap-2">
          <button onClick={doExport} className="btn">⬇️ Izvozi napredek</button>
          <label className="btn-secondary cursor-pointer">
            ⬆️ Uvozi
            <input type="file" accept=".json" className="hidden" onChange={e => e.target.files?.[0] && doImport(e.target.files[0])} />
          </label>
        </div>
        {msg && <p className="text-xs text-green-600 mt-2">{msg}</p>}
      </section>
    </div>
  )
}
