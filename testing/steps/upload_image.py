import requests
import os
from behave import given, when, then
from urllib.parse import urlencode
import pdb
current_directory = os.path.dirname(os.path.realpath(__file__))

# Assuming the image file is in the same directory as your script
image_file_path = os.path.join(current_directory, "img.jpg")

@given("I have logged into the application as uploader or admin")
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


@when("I make a POST request to the upload image endpoint")
def vote(context):
    context.headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {context.token}",
    } 
    context.url = "http://127.0.0.1:8000/image"
    context.files = {"file": ("img.jpeg", open(r"C:\Users\nermi\Desktop\img.jpg", "rb"), "image/jpeg")}

    response = requests.post(context.url, files=context.files, headers=context.headers)
    context.response = response
    context.image=context.response.json( ).get("image")


@then("I should receive a Successful upload response")
def verify_successful_vote(context):
    assert "message" in context.response.json()


@then("the response status code should be {status_code:d}")
def verify_response_status_code(context, status_code):
    assert context.response.status_code == status_code    


