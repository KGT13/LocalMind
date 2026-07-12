import React from 'react'
import ReactDOM from 'react-dom/client'
import { HashRouter, Routes, Route } from 'react-router-dom'
import { Layout } from './components/Layout'
import { SetupGuard } from './components/SetupGuard'
import Dashboard from './pages/Dashboard'
import Upload from './pages/Upload'
import Library from './pages/Library'
import Ask from './pages/Ask'
import Search from './pages/Search'
import Summarize from './pages/Summarize'
import Compare from './pages/Compare'
import Quiz from './pages/Quiz'
import Settings from './pages/Settings'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <HashRouter>
      <SetupGuard>
        <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="upload" element={<Upload />} />
          <Route path="library" element={<Library />} />
          <Route path="ask" element={<Ask />} />
          <Route path="search" element={<Search />} />
          <Route path="summarize" element={<Summarize />} />
          <Route path="compare" element={<Compare />} />
          <Route path="quiz" element={<Quiz />} />
          <Route path="settings" element={<Settings />} />
        </Route>
      </Routes>
      </SetupGuard>
    </HashRouter>
  </React.StrictMode>,
)
