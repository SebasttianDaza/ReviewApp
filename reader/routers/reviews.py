from fastapi import APIRouter, Request
from reader.models import ReviewReader, JSONAPIResponse

router = APIRouter(
    prefix="/reviews",
    tags=["reviews"]
)

@router.get("/", response_model=JSONAPIResponse)
async def get_reviews(request: Request):
    reviews = [review.serialize_jsonapi().dict() for review in ReviewReader.objects]

    return JSONAPIResponse(
        links={
            "self": str(request.url)
        },
        data=reviews,
    )

