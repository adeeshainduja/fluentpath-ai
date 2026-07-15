import axios from "axios";

const API_BASE_URL = "http://localhost:8000/api/v1";

export async function getRecommendation(
  learnerId: number
) {
  const response = await axios.get(
    `${API_BASE_URL}/recommendations/${learnerId}`
  );

  return response.data;
}