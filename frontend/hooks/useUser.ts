import { useQuery } from "@tanstack/react-query";
import { getCurrentUser } from "../lib/api/auth";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

export const useUser = ({ redirectTo = "", redirectIfFound = false } = {}) => {
    const router = useRouter();

    const { data: user, isLoading, isError, error } = useQuery({
        queryKey: ["user"],
        queryFn: getCurrentUser,
        retry: 0,
        staleTime: 1000 * 60 * 5, // 5 minutes
    });

    useEffect(() => {
        if (isLoading) return;

        // If no user and we should redirect (protecting a route)
        if (!user && redirectTo && !redirectIfFound) {
            router.push(redirectTo);
        }

        // If user exists and we should redirect (e.g., away from login page)
        if (user && redirectIfFound && redirectTo) {
            router.push(redirectTo);
        }
    }, [user, isLoading, redirectTo, redirectIfFound, router]);

    return { user, isLoading, isError, error };
};