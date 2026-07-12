import api from "./axios";

export const getDashboard = async (learnerId: number) => {
  const response = await api.get(`/dashboard/${learnerId}`);
  return response.data;
};