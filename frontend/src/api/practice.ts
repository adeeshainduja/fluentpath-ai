import axios from "./axios";

export async function getPractice(id: number) {
  const response = await axios.get(`/api/v1/practice/${id}`);
  return response.data;
}