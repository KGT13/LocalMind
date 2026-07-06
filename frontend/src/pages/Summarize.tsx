import { useEffect, useState, useRef } from "react";
import { FileText, Wand2, Loader2, AlertCircle } from "lucide-react";
import { getDocuments } from "../api";

export default function Summarize() {
  const [docs, setDocs] = useState<{name: string}[]>([]);
  const [selectedDoc, setSelectedDoc] = useState("");
  const [instruction, setInstruction] = useState("Provide a comprehensive summary of this document, highlighting the key points, main arguments, and conclusions.");
  
  const [summary, setSummary] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const summaryEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    getDocuments().then(data => {
      setDocs(data);
      if (data.length > 0) setSelectedDoc(data[0].name);
    }).catch(console.error);
  }, []);

  const handleSummarize = async () => {
    if (!selectedDoc) return;
    
    setIsGenerating(true);
    setSummary("");
    setError(null);
    
    try {
      const res = await fetch("http://localhost:8000/api/summarize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          document: selectedDoc,
          instruction: instruction
        })
      });

      if (!res.body) throw new Error("No response body");
      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      
      let done = false;
      while (!done) {
        const { value, done: readerDone } = await reader.read();
        done = readerDone;
        if (value) {
          const chunk = decoder.decode(value);
          const lines = chunk.split("\n");
          for (const line of lines) {
            if (line.startsWith("data:")) {
              const dataStr = line.replace("data:", "").trim();
              if (dataStr === "done") {
                done = true;
                break;
              }
              try {
                const data = JSON.parse(dataStr);
                if (data.text) {
                  setSummary(prev => prev + data.text);
                  summaryEndRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
                }
              } catch (e) {
                console.error("Parse error", e);
              }
            }
          }
        }
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="max-w-4xl animate-in fade-in duration-500 h-full flex flex-col">
      <div className="mb-6 shrink-0">
        <h1 className="text-3xl font-extrabold flex items-center gap-3 text-[var(--text-primary)] mb-2">
          <FileText className="w-8 h-8 text-[var(--accent)]" /> Summarize
        </h1>
        <p className="text-[var(--text-secondary)]">
          Generate comprehensive summaries of entire documents using local AI.
        </p>
      </div>

      <div className="glass-card mb-6 shrink-0">
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-semibold text-[var(--text-secondary)] mb-1">Select Document</label>
            <select 
              value={selectedDoc}
              onChange={(e) => setSelectedDoc(e.target.value)}
              className="w-full p-3 bg-[var(--bg-secondary)] text-[var(--text-primary)] border border-[var(--border)] rounded-xl outline-none focus:border-[var(--accent)] transition-colors"
            >
              {docs.length === 0 && <option value="">No documents available</option>}
              {docs.map(doc => (
                <option key={doc.name} value={doc.name}>{doc.name}</option>
              ))}
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-semibold text-[var(--text-secondary)] mb-1">Summary Instruction</label>
            <textarea 
              rows={3}
              value={instruction}
              onChange={(e) => setInstruction(e.target.value)}
              className="w-full p-3 bg-[var(--bg-secondary)] text-[var(--text-primary)] border border-[var(--border)] rounded-xl outline-none focus:border-[var(--accent)] transition-colors resize-none"
            />
          </div>
          
          <button 
            onClick={handleSummarize}
            disabled={!selectedDoc || isGenerating}
            className="w-full btn-primary p-3.5 rounded-xl font-semibold transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 shadow-sm"
          >
            {isGenerating ? <><Loader2 className="animate-spin w-5 h-5" /> Generating Summary...</> : <><Wand2 className="w-5 h-5" /> Generate Summary</>}
          </button>
        </div>
      </div>

      {error && (
        <div className="mb-6 p-4 bg-[var(--danger-bg)] border border-[var(--danger-border)] rounded-xl flex items-start gap-3 text-[var(--danger-text)] shrink-0">
          <AlertCircle className="w-5 h-5 mt-0.5 shrink-0" />
          <p>{error}</p>
        </div>
      )}

      {/* Summary Output */}
      {(summary || isGenerating) && (
        <div className="flex-1 glass-card overflow-y-auto min-h-[300px]">
          <h2 className="text-lg font-bold text-[var(--text-primary)] mb-6 flex items-center gap-2 border-b border-[var(--border)] pb-4">
            <Wand2 className="w-5 h-5 text-[var(--accent)]" /> Generated Summary for {selectedDoc}
          </h2>
          <div className="prose dark:prose-invert max-w-none whitespace-pre-wrap leading-relaxed text-[var(--text-primary)]">
            {summary}
            {isGenerating && (
              <span className="inline-block w-2 h-4 bg-[var(--accent)] ml-1 animate-pulse"></span>
            )}
          </div>
          <div ref={summaryEndRef} />
        </div>
      )}
    </div>
  );
}
