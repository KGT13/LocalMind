import { useEffect, useState } from "react";
import { getKbStats, getDocuments } from "../api";
import { Link } from "react-router-dom";
import { UploadCloud, Library, MessageSquare, Search, FileText, BrainCircuit, GitCompare, File as FileIcon } from "lucide-react";

export default function Dashboard() {
  const [stats, setStats] = useState({ documents: 0, chunks: 0, status: "Loading..." });
  const [docs, setDocs] = useState<{name: string, chunks: number}[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([getKbStats(), getDocuments()])
      .then(([statsData, docsData]) => {
        setStats(statsData);
        setDocs(docsData);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  const features = [
    { to: "/upload", icon: <UploadCloud className="w-8 h-8 text-blue-500" />, label: "Upload Documents" },
    { to: "/library", icon: <Library className="w-8 h-8 text-indigo-500" />, label: "Document Library" },
    { to: "/ask", icon: <MessageSquare className="w-8 h-8 text-emerald-500" />, label: "Ask LocalMind" },
    { to: "/search", icon: <Search className="w-8 h-8 text-amber-500" />, label: "Semantic Search" },
    { to: "/summarize", icon: <FileText className="w-8 h-8 text-purple-500" />, label: "Summarize" },
    { to: "/quiz", icon: <BrainCircuit className="w-8 h-8 text-rose-500" />, label: "Quiz Mode" },
    { to: "/compare", icon: <GitCompare className="w-8 h-8 text-cyan-500" />, label: "Compare Docs" },
  ];

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div>
        <h1 className="text-4xl font-extrabold tracking-tight text-[var(--accent)] mb-2">
          LocalMind
        </h1>
        <p className="text-lg text-[var(--text-secondary)] font-medium">
          AI That Stays With You — Your private, local knowledge assistant
        </p>
      </div>

      {error && (
        <div className="p-4 bg-red-50 dark:bg-red-500/10 border border-red-200 dark:border-red-500/20 rounded-xl text-red-600 dark:text-red-400">
          Failed to connect to the backend. Is FastAPI running? ({error})
        </div>
      )}

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="glass-card">
          <p className="text-[0.75rem] font-semibold text-[var(--text-secondary)] uppercase tracking-[0.1em] mb-2">Documents</p>
          <p className="text-4xl font-bold text-[var(--text-primary)]">{loading ? "-" : stats.documents}</p>
        </div>
        <div className="glass-card">
          <p className="text-[0.75rem] font-semibold text-[var(--text-secondary)] uppercase tracking-[0.1em] mb-2">Indexed Chunks</p>
          <p className="text-4xl font-bold text-[var(--text-primary)]">{loading ? "-" : stats.chunks}</p>
        </div>
        <div className="glass-card">
          <p className="text-[0.75rem] font-semibold text-[var(--text-secondary)] uppercase tracking-[0.1em] mb-2">Knowledge Base</p>
          <div className="flex items-center gap-2">
            <div className={`w-3 h-3 rounded-full ${stats.status === 'Online' ? 'bg-[var(--success-text)]' : 'bg-[var(--text-muted)]'}`} />
            <p className="text-4xl font-bold text-[var(--text-primary)]">{loading ? "-" : stats.status}</p>
          </div>
        </div>
      </div>

      <hr className="border-[var(--border)] my-8 section-divider" />

      {/* Quick Actions */}
      <div>
        <h2 className="text-xl font-bold mb-6 flex items-center gap-2 text-[var(--text-primary)]">
          <Search className="text-[var(--accent)]" /> What would you like to do?
        </h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {features.map((f) => (
            <Link 
              key={f.to} 
              to={f.to}
              className="glass-card group flex flex-col items-center text-center gap-4 hover:border-[var(--accent)] hover:shadow-lg transition-all duration-300 min-h-[120px]"
            >
              <div className="p-3 bg-[var(--bg-secondary)] rounded-xl group-hover:scale-110 group-hover:bg-[var(--accent-bg)] transition-all duration-300">
                {f.icon}
              </div>
              <span className="font-semibold text-[var(--text-primary)]">{f.label}</span>
            </Link>
          ))}
        </div>
      </div>

      {/* Recent Docs */}
      <div className="pt-4">
        <h2 className="text-xl font-bold mb-6 flex items-center gap-2 text-[var(--text-primary)]">
          <FileIcon className="text-[var(--accent)]" /> Documents in Knowledge Base
        </h2>
        <div className="space-y-3">
          {!loading && docs.length === 0 ? (
            <div className="p-6 text-center border-2 border-dashed border-[var(--border)] rounded-2xl text-[var(--text-secondary)]">
              No documents uploaded yet. Head to <Link to="/upload" className="text-[var(--accent)] font-medium hover:underline">Upload</Link> to get started!
            </div>
          ) : (
            docs.map(doc => (
              <div key={doc.name} className="glass-card flex items-center justify-between p-4 mb-3 cursor-default hover:border-[var(--accent)]">
                <div className="flex items-center gap-3">
                  <FileIcon className="text-[var(--accent)] w-5 h-5" />
                  <span className="font-semibold text-[var(--text-primary)]">{doc.name}</span>
                </div>
                <span className="text-xs font-semibold px-2.5 py-1 bg-[var(--accent-bg)] text-[var(--accent)] rounded-full border border-[var(--border)]">
                  {doc.chunks} chunks
                </span>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
