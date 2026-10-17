from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, inspect

ROOT = Path(__file__).resolve().parents[1]


def test_migrations_create_and_remove_schema(tmp_path: Path) -> None:
    database_url = f"sqlite:///{tmp_path / 'migrated.db'}"
    config = Config(str(ROOT / "alembic.ini"))
    config.set_main_option("sqlalchemy.url", database_url)

    command.upgrade(config, "head")

    engine = create_engine(database_url)
    inspector = inspect(engine)
    assert "items" in inspector.get_table_names()
    assert {"id", "name", "description", "created_at"} <= {
        column["name"] for column in inspector.get_columns("items")
    }

    command.downgrade(config, "base")

    inspector = inspect(engine)
    assert "items" not in inspector.get_table_names()
    engine.dispose()
