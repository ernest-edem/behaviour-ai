"use client";

export default function Error({
    error,
}: {
    error: Error;
}) {
    return (
        <div className="min-h-screen flex items-center justify-center text-red-400">
            Dashboard Error: {error.message}
        </div>
    );
}