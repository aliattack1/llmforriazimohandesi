@csrf_exempt
def chat_view(request):
    history = []

    if request.method == "POST":
        user_query = request.POST.get("query", "").strip()
        systemdoc = ''
        with open('doc.txt', 'r') as file:
            systemdoc = file.read()
        if user_query:
            payload = {
                "model": "meta-llama/llama-3.3-8b-instruct:free",
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant. answer questions using this document: " + systemdoc},
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

            history.append({
                "question": user_query,
                "answer": answer
            })

    return render(request, "index.html", {"history": history})
