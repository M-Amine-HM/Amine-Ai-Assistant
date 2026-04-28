const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function sendChat({ messages, systemPrompt, temperature, maxTokens }) {
    const response = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            messages,
            system_prompt: systemPrompt,
            temperature,
            max_tokens: maxTokens,
        }),
    });

    if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.detail || "Request failed");
    }

    return response.json();
}
