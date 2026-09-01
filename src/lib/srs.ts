import { fsrs, generatorParameters, createEmptyCard, type Grade, type Card as FSRSCard, type RecordLogItem } from 'ts-fsrs'
import { db, type CardState } from '../db/db'

const params = generatorParameters({ request_retention: 0.9, enable_fuzz: true })
const scheduler = fsrs(params)

export function emptyState(cardId: string): CardState {
  const c = createEmptyCard()
  return { cardId, due: c.due.getTime(), stability: c.stability, difficulty: c.difficulty, reps: c.reps, lapses: c.lapses, state: 'new' }
}

function toFsrs(s: CardState): FSRSCard {
  return {
    due: new Date(s.due), stability: s.stability, difficulty: s.difficulty,
    elapsed_days: 0, scheduled_days: 0, reps: s.reps, lapses: s.lapses,
    state: s.state === 'review' ? 2 : s.state === 'learning' ? 1 : s.state === 'relearning' ? 3 : 0,
  } as FSRSCard
}

function fromFsrs(cardId: string, c: FSRSCard, grade: Grade): CardState {
  return {
    cardId, due: c.due.getTime(), stability: c.stability, difficulty: c.difficulty,
    reps: c.reps, lapses: c.lapses,
    state: c.state === 2 ? 'review' : c.state === 1 ? 'learning' : c.state === 3 ? 'relearning' : 'new',
    lastGrade: grade,
  }
}

export async function gradeCard(cardId: string, grade: Grade): Promise<CardState> {
  let s = await db.cardStates.get(cardId)
  if (!s) s = emptyState(cardId)
  const now = new Date()
  const record: RecordLogItem = scheduler.repeat(toFsrs(s), now)[grade]
  const next = fromFsrs(cardId, record.card, grade)
  await db.cardStates.put(next)
  return next
}

export async function dueCards(allIds: string[]): Promise<string[]> {
  const now = Date.now()
  const states = await db.cardStates.bulkGet(allIds)
  const due: string[] = []
  allIds.forEach((id, i) => {
    const s = states[i]
    if (!s || s.due <= now) due.push(id)
  })
  return due
}

export async function srsStats(allIds: string[]) {
  const states = await db.cardStates.bulkGet(allIds)
  const now = Date.now()
  let newC = 0, learning = 0, review = 0, due = 0
  for (const s of states) {
    if (!s) { newC++; due++; continue }
    if (s.state === 'review') review++
    else learning++
    if (s.due <= now) due++
  }
  return { total: allIds.length, new: newC, learning, review, due }
}
