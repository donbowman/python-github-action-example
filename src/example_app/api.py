from collections.abc import Generator
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from . import crud
from .schemas import ItemCreate, ItemRead

router = APIRouter()


def get_session(request: Request) -> Generator[Session, None, None]:
    """Yield a database session from the application's session factory."""
    with request.app.state.session_factory() as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


@router.get("/healthz", tags=["ops"])
def healthz() -> dict[str, str]:
    """Liveness probe used by the container health check."""
    return {"status": "ok"}


@router.get("/items", response_model=list[ItemRead], tags=["items"])
def list_items(session: SessionDep) -> list[ItemRead]:
    """List all items."""
    return crud.list_items(session)


@router.post(
    "/items",
    response_model=ItemRead,
    status_code=status.HTTP_201_CREATED,
    tags=["items"],
)
def create_item(payload: ItemCreate, session: SessionDep) -> ItemRead:
    """Create an item."""
    return crud.create_item(session, payload)


@router.get("/items/{item_id}", response_model=ItemRead, tags=["items"])
def get_item(item_id: int, session: SessionDep) -> ItemRead:
    """Return a single item."""
    item = crud.get_item(session, item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )
    return item
