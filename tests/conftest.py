from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from example_app.config import Settings
from example_app.db import Base
from example_app.main import create_app


@pytest.fixture
def client(tmp_path) -> Iterator[TestClient]:
    """Run the real application against a throwaway SQLite database."""
    settings = Settings(database_url=f"sqlite:///{tmp_path / 'test.db'}")
    app = create_app(settings)

    with TestClient(app) as test_client:
        Base.metadata.create_all(app.state.engine)
        yield test_client
