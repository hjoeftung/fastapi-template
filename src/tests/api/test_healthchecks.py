from fastapi import FastAPI
from fastapi.testclient import TestClient
from starlette import status


class TestHealthChecks:
    def test_ping_healthcheck(self, app: FastAPI, client: TestClient) -> None:
        """Тест хелсчек апи."""

        response = client.get(app.url_path_for("check_if_alive"))
        assert response.status_code == status.HTTP_200_OK
        assert response.text == "OK"

    def test_db_healthcheck(self, app: FastAPI, client: TestClient) -> None:
        """Тест хелсчек апи."""

        response = client.get(app.url_path_for("check_database"))
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"status": "OK"}
