import { useEffect, useState } from "react";
import { BrainCircuit, Loader2, AlertCircle, CheckCircle, XCircle, Award } from "lucide-react";
import { getDocuments, generateQuiz, gradeQuizAnswer, saveQuizScore, getQuizWeakAreas } from "../api";

export default function Quiz() {
  const [docs, setDocs] = useState<{name: string}[]>([]);
  const [selectedDoc, setSelectedDoc] = useState("");
  const [numQuestions, setNumQuestions] = useState(5);
  const [qType, setQType] = useState("Multiple Choice");
  
  const [quizState, setQuizState] = useState<"setup" | "generating" | "playing" | "results">("setup");
  const [questions, setQuestions] = useState<any[]>([]);
  const [currentQIndex, setCurrentQIndex] = useState(0);
  const [userAnswer, setUserAnswer] = useState("");
  const [gradeResult, setGradeResult] = useState<any>(null);
  const [isGrading, setIsGrading] = useState(false);
  const [score, setScore] = useState(0);
  
  const [weakAreas, setWeakAreas] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getDocuments().then(data => {
      setDocs(data);
      if (data.length > 0) setSelectedDoc(data[0].name);
    }).catch(console.error);
  }, []);

  const handleGenerate = async () => {
    if (!selectedDoc) return;
    setQuizState("generating");
    setError(null);
    try {
      const q = await generateQuiz(selectedDoc, numQuestions, qType);
      if (!q || q.length === 0) throw new Error("Could not generate questions.");
      setQuestions(q);
      setCurrentQIndex(0);
      setScore(0);
      setGradeResult(null);
      setUserAnswer("");
      setQuizState("playing");
    } catch (err: any) {
      setError(err.message);
      setQuizState("setup");
    }
  };

  const submitAnswer = async () => {
    if (!userAnswer.trim()) return;
    setIsGrading(true);
    try {
      const res = await gradeQuizAnswer(questions[currentQIndex], userAnswer);
      setGradeResult(res);
      if (res.is_correct) {
        setScore(prev => prev + 1);
      }
    } catch (err: any) {
      alert("Error grading answer: " + err.message);
    } finally {
      setIsGrading(false);
    }
  };

  const nextQuestion = () => {
    if (currentQIndex < questions.length - 1) {
      setCurrentQIndex(prev => prev + 1);
      setGradeResult(null);
      setUserAnswer("");
    } else {
      finishQuiz();
    }
  };

  const finishQuiz = async () => {
    setQuizState("results");
    try {
      await saveQuizScore(selectedDoc, score, questions.length);
      const weak = await getQuizWeakAreas(selectedDoc);
      setWeakAreas(weak);
    } catch (err) {
      console.error(err);
    }
  };

  if (quizState === "setup" || quizState === "generating") {
    return (
      <div className="max-w-4xl animate-in fade-in duration-500">
        <div className="mb-8">
          <h1 className="text-3xl font-extrabold flex items-center gap-3 text-[var(--text-primary)] mb-2">
            <BrainCircuit className="w-8 h-8 text-[var(--accent)]" /> Knowledge Quiz
          </h1>
          <p className="text-[var(--text-secondary)]">
            Test your understanding of the knowledge base with AI-generated quizzes.
          </p>
        </div>

        <div className="glass-card max-w-2xl">
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-semibold text-[var(--text-secondary)] mb-1">Select Document to test on</label>
              <select 
                value={selectedDoc}
                onChange={(e) => setSelectedDoc(e.target.value)}
                disabled={quizState === "generating"}
                className="w-full p-3 bg-[var(--bg-secondary)] text-[var(--text-primary)] border border-[var(--border)] rounded-xl outline-none focus:border-[var(--accent)] transition-colors"
              >
                {docs.length === 0 && <option value="">No documents available</option>}
                {docs.map(doc => (
                  <option key={doc.name} value={doc.name}>{doc.name}</option>
                ))}
              </select>
            </div>
            
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-semibold text-[var(--text-secondary)] mb-1">Number of Questions</label>
                <input 
                  type="number"
                  min="1" max="20"
                  value={numQuestions}
                  onChange={(e) => setNumQuestions(parseInt(e.target.value) || 5)}
                  disabled={quizState === "generating"}
                  className="w-full p-3 bg-[var(--bg-secondary)] text-[var(--text-primary)] border border-[var(--border)] rounded-xl outline-none focus:border-[var(--accent)] transition-colors"
                />
              </div>
              <div>
                <label className="block text-sm font-semibold text-[var(--text-secondary)] mb-1">Question Type</label>
                <select 
                  value={qType}
                  onChange={(e) => setQType(e.target.value)}
                  disabled={quizState === "generating"}
                  className="w-full p-3 bg-[var(--bg-secondary)] text-[var(--text-primary)] border border-[var(--border)] rounded-xl outline-none focus:border-[var(--accent)] transition-colors"
                >
                  <option>Multiple Choice</option>
                  <option>True/False</option>
                  <option>Short Answer</option>
                </select>
              </div>
            </div>

            {error && (
              <div className="p-4 bg-[var(--danger-bg)] border border-red-500/20 rounded-xl flex items-start gap-3 text-[var(--danger-text)]">
                <AlertCircle className="w-5 h-5 mt-0.5 shrink-0" />
                <p className="text-sm font-medium">{error}</p>
              </div>
            )}

            <button 
              onClick={handleGenerate}
              disabled={!selectedDoc || quizState === "generating"}
              className="w-full btn-primary p-4 rounded-xl font-semibold transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 shadow-sm"
            >
              {quizState === "generating" ? <><Loader2 className="animate-spin w-5 h-5" /> Generating Quiz...</> : "Start Quiz"}
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (quizState === "playing") {
    const currentQ = questions[currentQIndex];
    return (
      <div className="max-w-3xl mx-auto animate-in fade-in duration-300">
        <div className="mb-6 flex items-center justify-between">
          <h2 className="text-xl font-bold text-[var(--text-primary)]">
            Question {currentQIndex + 1} of {questions.length}
          </h2>
          <div className="px-3 py-1 bg-[var(--bg-secondary)] border border-[var(--border)] rounded-lg text-sm font-semibold text-[var(--text-secondary)]">
            Score: {score}
          </div>
        </div>

        <div className="glass-card">
          <p className="text-lg md:text-xl font-semibold text-[var(--text-primary)] leading-relaxed mb-6">
            {currentQ.question}
          </p>

          {!gradeResult ? (
            <div className="space-y-4">
              {currentQ.options ? (
                <div className="grid gap-3">
                  {currentQ.options.map((opt: string, i: number) => (
                    <button
                      key={i}
                      onClick={() => setUserAnswer(opt)}
                      className={`text-left p-4 rounded-xl border transition-all ${
                        userAnswer === opt 
                          ? "border-[var(--accent)] bg-[var(--accent-bg)] text-[var(--accent)] font-medium" 
                          : "border-[var(--border)] hover:border-[var(--accent)] bg-[var(--bg-secondary)] text-[var(--text-primary)]"
                      }`}
                    >
                      {opt}
                    </button>
                  ))}
                </div>
              ) : (
                <textarea
                  value={userAnswer}
                  onChange={(e) => setUserAnswer(e.target.value)}
                  placeholder="Type your answer here..."
                  rows={4}
                  className="w-full p-4 bg-[var(--bg-secondary)] text-[var(--text-primary)] border border-[var(--border)] rounded-xl outline-none focus:border-[var(--accent)] transition-colors resize-none"
                />
              )}
              
              <button
                onClick={submitAnswer}
                disabled={!userAnswer || isGrading}
                className="w-full mt-4 btn-primary p-3.5 rounded-xl font-semibold transition-all disabled:opacity-50 flex items-center justify-center gap-2 shadow-sm"
              >
                {isGrading ? <><Loader2 className="w-5 h-5 animate-spin" /> Grading...</> : "Submit Answer"}
              </button>
            </div>
          ) : (
            <div className="space-y-6 animate-in slide-in-from-bottom-2 duration-300">
              <div className={`p-5 rounded-xl border flex items-start gap-4 ${
                gradeResult.is_correct 
                  ? "bg-[var(--success-bg)] border-[var(--success-border)] text-[var(--success-text)]"
                  : "bg-[var(--danger-bg)] border-[var(--danger-border)] text-[var(--danger-text)]"
              }`}>
                {gradeResult.is_correct ? <CheckCircle className="w-6 h-6 mt-0.5 shrink-0" /> : <XCircle className="w-6 h-6 mt-0.5 shrink-0" />}
                <div>
                  <h3 className="font-bold text-lg mb-1">{gradeResult.is_correct ? "Correct!" : "Incorrect"}</h3>
                  <p className="opacity-90">{gradeResult.explanation}</p>
                </div>
              </div>
              
              <button
                onClick={nextQuestion}
                className="w-full bg-[var(--bg-secondary)] border border-[var(--border)] hover:border-[var(--accent)] text-[var(--text-primary)] p-3.5 rounded-xl font-semibold transition-all shadow-sm"
              >
                {currentQIndex < questions.length - 1 ? "Next Question" : "View Results"}
              </button>
            </div>
          )}
        </div>
      </div>
    );
  }

  // Results State
  return (
    <div className="max-w-3xl mx-auto animate-in fade-in zoom-in-95 duration-500 text-center py-12">
      <div className="w-24 h-24 bg-gradient-to-br from-[var(--accent-light)] to-[var(--accent)] rounded-full mx-auto flex items-center justify-center text-white shadow-xl mb-6">
        <Award className="w-12 h-12" />
      </div>
      <h1 className="text-4xl font-extrabold text-[var(--text-primary)] mb-2">Quiz Complete!</h1>
      <p className="text-xl text-[var(--text-secondary)] mb-8">
        You scored <span className="font-bold text-[var(--accent)]">{score}</span> out of {questions.length}
      </p>

      {weakAreas && weakAreas !== "No weak areas detected yet!" && (
        <div className="glass-card text-left max-w-2xl mx-auto mb-8">
          <h3 className="font-bold text-lg mb-3 flex items-center gap-2 text-[var(--text-primary)] border-b border-[var(--border)] pb-2">
            <BrainCircuit className="w-5 h-5 text-[var(--accent)]" /> Needs Improvement
          </h3>
          <p className="text-[var(--text-secondary)] leading-relaxed">
            {weakAreas}
          </p>
        </div>
      )}

      <button
        onClick={() => setQuizState("setup")}
        className="btn-primary px-8 py-3 rounded-xl font-semibold shadow-sm"
      >
        Take Another Quiz
      </button>
    </div>
  );
}
