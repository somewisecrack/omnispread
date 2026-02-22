"use client";

import { useState, useEffect } from "react";
import { getPresets, type Presets } from "@/lib/api";

interface ScanFormProps {
    onScan: (tickers: string[], period: string, startDate?: string, endDate?: string) => void;
    isScanning: boolean;
}

const PERIODS = [
    { value: "6mo", label: "6 Months" },
    { value: "1y", label: "1 Year" },
    { value: "2y", label: "2 Years" },
    { value: "3y", label: "3 Years" },
    { value: "5y", label: "5 Years" },
    { value: "custom", label: "Custom" },
];

export default function ScanForm({ onScan, isScanning }: ScanFormProps) {
    const [tickerInput, setTickerInput] = useState("");
    const [period, setPeriod] = useState("3y");
    const [startDate, setStartDate] = useState("");
    const [endDate, setEndDate] = useState("");
    const [presets, setPresets] = useState<Presets>({});
    const [activePreset, setActivePreset] = useState<string | null>(null);

    useEffect(() => {
        getPresets()
            .then(setPresets)
            .catch(() => { });
    }, []);

    const handlePreset = (key: string) => {
        const tickers = presets[key];
        if (tickers) {
            setTickerInput(tickers.join(", "));
            setActivePreset(key);
        }
    };

    const handleScan = () => {
        const tickers = tickerInput
            .split(/[,\s]+/)
            .map((t) => t.trim().toUpperCase())
            .filter(Boolean);
        if (tickers.length >= 2) {
            if (period === "custom") {
                onScan(tickers, period, startDate, endDate);
            } else {
                onScan(tickers, period);
            }
        }
    };

    const formatPresetName = (key: string) =>
        key
            .split("_")
            .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
            .join(" ");

    return (
        <div className="glow-border" style={{
            borderRadius: "16px",
            padding: "28px",
            background: "linear-gradient(135deg, rgba(26, 26, 46, 0.8), rgba(18, 18, 26, 0.9))",
            backdropFilter: "blur(10px)",
        }}>
            {/* Preset Buttons */}
            <div style={{ marginBottom: "20px" }}>
                <label style={{
                    display: "block",
                    fontSize: "12px",
                    fontWeight: 600,
                    color: "var(--color-text-secondary)",
                    textTransform: "uppercase",
                    letterSpacing: "0.05em",
                    marginBottom: "10px",
                }}>
                    Presets
                </label>
                <div style={{ display: "flex", flexWrap: "wrap", gap: "8px" }}>
                    {Object.keys(presets).map((key) => (
                        <button
                            key={key}
                            onClick={() => handlePreset(key)}
                            style={{
                                padding: "6px 14px",
                                borderRadius: "8px",
                                fontSize: "13px",
                                fontWeight: 500,
                                cursor: "pointer",
                                transition: "all 0.2s",
                                border: activePreset === key
                                    ? "1px solid var(--color-accent-blue)"
                                    : "1px solid var(--color-border)",
                                background: activePreset === key
                                    ? "rgba(99, 102, 241, 0.15)"
                                    : "rgba(42, 42, 64, 0.5)",
                                color: activePreset === key
                                    ? "var(--color-accent-cyan)"
                                    : "var(--color-text-secondary)",
                            }}
                        >
                            {formatPresetName(key)}
                        </button>
                    ))}
                </div>
            </div>

            {/* Ticker Input */}
            <div style={{ marginBottom: "20px" }}>
                <label style={{
                    display: "block",
                    fontSize: "12px",
                    fontWeight: 600,
                    color: "var(--color-text-secondary)",
                    textTransform: "uppercase",
                    letterSpacing: "0.05em",
                    marginBottom: "8px",
                }}>
                    Tickers (comma-separated)
                </label>
                <textarea
                    value={tickerInput}
                    onChange={(e) => {
                        setTickerInput(e.target.value);
                        setActivePreset(null);
                    }}
                    placeholder="AAPL, MSFT, GOOGL, AMZN, META, NVDA..."
                    rows={2}
                    style={{
                        width: "100%",
                        padding: "12px 16px",
                        borderRadius: "10px",
                        border: "1px solid var(--color-border)",
                        background: "rgba(10, 10, 15, 0.6)",
                        color: "var(--color-text-primary)",
                        fontSize: "14px",
                        fontFamily: "var(--font-mono)",
                        resize: "none",
                        outline: "none",
                        transition: "border-color 0.2s",
                    }}
                    onFocus={(e) => (e.target.style.borderColor = "var(--color-accent-blue)")}
                    onBlur={(e) => (e.target.style.borderColor = "var(--color-border)")}
                />
            </div>

            {/* Period + Scan */}
            <div style={{ display: "flex", gap: "12px", alignItems: "flex-end" }}>
                <div style={{ flex: 1 }}>
                    <label style={{
                        display: "block",
                        fontSize: "12px",
                        fontWeight: 600,
                        color: "var(--color-text-secondary)",
                        textTransform: "uppercase",
                        letterSpacing: "0.05em",
                        marginBottom: "8px",
                    }}>
                        Lookback Period
                    </label>
                    <div style={{ display: "flex", gap: "6px" }}>
                        {PERIODS.map((p) => (
                            <button
                                key={p.value}
                                onClick={() => setPeriod(p.value)}
                                style={{
                                    flex: 1,
                                    padding: "10px 4px",
                                    borderRadius: "8px",
                                    fontSize: "13px",
                                    fontWeight: 500,
                                    cursor: "pointer",
                                    transition: "all 0.2s",
                                    border: period === p.value
                                        ? "1px solid var(--color-accent-blue)"
                                        : "1px solid var(--color-border)",
                                    background: period === p.value
                                        ? "rgba(99, 102, 241, 0.2)"
                                        : "transparent",
                                    color: period === p.value
                                        ? "var(--color-accent-cyan)"
                                        : "var(--color-text-muted)",
                                }}
                            >
                                {p.label}
                            </button>
                        ))}
                    </div>

                    {/* Custom Date Inputs */}
                    {period === "custom" && (
                        <div style={{ display: "flex", gap: "10px", marginTop: "12px", animation: "fadeIn 0.2s" }}>
                            <div style={{ flex: 1 }}>
                                <label style={{ display: "block", fontSize: "10px", color: "var(--color-text-muted)", marginBottom: "4px" }}>Start Date</label>
                                <input
                                    type="date"
                                    value={startDate}
                                    onChange={(e) => setStartDate(e.target.value)}
                                    style={{
                                        width: "100%", padding: "8px 12px", borderRadius: "8px", border: "1px solid var(--color-border)",
                                        background: "rgba(10, 10, 15, 0.6)", color: "var(--color-text-primary)", fontSize: "13px",
                                    }}
                                />
                            </div>
                            <div style={{ flex: 1 }}>
                                <label style={{ display: "block", fontSize: "10px", color: "var(--color-text-muted)", marginBottom: "4px" }}>End Date</label>
                                <input
                                    type="date"
                                    value={endDate}
                                    onChange={(e) => setEndDate(e.target.value)}
                                    style={{
                                        width: "100%", padding: "8px 12px", borderRadius: "8px", border: "1px solid var(--color-border)",
                                        background: "rgba(10, 10, 15, 0.6)", color: "var(--color-text-primary)", fontSize: "13px",
                                    }}
                                />
                            </div>
                        </div>
                    )}
                </div>

                <button
                    onClick={handleScan}
                    disabled={isScanning || tickerInput.trim().length === 0}
                    style={{
                        padding: "12px 32px",
                        borderRadius: "10px",
                        border: "none",
                        fontSize: "14px",
                        fontWeight: 600,
                        cursor: isScanning ? "not-allowed" : "pointer",
                        background: isScanning
                            ? "rgba(99, 102, 241, 0.3)"
                            : "linear-gradient(135deg, #6366f1, #4f46e5)",
                        color: "#fff",
                        transition: "all 0.2s",
                        opacity: tickerInput.trim().length === 0 ? 0.5 : 1,
                        display: "flex",
                        alignItems: "center",
                        gap: "8px",
                        whiteSpace: "nowrap",
                    }}
                >
                    {isScanning && (
                        <span style={{
                            width: "16px",
                            height: "16px",
                            border: "2px solid rgba(255,255,255,0.3)",
                            borderTop: "2px solid #fff",
                            borderRadius: "50%",
                            display: "inline-block",
                        }} className="animate-spin" />
                    )}
                    {isScanning ? "Scanning..." : "Run Scan"}
                </button>
            </div>
        </div>
    );
}
