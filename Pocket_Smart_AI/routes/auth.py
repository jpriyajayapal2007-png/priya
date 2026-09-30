from fastapi import APIRouter
from fastapi import Depends
from fastapi import Form
from fastapi import HTTPException

from fastapi.responses import RedirectResponse

from sqlalchemy.orm import Session

from app.database import get_db

from app.dependencies import (
    create_access_token,
    get_current_user
)

from app.models.user import User

from app.services.auth import (
    authenticate,
    register_user
)


router = APIRouter()


@router.post(
    "/register"
)
async def register(

    name: str = Form(...),

    email: str = Form(...),

    password: str = Form(...),

    db: Session = Depends(get_db)
):

    try:

        user = register_user(
            db,
            name,
            email,
            password
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )

    response = RedirectResponse(
        "/dashboard",
        status_code=303
    )

    response.set_cookie(
        "access_token",
        create_access_token(
            user.id
        ),
        httponly=True,
        samesite="lax"
    )

    return response


@router.post(
    "/login"
)
async def login(

    email: str = Form(...),

    password: str = Form(...),

    db: Session = Depends(get_db)
):

    user = authenticate(
        db,
        email,
        password
    )

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    response = RedirectResponse(
        "/dashboard",
        status_code=303
    )

    response.set_cookie(
        "access_token",
        create_access_token(
            user.id
        ),
        httponly=True,
        samesite="lax"
    )

    return response


@router.post(
    "/logout"
)
async def logout():

    response = RedirectResponse(
        "/",
        status_code=303
    )

    response.delete_cookie(
        "access_token"
    )

    return response


@router.post(
    "/token"
)
async def token(

    email: str = Form(...),

    password: str = Form(...),

    db: Session = Depends(get_db)
):

    user = authenticate(
        db,
        email,
        password
    )

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials."
        )

    return {

        "access_token":
            create_access_token(
                user.id
            ),

        "token_type":
            "bearer"
    }


@router.get(
    "/session-info"
)
async def session_info(
    user: User = Depends(
        get_current_user
    )
):

    return {

        "logged_in": True,

        "user_id":
            user.id,

        "name":
            user.name,

        "email":
            user.email
    }


@router.get(
    "/session-data"
)
async def session_data(
    user: User = Depends(
        get_current_user
    )
):

    return {

        "user_id":
            user.id,

        "preferences": {},

        "recommendation_tracking":
            "enabled",

        "message":
            "Session personalization data is ready."
    }