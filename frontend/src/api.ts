import axios from "axios";

export const API_BASE = "http://localhost:8000/api";

const api = axios.create({
  baseURL: API_BASE,
});

export const getKbStats = async () => {
  const { data } = await api.get("/kb/stats");
  return data;
};

export const getConfig = async () => {
  const { data } = await api.get("/config");
  return data;
};

export const getModels = async () => {
  const { data } = await api.get("/models");
  return data;
};

export const switchModel = async (modelName: string) => {
  const { data } = await api.post("/models/switch", { model_name: modelName });
  return data;
};

export const pullModel = async (modelName: string) => {
  const { data } = await api.post("/models/pull", { model_name: modelName });
  return data;
};


export const getDocuments = async () => {
  const { data } = await api.get("/documents");
  return data.documents;
};

export const deleteDocument = async (filename: string) => {
  const { data } = await api.delete(`/documents/${filename}`);
  return data;
};

export const uploadFile = async (file: File) => {
  const formData = new FormData();
  formData.append("file", file);
  const { data } = await api.post("/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data;
};

export const uploadText = async (title: string, content: string) => {
  const formData = new FormData();
  formData.append("title", title);
  formData.append("content", content);
  const { data } = await api.post("/upload/text", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data;
};

export const searchDocuments = async (
  question: string,
  topK: number,
  filterSource?: string
) => {
  const formData = new FormData();
  formData.append("question", question);
  formData.append("top_k", topK.toString());
  if (filterSource && filterSource !== "All Documents") {
    formData.append("filter_source", filterSource);
  }
  
  const { data } = await api.post("/search", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data.results;
};

export const compareDocs = async (docA: string, docB: string) => {
  const { data } = await api.post("/compare", { doc_a: docA, doc_b: docB });
  return data;
};

export const generateQuiz = async (
  document: string,
  numQuestions: number,
  qType: string
) => {
  const { data } = await api.post("/quiz/generate", {
    document,
    num_questions: numQuestions,
    q_type: qType,
  });
  return data.questions;
};

export const gradeQuizAnswer = async (
  questionObj: any,
  userAnswer: string
) => {
  const { data } = await api.post("/quiz/grade", {
    question_obj: questionObj,
    user_answer: userAnswer,
  });
  return data;
};

export const saveQuizScore = async (
  document: string,
  correctCount: number,
  total: number
) => {
  const formData = new FormData();
  formData.append("document", document);
  formData.append("correct_count", correctCount.toString());
  formData.append("total", total.toString());
  
  const { data } = await api.post("/quiz/save_score", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data;
};

export const getQuizWeakAreas = async (document: string) => {
  const { data } = await api.get(`/quiz/weak_areas?document=${encodeURIComponent(document)}`);
  return data.analysis;
};
export const saveNote = async (
  text: string,
  sourceLabel: string,
  bypassValidation: boolean = false
) => {
  const { data } = await api.post("/notes", {
    text,
    source_label: sourceLabel,
    bypass_validation: bypassValidation,
  });
  return data;
};
