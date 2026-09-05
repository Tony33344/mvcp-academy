import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Home from './pages/Home'
import ExamDashboard from './pages/ExamDashboard'
import Guide, { TopicDetail } from './pages/Guide'
import GreenBook from './pages/GreenBook'
import Simulator from './pages/Simulator'
import Learn from './pages/Learn'
import Seminars from './pages/Seminars'
import Practice from './pages/Practice'
import Flashcards from './pages/Flashcards'
import Quiz from './pages/Quiz'
import Graph from './pages/Graph'
import Sources from './pages/Sources'
import Progress from './pages/Progress'
import About from './pages/About'
import CheatSheetPrint from './pages/CheatSheetPrint'

export default function App() {
  return (
    <Routes>
      <Route path="/exam/print" element={<CheatSheetPrint />} />
      <Route element={<Layout />}>
        <Route path="/" element={<Home />} />
        <Route path="/exam" element={<ExamDashboard />} />
        <Route path="/exam/guide" element={<Guide />} />
        <Route path="/exam/guide/:topicId" element={<TopicDetail />} />
        <Route path="/exam/green-book" element={<GreenBook />} />
        <Route path="/exam/simulator" element={<Simulator />} />
        <Route path="/learn" element={<Learn />} />
        <Route path="/learn/seminars" element={<Seminars />} />
        <Route path="/practice" element={<Practice />} />
        <Route path="/practice/flashcards" element={<Flashcards />} />
        <Route path="/practice/quiz" element={<Quiz />} />
        <Route path="/explore" element={<Graph />} />
        <Route path="/sources" element={<Sources />} />
        <Route path="/progress" element={<Progress />} />
        <Route path="/about" element={<About />} />
        <Route path="*" element={<Home />} />
      </Route>
    </Routes>
  )
}
