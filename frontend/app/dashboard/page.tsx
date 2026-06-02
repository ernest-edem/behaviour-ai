"use client";

import { useDashboard } from "../../hooks/useDashboard";
import { useUser } from "../../hooks/useUser";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "../../components/ui/card";
import { Button } from "../../components/ui/button";
import { Activity, AlertTriangle, ShieldCheck, HeartPulse, LogOut, Loader2 } from "lucide-react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { useRouter } from "next/navigation";
import { useQueryClient } from "@tanstack/react-query";

import { logoutUser } from "../../lib/api/auth";

export default function DashboardPage() {
    const router = useRouter();
    const queryClient = useQueryClient();
    
    // Protect route: requires login
    const { user, isLoading: userLoading } = useUser({ redirectTo: "/login" });
    
    const { data, isLoading: dashboardLoading, isError } = useDashboard(user?.id || null);

    const handleLogout = async () => {
        try {
            await logoutUser();
        } catch (error) {
            console.error("Logout failed", error);
        } finally {
            queryClient.clear();
            router.push("/login");
        }
    };

    if (userLoading || (user && dashboardLoading)) {
        return (
            <div className="min-h-screen bg-zinc-950 flex flex-col items-center justify-center text-white space-y-4">
                <Loader2 className="h-8 w-8 animate-spin text-zinc-400" />
                <p className="text-zinc-400">Loading your AI Dashboard...</p>
            </div>
        );
    }

    if (!user) return null; // Will redirect

    return (
        <div className="min-h-screen bg-zinc-950 text-white p-6 md:p-10">
            <div className="max-w-7xl mx-auto space-y-8">
                
                {/* Header Section */}
                <header className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                    <div>
                        <h1 className="text-3xl font-bold tracking-tight text-zinc-100">Welcome, {user.name}</h1>
                        <p className="text-zinc-400">Here is your AI-driven health and behavioral overview.</p>
                    </div>
                    <Button variant="outline" onClick={handleLogout} className="border-zinc-700 text-zinc-300 hover:bg-zinc-800 hover:text-white">
                        <LogOut className="mr-2 h-4 w-4" />
                        Log Out
                    </Button>
                </header>

                {isError ? (
                    <Card className="bg-red-900/10 border-red-900">
                        <CardContent className="pt-6 text-red-500 flex items-center">
                            <AlertTriangle className="h-5 w-5 mr-3" />
                            Failed to load dashboard data. Please try again later.
                        </CardContent>
                    </Card>
                ) : data?.message ? (
                    <Card className="bg-zinc-900 border-zinc-800">
                        <CardContent className="pt-6 text-zinc-400 flex flex-col items-center justify-center py-12">
                            <Activity className="h-12 w-12 mb-4 text-zinc-600" />
                            <p className="text-lg">No health data available yet.</p>
                            <p className="text-sm">Complete your first assessment to generate insights.</p>
                        </CardContent>
                    </Card>
                ) : (
                    <>
                        {/* Metrics Grid */}
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                            <Card className="bg-zinc-900 border-zinc-800 text-white">
                                <CardHeader className="flex flex-row items-center justify-between pb-2">
                                    <CardTitle className="text-sm font-medium text-zinc-400">Avg Health Score</CardTitle>
                                    <HeartPulse className="h-4 w-4 text-emerald-500" />
                                </CardHeader>
                                <CardContent>
                                    <div className="text-2xl font-bold">{data?.average_health_score || 0}%</div>
                                </CardContent>
                            </Card>

                            <Card className="bg-zinc-900 border-zinc-800 text-white">
                                <CardHeader className="flex flex-row items-center justify-between pb-2">
                                    <CardTitle className="text-sm font-medium text-zinc-400">Avg Risk Score</CardTitle>
                                    <AlertTriangle className="h-4 w-4 text-amber-500" />
                                </CardHeader>
                                <CardContent>
                                    <div className="text-2xl font-bold">{data?.average_risk_score || 0}%</div>
                                </CardContent>
                            </Card>

                            <Card className="bg-zinc-900 border-zinc-800 text-white">
                                <CardHeader className="flex flex-row items-center justify-between pb-2">
                                    <CardTitle className="text-sm font-medium text-zinc-400">Latest Status</CardTitle>
                                    <ShieldCheck className="h-4 w-4 text-blue-500" />
                                </CardHeader>
                                <CardContent>
                                    <div className="text-2xl font-bold capitalize">{data?.latest_risk_level || "Unknown"}</div>
                                    <p className="text-xs text-zinc-500 mt-1">Urgency: {data?.latest_urgency}</p>
                                </CardContent>
                            </Card>

                            <Card className="bg-zinc-900 border-zinc-800 text-white">
                                <CardHeader className="flex flex-row items-center justify-between pb-2">
                                    <CardTitle className="text-sm font-medium text-zinc-400">Common Condition</CardTitle>
                                    <Activity className="h-4 w-4 text-purple-500" />
                                </CardHeader>
                                <CardContent>
                                    <div className="text-2xl font-bold capitalize truncate">{data?.most_common_disease || "None"}</div>
                                </CardContent>
                            </Card>
                        </div>

                        {/* Chart Section */}
                        <Card className="bg-zinc-900 border-zinc-800 text-white">
                            <CardHeader>
                                <CardTitle>Health & Risk Trend</CardTitle>
                                <CardDescription className="text-zinc-400">Your prediction history over time</CardDescription>
                            </CardHeader>
                            <CardContent className="h-[350px] w-full">
                                {data?.risk_trend && data.risk_trend.length > 0 ? (
                                    <ResponsiveContainer width="100%" height="100%">
                                        <LineChart data={data.risk_trend} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
                                            <CartesianGrid strokeDasharray="3 3" stroke="#3f3f46" vertical={false} />
                                            <XAxis 
                                                dataKey="date" 
                                                stroke="#a1a1aa" 
                                                fontSize={12} 
                                                tickFormatter={(val) => new Date(val).toLocaleDateString()}
                                            />
                                            <YAxis stroke="#a1a1aa" fontSize={12} />
                                            <Tooltip 
                                                contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', color: '#fff' }}
                                                labelFormatter={(val) => new Date(val).toLocaleString()}
                                            />
                                            <Line type="monotone" dataKey="health_score" name="Health Score" stroke="#10b981" strokeWidth={2} dot={{ r: 4 }} activeDot={{ r: 6 }} />
                                            <Line type="monotone" dataKey="risk_score" name="Risk Score" stroke="#f59e0b" strokeWidth={2} dot={{ r: 4 }} activeDot={{ r: 6 }} />
                                        </LineChart>
                                    </ResponsiveContainer>
                                ) : (
                                    <div className="h-full flex items-center justify-center text-zinc-500">
                                        Not enough trend data to display chart.
                                    </div>
                                )}
                            </CardContent>
                        </Card>
                    </>
                )}
            </div>
        </div>
    );
}