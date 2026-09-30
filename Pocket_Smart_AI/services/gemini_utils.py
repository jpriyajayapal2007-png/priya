import json
from typing import Any

from google import genai
from google.genai import types

from app.config import get_settings

from app.services.catalog import demo_products

from app.services.prompts import (
    SYSTEM,
    build_prompt
)


settings = get_settings()


def _demo(
    planner: str,
    data: dict,
    image_note: str | None = None
) -> dict:

    budget = float(
        data["budget"]
    )

    if planner == "home":

        allocation = [

            {
                "category": "Furniture",
                "amount": round(
                    budget * 0.40,
                    2
                ),
                "reason":
                    "Core functional pieces"
            },

            {
                "category": "Lighting",
                "amount": round(
                    budget * 0.15,
                    2
                ),
                "reason":
                    "Functional and ambient lighting"
            },

            {
                "category": "Decor",
                "amount": round(
                    budget * 0.20,
                    2
                ),
                "reason":
                    "Visual finishing touches"
            },

            {
                "category": "Appliances",
                "amount": round(
                    budget * 0.15,
                    2
                ),
                "reason":
                    "Useful room equipment"
            },

            {
                "category": "Buffer",
                "amount": round(
                    budget * 0.10,
                    2
                ),
                "reason":
                    "Unexpected costs"
            }
        ]

        summary = (
            f"A balanced "
            f"{data.get('style', 'modern')} "
            f"home plan for a budget of "
            f"₹{budget:,.0f}."
        )

    elif planner == "party":

        allocation = [

            {
                "category": "Food",
                "amount": round(
                    budget * 0.45,
                    2
                ),
                "reason":
                    "Main guest expense"
            },

            {
                "category": "Venue",
                "amount": round(
                    budget * 0.25,
                    2
                ),
                "reason":
                    "Space and basic facilities"
            },

            {
                "category": "Decoration",
                "amount": round(
                    budget * 0.15,
                    2
                ),
                "reason":
                    "Theme and atmosphere"
            },

            {
                "category": "Entertainment",
                "amount": round(
                    budget * 0.10,
                    2
                ),
                "reason":
                    "Activities and music"
            },

            {
                "category": "Buffer",
                "amount": round(
                    budget * 0.05,
                    2
                ),
                "reason":
                    "Contingency"
            }
        ]

        summary = (
            f"A "
            f"{data.get('event_type', 'event')} "
            f"plan for "
            f"{data.get('guests')} guests "
            f"within ₹{budget:,.0f}."
        )

    else:

        allocation = [

            {
                "category": "Primary jewelry",
                "amount": round(
                    budget * 0.55,
                    2
                ),
                "reason":
                    "Main statement piece"
            },

            {
                "category": "Secondary piece",
                "amount": round(
                    budget * 0.25,
                    2
                ),
                "reason":
                    "Coordination"
            },

            {
                "category": "Reserve",
                "amount": round(
                    budget * 0.20,
                    2
                ),
                "reason":
                    "Alternative or adjustment"
            }
        ]

        summary = (
            f"A "
            f"{data.get('style', 'elegant')} "
            f"jewelry plan for a "
            f"{data.get('occasion', 'special')} "
            f"occasion within "
            f"₹{budget:,.0f}."
        )

        if image_note:

            summary += (
                " The uploaded outfit image was "
                "received and considered for visual coordination."
            )

    recommendations = demo_products(
        "",
        budget,
        planner
    )

    return {

        "summary": summary,

        "allocation": allocation,

        "recommendations":
            recommendations,

        "tips": [

            "Treat displayed prices as estimates unless a connected provider supplies live pricing.",

            "Compare shipping, taxes, delivery time and return policies before purchase.",

            "Keep the buffer category available instead of spending the full budget immediately."
        ]
    }


def generate_recommendation(
    planner: str,
    data: dict,
    image_bytes: bytes | None = None,
    mime_type: str | None = None
) -> tuple[dict, str]:

    image_note = None

    if image_bytes:

        image_note = (
            f"An image ({mime_type or 'image'}) "
            "was uploaded for visual style analysis."
        )

    # No API key = demo mode
    if not settings.gemini_api_key:

        return (
            _demo(
                planner,
                data,
                image_note
            ),
            "demo"
        )

    try:

        client = genai.Client(
            api_key=settings.gemini_api_key
        )

        catalog = demo_products(
            "",
            float(data["budget"]),
            planner
        )

        contents: list[Any] = [

            build_prompt(
                planner,
                data,
                catalog
            )
        ]

        if image_bytes:

            contents.append(
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=mime_type or "image/jpeg"
                )
            )

        response = client.models.generate_content(

            model=settings.gemini_model,

            contents=contents,

            config=types.GenerateContentConfig(

                system_instruction=SYSTEM,

                response_mime_type="application/json",

                temperature=0.4
            )
        )

        parsed = json.loads(
            response.text
        )

        parsed.setdefault(
            "recommendations",
            []
        )

        parsed.setdefault(
            "allocation",
            []
        )

        parsed.setdefault(
            "tips",
            []
        )

        parsed.setdefault(
            "summary",
            "Generated budget recommendations."
        )

        return (
            parsed,
            "gemini"
        )

    except Exception:

        # Graceful fallback
        return (
            _demo(
                planner,
                data,
                image_note
            ),
            "demo"
        )


def validate_image(
    raw: bytes,
    content_type: str | None,
    max_mb: int
) -> None:

    if len(raw) > max_mb * 1024 * 1024:

        raise ValueError(
            f"Image must be smaller than {max_mb} MB."
        )

    allowed = {
        "image/jpeg",
        "image/png",
        "image/webp"
    }

    if content_type not in allowed:

        raise ValueError(
            "Only JPEG, PNG, and WebP images are supported."
        )

    try:

        from io import BytesIO

        from PIL import Image

        with Image.open(
            BytesIO(raw)
        ) as image:

            image.verify()

    except Exception as exc:

        raise ValueError(
            "The uploaded file is not a valid image."
        ) from exc