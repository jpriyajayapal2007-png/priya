from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request

from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse

from fastapi.templating import Jinja2Templates

from app.dependencies import get_current_user
from app.models.user import User


router = APIRouter()


templates = Jinja2Templates(
    directory="app/templates"
)


@router.get(
    "/",
    response_class=HTMLResponse
)
async def home(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@router.get(
    "/register",
    response_class=HTMLResponse
)
async def register_page(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="register.html"
    )


@router.get(
    "/login",
    response_class=HTMLResponse
)
async def login_page(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="login.html"
    )


@router.get(
    "/dashboard",
    response_class=HTMLResponse
)
async def dashboard(
    request: Request,
    user: User = Depends(
        get_current_user
    )
):

    return templates.TemplateResponse(

        request=request,

        name="dashboard.html",

        context={
            "user": user
        }
    )


@router.get(
    "/planner/{planner}",
    response_class=HTMLResponse
)
async def planner_page(
    request: Request,
    planner: str,
    user: User = Depends(
        get_current_user
    )
):

    if planner not in {
        "home",
        "party",
        "jewelry"
    }:

        return RedirectResponse("/")

    return templates.TemplateResponse(

        request=request,

        name=f"{planner}_planner.html",

        context={
            "user": user
        }
    )