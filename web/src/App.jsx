import { useMemo, useState } from "react";
import { sendChat } from "./api.js";

const defaultPrompt =
    "You are a helpful AI assistant. Answer clearly and concisely.";

export default function App() {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");
    const [systemPrompt, setSystemPrompt] = useState(defaultPrompt);
    const [temperature, setTemperature] = useState(0.7);
    const [maxTokens, setMaxTokens] = useState(1024);
    const [isSending, setIsSending] = useState(false);
    const [error, setError] = useState("");
    const [showTuning, setShowTuning] = useState(true);

    const persona = useMemo(() => {
        if (temperature <= 0.4) return "Precise";
        if (temperature <= 1.1) return "Balanced";
        return "Expressive";
    }, [temperature]);

    const handleSend = async () => {
        const trimmed = input.trim();
        if (!trimmed || isSending) return;

        const nextMessages = [...messages, { role: "user", content: trimmed }];
        setMessages(nextMessages);
        setInput("");
        setIsSending(true);
        setError("");

        try {
            const data = await sendChat({
                messages: nextMessages,
                systemPrompt,
                temperature,
                maxTokens,
            });
            setMessages((prev) => [
                ...prev,
                { role: "assistant", content: data.answer },
            ]);
        } catch (err) {
            setError(err.message || "Something went wrong");
        } finally {
            setIsSending(false);
        }
    };

    const handleKeyDown = (event) => {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            handleSend();
        }
    };

    const handleClear = () => {
        setMessages([]);
        setError("");
    };

    return (
        <div className="app">
            <div className="background-orb" aria-hidden="true"></div>
            <header className="hero">
                <span className="badge">Groq Llama 3.3 70B</span>
                <h1>Amine Ai assistant</h1>
                <p>
                    A cinematic command deck for your AI assistant. Tune the tone, keep the
                    thread, and ship answers fast.
                </p>
            </header>

            <main className="layout">
                <section className="panel conversation">
                    <div className="panel-header">
                        <div>
                            <h2>Conversation</h2>
                            <span className="sub">Persona: {persona}</span>
                        </div>
                        <button className="ghost" onClick={handleClear}>
                            Clear
                        </button>
                    </div>

                    <div className="chat-window">
                        {messages.length === 0 ? (
                            <div className="empty-state">
                                <h3>Start with a bold question</h3>
                                <p>
                                    Ask for a plan, a rewrite, or a brainstorm. The assistant will
                                    answer in seconds.
                                </p>
                            </div>
                        ) : (
                            messages.map((msg, index) => (
                                <div
                                    key={`${msg.role}-${index}`}
                                    className={`bubble ${msg.role}`}
                                >
                                    <span className="role">{msg.role}</span>
                                    <p>{msg.content}</p>
                                </div>
                            ))
                        )}
                        {isSending && (
                            <div className="bubble assistant typing">
                                <span className="role">assistant</span>
                                <p>Thinking...</p>
                            </div>
                        )}
                    </div>

                    {error && <div className="error-banner">{error}</div>}

                    <div className="composer">
                        <textarea
                            value={input}
                            onChange={(event) => setInput(event.target.value)}
                            onKeyDown={handleKeyDown}
                            placeholder="Type your message..."
                            rows={3}
                        />
                        <button onClick={handleSend} disabled={isSending}>
                            {isSending ? "Sending..." : "Send"}
                        </button>
                    </div>
                </section>

                <section className="panel settings">
                    <div className="panel-header">
                        <div>
                            <h2>Controls</h2>
                            <span className="sub">Fine-tune the voice</span>
                        </div>
                        <button
                            className="ghost"
                            onClick={() => setShowTuning((prev) => !prev)}
                            type="button"
                        >
                            {showTuning ? "Hide tuning" : "Show tuning"}
                        </button>
                    </div>

                    <label>
                        System prompt
                        <textarea
                            value={systemPrompt}
                            onChange={(event) => setSystemPrompt(event.target.value)}
                            rows={5}
                        />
                    </label>

                    {showTuning && (
                        <div className="tuning-controls">
                            <label>
                                Temperature: <strong>{temperature.toFixed(1)}</strong>
                                <input
                                    type="range"
                                    min="0"
                                    max="2"
                                    step="0.1"
                                    value={temperature}
                                    onChange={(event) =>
                                        setTemperature(Number(event.target.value))
                                    }
                                />
                            </label>

                            <label>
                                Max tokens: <strong>{maxTokens}</strong>
                                <input
                                    type="range"
                                    min="50"
                                    max="2048"
                                    step="50"
                                    value={maxTokens}
                                    onChange={(event) =>
                                        setMaxTokens(Number(event.target.value))
                                    }
                                />
                            </label>
                        </div>
                    )}

                    <div className="meta">
                        <div>
                            <span>Provider</span>
                            <strong>Groq Cloud</strong>
                        </div>
                        <div>
                            <span>Model</span>
                            <strong>llama-3.3-70b</strong>
                        </div>
                    </div>
                </section>
            </main>
        </div>
    );
}
