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
  Sun
} from "lucide-react";
import { useState, useEffect } from "react";

export function Layout() {
  const [isDark, setIsDark] = useState(false);

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
    <div className="flex h-screen bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-50 overflow-hidden font-sans transition-colors duration-300">
      {/* Sidebar */}
      <div className="w-64 border-r border-[var(--border)] bg-[var(--bg-card)] flex flex-col transition-colors duration-300">
        <div className="p-6 flex items-center justify-center border-b border-[var(--border)]">
          <img src="/localmind_logo.png" alt="LocalMind" className="max-h-12 w-auto object-contain rounded-lg" />
        </div>
        
        <div className="flex-1 overflow-y-auto py-4 px-3 space-y-1">
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

        <div className="p-4 border-t border-[var(--border)]">
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
          <p className="text-[10px] text-[var(--text-muted)] text-center mt-3">Your documents never leave your machine...</p>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-y-auto bg-[var(--bg-primary)] dotted-background relative text-[var(--text-primary)]">
        <div className="p-8 max-w-6xl mx-auto min-h-full">
          <Outlet />
        </div>
      </div>
    </div>
  );
}
