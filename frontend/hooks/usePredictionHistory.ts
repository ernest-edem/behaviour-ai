import { useQuery } from "@tanstack/react-query";
import { getPredictionHistory } from "@/lib/api/dashboardApi";

export function usePredictionHistory() {
    return useQuery({
        queryKey: ["prediction-history"],
        queryFn: () => getPredictionHistory().then(res => res.data.history),
    });
}