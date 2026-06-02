import { apiClient } from "./client";

export const getDashboard = async (userId: string) => {
    // Backend expects /dashboard/{user_id}
    const res = await apiClient.get(`/dashboard/${userId}`);
    return res.data;
};