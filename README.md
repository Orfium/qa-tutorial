# QA Tutorial


A test project created to include useful files for API test automation projects using Tavern API testing framework.
More [here](https://orfium.atlassian.net/wiki/spaces/~59128028/pages/2292940865/API+Test+Automation+in+Orfium)

# Tips & Hints

If you want to run something once in your tests, you can utilize the pytest hooks named pytest_sessionstart & pytest_sessionfinish . The first one runs once before the pytest session starts to collect the available tests. The latter runs once when every test session is finished.

Keep in mind that if you use pytest-xdist plugin, the tests run in parallel sessions, hence the hooks mentioned above run every time one of these sessions is finished meaning that anything inside pytest_sessionstart / pytest_sessionfinish will be executed more than one times. To avoid that case, you can add the following condition:

```python
from xdist import get_xdist_worker_id

def pytest_sessionfinish(session):
    if get_xdist_worker_id(session) == "master" and session.testscollected > 0:
        # Do whatever you want once e.g. Delete test data
        # print("\nTest data are deleted")If your test just has a huge amount of data that you would like to keep in a separate file, you can also (ab)use the !include tag to directly include data into a test. For example:
request:
     url: "{service:s}/new_user"
     method: POST
     json: !include test_data.json }`
```

If a stage of your tavern.yaml file is reused in many other tests within the same file, you can use the anchor feature. Anchors are a feature of YAML which allows you to reuse parts of the code. Define an anchor using &name_of_anchor. This can then be assigned to another object using new_object: *name_or_anchor, or they can be used to extend objects using <<: *name_of_anchor. 

If you want to use external functions to verify your response, create a python file in the same folder that includes your tavern.yaml files and below verify_response_with key, add the sub-key function

and add as a value the python file name and the name of the method that will verify the response. For example:


```python
#test_login.tavern.yaml
 response:
      status_code: 400
      verify_response_with:
        function: login_verification:validate_login_token
#login_verification.py
def validate_login_token(response):
    login_response = response.json()
    assert type(login_response.get("token")) == str 
```

If you want to pass a request body via an external function, in the json sub-key of the request, you can also give the external function name. Ensure that this method will return a json that can be utilized in the request as a body. For example:
```python
#utils.py
def signup_json_body():
    email = helpers.random_email()
    password = helpers.random_password()
    body = {"email": email, "password": password, "first_name": "Rudy", "last_name": "Madog", "group": 1}
    return body
  

#test_signup.tavern.yaml
stages:
  - name: User is able to sign up with valid registration details
    request:
      url: "{tavern.env_vars.staging_url}:{signup_route}"
      json:
        $ext:
          function: utils:signup_json_body
```
If you want to pass arguments in an external function, you can use the extra_kwargs subkey. For example:

```python
#testing_utils.py
def verify_processed_logs_response_usages_values(response, expected_value):
    processed_logs_response = response.json()
    assert processed_logs_response.get("results")[0].get("use_type") == expected_value.title()
# tavern.yaml file
verify_response_with:
        function: testing_utils:verify_processed_logs_response_usages_values
        extra_kwargs:
          expected_value: "{usages.use_type.tv}"
```


If you want to run the same test multiple times with different parameters, you can use the parametrize mark:

We have the following function which takes collect_bool as an argument:

In our Tavern test file we pass the collect_bool argument under extra_kwargs:

```yaml
marks:
  - parametrize:
      key:
        - collect_bool_param # THE NAME OF THE VARIABLE THAT WILL BE FORMATTED
      vals: # THE LIST OF VALUES TO BE FORMATTED
        - ["true"]
        - ["false"]
 
- name: Verified adds invalid published share in parties
  request:
    url: "{tavern.env_vars.BASE_URL}{works_route}{test_id:d}{works_parties_route}"
    json:
      $ext:
        function: publisher_party_details_verifications:works_parties_missing_required_details_body
        extra_kwargs:
        collect_bool: {"collect_bool_param"} # HERE WE USE THE collect_bool VARIABLE
    method: POST
    headers:
      accept: application/json
      Authorization: "Token {test_token}"
  response:
    status_code: 400
    verify_response_with:
      function: publisher_party_details_verifications:validate_party_details_bad_response
      extra_kwargs:
        expected_error_msg: "[{{'writer': {{'first_name': [ErrorDetail(string='This field is required.', code='required')]}}, 'publishers': [{{'legal_entity_name': [ErrorDetail(string='This field is required.', code='required')]}}]}}]"
```

This way, the test is going to run two times; One time for the true collect_bool parameter and one time for the false collect_bool parameter.

Note that since key is a list, vals must be a list of lists where each list is the same length as key
In our example, vals is a list with two lists whose length = 1 because we only have 1 key.

If we want to use 2 (or more) parameters (thus, 2 keys) we could also have vals with lists of length = 2 :

``` yaml
marks:
  - parametrize:
      key:
        - first_boolean_param
        - second_boolean_param
      vals:
        - ["true", "true"] # A List with length = 2
        - ["true", "false"]
        - ["false", "true"]
        - ["false", "false"]
we would call those params as follows:

function: some_verifications:two_boolean_arguments_body
extra_kwargs:
  first_boolean_arg: "{first_boolean_param}"
  second_boolean_arg: "{second_boolean_param}"
```

and we would produce four test runs that would test the true-true, true-false, false-true, and false-false combos. An alternative implementation of the example above is the following:

```yaml
marks:
  - parametrize:
      key:
        - first_boolean_paramam
      vals:
        - ["true"]
        - ["false"]
 
  - parametrize:
      key:
        - second_boolean_param
      vals:
        - ["true"]
        - ["false"]

```

which would produce the true-true, true-false, false-true, and false-false combos.
For more info on the parametrize mark, check Tavern documentation https://tavern.readthedocs.io/en/latest/basics.html#parametrize .