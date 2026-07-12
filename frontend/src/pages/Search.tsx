import { useEffect, useState } from "react";
import { Search as SearchIcon, FileText, Filter, Loader2, AlertCircle } from "lucide-react";
import { getDocuments, searchDocuments } from "../api";
import { useStore } from "../store";

export default function Search() {
  const [docs, setDocs] = useState<{name: string}[]>([]);
  
  const {
    searchQuery: query,
    setSearchQuery: setQuery,
    searchFilterSource: filterSource,
    setSearchFilterSource: setFilterSource,
    searchTopK: topK,
    setSearchTopK: setTopK,
    searchResults: results,
    setSearchResults: setResults,
  } = useStore();

  const [isSearching, setIsSearching] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getDocuments().then(setDocs).catch(console.error);
  }, []);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    
    setIsSearching(true);
    setError(null);
    try {
      const res = await searchDocuments(query, topK, filterSource);
      setResults(res);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsSearching(false);
    }
  };

  return (
    <div className="max-w-5xl animate-in fade-in duration-500">
      <div className="mb-8">
        <h1 className="text-3xl font-extrabold flex items-center gap-3 text-[var(--text-primary)] mb-2">
          <SearchIcon className="w-8 h-8 text-[var(--accent)]" /> Semantic Search
        </h1>
        <p className="text-[var(--text-secondary)]">
          Find exact chunks of text across your documents based on meaning, not just keywords.
        </p>
      </div>

      <div className="glass-card mb-8">
        <form onSubmit={handleSearch} className="space-y-6">
          <div className="relative">
            <SearchIcon className="absolute left-4 top-1/2 -translate-y-1/2 w-6 h-6 text-[var(--text-muted)]" />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="What are you looking for?"
              className="w-full pl-12 pr-4 py-4 text-lg bg-[var(--bg-secondary)] text-[var(--text-primary)] border border-[var(--border)] rounded-xl focus:border-[var(--accent)] outline-none transition-all shadow-inner"
            />
          </div>
          
          <div className="flex flex-col sm:flex-row items-center gap-4">
            <div className="w-full sm:w-1/2 flex items-center gap-3">
              <Filter className="w-5 h-5 text-[var(--text-muted)] shrink-0" />
              <select 
                value={filterSource}
                onChange={(e) => setFilterSource(e.target.value)}
                className="w-full p-3 bg-[var(--bg-secondary)] text-[var(--text-primary)] border border-[var(--border)] rounded-xl outline-none focus:border-[var(--accent)] transition-colors"
              >
                <option>All Documents</option>
                {docs.map(doc => (
                  <option key={doc.name} value={doc.name}>{doc.name}</option>
                ))}
              </select>
            </div>
            <div className="w-full sm:w-1/2 flex items-center gap-3">
              <span className="text-sm font-medium text-[var(--text-secondary)] shrink-0 whitespace-nowrap">Results to show:</span>
              <input 
                type="range" 
                min="1" 
                max="20" 
                value={topK} 
                onChange={(e) => setTopK(parseInt(e.target.value))}
                className="w-full h-2 bg-[var(--border)] rounded-lg appearance-none cursor-pointer accent-[var(--accent)]"
              />
              <span className="text-sm font-bold bg-[var(--accent-bg)] text-[var(--accent)] px-3 py-1 rounded-md min-w-[3rem] text-center">{topK}</span>
            </div>
          </div>

          <button 
            type="submit"
            disabled={!query.trim() || isSearching}
            className="w-full btn-primary p-4 rounded-xl font-semibold transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 shadow-sm"
          >
            {isSearching ? <><Loader2 className="animate-spin w-5 h-5" /> Searching...</> : "Search"}
          </button>
        </form>
      </div>

      {error && (
        <div className="mb-6 p-4 bg-[var(--danger-bg)] border border-[var(--danger-border)] rounded-xl flex items-start gap-3 text-[var(--danger-text)]">
          <AlertCircle className="w-5 h-5 mt-0.5 shrink-0" />
          <p>{error}</p>
        </div>
      )}

      {/* Results */}
      {!isSearching && results.length === 0 && query && !error && (
        <div className="p-8 text-center glass-card animate-in fade-in">
          <FileText className="w-12 h-12 text-[var(--text-muted)] mx-auto mb-3 opacity-50" />
          <h3 className="text-lg font-semibold text-[var(--text-primary)]">No results found</h3>
          <p className="text-[var(--text-secondary)] mt-1">Try adjusting your search terms or filters.</p>
        </div>
      )}
      
      {results.length > 0 && (
        <div className="space-y-4 animate-in slide-in-from-bottom-4 duration-500">
          <h2 className="text-xl font-bold mb-4 text-[var(--text-primary)] flex items-center gap-2">
            Top Results <span className="px-2.5 py-0.5 bg-[var(--bg-secondary)] rounded-md text-sm font-medium text-[var(--text-secondary)]">{results.length}</span>
          </h2>
          
          <div className="grid gap-4">
            {results.map((result, i) => (
              <div key={i} className="glass-card hover:shadow-md transition-shadow relative overflow-hidden group">
                {/* Relevance bar */}
                <div 
                  className={`absolute left-0 top-0 bottom-0 w-1 ${
                    result.relevance > 80 ? 'bg-[var(--success-text)]' : 
                    result.relevance > 60 ? 'bg-[var(--warning-text)]' : 'bg-[var(--danger-text)]'
                  }`}
                />
                
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-2 text-sm font-medium text-[var(--text-secondary)]">
                    <FileText className="w-4 h-4 text-[var(--accent)]" />
                    <span className="text-[var(--text-primary)]">{result.source}</span>
                    <span className="px-2 py-0.5 bg-[var(--bg-secondary)] rounded text-xs">Pg {result.page}</span>
                  </div>
                  <div className="flex items-center gap-1.5 px-2.5 py-1 bg-[var(--bg-secondary)] rounded-lg text-xs font-semibold">
                    <span className={
                      result.relevance > 80 ? 'text-[var(--success-text)]' : 
                      result.relevance > 60 ? 'text-[var(--warning-text)]' : 'text-[var(--danger-text)]'
                    }>{result.relevance}% Match</span>
                  </div>
                </div>
                
                <p className="text-[var(--text-secondary)] leading-relaxed italic border-l-2 border-[var(--border)] pl-4 py-1">
                  "{result.text}"
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
