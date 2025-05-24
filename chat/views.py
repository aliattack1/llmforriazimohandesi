# assistant/views.py
import requests, logging
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = "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"

@csrf_exempt
def chat_view(request):
    answer = ""

    if request.method == "POST":
        user_query = request.POST.get("query", "").strip()
        if user_query:
            payload = {
                "model": "meta-llama/llama-3.3-8b-instruct:free",
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user",   "content": user_query}
                ]
            }
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }

            try:
                resp = requests.post(
                    OPENROUTER_URL,
                    headers=headers,
                    json=payload,
                    timeout=15
                )
                resp.raise_for_status()
                data = resp.json()
                choices = data.get("choices", [])
                answer = choices[0]["message"]["content"] if choices else "No response"
            except Exception as e:
                logger.exception("OpenRouter error")
                answer = f"[Error contacting AI: {e}]"

    return render(request, "index.html", {"answer": answer})
