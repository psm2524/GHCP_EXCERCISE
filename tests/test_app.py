import asyncio

import httpx

from src import app as app_module


def test_unregister_participant_removes_email_from_activity():
    async def run_test():
        # Arrange
        activity_name = "Chess Club"
        email = "student@example.com"

        transport = httpx.ASGITransport(app=app_module.app)
        async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
            # Act
            signup_response = await client.post(f"/activities/{activity_name}/signup?email={email}")
            unregister_response = await client.delete(f"/activities/{activity_name}/participants/{email}")
            activities_response = await client.get("/activities")

        # Assert
        assert signup_response.status_code == 200
        assert unregister_response.status_code == 200

        payload = unregister_response.json()
        assert "removed" in payload["message"].lower()
        assert email not in activities_response.json()[activity_name]["participants"]

    asyncio.run(run_test())
