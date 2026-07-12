import { useEffect, useState } from "react";
import { Loader2, AlertCircle, Download, CheckCircle, Brain } from "lucide-react";
import { API_BASE, pullModel, switchModel } from "../api";
import axios from "axios";

export function SetupGuard({ children }: { children: React.ReactNode }) {
  const [status, setStatus] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [isPulling, setIsPulling] = useState(false);
  const [pullProgress, setPullProgress] = useState("");
  const [error, setError] = useState<string | null>(null);

  const checkStatus = async () => {
    try {
      const res = await axios.get(`${API_BASE}/setup/status`);
      setStatus(res.data);
    } catch (err: any) {
      setError("Cannot connect to backend. Make sure the LocalMind backend is running.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    checkStatus();
  }, []);

  const handleDownloadModels = async () => {
    if (!status) return;
    setIsPulling(true);
    setError(null);
    try {
      setPullProgress(`Downloading Embed Model (${status.embed_model})... This takes a few seconds.`);
      await pullModel(status.embed_model); 
      setPullProgress(`Downloading Chat Model (${status.chat_model})... This may take a few minutes.`);
      await pullModel(status.chat_model);
      await switchModel(status.chat_model); // Set the chat model as active
      
      setPullProgress("Download complete!");
      await checkStatus();
    } catch (err: any) {
      setError("Failed to download models: " + (err.response?.data?.detail || err.message));
    } finally {
      setIsPulling(false);
    }
  };

  if (loading) {
    return (
      <div className="flex-1 flex items-center justify-center min-h-screen bg-[var(--bg-primary)]">
        <Loader2 className="w-8 h-8 animate-spin text-[var(--accent)]" />
      </div>
    );
  }

  if (error && !status) {
    return (
      <div className="flex-1 flex items-center justify-center min-h-screen bg-[var(--bg-primary)] p-8">
        <div className="max-w-md w-full glass-card text-center space-y-4">
          <AlertCircle className="w-12 h-12 text-[var(--danger-text)] mx-auto" />
          <h2 className="text-xl font-bold text-[var(--text-primary)]">Backend Disconnected</h2>
          <p className="text-[var(--text-secondary)]">{error}</p>
          <button onClick={() => { setLoading(true); checkStatus(); }} className="btn-primary px-6 py-2 rounded-lg mt-4">
            Retry Connection
          </button>
        </div>
      </div>
    );
  }

  if (status && (!status.ollama_running || !status.chat_model_ready || !status.embed_model_ready)) {
    return (
      <div className="flex-1 flex items-center justify-center min-h-screen bg-[var(--bg-primary)] p-8">
        <div className="max-w-xl w-full glass-card space-y-6 animate-in fade-in zoom-in-95 duration-500">
          <div className="text-center">
            <div className="w-16 h-16 bg-[var(--accent-bg)] rounded-full flex items-center justify-center mx-auto mb-4">
              <Brain className="w-8 h-8 text-[var(--accent)]" />
            </div>
            <h1 className="text-2xl font-bold text-[var(--text-primary)]">LocalMind Setup</h1>
            <p className="text-[var(--text-secondary)] mt-2">
              Let's get your local AI environment ready.
            </p>
          </div>

          <div className="space-y-4">
            <div className="flex items-center gap-4 p-4 rounded-xl border border-[var(--border)] bg-[var(--bg-secondary)]">
              {status.ollama_running ? <CheckCircle className="w-6 h-6 text-[var(--success-text)] shrink-0" /> : <AlertCircle className="w-6 h-6 text-[var(--danger-text)] shrink-0" />}
              <div>
                <h3 className="font-semibold text-[var(--text-primary)]">Ollama AI Engine</h3>
                <p className="text-sm text-[var(--text-secondary)]">
                  {status.ollama_running ? "Running normally on port 11434" : "Not running. Please install Ollama from ollama.com or run the setup installer."}
                </p>
              </div>
            </div>

            <div className="flex items-center gap-4 p-4 rounded-xl border border-[var(--border)] bg-[var(--bg-secondary)]">
              {status.chat_model_ready && status.embed_model_ready ? <CheckCircle className="w-6 h-6 text-[var(--success-text)] shrink-0" /> : <AlertCircle className="w-6 h-6 text-[var(--warning-text)] shrink-0" />}
              <div>
                <h3 className="font-semibold text-[var(--text-primary)]">AI Models</h3>
                <p className="text-sm text-[var(--text-secondary)]">
                  {status.chat_model_ready && status.embed_model_ready 
                    ? "Models downloaded and ready to use." 
                    : `Required models (${status.chat_model}, ${status.embed_model}) are not downloaded yet.`}
                </p>
              </div>
            </div>
          </div>

          {error && (
            <div className="p-4 bg-[var(--danger-bg)] text-[var(--danger-text)] rounded-xl border border-[var(--danger-border)] text-sm">
              {error}
            </div>
          )}

          {!status.ollama_running ? (
            <button disabled className="w-full btn-primary p-3 rounded-xl opacity-50 cursor-not-allowed">
              Waiting for Ollama...
            </button>
          ) : (
            <button 
              onClick={handleDownloadModels}
              disabled={isPulling}
              className="w-full btn-primary p-4 rounded-xl font-bold text-lg flex items-center justify-center gap-2 transition-all shadow-md hover:shadow-lg disabled:opacity-70 disabled:cursor-wait"
            >
              {isPulling ? (
                <><Loader2 className="w-5 h-5 animate-spin" /> {pullProgress}</>
              ) : (
                <><Download className="w-5 h-5" /> Download Models and Start</>
              )}
            </button>
          )}
        </div>
      </div>
    );
  }

  // If everything is good, render the children
  return <>{children}</>;
}
