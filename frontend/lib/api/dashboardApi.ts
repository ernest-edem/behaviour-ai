import { apiClient } from "./client";

// =====================================
// DASHBOARD API
// =====================================

export function getDashboard(userId: number) {
    const url = `/dashboard/${userId}`;

    console.log("[Dashboard API]", url);

    return apiClient.get(url);
}

// =====================================
// PREDICTION HISTORY API
// =====================================

export function getPredictionHistory() {
    const url = `/predictions/history`;

    console.log("[Prediction History API]", url);

    return apiClient.get(url);
}

// =====================================
// INSIGHTS API
// =====================================

export function getInsights(userId: number) {
    const url = `/insights/${userId}`;

    console.log("[Insights API]", url);

    return apiClient.get(url);
}

// =====================================
// ALERTS API
// =====================================

export function getAlerts(userId: number) {
    const url = `/alerts/${userId}`;

    console.log("[Alerts API]", url);

    return apiClient.get(url);
}