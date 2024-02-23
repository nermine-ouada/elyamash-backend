from behave import given, when, then
import requests
from urllib.parse import urlencode
import pdb



@given("I have user authentication credentials")
def set_authentication_credentials(context):
    context.url = "http://127.0.0.1:8000/token" 
    context.headers = {"content-type": "application/x-www-form-urlencoded"}
    context.body = urlencode(
        {
            "username": "ali1",
            "password": "ali",
        }
    )


@when("I make a POST request to the login endpoint")
def make_login_request(context):
    response = requests.post(context.url, data=context.body, headers=context.headers)
    context.response = response

@then("I should receive a valid access token")
def verify_access_token(context):
    assert "access_token" in context.response.json()


@then("the response status code should be {status_code:d}")
def verify_response_status_code(context, status_code):
    assert context.response.status_code == status_code
