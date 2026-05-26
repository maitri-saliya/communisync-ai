from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi import Request

from database import Session
from database import Need


router = APIRouter()

templates = (
    Jinja2Templates(
        directory="templates"
    )
)


@router.get("/dashboard")
def dashboard(
    request: Request
):

    session = Session()

    rows = (
        session
        .query(Need)
        .order_by(
            Need.id.desc()
        )
        .all()
    )

    return templates.TemplateResponse(

        "dashboard.html",

        {
            "request":
            request,

            "rows":
            rows,

            "total":
            len(rows)
        }
    )