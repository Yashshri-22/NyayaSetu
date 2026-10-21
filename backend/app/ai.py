from app.core import settings
def generate(prompt):
    if not settings.gemini_api_key:return ""
    try:
        import google.generativeai as genai
        genai.configure(api_key=settings.gemini_api_key)
        return (genai.GenerativeModel(settings.gemini_model).generate_content(prompt).text or "").strip()
    except Exception:return ""
