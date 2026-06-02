import axios from "axios";

const API_URL =
    process.env.NEXT_PUBLIC_API_URL ||
    "http://localhost:8000";

export const apiClient = axios.create({
    baseURL: API_URL,
    withCredentials: true, // Send HTTP-Only cookies with requests
    headers: {
        "Content-Type": "application/json",
    },
});

// Intercept responses to handle global authentication errors
apiClient.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            if (typeof window !== "undefined") {
                // Trigger a global unauthorized event (can be listened to by Auth providers)
                window.dispatchEvent(new Event("unauthorized"));
            }
        }
        return Promise.reject(error);
    }
);