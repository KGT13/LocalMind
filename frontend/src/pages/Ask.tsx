import { useState, useRef, useEffect } from "react";
import { MessageSquare, Send, Bot, User, FileText, Loader2 } from "lucide-react";
import { getDocuments } from "../api";
import { useSearchParams } from "react-router-dom";

type Message = {
  role: "user" | "assistant";
  content: string;
  sources?: {source: string, page: number}[];
};

export default function Ask() {
  const [searchParams] = useSearchParams();
  const initialDoc = searchParams.get("doc");
  
  const [docs, setDocs] = useState<{name: string}[]>([]);
  const [filterSource, setFilterSource] = useState<string>(initialDoc || "All Documents");
  
  const [messages, setMessages] = useState<Message[]>([
    { role: "assistant", content: "Hi there! Ask me anything about your knowledge base." }
  ]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    getDocuments().then(setDocs).catch(console.error);
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isTyping) return;

    const userMsg = input.trim();
    setInput("");
    setMessages(prev => [...prev, { role: "user", content: userMsg }]);
    setIsTyping(true);

    try {
      // Add a placeholder message for the assistant
      setMessages(prev => [...prev, { role: "assistant", content: "", sources: [] }]);
      
      const res = await fetch("http://localhost:8000/api/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          question: userMsg,
          filter_source: filterSource === "All Documents" ? null : filterSource,
          conversation_history: messages.map(m => ({
            role: m.role, 
            content: m.content
          }))
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
                // Update the last message in state
                setMessages(prev => {
                  const newMsgs = [...prev];
                  const lastIdx = newMsgs.length - 1;
                  
                  // Check if it's sources array or text chunk
                  if (Array.isArray(data)) {
                    newMsgs[lastIdx] = { ...newMsgs[lastIdx], sources: data };
                  } else if (data.text) {
                    newMsgs[lastIdx] = { 
                      ...newMsgs[lastIdx], 
                      content: newMsgs[lastIdx].content + data.text 
                    };
                  }
                  return newMsgs;
                });
              } catch (e) {
                console.error("Parse error", e);
              }
            }
          }
        }
      }
    } catch (err) {
      console.error(err);
      setMessages(prev => {
        const newMsgs = [...prev];
        newMsgs[newMsgs.length - 1].content = "Sorry, an error occurred while generating the response.";
        return newMsgs;
      });
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="h-[calc(100vh-64px)] flex flex-col animate-in fade-in duration-500 -m-8">
      {/* Header */}
      <div className="bg-[var(--bg-card)] border-b border-[var(--border)] p-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4 shrink-0 z-10 shadow-sm">
        <div>
          <h1 className="text-2xl font-extrabold flex items-center gap-2 text-[var(--text-primary)]">
            <MessageSquare className="w-6 h-6 text-[var(--accent)]" /> Chat with Knowledge Base
          </h1>
          <p className="text-sm text-[var(--text-secondary)] mt-1">Ask questions and get answers based on your documents.</p>
        </div>
        <div className="flex items-center gap-2">
          <FileText className="w-4 h-4 text-[var(--text-muted)]" />
          <select 
            value={filterSource}
            onChange={(e) => setFilterSource(e.target.value)}
            className="p-2 text-sm bg-[var(--bg-secondary)] text-[var(--text-primary)] border border-[var(--border)] rounded-lg outline-none focus:border-[var(--accent)] transition-colors"
          >
            <option>All Documents</option>
            {docs.map(doc => (
              <option key={doc.name} value={doc.name}>{doc.name}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Chat Area */}
      <div className="flex-1 overflow-y-auto p-4 sm:p-8 space-y-6 bg-transparent">
        {messages.map((msg, i) => (
          <div key={i} className={`flex gap-4 max-w-4xl mx-auto ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}>
            <div className={`w-10 h-10 rounded-full flex items-center justify-center shrink-0 shadow-sm ${
              msg.role === 'user' 
                ? 'bg-[var(--accent)] text-white' 
                : 'bg-[var(--bg-card)] border border-[var(--border)] text-[var(--accent)]'
            }`}>
              {msg.role === 'user' ? <User className="w-5 h-5" /> : <Bot className="w-5 h-5" />}
            </div>
            
            <div className={`flex flex-col gap-2 max-w-[80%] ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>
              <div className={`p-4 rounded-2xl shadow-sm ${
                msg.role === 'user' 
                  ? 'bg-[var(--accent)] text-white rounded-tr-sm' 
                  : 'bg-[var(--bg-card)] border border-[var(--border)] text-[var(--text-primary)] rounded-tl-sm'
              }`}>
                {msg.content ? (
                  <div className="prose dark:prose-invert prose-p:leading-relaxed max-w-none prose-sm sm:prose-base whitespace-pre-wrap">
                    {msg.content}
                  </div>
                ) : (
                  <div className="flex items-center gap-2 h-6">
                    <span className="w-2 h-2 bg-[var(--accent-light)] rounded-full animate-bounce [animation-delay:-0.3s]"></span>
                    <span className="w-2 h-2 bg-[var(--accent-light)] rounded-full animate-bounce [animation-delay:-0.15s]"></span>
                    <span className="w-2 h-2 bg-[var(--accent-light)] rounded-full animate-bounce"></span>
                  </div>
                )}
              </div>
              
              {msg.sources && msg.sources.length > 0 && (
                <div className="flex flex-wrap gap-2 mt-1">
                  {msg.sources.map((src, idx) => (
                    <span key={idx} className="inline-flex items-center gap-1 px-2.5 py-1 rounded-md text-xs font-medium bg-[var(--bg-secondary)] text-[var(--text-secondary)] border border-[var(--border)]">
                      <FileText className="w-3 h-3" />
                      {src.source} (pg {src.page})
                    </span>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="p-4 sm:p-6 bg-[var(--bg-card)] border-t border-[var(--border)] shrink-0">
        <form onSubmit={handleSubmit} className="max-w-4xl mx-auto relative">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={isTyping}
            placeholder="Type your question..."
            className="w-full pl-6 pr-16 py-4 bg-[var(--bg-secondary)] text-[var(--text-primary)] border border-[var(--border)] rounded-2xl focus:border-[var(--accent)] focus:ring-1 focus:ring-[var(--accent)] outline-none transition-all shadow-inner disabled:opacity-50"
          />
          <button 
            type="submit"
            disabled={!input.trim() || isTyping}
            className="absolute right-2 top-1/2 -translate-y-1/2 p-2.5 btn-primary disabled:opacity-50 flex items-center justify-center"
          >
            {isTyping ? <Loader2 className="w-5 h-5 animate-spin" /> : <Send className="w-5 h-5" />}
          </button>
        </form>
      </div>
    </div>
  );
}
