# API endpoint for AI-generated charity event suggestions
# Integrates with OpenAI to create short, engaging event descriptions

from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny 
from rest_framework.response import Response
from rest_framework import status

# prevents errors if openAI SDK isn't installed
try:
    from openai import OpenAI
except Exception as e:
    OpenAI = None

# helper to initialise openAI client if API key is available
def _ai_client():
    key = getattr(settings, "OPENAI_API_KEY", None)
    if not key or not OpenAI:
        return None
    return OpenAI(api_key=key)

@api_view(["POST"])
@permission_classes([AllowAny])
def ai_suggest_event(request):
    # handle AI service availability and config checks
    if not getattr(settings, "AI_ENABLED", False):
        return Response({"error": "AI is disabled"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    if not getattr(settings, "OPENAI_API_KEY", None):
        return Response({"error": "Missing API key"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    if OpenAI is None:
        return Response({"error": "OpenAI SDK not installed"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    # extract request data and build prompt for AI model
    payload = request.data or {}
    cause = payload.get("cause", "charity event")
    location = payload.get("location", "Ireland")
    date = payload.get("date", "soon")
    tone = payload.get("tone", "friendly")

    prompt = (
        f"Write a short, {tone} description for a fundraiser.\n"
        f"Cause: {cause}\nLocation: {location}\nDate: {date}\n"
        f"Keep it under 120 words and include a call to action."
    )

    try:
        client = _ai_client()
        if client is None:
            return Response({"error": "AI service not available"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
        # generate text suggestion using openAI chat model
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for a charity platform."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )

        # return the generated event suggestion
        text = resp.choices[0].message.content.strip()
        return Response({"suggestion": text}, status=status.HTTP_200_OK)
    
    # handle AI- related errors
    except Exception as e:
        print("AI error:", repr(e))
        return Response({"error": "AI service not available"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
