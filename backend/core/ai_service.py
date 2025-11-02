# AI service module for CharityConnect
# Provides safe, OpenAI-powered text generation and moderation for event titles and descriptions

import os
from django.conf import settings
from typing import Dict, Any
from openai import OpenAI

# Create an authenticated OpenAI client
def _client() -> "OpenAI":
    # ensure AI features are enabled and an ALI key is available
    if not settings.AI_ENABLED or not settings.OPENAI_API_KEY:
        raise RuntimeError("AI is disabled or missing key")
    return OpenAI(api_key=settings.OPENAI_API_KEY)

# content moderation
def moderate_text(text: str) -> Dict[str, Any]:
    client = _client()
    resp = client.moderations.create(
        model="omni-moderation-latest",
        input=text[:6000]
    )
    result = resp.results[0]
    return {"allowed": not result.flagged, "categories": result.categories}

# system rules to guide AI behaviour
SYSTEM_RULES = (
    "You help charity event organisers draft clear, concise, positive event titles and "
    "descriptions. Keep under 120 words, avoid sensationalism, never invent facts, "
    "and ask for organiser review before publishing."
)

# main function: Generate suggested event
def suggest_event_copy(context: Dict[str, str]) -> Dict[str, str]:
    client = _client()

    # build user prompt dynamically from context values
    user_prompt = (
        f"Draft a short event title and 1-paragraph description for a charity event.\n"
        f"Cause: {context.get('cause','')}\nLocation: {context.get('location','')}\n"
        f"Date: {context.get('date','')}\nTone: {context.get('tone','friendly')}\n"
        f"Audience: {context.get('audience','general public')}\n"
        f"Optional title hint: {context.get('title_hint','')}\n"
        f"Constraints: 6–10 word title; 80–120 word description; no promises or claims; "
        f"include call-to-action and mention that details will be confirmed by organiser."
    )

    # check prompt saftey before sending to OpenAI
    mod = moderate_text(user_prompt)
    if not mod["allowed"]:
        raise ValueError("Input failed moderation; please adjust your details.")
    
    # generate AI response following system rules
    chat = client.chat.completions.create(
        model=settings.AI_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_RULES},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
    )

    # parse output into title and discription
    text = chat.choices[0].message.content or ""
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    title = lines[0].strip(" \"'")
    desc = " ".join(lines[1:]) if len(lines) > 1 else ""

    # moderate AI output fir saftey and compliance
    out_mod = moderate_text(f"{title}\n{desc}")
    if not out_mod["allowed"]:
        raise ValueError("Generated text failed moderation; try different tone or fewer details.")
    return {"title": title, "description": desc}
