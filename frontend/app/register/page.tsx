"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { registerUser } from "../../lib/api/auth";
import { useUser } from "../../hooks/useUser";

import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "../../components/ui/card";
import { Input } from "../../components/ui/input";
import { Label } from "../../components/ui/label";
import { Button } from "../../components/ui/button";
import { Alert, AlertDescription } from "../../components/ui/alert";
import { Loader2 } from "lucide-react";
import Link from "next/link";

const registerSchema = z.object({
    name: z.string().min(2, { message: "Name must be at least 2 characters" }),
    email: z.string().email({ message: "Invalid email address" }),
    password: z.string().min(6, { message: "Password must be at least 6 characters" }),
});

type RegisterFormValues = z.infer<typeof registerSchema>;

export default function RegisterPage() {
    const router = useRouter();
    const [error, setError] = useState<string | null>(null);

    // If user is already logged in, redirect to dashboard
    useUser({ redirectTo: "/dashboard", redirectIfFound: true });

    const {
        register,
        handleSubmit,
        formState: { errors, isSubmitting },
    } = useForm<RegisterFormValues>({
        resolver: zodResolver(registerSchema),
    });

    const onSubmit = async (data: RegisterFormValues) => {
        setError(null);
        try {
            await registerUser(data);
            router.push("/login");
        } catch (err: any) {
            setError(err.response?.data?.detail || "Registration failed. Please try again.");
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-zinc-950 p-4">
            <Card className="w-full max-w-md bg-zinc-900 border-zinc-800 text-white">
                <CardHeader className="space-y-1">
                    <CardTitle className="text-2xl font-bold tracking-tight">Create an account</CardTitle>
                    <CardDescription className="text-zinc-400">
                        Enter your information to get started with Behaviour AI
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
                        {error && (
                            <Alert variant="destructive" className="bg-red-900/20 border-red-900 text-red-500">
                                <AlertDescription>{error}</AlertDescription>
                            </Alert>
                        )}
                        <div className="space-y-2">
                            <Label htmlFor="name" className="text-zinc-300">Name</Label>
                            <Input
                                id="name"
                                type="text"
                                placeholder="John Doe"
                                className="bg-zinc-800 border-zinc-700 text-white placeholder:text-zinc-500 focus-visible:ring-zinc-600"
                                {...register("name")}
                            />
                            {errors.name && (
                                <p className="text-sm text-red-500">{errors.name.message}</p>
                            )}
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="email" className="text-zinc-300">Email</Label>
                            <Input
                                id="email"
                                type="email"
                                placeholder="name@example.com"
                                className="bg-zinc-800 border-zinc-700 text-white placeholder:text-zinc-500 focus-visible:ring-zinc-600"
                                {...register("email")}
                            />
                            {errors.email && (
                                <p className="text-sm text-red-500">{errors.email.message}</p>
                            )}
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="password" className="text-zinc-300">Password</Label>
                            <Input
                                id="password"
                                type="password"
                                className="bg-zinc-800 border-zinc-700 text-white focus-visible:ring-zinc-600"
                                {...register("password")}
                            />
                            {errors.password && (
                                <p className="text-sm text-red-500">{errors.password.message}</p>
                            )}
                        </div>
                        <Button 
                            type="submit" 
                            className="w-full bg-white text-black hover:bg-zinc-200"
                            disabled={isSubmitting}
                        >
                            {isSubmitting ? (
                                <>
                                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                                    Creating account...
                                </>
                            ) : (
                                "Sign Up"
                            )}
                        </Button>
                    </form>
                </CardContent>
                <CardFooter className="flex flex-col space-y-4">
                    <div className="text-sm text-center text-zinc-400">
                        Already have an account?{" "}
                        <Link href="/login" className="text-white hover:underline underline-offset-4">
                            Sign in
                        </Link>
                    </div>
                </CardFooter>
            </Card>
        </div>
    );
}
