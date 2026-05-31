export default function TrendBadge({ trend }: any) {
    const color =
        trend === "improving"
            ? "bg-green-500"
            : trend === "declining"
                ? "bg-red-500"
                : "bg-yellow-500";

    return (
        <span className={`px-3 py-1 rounded-full text-xs ${color}`}>
            {trend}
        </span>
    );
}