import { Settings as SettingsIcon, Server, Database, Brain, Cpu, ShieldCheck } from "lucide-react";

export default function Settings() {
  return (
    <div className="max-w-4xl animate-in fade-in duration-500">
      <div className="mb-8">
        <h1 className="text-3xl font-extrabold flex items-center gap-3 text-slate-900 dark:text-white mb-2">
          <SettingsIcon className="w-8 h-8 text-slate-500" /> Settings & Info
        </h1>
        <p className="text-slate-600 dark:text-slate-400">
          Configuration for your local AI environment.
        </p>
      </div>

      <div className="space-y-6">
        {/* System Status */}
        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 sm:p-8 shadow-sm">
          <h2 className="text-xl font-bold text-slate-900 dark:text-white mb-6 border-b border-slate-100 dark:border-slate-800 pb-4">
            System Status
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="flex items-center gap-4 p-4 bg-slate-50 dark:bg-slate-800/50 rounded-xl border border-slate-100 dark:border-slate-700">
              <div className="w-12 h-12 rounded-full bg-emerald-100 dark:bg-emerald-500/20 flex items-center justify-center text-emerald-600 dark:text-emerald-400">
                <Server className="w-6 h-6" />
              </div>
              <div>
                <p className="text-sm font-semibold text-slate-500 dark:text-slate-400">FastAPI Backend</p>
                <p className="font-bold text-slate-900 dark:text-white flex items-center gap-2">
                  <span className="w-2 h-2 rounded-full bg-emerald-500"></span> Online (Port 8000)
                </p>
              </div>
            </div>
            
            <div className="flex items-center gap-4 p-4 bg-slate-50 dark:bg-slate-800/50 rounded-xl border border-slate-100 dark:border-slate-700">
              <div className="w-12 h-12 rounded-full bg-indigo-100 dark:bg-indigo-500/20 flex items-center justify-center text-indigo-600 dark:text-indigo-400">
                <Database className="w-6 h-6" />
              </div>
              <div>
                <p className="text-sm font-semibold text-slate-500 dark:text-slate-400">ChromaDB Vector Store</p>
                <p className="font-bold text-slate-900 dark:text-white flex items-center gap-2">
                  <span className="w-2 h-2 rounded-full bg-indigo-500"></span> Connected
                </p>
              </div>
            </div>
            
            <div className="flex items-center gap-4 p-4 bg-slate-50 dark:bg-slate-800/50 rounded-xl border border-slate-100 dark:border-slate-700">
              <div className="w-12 h-12 rounded-full bg-purple-100 dark:bg-purple-500/20 flex items-center justify-center text-purple-600 dark:text-purple-400">
                <Brain className="w-6 h-6" />
              </div>
              <div>
                <p className="text-sm font-semibold text-slate-500 dark:text-slate-400">LLM Generation Model</p>
                <p className="font-bold text-slate-900 dark:text-white">llama3</p>
              </div>
            </div>
            
            <div className="flex items-center gap-4 p-4 bg-slate-50 dark:bg-slate-800/50 rounded-xl border border-slate-100 dark:border-slate-700">
              <div className="w-12 h-12 rounded-full bg-blue-100 dark:bg-blue-500/20 flex items-center justify-center text-blue-600 dark:text-blue-400">
                <Cpu className="w-6 h-6" />
              </div>
              <div>
                <p className="text-sm font-semibold text-slate-500 dark:text-slate-400">Embedding Model</p>
                <p className="font-bold text-slate-900 dark:text-white">nomic-embed-text</p>
              </div>
            </div>
          </div>
        </div>

        {/* Privacy Promise */}
        <div className="bg-gradient-to-r from-indigo-500 to-purple-600 rounded-2xl p-6 sm:p-8 shadow-sm text-white flex flex-col sm:flex-row items-center gap-6">
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
        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 sm:p-8 shadow-sm">
          <h2 className="text-xl font-bold text-slate-900 dark:text-white mb-6 border-b border-slate-100 dark:border-slate-800 pb-4">
            Configuration (backend/src/config.py)
          </h2>
          <div className="space-y-4 font-mono text-sm">
            <div className="flex justify-between p-3 bg-slate-50 dark:bg-slate-800 rounded-lg">
              <span className="text-slate-500 dark:text-slate-400">OLLAMA_URL</span>
              <span className="text-slate-900 dark:text-slate-200 font-medium">http://localhost:11434</span>
            </div>
            <div className="flex justify-between p-3 bg-slate-50 dark:bg-slate-800 rounded-lg">
              <span className="text-slate-500 dark:text-slate-400">CHUNK_SIZE</span>
              <span className="text-slate-900 dark:text-slate-200 font-medium">800</span>
            </div>
            <div className="flex justify-between p-3 bg-slate-50 dark:bg-slate-800 rounded-lg">
              <span className="text-slate-500 dark:text-slate-400">CHUNK_OVERLAP</span>
              <span className="text-slate-900 dark:text-slate-200 font-medium">100</span>
            </div>
            <div className="flex justify-between p-3 bg-slate-50 dark:bg-slate-800 rounded-lg">
              <span className="text-slate-500 dark:text-slate-400">TOP_K</span>
              <span className="text-slate-900 dark:text-slate-200 font-medium">3</span>
            </div>
          </div>
          <p className="text-xs text-slate-500 mt-4 text-center">
            To change these settings, edit <code className="bg-slate-100 dark:bg-slate-800 px-1 rounded">backend/src/config.py</code> and restart the backend server.
          </p>
        </div>
      </div>
    </div>
  );
}
