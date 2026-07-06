import { useState } from "react";
import { uploadFile, uploadText } from "../api";
import { Upload, FileText, CheckCircle2, AlertCircle, Loader2 } from "lucide-react";

export default function UploadPage() {
  const [tab, setTab] = useState<"files" | "text">("files");
  
  // File state
  const [file, setFile] = useState<File | null>(null);
  
  // Text state
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  
  // Progress state
  const [isUploading, setIsUploading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileUpload = async () => {
    if (!file) return;
    setIsUploading(true);
    setResult(null);
    setError(null);
    try {
      const res = await uploadFile(file);
      setResult(res);
      setFile(null);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message);
    } finally {
      setIsUploading(false);
    }
  };

  const handleTextUpload = async () => {
    if (!title.trim() || !content.trim()) return;
    setIsUploading(true);
    setResult(null);
    setError(null);
    try {
      const res = await uploadText(title, content);
      setResult(res);
      setTitle("");
      setContent("");
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="max-w-3xl animate-in fade-in duration-500">
      <div className="mb-8">
        <h1 className="text-3xl font-extrabold flex items-center gap-3 text-[var(--text-primary)] mb-2">
          <Upload className="w-8 h-8 text-[var(--accent)]" /> Add Documents
        </h1>
        <p className="text-[var(--text-secondary)]">
          Add documents to your local knowledge base by uploading files or writing text directly.
        </p>
      </div>

      <div className="flex border-b border-[var(--border)] mb-6">
        <button
          onClick={() => setTab("files")}
          className={`px-4 py-3 font-medium text-sm transition-colors border-b-2 ${
            tab === "files" ? "border-[var(--accent)] text-[var(--accent)]" : "border-transparent text-[var(--text-secondary)] hover:text-[var(--text-primary)]"
          }`}
        >
          Upload Files
        </button>
        <button
          onClick={() => setTab("text")}
          className={`px-4 py-3 font-medium text-sm transition-colors border-b-2 ${
            tab === "text" ? "border-[var(--accent)] text-[var(--accent)]" : "border-transparent text-[var(--text-secondary)] hover:text-[var(--text-primary)]"
          }`}
        >
          Write Text
        </button>
      </div>

      <div className="glass-card">
        {tab === "files" ? (
          <div className="space-y-6">
            <div className="border-2 border-dashed border-[var(--border)] hover:border-[var(--accent)] rounded-2xl p-10 flex flex-col items-center justify-center text-center bg-[var(--bg-secondary)] transition-colors group">
              <Upload className="w-12 h-12 text-[var(--text-muted)] group-hover:text-[var(--accent)] transition-colors mb-4" />
              <p className="text-lg font-medium text-[var(--text-primary)] mb-2">
                Click to browse or drag and drop
              </p>
              <p className="text-sm text-[var(--text-secondary)] mb-6">
                Supports PDF, DOCX, TXT, MD
              </p>
              <label className="btn-primary px-6 py-2.5 rounded-xl font-medium cursor-pointer shadow-sm">
                Select File
                <input 
                  type="file" 
                  className="hidden" 
                  accept=".pdf,.docx,.txt,.md"
                  onChange={(e) => setFile(e.target.files?.[0] || null)}
                />
              </label>
            </div>
            
            {file && (
              <div className="flex items-center justify-between p-4 bg-[var(--bg-secondary)] rounded-xl border border-[var(--border)]">
                <div className="flex items-center gap-3">
                  <FileText className="text-[var(--accent)] w-5 h-5" />
                  <span className="font-semibold text-[var(--text-primary)]">{file.name}</span>
                </div>
                <span className="text-sm font-medium text-[var(--text-secondary)]">{(file.size / 1024).toFixed(1)} KB</span>
              </div>
            )}
            
            <button 
              onClick={handleFileUpload}
              disabled={!file || isUploading}
              className="w-full btn-primary p-3.5 rounded-xl font-semibold transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 shadow-sm"
            >
              {isUploading ? <><Loader2 className="animate-spin w-5 h-5" /> Processing...</> : "Ingest Document"}
            </button>
          </div>
        ) : (
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-semibold text-[var(--text-secondary)] mb-1">Document Title</label>
              <input 
                type="text" 
                value={title}
                onChange={e => setTitle(e.target.value)}
                placeholder="e.g., meeting_notes"
                className="w-full p-3 bg-[var(--bg-secondary)] text-[var(--text-primary)] border border-[var(--border)] rounded-xl focus:ring-1 focus:ring-[var(--accent)] focus:border-[var(--accent)] outline-none transition-all"
              />
            </div>
            <div>
              <label className="block text-sm font-semibold text-[var(--text-secondary)] mb-1">Content</label>
              <textarea 
                rows={10}
                value={content}
                onChange={e => setContent(e.target.value)}
                placeholder="Type or paste your text here..."
                className="w-full p-3 bg-[var(--bg-secondary)] text-[var(--text-primary)] border border-[var(--border)] rounded-xl focus:ring-1 focus:ring-[var(--accent)] focus:border-[var(--accent)] outline-none transition-all resize-none"
              />
            </div>
            <button 
              onClick={handleTextUpload}
              disabled={!title.trim() || !content.trim() || isUploading}
              className="w-full btn-primary p-3.5 rounded-xl font-semibold transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 shadow-sm"
            >
              {isUploading ? <><Loader2 className="animate-spin w-5 h-5" /> Processing...</> : "Save & Ingest Text"}
            </button>
          </div>
        )}

        {/* Results */}
        {result && (
          <div className={`mt-6 p-4 rounded-xl border flex items-start gap-3 ${
            result.message === "File already exist" 
              ? "bg-[var(--warning-bg)] border-[var(--warning-border)] text-[var(--warning-text)]" 
              : "bg-[var(--success-bg)] border-[var(--success-border)] text-[var(--success-text)]"
          }`}>
            {result.message === "File already exist" ? <AlertCircle className="w-5 h-5 mt-0.5 shrink-0" /> : <CheckCircle2 className="w-5 h-5 mt-0.5 shrink-0" />}
            <div>
              <p className="font-semibold">{result.filename} processed</p>
              {result.chunks_stored > 0 && (
                <p className="text-sm opacity-90 mt-1">
                  Pages: {result.pages} • Chunks stored: {result.chunks_stored}
                </p>
              )}
              {result.message === "File already exist" && (
                <p className="text-sm opacity-90 mt-1">This file has already been ingested.</p>
              )}
            </div>
          </div>
        )}

        {error && (
          <div className="mt-6 p-4 bg-[var(--danger-bg)] border border-[var(--danger-border)] rounded-xl flex items-start gap-3 text-[var(--danger-text)]">
            <AlertCircle className="w-5 h-5 mt-0.5 shrink-0" />
            <div>
              <p className="font-semibold">Error processing document</p>
              <p className="text-sm opacity-90 mt-1">{error}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
