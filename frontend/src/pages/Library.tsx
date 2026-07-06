import { useEffect, useState } from "react";
import { getDocuments, deleteDocument } from "../api";
import { Library as LibraryIcon, FileText, Trash2, Loader2, AlertCircle } from "lucide-react";
import { Link } from "react-router-dom";

export default function Library() {
  const [docs, setDocs] = useState<{name: string, chunks: number}[]>([]);
  const [loading, setLoading] = useState(true);
  const [deleting, setDeleting] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const fetchDocs = () => {
    setLoading(true);
    getDocuments()
      .then(setDocs)
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchDocs();
  }, []);

  const handleDelete = async (filename: string) => {
    if (!confirm(`Are you sure you want to delete ${filename}?`)) return;
    setDeleting(filename);
    try {
      await deleteDocument(filename);
      fetchDocs();
    } catch (err: any) {
      alert("Error deleting document: " + err.message);
    } finally {
      setDeleting(null);
    }
  };

  return (
    <div className="max-w-4xl animate-in fade-in duration-500">
      <div className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-extrabold flex items-center gap-3 text-[var(--text-primary)] mb-2">
            <LibraryIcon className="w-8 h-8 text-[var(--accent)]" /> Document Library
          </h1>
          <p className="text-[var(--text-secondary)]">
            Manage files currently indexed in your knowledge base.
          </p>
        </div>
        <Link 
          to="/upload" 
          className="btn-primary shadow-sm"
        >
          + Add Document
        </Link>
      </div>

      {error && (
        <div className="mb-6 p-4 bg-red-50 dark:bg-red-500/10 border border-red-200 dark:border-red-500/20 rounded-xl flex items-start gap-3 text-red-600 dark:text-red-400">
          <AlertCircle className="w-5 h-5 mt-0.5 shrink-0" />
          <p>{error}</p>
        </div>
      )}

      <div className="glass-card !p-0 overflow-hidden">
        {loading ? (
          <div className="p-12 flex justify-center">
            <Loader2 className="w-8 h-8 animate-spin text-indigo-500" />
          </div>
        ) : docs.length === 0 ? (
          <div className="p-16 flex flex-col items-center justify-center text-center bg-[var(--bg-secondary)]">
            <div className="w-16 h-16 bg-[var(--bg-card)] rounded-full flex items-center justify-center mb-4 border border-[var(--border)]">
              <LibraryIcon className="w-8 h-8 text-[var(--text-muted)]" />
            </div>
            <h3 className="text-xl font-bold text-[var(--text-primary)] mb-2">Your library is empty</h3>
            <p className="text-[var(--text-secondary)] max-w-sm mb-6">
              Upload PDF, DOCX, TXT, or MD files to start building your personal AI knowledge base.
            </p>
            <Link 
              to="/upload" 
              className="bg-[var(--bg-card)] border border-[var(--border)] hover:border-[var(--accent)] text-[var(--text-primary)] px-6 py-2.5 rounded-xl font-medium transition-colors shadow-sm"
            >
              Go to Upload Page
            </Link>
          </div>
        ) : (
          <div className="divide-y divide-[var(--border)]">
            {docs.map(doc => (
              <div key={doc.name} className="p-4 sm:p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-4 hover:bg-[var(--bg-secondary)] transition-colors">
                <div className="flex items-start gap-4">
                  <div className="w-10 h-10 rounded-lg bg-[var(--accent-bg)] flex items-center justify-center shrink-0">
                    <FileText className="w-5 h-5 text-[var(--accent)]" />
                  </div>
                  <div>
                    <h4 className="font-semibold text-[var(--text-primary)]">{doc.name}</h4>
                    <p className="text-sm text-[var(--text-secondary)] mt-1">
                      {doc.chunks} indexed chunks
                    </p>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <Link 
                    to={`/ask?doc=${encodeURIComponent(doc.name)}`}
                    className="px-4 py-2 text-sm font-medium text-[var(--text-primary)] bg-[var(--bg-card)] border border-[var(--border)] rounded-lg hover:bg-[var(--bg-secondary)] transition-colors shadow-sm"
                  >
                    Ask about this
                  </Link>
                  <button 
                    onClick={() => handleDelete(doc.name)}
                    disabled={deleting === doc.name}
                    className="p-2 text-[var(--text-muted)] hover:text-[var(--danger-text)] hover:bg-[var(--danger-bg)] rounded-lg transition-colors disabled:opacity-50"
                    title="Delete document"
                  >
                    {deleting === doc.name ? <Loader2 className="w-5 h-5 animate-spin" /> : <Trash2 className="w-5 h-5" />}
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
