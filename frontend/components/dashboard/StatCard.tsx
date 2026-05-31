export default function StatCard({ title, value, subtitle, color = "text-white" }: any) {
    return (
        <div className="bg-zinc-900 p-4 rounded-xl border border-zinc-800">
            <p className="text-sm text-gray-400">{title}</p>
            <p className={`text-2xl font-bold ${color}`}>{value}</p>
            {subtitle && (
                <p className="text-xs text-gray-500">{subtitle}</p>
            )}
        </div>
    );
}