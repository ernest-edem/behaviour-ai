import { apiClient } from "./client";

export interface User {
    id: string;
    name: string;
    email: string;
    is_active: boolean;
    created_at: string;
}

export const registerUser = async (data: any) => {
    const res = await apiClient.post("/users/register", data);
    return res.data;
};

export const loginUser = async (credentials: any) => {
    const res = await apiClient.post("/users/login", credentials);
    return res.data;
};

export const getCurrentUser = async (): Promise<User> => {
    const res = await apiClient.get("/users/me");
    return res.data;
};

export const logoutUser = async () => {
    const res = await apiClient.post("/users/logout");
    return res.data;
};
