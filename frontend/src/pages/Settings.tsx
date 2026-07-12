import { useEffect, useState } from "react";
import { Settings as SettingsIcon, Server, Database, Brain, Cpu, ShieldCheck, Loader2 } from "lucide-react";
import { getConfig, switchModel } from "../api";

interface Config {
  ollama_url: string;
  chunk_size: number;
  chunk_overlap: number;
  top_k: number;
  chat_model: string;
  embed_model: string;
  available_models: string[];
}

export default function Settings() {
  const [config, setConfig] = useState<Config | null>(null);
  const [error, setError] = useState("");
  const [isSwitching, setIsSwitching] = useState(false);
  const [switchStatus, setSwitchStatus] = useState("");

  useEffect(() => {
    getConfig()
      .then(setConfig)
      .catch((err) => setError(err.response?.data?.detail || err.message));
  }, []);

  return (
    <div className="max-w-4xl animate-in fade-in duration-500">
      <div className="mb-8">
        <h1 className="text-3xl font-extrabold flex items-center gap-3 text-[var(--text-primary)] mb-2">
          <SettingsIcon className="w-8 h-8 text-[var(--accent)]" /> Settings & Info
        </h1>
        <p className="text-[var(--text-secondary)]">
          Configuration for your local AI environment.
        </p>
      </div>

      <div className="space-y-6">
        {/* System Status */}
        <div className="glass-card">
          <h2 className="text-xl font-bold text-[var(--text-primary)] mb-6 border-b border-[var(--border)] pb-4">
            System Status
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="flex items-center gap-4 p-4 bg-[var(--bg-secondary)] rounded-xl border border-[var(--border)]">
              <div className="w-12 h-12 rounded-full bg-[var(--success-bg)] flex items-center justify-center text-[var(--success-text)]">
                <Server className="w-6 h-6" />
              </div>
              <div>
                <p className="text-sm font-semibold text-[var(--text-secondary)]">FastAPI Backend</p>
                <p className="font-bold text-[var(--text-primary)] flex items-center gap-2">
                  <span className="w-2 h-2 rounded-full bg-[var(--match-color)]"></span> Online (Port 8000)
                </p>
              </div>
            </div>

            <div className="flex items-center gap-4 p-4 bg-[var(--bg-secondary)] rounded-xl border border-[var(--border)]">
              <div className="w-12 h-12 rounded-full bg-[var(--accent-bg)] flex items-center justify-center text-[var(--accent)]">
                <Database className="w-6 h-6" />
              </div>
              <div>
                <p className="text-sm font-semibold text-[var(--text-secondary)]">ChromaDB Vector Store</p>
                <p className="font-bold text-[var(--text-primary)] flex items-center gap-2">
                  <span className="w-2 h-2 rounded-full bg-[var(--accent)]"></span> Connected
                </p>
              </div>
            </div>

            <div className="flex items-center gap-4 p-4 bg-[var(--bg-secondary)] rounded-xl border border-[var(--border)] relative">
              <div className="w-12 h-12 rounded-full bg-[var(--accent-bg)] flex items-center justify-center text-[var(--accent)] shrink-0">
                {isSwitching ? <Loader2 className="w-6 h-6 animate-spin" /> : <Brain className="w-6 h-6" />}
              </div>
              <div className="flex-1 w-full min-w-0">
                <p className="text-sm font-semibold text-[var(--text-secondary)]">LLM Generation Model</p>
                <select
                  value={config?.chat_model || ""}
                  onChange={async (e) => {
                    const newModel = e.target.value;
                    if (!config || newModel === config.chat_model) return;
                    setIsSwitching(true);
                    setSwitchStatus(`Downloading and switching to ${newModel}... This may take a few minutes.`);
                    setError("");
                    try {
                      await switchModel(newModel);
                      setConfig({ ...config, chat_model: newModel });
                      setSwitchStatus("Successfully switched model!");
                      setTimeout(() => setSwitchStatus(""), 3000);
                    } catch (err: any) {
                      setError(err.response?.data?.detail || err.message);
                      setSwitchStatus("");
                    } finally {
                      setIsSwitching(false);
                    }
                  }}
                  disabled={!config || isSwitching}
                  className="mt-1 w-full p-2 bg-[var(--bg-card)] text-[var(--text-primary)] border border-[var(--border)] rounded-lg outline-none focus:border-[var(--accent)] transition-colors disabled:opacity-50 text-sm font-bold truncate"
                >
                  {config?.available_models ? (
                    config.available_models.map((m) => (
                      <option key={m} value={m}>{m}</option>
                    ))
                  ) : (
                    <option value={config?.chat_model || ""}>{config?.chat_model || "..."}</option>
                  )}
                </select>
              </div>
            </div>

            <div className="flex items-center gap-4 p-4 bg-[var(--bg-secondary)] rounded-xl border border-[var(--border)]">
              <div className="w-12 h-12 rounded-full bg-[var(--accent-bg)] flex items-center justify-center text-[var(--accent)]">
                <Cpu className="w-6 h-6" />
              </div>
              <div>
                <p className="text-sm font-semibold text-[var(--text-secondary)]">Embedding Model</p>
                <p className="font-bold text-[var(--text-primary)]">{config?.embed_model ?? "..."}</p>
              </div>
            </div>
          </div>
          
          {switchStatus && (
            <div className="mt-4 p-3 bg-[var(--success-bg)] text-[var(--success-text)] border border-[var(--success-border)] rounded-xl text-sm font-medium">
              {switchStatus}
            </div>
          )}
        </div>

        {/* Privacy Promise */}
        <div className="bg-gradient-to-r from-[var(--btn-gradient-start)] to-[var(--btn-gradient-end)] rounded-2xl p-6 sm:p-8 shadow-sm text-white flex flex-col sm:flex-row items-center gap-6">
          <div className="w-16 h-16 rounded-full bg-white/20 flex items-center justify-center shrink-0">
            <ShieldCheck className="w-8 h-8 text-white" />
          </div>
          <div>
            <h2 className="text-xl font-bold mb-2">100% Local & Private</h2>
            <p className="text-white/80 leading-relaxed">
              LocalMind runs entirely on your machine. Your documents are never uploaded to the cloud, and the AI models run locally via Ollama. You have complete ownership and privacy over your data.
            </p>
          </div>
        </div>

        {/* Backend Configuration (Read Only) */}
        <div className="glass-card">
          <h2 className="text-xl font-bold text-[var(--text-primary)] mb-6 border-b border-[var(--border)] pb-4">
            Configuration
          </h2>

          {error && (
            <p className="text-sm text-[var(--danger-text)] mb-4">
              Could not load live config from backend: {error}. Showing may be stale.
            </p>
          )}

          <div className="space-y-4 font-mono text-sm">
            <div className="flex justify-between p-3 bg-[var(--bg-secondary)] rounded-lg border border-[var(--border)]">
              <span className="text-[var(--text-secondary)]">OLLAMA_URL</span>
              <span className="text-[var(--text-primary)] font-medium">{config?.ollama_url ?? "..."}</span>
            </div>
            <div className="flex justify-between p-3 bg-[var(--bg-secondary)] rounded-lg border border-[var(--border)]">
              <span className="text-[var(--text-secondary)]">CHUNK_SIZE</span>
              <span className="text-[var(--text-primary)] font-medium">{config?.chunk_size ?? "..."}</span>
            </div>
            <div className="flex justify-between p-3 bg-[var(--bg-secondary)] rounded-lg border border-[var(--border)]">
              <span className="text-[var(--text-secondary)]">CHUNK_OVERLAP</span>
              <span className="text-[var(--text-primary)] font-medium">{config?.chunk_overlap ?? "..."}</span>
            </div>
            <div className="flex justify-between p-3 bg-[var(--bg-secondary)] rounded-lg border border-[var(--border)]">
              <span className="text-[var(--text-secondary)]">TOP_K</span>
              <span className="text-[var(--text-primary)] font-medium">{config?.top_k ?? "..."}</span>
            </div>
          </div>
          
        </div>
      </div>
    </div>
  );
}