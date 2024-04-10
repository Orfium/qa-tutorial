def validate_firstname_lastname_of_booking_response(response, firstname, lastname):
    booking_response = response.json().get("booking")
    assert booking_response.get("firstname") == firstname
    assert booking_response.get("lastname") == lastname
