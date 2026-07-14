import pytest
from fastapi.testclient import TestClient

from src import app as app_module
from src.app import app as fastapi_app


@pytest.fixture(autouse=True)
def reset_app_state():
    app_module.reset_activities()
    yield
    app_module.reset_activities()


@pytest.fixture()
def client():
    with TestClient(fastapi_app) as test_client:
        yield test_client


def test_signup_endpoint_adds_participant(client):
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}

    activities_response = client.get("/activities")
    assert activities_response.status_code == 200
    assert email in activities_response.json()[activity_name]["participants"]


def test_unregister_endpoint_removes_participant(client):
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_response.status_code == 200

    unregister_response = client.delete(f"/activities/{activity_name}/participants/{email}")

    assert unregister_response.status_code == 200
    assert unregister_response.json() == {"message": f"Removed {email} from {activity_name}"}

    activities_response = client.get("/activities")
    assert activities_response.status_code == 200
    assert email not in activities_response.json()[activity_name]["participants"]
