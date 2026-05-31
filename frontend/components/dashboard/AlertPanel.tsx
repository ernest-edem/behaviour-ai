"use client";

import { useEffect, useState } from "react";
import axios from "axios";

export default function AlertPanel() {
    const [alerts, setAlerts] = useState([]);

    useEffect(() => {
        async function load() {
            try {
                const user = JSON.parse(
                    localStorage.getItem("user") || "null"
                );

                if (!user) return;

                const res = await axios.get(
                    `http://127.0.0.1:8000/alerts/${user.id}`,
                    {
                        headers: {
                            Authorization: `Bearer ${localStorage.getItem("token")}`,
                        },
                    }
                );

                setAlerts(res.data.alerts || []);
            } catch (err) {
                console.error(err);
            }
        }

        load();
    }, []);

    return (
        <div className="bg-zinc-900 p-4 rounded-xl">
            <h2 className="text-sm text-gray-400 mb-3">
                Health Alerts
            </h2>

            <div className="space-y-2">
                {alerts.map((a: any, i) => (
                    <div key={i} className="p-2 bg-zinc-800 rounded text-sm">
                        {a.message}
                    </div>
                ))}
            </div>
        </div>
    );
}