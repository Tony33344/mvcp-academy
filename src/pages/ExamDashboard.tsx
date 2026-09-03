import { useState } from 'react'
import { Link } from 'react-router-dom'
import { topics, core } from '../lib/data'
import Md from '../components/Md'

const TRAP_DRILL = [
  {
    q: "Odbor za ČP ima 47 držav članic, izvoljenih po regionalnem ključu s tajnim glasovanjem?",
    ans: false,
    expl: "PAST! To je Svet za ČP (charter-based telo)! Odbor za ČP (po MPDPP čl. 28) ima 18 neodvisnih strokovnjakov."
  },
  {
    q: "Čl. 41 MPDPP ureja individualne pritožbe posameznikov pred Odborom za ČP?",
    ans: false,
    expl: "PAST! Čl. 41 ureja MEDDRŽAVNE komunikacije. Individualne pritožbe so v 1. Fakultativnem protokolu (1. OP)!"
  },
  {
    q: "Pravica do čistega in zdravega okolja je bila formalno priznana že v Splošni deklaraciji (SDČP 1948)?",
    ans: false,
    expl: "PAST! Pred 1972 (Stockholm) okolje NI omenjeno v nobenem globalnem dokumentu! GS OZN jo je priznala šele 2022 (A/RES/76/300)."
  },
  {
    q: "Pravica do razvoja (Deklaracija 1986) je pravno zavezujoča mednarodna pogodba?",
    ans: false,
    expl: "PAST! Je zgolj politična deklaracija Generalne skupščine (res. 41/128) in NI pravno zavezujoča (glej Subedi / Schrijver)."
  },
  {
    q: "CAT čl. 1 definicija mučenja izrecno izključuje bolečino, ki izhaja iz zakonitih sankcij?",
    ans: true,
    expl: "RESNICA! CAT čl. 1 izrecno določa: 'Ne vključuje bolečine ali trpljenja, ki izhaja zgolj iz zakonitih sankcij'."
  },
  {
    q: "Progresivna realizacija (MPESKP čl. 2(1)) pomeni, da država lahko odloži vse ukrepe, če nima denarja?",
    ans: false,
    expl: "PAST! Minimalne osnovne obveznosti (minimum core obligations) in načelo nediskriminacije veljajo TAKOJ, ne glede na sredstva."
  },
  {
    q: "V primeru beguncev načelo non-refoulement velja tudi za ekonomske migrante po Konvenciji 1951?",
    ans: false,
    expl: "PAST! Konvencija 1951 ščiti le tiste z utemeljenim strahom pred preganjanjem (5 razlogov). Toda pazi: CAT čl. 3 prepoveduje vračanje v mučenje za VSAKOGAR."
  },
  {
    q: "Dolus specialis (posebni namen uničiti skupino) je obvezen element za kvalifikacijo genocida?",
    ans: true,
    expl: "RESNICA! Brez dokaza dolus specialis gre lahko za vojni zločin ali zločin proti človeškosti, ne pa za genocid (Konvencija čl. II)."
  },
  {
    q: "Sodbe Evropskega sodišča za človekove pravice (ESČP) so za države pogodbenice le priporočilo?",
    ans: false,
    expl: "PAST! Po čl. 46 EKČP so sodbe ESČP za toženo državo pogodbenico pravno ZAVEZUJOČE. Priporočila izdajajo odbori OZN."
  },
  {
    q: "Splošna deklaracija človekovih pravic (SDČP 1948) je bila sprejeta kot pravno zavezujoča konvencija?",
    ans: false,
    expl: "PAST! SDČP je resolucija GS OZN (skupni ideal) — pravno zavezujoči sta postali šele pakta (MPDPP in MPESKP) leta 1966/76."
  }
]

export default function ExamDashboard() {
  const [trapIdx, setTrapIdx] = useState(0)
  const [trapAnswered, setTrapAnswered] = useState<boolean | null>(null)
  const [trapScore, setTrapScore] = useState(0)
  const [trapActive, setTrapActive] = useState(false)

  const curTrap = TRAP_DRILL[trapIdx % TRAP_DRILL.length]

  function handleTrapAnswer(userChoice: boolean) {
    const isCorrect = userChoice === curTrap.ans
    setTrapAnswered(isCorrect)
    if (isCorrect) setTrapScore(s => s + 1)
  }

  function nextTrap() {
    setTrapAnswered(null)
    setTrapIdx(i => i + 1)
  }

  return (
    <div className="space-y-10">
      {/* Header */}
      <div>
        <div className="flex items-center gap-2 mb-2">
          <span className="badge bg-red-100 text-red-800 font-semibold px-2.5 py-1">
            ⚡ IZPIT JE 8. 9. — 4 DNI DO IZPITA
          </span>
          <span className="kicker">FDV · prof. dr. Petra Roter</span>
        </div>
        <h1 className="font-display text-4xl font-semibold tracking-tight">Izpitni načrt & simulator</h1>
        <p className="text-sm text-stone-600 mt-2 leading-relaxed max-w-2xl">
          75 minut, na papir · dovoljena knjiga <em>Dokumenti človekovih pravic</em> · minimum 35/60 točk ·
          odgovori v jedrnatih alinejah (vir + točen člen + mehanizem + avtor/primer).
        </p>
      </div>

      {/* 4-DAY SPRINT ROADMAP */}
      <section className="card !p-6 border-stone-300 bg-stone-50/70">
        <div className="flex flex-wrap items-baseline justify-between gap-2 mb-4">
          <h2 className="font-display text-xl font-semibold">📅 4-dnevni izpitni načrt (8. 9. 2026)</h2>
          <span className="text-xs text-stone-500 font-medium uppercase tracking-wider">Maksimalni izkoristek točk</span>
        </div>
        <div className="grid sm:grid-cols-2 md:grid-cols-4 gap-3">
          <div className="card !p-4 bg-white border-l-4 border-l-blue-600">
            <div className="kicker text-blue-700 mb-1">DAN 1 (4. 9.)</div>
            <div className="font-semibold text-sm">10 TOČK JEDRA</div>
            <p className="text-xs text-stone-600 mt-1.5 leading-relaxed">
              Vincent (5 elementov), Odbor vs. Svet vs. Komisija, običaj (38(1)(b)) vs. pogodba, ESČP formacije, DN vs. OZN.
            </p>
            <Link to="/exam/guide" className="inline-block mt-3 text-xs text-blue-600 font-medium">Odpri jedro →</Link>
          </div>

          <div className="card !p-4 bg-white border-l-4 border-l-amber-600">
            <div className="kicker text-amber-700 mb-1">DAN 2 (5. 9.)</div>
            <div className="font-semibold text-sm">6 "MUST-HAVE" TEM</div>
            <p className="text-xs text-stone-600 mt-1.5 leading-relaxed">
              Genocid (čl. II + dolus specialis), Mučenje (4 elementi CAT), Okolje (Stockholm→2022), Begunci (1A(2)), Izražanje (10(2)), ESKP (čl. 2(1)).
            </p>
            <Link to="/exam/guide" className="inline-block mt-3 text-xs text-amber-600 font-medium">Preglej 6 tem →</Link>
          </div>

          <div className="card !p-4 bg-white border-l-4 border-l-purple-600">
            <div className="kicker text-purple-700 mb-1">DAN 3 (6. 9.)</div>
            <div className="font-semibold text-sm">PASTI & ZELENI KAZIPOT</div>
            <p className="text-xs text-stone-600 mt-1.5 leading-relaxed">
              Reši Hitri drill pasti, nalepi zavihke v zeleni priročnik, preveri členske družine in reši vsa scenarijska vprašanja.
            </p>
            <button onClick={() => setTrapActive(true)} className="inline-block mt-3 text-xs text-purple-600 font-medium text-left">Zaženi drill pasti →</button>
          </div>

          <div className="card !p-4 bg-white border-l-4 border-l-red-600">
            <div className="kicker text-red-700 mb-1">DAN 4 (7. 9.)</div>
            <div className="font-semibold text-sm">2 CELOTNA MOCKA</div>
            <p className="text-xs text-stone-600 mt-1.5 leading-relaxed">
              Reši 1. rok 2026 na štoparico (75 min). Natisni A4 Cheat Sheet za branje v ponedeljek zjutraj pred predavalnico.
            </p>
            <Link to="/exam/simulator" className="inline-block mt-3 text-xs text-red-600 font-medium">Odpri simulator →</Link>
          </div>
        </div>
      </section>

      {/* QUICK-FIRE TRAPS DRILL */}
      <section className="card !p-6 border-amber-300 bg-amber-50/40">
        <div className="flex flex-wrap items-center justify-between gap-2 mb-4">
          <div>
            <div className="kicker text-amber-800">HITRI DRILL IZPITNIH PASTI</div>
            <h2 className="font-display text-xl font-semibold">Past ali Resnica? (Tipične napake na izpitu)</h2>
          </div>
          <span className="badge bg-amber-100 text-amber-900">
            Rezultat: {trapScore} / {trapIdx + (trapAnswered !== null ? 1 : 0)}
          </span>
        </div>

        <div className="space-y-4">
          <div className="p-4 bg-white rounded-xl border border-stone-200">
            <div className="text-xs text-stone-600 mb-1">Vprašanje {trapIdx + 1} / {TRAP_DRILL.length}:</div>
            <p className="font-medium text-base leading-snug">{curTrap.q}</p>
          </div>

          {trapAnswered === null ? (
            <div className="flex gap-3">
              <button
                onClick={() => handleTrapAnswer(true)}
                className="btn !bg-emerald-700 hover:!bg-emerald-600 text-white flex-1 min-h-[48px]"
              >
                ✓ RESNICA
              </button>
              <button
                onClick={() => handleTrapAnswer(false)}
                className="btn !bg-red-700 hover:!bg-red-600 text-white flex-1 min-h-[48px]"
              >
                ✗ PAST / NAPAČNO
              </button>
            </div>
          ) : (
            <div className="space-y-3 pt-2">
              <div className={`p-4 rounded-xl text-sm ${trapAnswered ? 'bg-emerald-100 text-emerald-950' : 'bg-red-100 text-red-950'}`}>
                <div className="font-bold mb-1">{trapAnswered ? 'Točno! Odlično poznaš to past.' : 'Napačno! Pozor na izpitu:'}</div>
                <div>{curTrap.expl}</div>
              </div>
              <button onClick={nextTrap} className="btn w-full">Naslednja past →</button>
            </div>
          )}
        </div>
      </section>

      {/* Quick Launch Buttons */}
      <div className="grid sm:grid-cols-4 gap-3">
        <Link to="/exam/guide" className="card card-hover !p-5">
          <div className="kicker mb-2">01</div>
          <div className="font-semibold text-sm">Vodnik (16 tem)</div>
          <div className="text-xs text-stone-500 mt-1">Pasporti s 4 sidri in točnimi členi</div>
        </Link>
        <Link to="/exam/green-book" className="card card-hover !p-5">
          <div className="kicker mb-2">02</div>
          <div className="font-semibold text-sm">Zeleni priročnik</div>
          <div className="text-xs text-stone-500 mt-1">Instant iskalnik členov + speed drill</div>
        </Link>
        <Link to="/exam/simulator" className="card card-hover !p-5">
          <div className="kicker mb-2">03</div>
          <div className="font-semibold text-sm">Simulator (75 min)</div>
          <div className="text-xs text-stone-500 mt-1">1. rok 2026, 2. rok 2026, 1. rok 2025</div>
        </Link>
        <Link to="/exam/print" className="card card-hover !p-5 border-blue-300 bg-blue-50/20">
          <div className="kicker text-blue-600 mb-2">04 PRINT</div>
          <div className="font-semibold text-sm">A4 Cheat Sheet</div>
          <div className="text-xs text-stone-500 mt-1">Zadnji dan: natisni in ponovi na busu</div>
        </Link>
      </div>

      {/* Core Blocks (Jedro) */}
      <section>
        <div className="flex items-baseline justify-between mb-3">
          <h2 className="kicker">JEDRO SNOVI — NA VSAKEM IZPITU (OBVEZNO ZNATI)</h2>
          <span className="text-xs text-stone-600">Klikni za celoten model odgovora</span>
        </div>
        <div className="space-y-2">
          {core.map((c, i) => (
            <details key={c.id} className="card !py-0">
              <summary className="cursor-pointer text-sm py-3.5 flex items-center gap-4 list-none font-medium">
                <span className="font-display text-stone-500 font-semibold">{String(i + 1).padStart(2, '0')}</span>
                <span className="flex-1">{c.title}</span>
                <span className="badge bg-stone-100 text-stone-700 text-xs">{c.points}T</span>
              </summary>
              <div className="pb-4 pt-2 border-t border-stone-100"><Md>{c.body}</Md></div>
            </details>
          ))}
        </div>
      </section>

      {/* 16 Seminar Topics */}
      <section>
        <div className="flex items-baseline justify-between mb-3">
          <h2 className="kicker">16 SEMINARSKIH TEM — BAZEN (PROFESORICA IZBERE 6, ŠTUDENT 4)</h2>
          <span className="text-xs text-stone-600">Vsebuje razširjene primere in avtorje</span>
        </div>
        <div className="grid sm:grid-cols-2 gap-2">
          {topics.map(t => (
            <Link key={t.id} to={`/exam/guide/${t.id}`} className="card card-hover !p-0 overflow-hidden block">
              <div className="flex items-center">
                <div className="w-14 shrink-0 text-center py-4 border-r border-stone-100 font-display text-stone-500">
                  {String(t.n).padStart(2, '0')}
                </div>
                <div className="px-4 py-3">
                  <div className="font-medium text-sm leading-snug flex items-center gap-1.5">
                    <span>{t.title}</span>
                    {t.status.includes('jedro') && <span className="text-[10px] bg-red-100 text-red-700 px-1.5 py-0.2 rounded font-semibold">JEDRO</span>}
                  </div>
                  <div className="text-[11px] text-stone-600 mt-0.5">{t.titleEn}</div>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </section>
    </div>
  )
}
