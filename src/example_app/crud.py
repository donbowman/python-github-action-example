from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Item
from .schemas import ItemCreate


def create_item(session: Session, payload: ItemCreate) -> Item:
    """Insert and return a new item."""
    item = Item(name=payload.name, description=payload.description)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


def list_items(session: Session) -> list[Item]:
    """Return every item, ordered by id."""
    return list(session.scalars(select(Item).order_by(Item.id)))


def get_item(session: Session, item_id: int) -> Item | None:
    """Return one item, or ``None`` when it does not exist."""
    return session.get(Item, item_id)
