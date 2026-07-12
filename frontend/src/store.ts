import { create } from 'zustand';

interface StoreState {
  // Ask Page
  askMessages: { role: string; content: string; sources?: {source: string, page: number}[] }[];
  askFilterSource: string;
  setAskMessages: (messages: { role: string; content: string; sources?: {source: string, page: number}[] }[]) => void;
  setAskFilterSource: (source: string) => void;
  
  // Search Page
  searchQuery: string;
  searchFilterSource: string;
  searchTopK: number;
  searchResults: any[];
  setSearchQuery: (query: string) => void;
  setSearchFilterSource: (source: string) => void;
  setSearchTopK: (topK: number) => void;
  setSearchResults: (results: any[]) => void;
  
  // Summarize Page
  summarizeSelectedDoc: string;
  summarizeInstruction: string;
  summarizeResult: string;
  setSummarizeSelectedDoc: (doc: string) => void;
  setSummarizeInstruction: (instruction: string) => void;
  setSummarizeResult: (result: string) => void;
  
  // Compare Page
  compareDocA: string;
  compareDocB: string;
  compareResult: any;
  setCompareDocA: (doc: string) => void;
  setCompareDocB: (doc: string) => void;
  setCompareResult: (result: any) => void;
  
  // Quiz Page
  quizSelectedDoc: string;
  quizNumQuestions: number;
  quizQType: string;
  quizState: "setup" | "generating" | "playing" | "results";
  quizQuestions: any[];
  quizCurrentQIndex: number;
  quizAnswers: Record<number, string>;
  quizScore: { correct: number; total: number } | null;
  quizWeakAreas: string;
  
  setQuizSelectedDoc: (doc: string) => void;
  setQuizNumQuestions: (num: number) => void;
  setQuizQType: (type: string) => void;
  setQuizState: (state: "setup" | "generating" | "playing" | "results") => void;
  setQuizQuestions: (questions: any[]) => void;
  setQuizCurrentQIndex: (index: number) => void;
  setQuizAnswers: (answers: Record<number, string>) => void;
  setQuizScore: (score: { correct: number; total: number } | null) => void;
  setQuizWeakAreas: (areas: string) => void;
}

export const useStore = create<StoreState>((set) => ({
  // Ask
  askMessages: [],
  askFilterSource: "All Documents",
  setAskMessages: (messages) => set({ askMessages: messages }),
  setAskFilterSource: (source) => set({ askFilterSource: source }),
  
  // Search
  searchQuery: "",
  searchFilterSource: "All Documents",
  searchTopK: 3,
  searchResults: [],
  setSearchQuery: (query) => set({ searchQuery: query }),
  setSearchFilterSource: (source) => set({ searchFilterSource: source }),
  setSearchTopK: (topK) => set({ searchTopK: topK }),
  setSearchResults: (results) => set({ searchResults: results }),
  
  // Summarize
  summarizeSelectedDoc: "",
  summarizeInstruction: "",
  summarizeResult: "",
  setSummarizeSelectedDoc: (doc) => set({ summarizeSelectedDoc: doc }),
  setSummarizeInstruction: (instruction) => set({ summarizeInstruction: instruction }),
  setSummarizeResult: (result) => set({ summarizeResult: result }),
  
  // Compare
  compareDocA: "",
  compareDocB: "",
  compareResult: null,
  setCompareDocA: (doc) => set({ compareDocA: doc }),
  setCompareDocB: (doc) => set({ compareDocB: doc }),
  setCompareResult: (result) => set({ compareResult: result }),
  
  // Quiz
  quizSelectedDoc: "",
  quizNumQuestions: 5,
  quizQType: "mcq",
  quizState: "setup",
  quizQuestions: [],
  quizCurrentQIndex: 0,
  quizAnswers: {},
  quizScore: null,
  quizWeakAreas: "",
  
  setQuizSelectedDoc: (doc) => set({ quizSelectedDoc: doc }),
  setQuizNumQuestions: (num) => set({ quizNumQuestions: num }),
  setQuizQType: (type) => set({ quizQType: type }),
  setQuizState: (state) => set({ quizState: state }),
  setQuizQuestions: (questions) => set({ quizQuestions: questions }),
  setQuizCurrentQIndex: (index) => set({ quizCurrentQIndex: index }),
  setQuizAnswers: (answers) => set({ quizAnswers: answers }),
  setQuizScore: (score) => set({ quizScore: score }),
  setQuizWeakAreas: (areas) => set({ quizWeakAreas: areas }),
}));
