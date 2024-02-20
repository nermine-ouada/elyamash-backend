import requests
from behave import given, when, then
from urllib.parse import urlencode
import pdb



@given("I have logged into the application")
def login(context):
    context.url = "http://127.0.0.1:8000/token"
    context.headers = {"content-type": "application/x-www-form-urlencoded"}
    context.body = urlencode(
        {
            "username": "ahmed.abassi",
            "password": "ahmed123",
        }
    )
    response = requests.post(context.url, data=context.body, headers=context.headers)
    context.response = response
    context.token = response.json().get("access_token")


@when("I make a POST request to the vote endpoint")
def vote(context):
    context.headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {context.token}",
        "Content-Type": "application/json",
    }
    context.url = "http://127.0.0.1:8000/vote"
    context.body = {
        "image1": "807b1c62-b332-41f2-b3bd-7e72202f0518",
        "image2": "ed3d6bcd-8d83-401e-b464-93567069ae4b",
        "score1": 1,
        "score2": 0,
    }
    response = requests.post(context.url, json=context.body, headers=context.headers)
    context.response = response


@then("I should receive a Successful vote response")
def verify_successful_vote(context):
    assert "message" in context.response.json()


@then("the response status code should be {status_code:d}")
def verify_response_status_code(context, status_code):
    assert context.response.status_code == status_code
