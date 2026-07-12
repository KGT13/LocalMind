import { Outlet, NavLink } from "react-router-dom";
import { 
  LayoutDashboard, 
  UploadCloud, 
  Library, 
  MessageSquare, 
  Search, 
  FileText, 
  GitCompare, 
  BrainCircuit, 
  Settings,
  Lock,
  Moon,
  Sun,
  Minus,
  Maximize2,
  X,
  Menu
} from "lucide-react";
import { useState, useEffect } from "react";

declare global {
  interface Window {
    electron?: {
      ipcRenderer: {
        send: (channel: string, data?: any) => void;
      };
    };
  }
}

export function Layout() {
  const [isDark, setIsDark] = useState(false);
  const logoPath = isDark 
    ? `${import.meta.env.BASE_URL}logo-dark.png` 
    : `${import.meta.env.BASE_URL}logo-light.png`;
  const iconPath = `${import.meta.env.BASE_URL}icon.ico`;
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  const isElectron = typeof window !== "undefined" && !!window.electron?.ipcRenderer?.send;

  const minimizeWindow = () => {
    if (isElectron) window.electron?.ipcRenderer.send("window-minimize");
  };

  const maximizeWindow = () => {
    if (isElectron) window.electron?.ipcRenderer.send("window-maximize");
  };

  const closeWindow = () => {
    if (isElectron) window.electron?.ipcRenderer.send("window-close");
  };

  useEffect(() => {
    if (isDark) {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
  }, [isDark]);

  const navItems = [
    { to: "/", icon: <LayoutDashboard size={20} />, label: "Dashboard" },
    { to: "/upload", icon: <UploadCloud size={20} />, label: "Upload" },
    { to: "/library", icon: <Library size={20} />, label: "Library" },
    { to: "/ask", icon: <MessageSquare size={20} />, label: "Ask" },
    { to: "/search", icon: <Search size={20} />, label: "Search" },
    { to: "/summarize", icon: <FileText size={20} />, label: "Summarize" },
    { to: "/compare", icon: <GitCompare size={20} />, label: "Compare" },
    { to: "/quiz", icon: <BrainCircuit size={20} />, label: "Quiz" },
    { to: "/settings", icon: <Settings size={20} />, label: "Settings" },
  ];

  return (
    <div className="flex flex-col h-screen w-full bg-[var(--bg-primary)] text-[var(--text-primary)] overflow-hidden font-sans transition-colors duration-300">
      {/* Title Bar */}
      <div 
        className="h-11 shrink-0 flex items-center justify-between px-3 bg-[var(--bg-card)] border-b border-[var(--border)] z-20" 
        style={{ WebkitAppRegion: 'drag' } as any}
      >
        <div className="flex items-center gap-3" style={{ WebkitAppRegion: 'no-drag' } as any}>
          <button
            onClick={() => setIsSidebarOpen(!isSidebarOpen)}
            className="p-1.5 rounded-md hover:bg-[var(--accent-bg)] text-[var(--text-secondary)] transition-colors"
            aria-label="Toggle Sidebar"
          >
            <Menu size={18} />
          </button>
          <img src={iconPath} alt="LocalMind Icon" className="h-6 w-auto object-contain" />
          <span className="text-sm font-semibold text-[var(--text-primary)] hidden sm:block">LocalMind</span>
        </div>
        
        <div className="flex items-center gap-1" style={{ WebkitAppRegion: 'no-drag' } as any}>
          <button
            type="button"
            onClick={minimizeWindow}
            className="p-2 rounded-md hover:bg-[var(--accent-bg)] transition-colors text-slate-700 dark:text-slate-300"
            aria-label="Minimize"
          >
            <Minus size={16} />
          </button>
          <button
            type="button"
            onClick={maximizeWindow}
            className="p-2 rounded-md hover:bg-[var(--accent-bg)] transition-colors text-slate-700 dark:text-slate-300"
            aria-label="Maximize"
          >
            <Maximize2 size={16} />
          </button>
          <button
            type="button"
            onClick={closeWindow}
            className="p-2 rounded-md hover:bg-red-500 hover:text-white transition-colors text-slate-700 dark:text-slate-300"
            aria-label="Close"
          >
            <X size={16} />
          </button>
        </div>
      </div>

      {/* Main Body */}
      <div className="flex flex-1 overflow-hidden w-full">
        {/* Sidebar */}
        <div 
          className={`border-r border-[var(--border)] bg-[var(--bg-card)] flex flex-col transition-all duration-300 ${
            isSidebarOpen ? 'w-64 opacity-100' : 'w-0 opacity-0 overflow-hidden border-none'
          }`}
        >
          <div className="py-1 px-1 flex flex-col items-center justify-center border-b border-[var(--border)] shrink-0 min-w-[16rem]">
            <img src={logoPath} alt="LocalMind Logo" className="h-42 w-auto object-contain" />
          </div>

          <div className="flex-1 overflow-y-auto py-4 px-3 space-y-1 min-w-[16rem]">
            {navItems.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) =>
                  `flex items-center gap-3 px-3 py-2.5 rounded-lg font-medium transition-all duration-200 ${
                    isActive 
                      ? "bg-[var(--accent-bg)] text-[var(--accent)] border-r-4 border-[var(--accent)] rounded-r-none" 
                      : "text-[var(--text-secondary)] hover:bg-[var(--accent-bg)] hover:text-[var(--accent)]"
                  }`
                }
              >
                {item.icon}
                {item.label}
              </NavLink>
            ))}
          </div>

          <div className="p-4 border-t border-[var(--border)] shrink-0 min-w-[16rem]">
            <div className="flex items-center justify-between px-2 mb-4">
              <span className="text-sm font-medium text-[var(--text-secondary)]">Theme</span>
              <button 
                onClick={() => setIsDark(!isDark)}
                className="p-1.5 rounded-md hover:bg-[var(--accent-bg)] transition-colors text-[var(--text-secondary)]"
              >
                {isDark ? <Sun size={18} /> : <Moon size={18} />}
              </button>
            </div>
            
            <div className="bg-[var(--success-bg)] border border-[var(--success-border)] rounded-full px-3 py-1.5 flex items-center gap-2 justify-center shadow-sm">
              <Lock size={14} className="text-[var(--success-text)]" />
              <span className="text-xs font-bold text-[var(--success-text)] uppercase tracking-wider">100% Local & Private</span>
            </div>
            <p className="text-[10px] text-[var(--text-muted)] text-center mt-3">Your documents never leave your machine.</p>
          </div>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto bg-[var(--bg-primary)] dotted-background relative text-[var(--text-primary)] min-w-0">
          <div className="p-4 sm:p-8 max-w-6xl mx-auto min-h-full">
            <Outlet />
          </div>
        </div>
      </div>
    </div>
  );
}
