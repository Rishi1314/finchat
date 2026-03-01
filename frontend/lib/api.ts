import axios from "axios";
const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export type AskRes = {
  answer: string;
  sources: { source: string; score?: number }[];
  confidence?: string;
  latency_ms?: number;
};

export async function ask(question: string): Promise<AskRes> {
  const { data } = await axios.post(`${API}/ask`, { question }, { timeout: 60000 });
  return data as AskRes;
}
