from typing import Any
from typing import Literal

from pydantic import BaseModel
from pydantic import Field


class RegisterRequest(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=80
    )

    email: str = Field(
        min_length=5,
        max_length=255
    )

    password: str = Field(
        min_length=8,
        max_length=128
    )


class LoginRequest(BaseModel):

    email: str

    password: str


class HomeItem(BaseModel):

    category: str = Field(
        min_length=1,
        max_length=80
    )

    quantity: int = Field(
        default=1,
        ge=1,
        le=50
    )


class HomeRequest(BaseModel):

    budget: float = Field(
        gt=0,
        le=10_000_000
    )

    rooms: list[str] = Field(
        default_factory=list
    )

    style: str = Field(
        default="modern",
        max_length=80
    )

    items: list[HomeItem] = Field(
        default_factory=list
    )

    city: str = Field(
        default="Chennai",
        max_length=100
    )


class PartyRequest(BaseModel):

    budget: float = Field(
        gt=0,
        le=10_000_000
    )

    guests: int = Field(
        gt=0,
        le=10_000
    )

    event_type: str = Field(
        default="birthday",
        max_length=80
    )

    venue: str = Field(
        default="indoor",
        max_length=100
    )

    city: str = Field(
        default="Chennai",
        max_length=100
    )

    food_preference: str = Field(
        default="mixed",
        max_length=80
    )


class JewelryRequest(BaseModel):

    budget: float = Field(
        gt=0,
        le=10_000_000
    )

    occasion: str = Field(
        default="wedding",
        max_length=80
    )

    style: str = Field(
        default="elegant",
        max_length=80
    )

    metal: str = Field(
        default="any",
        max_length=80
    )

    notes: str = Field(
        default="",
        max_length=1000
    )


class RecommendationResponse(BaseModel):

    planner: Literal[
        "home",
        "party",
        "jewelry"
    ]

    source: Literal[
        "gemini",
        "demo"
    ]

    summary: str

    budget: float

    allocation: list[
        dict[str, Any]
    ]

    recommendations: list[
        dict[str, Any]
    ]

    tips: list[str]