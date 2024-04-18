import json
import pdb


def validate_firstname_lastname_of_booking_response(response, firstname, lastname):
    booking_response = response.json().get("booking")
    assert booking_response.get("firstname") == firstname
    assert booking_response.get("lastname") == lastname


def debug_response(response, variable=None):
    # if the test passes, no prints will be shown
    # enable pdb to debug the response
    # pdb.set_trace()

    print(f"Status code: {response.status_code}")
    print(f"Reason: {response.reason}")
    if variable:
        print(f"Booking ID: {variable}")
    try:
        response_json = response.json()
        print(f"Response body: {json.dumps(response_json, indent=4)}")
    except json.decoder.JSONDecodeError:
        pass

