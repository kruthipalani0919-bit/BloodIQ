from __future__ import annotations

from langchain_google_genai import ChatGoogleGenerativeAI

from config import get_settings


def get_llm(temperature: float = 0.1):
    settings = get_settings()

    if settings.llm_provider in {"gemini", "google", "google_gemini"}:
        if not settings.google_api_key:
            raise RuntimeError(
                "GOOGLE_API_KEY is required when LLM_PROVIDER is set to gemini."
            )

        return ChatGoogleGenerativeAI(
            model=settings.llm_model,
            google_api_key=settings.google_api_key,
            temperature=temperature,
        )

    raise NotImplementedError(
        f"LLM provider '{settings.llm_provider}' is not configured in the current phase."
    )