import entitiesData from '../data/entities.json'
import coreData from '../data/core.json'
import topicsData from '../data/topics.json'
import comparisonsData from '../data/comparisons.json'
import flashcardsData from '../data/flashcards.json'
import quizData from '../data/quiz.json'
import sourcesData from '../data/sources.json'
import greenbookData from '../data/greenbook.json'
import examsData from '../data/exams.json'
import glossaryData from '../data/glossary.json'
import docsData from '../data/docs-manifest.json'
import seminarsData from '../data/seminars.json'

export interface Entity { id: string; type: string; typeSl: string; label: string; facts: string; authority: string }
export interface CoreBlock { id: string; title: string; titleEn: string; points: number; body: string }
export interface Topic { id: string; n: number; title: string; titleEn: string; status: string; legal: string; monitoring: string; problems: string; model: string; materials: string[] }
export interface Comparison { id: string; title: string; rows: string[][] }
export interface Flashcard { id: string; prompt: string; answer: string; kind: string; topics: string[]; authority: string; source?: string }
export interface QuizQ { id: string; type: string; prompt: string; points: number; topics: string[]; answerOutline: string[]; provenance: string; officialStatus: string; keywords?: string[]; mcq?: { options: string[]; correct: number } | null }
export interface Source { id: string; title: string; titleEn?: string; url: string; body: string; topics: string[] }
export interface GreenBookEntry { topic: string; articles: string; inBook?: boolean; bookPages?: string; missingWarning?: string | null }
export interface Exam { id: string; title: string; year: number; durationMin: number; questionIds: string[]; formatNote: string }
export interface GlossaryItem { term: string; sl: string }
export interface DocManifestItem { id: string; title: string; url: string; file: string; topics: string[]; authority: string }
export interface Seminar { id: string; n: number; title: string; folder: string; convention: string; definition: string; omejitve: string; pomembnost: string; izzivi: string; primeri: string; studentWork: string[]; examQuestions: string[] }

export const entities = entitiesData.entities as Entity[]
export const entityEdges = entitiesData.edges as { source: string; target: string; relation: string; authority: string; note: string }[]
export const core = coreData as CoreBlock[]
export const topics = topicsData as Topic[]
export const comparisons = comparisonsData as Comparison[]
export const flashcards = flashcardsData as Flashcard[]
export const quiz = (quizData as unknown) as QuizQ[]
export const sources = sourcesData as Source[]
export const greenbook = greenbookData as GreenBookEntry[]
export const exams = examsData as Exam[]
export const glossary = glossaryData as GlossaryItem[]
export const docsManifest = docsData as DocManifestItem[]
export const seminars = seminarsData as Seminar[]

export const entityById = Object.fromEntries(entities.map(e => [e.id, e]))
export const topicById = Object.fromEntries(topics.map(t => [t.id, t]))
export const quizById = Object.fromEntries(quiz.map(q => [q.id, q]))

export const TOPIC_COLORS: Record<string, string> = {
  history: '#7c3aed', treaty: '#2563eb', institution: '#ea580c', procedure: '#a855f7',
  right: '#16a34a', concept: '#059669', problem: '#b45309', case: '#dc2626',
  author: '#0d9488', exam: '#e11d48', material: '#64748b',
}
export const TYPE_NAMES: Record<string, string> = {
  history: 'Zgodovina', treaty: 'Pogodbe', institution: 'Institucije', procedure: 'Postopki',
  right: 'Pravice', concept: 'Koncepti', problem: 'Težave', case: 'Primeri',
  author: 'Avtorji', exam: 'Izpitna vprašanja', material: 'Gradiva',
}
export const AUTHORITY_LABELS: Record<string, string> = {
  A: 'A — primarni dokument', B: 'B — profesorica', C: 'C — znanstveni članek',
  D: 'D — sinteza zapiskov', E: 'E — spomin študentov',
}
