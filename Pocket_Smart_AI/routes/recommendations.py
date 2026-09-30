import json

from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import Form
from fastapi import HTTPException
from fastapi import UploadFile

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db

from app.dependencies import get_current_user

from app.models.recommendation import Recommendation
from app.models.user import User

from app.schemas import (
    HomeRequest,
    PartyRequest,
    JewelryRequest
)

from app.services.gemini_utils import (
    generate_recommendation,
    validate_image
)


router = APIRouter()

settings = get_settings()


def save_history(

    db: Session,

    user_id: int,

    planner: str,

    request_data: dict,

    response_data: dict

):

    row = Recommendation(

        user_id=user_id,

        planner_type=planner,

        request_json=json.dumps(
            request_data,
            ensure_ascii=False
        ),

        response_json=json.dumps(
            response_data,
            ensure_ascii=False
        )
    )

    db.add(row)

    db.commit()


@router.post(
    "/generate-home"
)
async def generate_home(

    payload: HomeRequest,

    user: User = Depends(
        get_current_user
    ),

    db: Session = Depends(
        get_db
    )
):

    data = payload.model_dump()

    result, source = generate_recommendation(
        "home",
        data
    )

    save_history(
        db,
        user.id,
        "home",
        data,
        result
    )

    return {

        "planner":
            "home",

        "source":
            source,

        "budget":
            payload.budget,

        **result
    }


@router.post(
    "/generate-party"
)
async def generate_party(

    payload: PartyRequest,

    user: User = Depends(
        get_current_user
    ),

    db: Session = Depends(
        get_db
    )
):

    data = payload.model_dump()

    result, source = generate_recommendation(
        "party",
        data
    )

    save_history(
        db,
        user.id,
        "party",
        data,
        result
    )

    return {

        "planner":
            "party",

        "source":
            source,

        "budget":
            payload.budget,

        **result
    }


@router.post(
    "/generate-jewelry"
)
async def generate_jewelry(

    budget: float = Form(...),

    occasion: str = Form(
        "wedding"
    ),

    style: str = Form(
        "elegant"
    ),

    metal: str = Form(
        "any"
    ),

    notes: str = Form(
        ""
    ),

    outfit_image:
        UploadFile | None = File(
            None
        ),

    user: User = Depends(
        get_current_user
    ),

    db: Session = Depends(
        get_db
    )
):

    payload = JewelryRequest(

        budget=budget,

        occasion=occasion,

        style=style,

        metal=metal,

        notes=notes
    )

    image_bytes = None

    mime_type = None

    if (
        outfit_image
        and
        outfit_image.filename
    ):

        image_bytes = await (
            outfit_image.read()
        )

        mime_type = (
            outfit_image.content_type
        )

        try:

            validate_image(

                image_bytes,

                mime_type,

                settings.max_upload_mb
            )

        except ValueError as exc:

            raise HTTPException(
                status_code=400,
                detail=str(exc)
            )

    data = payload.model_dump()

    result, source = generate_recommendation(

        "jewelry",

        data,

        image_bytes,

        mime_type
    )

    save_history(

        db,

        user.id,

        "jewelry",

        data,

        result
    )

    return {

        "planner":
            "jewelry",

        "source":
            source,

        "budget":
            payload.budget,

        **result
    }


@router.get(
    "/recommendations-details"
)
async def recommendation_details(

    user: User = Depends(
        get_current_user
    ),

    db: Session = Depends(
        get_db
    )
):

    rows = db.scalars(

        select(
            Recommendation
        )

        .where(
            Recommendation.user_id
            == user.id
        )

        .order_by(
            Recommendation.created_at.desc()
        )

        .limit(20)

    ).all()

    return [

        {

            "id":
                row.id,

            "planner":
                row.planner_type,

            "created_at":
                row.created_at.isoformat(),

            "request":
                json.loads(
                    row.request_json
                ),

            "response":
                json.loads(
                    row.response_json
                )
        }

        for row in rows
    ]


@router.get(
    "/history"
)
async def history(

    user: User = Depends(
        get_current_user
    ),

    db: Session = Depends(
        get_db
    )
):

    rows = db.scalars(

        select(
            Recommendation
        )

        .where(
            Recommendation.user_id
            == user.id
        )

        .order_by(
            Recommendation.created_at.desc()
        )

    ).all()

    return [

        {

            "id":
                row.id,

            "planner":
                row.planner_type,

            "created_at":
                row.created_at.isoformat()
        }

        for row in rows
    ]