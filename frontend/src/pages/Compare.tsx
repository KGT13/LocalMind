import { useEffect, useState } from "react";
import { GitCompare, Loader2, AlertCircle, CheckCircle } from "lucide-react";
import { getDocuments, compareDocs } from "../api";

export default function Compare() {
  const [docs, setDocs] = useState<{name: string}[]>([]);
  const [docA, setDocA] = useState("");
  const [docB, setDocB] = useState("");
  
  const [comparison, setComparison] = useState<any>(null);
  const [isComparing, setIsComparing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getDocuments().then(data => {
      setDocs(data);
      if (data.length >= 2) {
        setDocA(data[0].name);
        setDocB(data[1].name);
      }
    }).catch(console.error);
  }, []);

  const handleCompare = async () => {
    if (!docA || !docB || docA === docB) return;
    
    setIsComparing(true);
    setComparison(null);
    setError(null);
    
    try {
      const res = await compareDocs(docA, docB);
      if (res.error) throw new Error(res.error);
      setComparison(res);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsComparing(false);
    }
  };

  return (
    <div className="max-w-5xl animate-in fade-in duration-500">
      <div className="mb-8">
        <h1 className="text-3xl font-extrabold flex items-center gap-3 text-[var(--text-primary)] mb-2">
          <GitCompare className="w-8 h-8 text-[var(--accent)]" /> Compare Documents
        </h1>
        <p className="text-[var(--text-secondary)]">
          Identify key differences and similarities between two documents.
        </p>
      </div>

      <div className="glass-card mb-8">
        <div className="flex flex-col md:flex-row items-center gap-4">
          <div className="flex-1 w-full">
            <label className="block text-sm font-semibold text-[var(--text-secondary)] mb-1">Document A</label>
            <select 
              value={docA}
              onChange={(e) => setDocA(e.target.value)}
              className="w-full p-3 bg-[var(--bg-secondary)] text-[var(--text-primary)] border border-[var(--border)] rounded-xl outline-none focus:border-[var(--accent)] transition-colors"
            >
              <option value="">Select Document...</option>
              {docs.map(doc => (
                <option key={doc.name} value={doc.name}>{doc.name}</option>
              ))}
            </select>
          </div>
          
          <div className="shrink-0 flex items-center justify-center mt-6">
            <div className="w-10 h-10 rounded-full bg-[var(--accent-bg)] flex items-center justify-center">
              <span className="text-[var(--accent)] font-bold text-sm">VS</span>
            </div>
          </div>
          
          <div className="flex-1 w-full">
            <label className="block text-sm font-semibold text-[var(--text-secondary)] mb-1">Document B</label>
            <select 
              value={docB}
              onChange={(e) => setDocB(e.target.value)}
              className="w-full p-3 bg-[var(--bg-secondary)] text-[var(--text-primary)] border border-[var(--border)] rounded-xl outline-none focus:border-[var(--accent)] transition-colors"
            >
              <option value="">Select Document...</option>
              {docs.map(doc => (
                <option key={doc.name} value={doc.name}>{doc.name}</option>
              ))}
            </select>
          </div>
        </div>

        {docA && docB && docA === docB && (
          <p className="text-amber-600 dark:text-amber-400 text-sm mt-3 flex items-center gap-1 font-medium">
            <AlertCircle className="w-4 h-4" /> Please select two different documents to compare.
          </p>
        )}

        <button 
          onClick={handleCompare}
          disabled={!docA || !docB || docA === docB || isComparing}
          className="w-full mt-6 btn-primary p-3.5 rounded-xl font-semibold transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 shadow-sm"
        >
          {isComparing ? <><Loader2 className="animate-spin w-5 h-5" /> Analyzing differences...</> : "Run Comparison"}
        </button>
      </div>

      {error && (
        <div className="mb-6 p-4 bg-red-50 dark:bg-red-500/10 border border-red-200 dark:border-red-500/20 rounded-xl flex items-start gap-3 text-red-600 dark:text-red-400">
          <AlertCircle className="w-5 h-5 mt-0.5 shrink-0" />
          <p>{error}</p>
        </div>
      )}

      {comparison && (
        <div className="animate-in slide-in-from-bottom-4 duration-500 space-y-6">
          <div className="glass-card">
            <h2 className="text-xl font-bold text-[var(--text-primary)] mb-6 border-b border-[var(--border)] pb-4 flex items-center gap-2">
              <CheckCircle className="text-[var(--success-text)] w-6 h-6" /> Key Similarities
            </h2>
            <div className="prose dark:prose-invert max-w-none">
              <ul className="space-y-2">
                {comparison.similarities.map((item: string, i: number) => (
                  <li key={i} className="text-[var(--text-secondary)] bg-[var(--bg-secondary)] p-3 rounded-lg border border-[var(--border)]">
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          </div>
          
          <div className="glass-card">
            <h2 className="text-xl font-bold text-[var(--text-primary)] mb-6 border-b border-[var(--border)] pb-4 flex items-center gap-2">
              <GitCompare className="text-[var(--warning-text)] w-6 h-6" /> Key Differences
            </h2>
            <div className="prose dark:prose-invert max-w-none">
              <ul className="space-y-2">
                {comparison.differences.map((item: string, i: number) => (
                  <li key={i} className="text-[var(--text-secondary)] bg-[var(--bg-secondary)] p-3 rounded-lg border border-[var(--border)]">
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          </div>
          
          <div className="glass-card">
            <h2 className="text-xl font-bold text-[var(--text-primary)] mb-6 border-b border-[var(--border)] pb-4">
              Detailed Summary
            </h2>
            <div className="prose dark:prose-invert max-w-none whitespace-pre-wrap text-[var(--text-secondary)] leading-relaxed">
              {comparison.summary}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
