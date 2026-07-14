import api from "./axios";

export const getPractice = async (id: number) => {
  const response = await api.get(`/practice/${id}`);
  return response.data;
};

export const submitPractice = async (
  id: number,
  answer: string
) => {
  const response = await api.post(`/practice/${id}/submit`, {
    answer,
  });

  return response.data;
};

export const regeneratePractice = async (id: number) => {
  const response = await api.post(`/practice/${id}/regenerate`);
  return response.data;
};

export const completePractice = async (id: number) => {
  const response = await api.post(`/practice/${id}/complete`);
  return response.data;
};