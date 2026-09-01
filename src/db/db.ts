import Dexie, { type Table } from 'dexie'

export interface CardState {
  cardId: string
  due: number          // timestamp
  stability: number
  difficulty: number
  reps: number
  lapses: number
  state: 'new' | 'learning' | 'review' | 'relearning'
  lastGrade?: 1 | 2 | 3 | 4
}

export interface QuizAttempt {
  id?: number
  questionId: string
  score: number        // 0..points self-scored
  points: number
  confidence: 1 | 2 | 3 | 4
  at: number
  mode: 'quiz' | 'exam' | 'practice'
}

export interface Settings {
  key: string
  value: unknown
}

export interface TopicMastery {
  topicId: string
  level: 'red' | 'yellow' | 'green'
  updatedAt: number
}

class MvcpDB extends Dexie {
  cardStates!: Table<CardState, string>
  quizAttempts!: Table<QuizAttempt, number>
  settings!: Table<Settings, string>
  topicMastery!: Table<TopicMastery, string>

  constructor() {
    super('mvcp-academy')
    this.version(1).stores({
      cardStates: 'cardId, due, state',
      quizAttempts: '++id, questionId, at, mode',
      settings: 'key',
      topicMastery: 'topicId, updatedAt',
    })
  }
}

export const db = new MvcpDB()

export async function exportBackup(): Promise<string> {
  const [cardStates, quizAttempts, settings, topicMastery] = await Promise.all([
    db.cardStates.toArray(), db.quizAttempts.toArray(), db.settings.toArray(), db.topicMastery.toArray(),
  ])
  return JSON.stringify({ schemaVersion: 1, exportedAt: new Date().toISOString(), cardStates, quizAttempts, settings, topicMastery }, null, 1)
}

export async function importBackup(json: string): Promise<void> {
  const d = JSON.parse(json)
  if (!d.schemaVersion) throw new Error('Neveljavna varnostna kopija')
  await db.transaction('rw', db.cardStates, db.quizAttempts, db.settings, db.topicMastery, async () => {
    await db.cardStates.clear(); if (d.cardStates) await db.cardStates.bulkPut(d.cardStates)
    await db.quizAttempts.clear(); if (d.quizAttempts) await db.quizAttempts.bulkPut(d.quizAttempts)
    await db.settings.clear(); if (d.settings) await db.settings.bulkPut(d.settings)
    await db.topicMastery.clear(); if (d.topicMastery) await db.topicMastery.bulkPut(d.topicMastery)
  })
}

export async function getSetting<T>(key: string, fallback: T): Promise<T> {
  const row = await db.settings.get(key)
  return row ? (row.value as T) : fallback
}

export async function setSetting(key: string, value: unknown): Promise<void> {
  await db.settings.put({ key, value })
}
