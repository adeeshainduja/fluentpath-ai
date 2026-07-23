import api from "../api/axios";;

export const getPractice = async (id: number) => {
  const response = await api.get(`/practice/${id}`);
  return response.data;
};

export const submitPractice = async (
  id: number,
  answer: string
) => {
  const response = await api.post(
    `/practice-tasks/${id}/submit`,
    {
      text: answer,
    }
  );

  return response.data;
};

// TODO: Create backend endpoints later
export const regeneratePractice = async (id: number) => {
  console.log("Regenerate:", id);

  return {
    success: true,
    message: "Regenerate not implemented yet.",
  };
};

export const completePractice = async (id: number) => {
  console.log("Complete:", id);

  return {
    success: true,
    message: "Complete not implemented yet.",
  };
};