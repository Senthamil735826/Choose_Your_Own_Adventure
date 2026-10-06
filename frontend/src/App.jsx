import './App.css'
import { BrowserRouter as Router, Routes, Route } from "react-router-dom"
import StoryLoader from "./components/StoryLoader"
import StoryGenerator from "./components/StoryGenerator.jsx"

function App() {
  return (
    <Router basename={import.meta.env.DEV ? "/" : "/Choose_Your_Own_Adventure"}>
      <div className="app-container">
        <header>
          <h1>Interactive Story Generator</h1>
        </header>

        <main>
          <Routes>
            <Route path="/story/:id" element={<StoryLoader />} />
            <Route path="/" element={<StoryGenerator />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App