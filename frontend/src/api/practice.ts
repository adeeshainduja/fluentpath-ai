import axios from "./axios";

export async function getPractice(id: number) {
  const response = await axios.get(`/practice/${id}`);
  return response.data;
}