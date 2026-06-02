import { apiClient } from "./client";

export const getPredictionHistory = async () => {
    // The apiClient automatically attaches the secure HTTP-Only cookie,
    // so there's no need to manually pass or retrieve a token here.
    const response = await apiClient.get("/predictions/history");
    return response.data;
};
