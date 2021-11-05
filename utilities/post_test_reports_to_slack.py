import json
import os
import requests


def post_reports_to_slack(exitstatus):
    webhook_url = "https://hooks.slack.com/services/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"
    channel = None  # Use channel ID to override default channel(#qatestreports)

    # To generate report file add "> pytest_report.log" at end of py.test command
    os.chdir(os.path.join(os.path.dirname(__file__), 'tests'))
    test_report_file = os.path.abspath(
        os.path.join(os.getcwd(), 'pytest_report.log'))  # Add report file name and address here

    # Open report file and read data
    with open(test_report_file, "r") as in_file:
        test_data = ""
        for line in in_file:
            test_data = test_data + '\n' + line
    # Set Slack Pass Fail bar indicator color according to test results
    # You can choose from "good", "warning", "danger" or any hex color codes
    if int(exitstatus) != 0:
        bar_color = "#ff0000"
        emoji = ':thumbsdown:'
    else:
        bar_color = "good"
        emoji = ':thumbsup:'

    # Arrange your data in pre-defined format. Test your data format here: https://api.slack.com/docs/messages/builder?
    attachments_pattern = {
        "fallback": "Test report from QA automation tests // Video Hunter 2",
        "color": bar_color,
        "title": "Test Report from Video Hunter v.2",
        "text": test_data
    }
    payload = {"attachments": [attachments_pattern],
               "channel": channel,
               "icon_emoji": emoji}
    json_params_encoded = json.dumps(payload)
    slack_response = requests.post(url=webhook_url, data=json_params_encoded, headers={"Content-type": "application/json"})
    if slack_response.text == 'ok':
        print('\n Successfully posted pytest report on Slack channel')
    else:
        print('\n Something went wrong. Unable to post pytest report on Slack channel. Slack Response:', slack_response)

    # ---USAGE EXAMPLES


if __name__ == '__main__':
    post_reports_to_slack(exitstatus=0)
