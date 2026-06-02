import { useQuery } from "@tanstack/react-query";
import { getDashboard } from "@/lib/api";

export const useDashboard = (userId: string | null) => {
    return useQuery({
        queryKey: ["dashboard", userId],

        enabled: !!userId,

        queryFn: async () => {
            return getDashboard(userId!);
        },

        staleTime: 60_000,
        refetchOnWindowFocus: false,
        retry: 1,
    });
};