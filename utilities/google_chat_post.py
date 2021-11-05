import json
import os
import requests


def post_reports_to_google_chat(exitstatus):
    webhook_url = "https://chat.googleapis.com/v1/spaces/AAAAUZliscg/messages" \
                  "?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=ANMLGtmYat00P-Y4X4xnkTkhWfuKWUgzm69VPrdQNAE%3D"
    pytest_log_jenkins_url = ""
    project_title = "My Project name here"

    # To generate report file add "> pytest_report.log" at end of py.test command
    os.chdir(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tests'))
    test_report_file = os.path.abspath(
        os.path.join(os.getcwd(), 'pytest_report.log'))  # Add report file name and address here

    # Open report file and read data
    with open(test_report_file, "r") as in_file:
        test_data = ""
        for line in in_file:
            test_data = test_data + '\n' + line
    # Set context of message depending on the exit status
    if int(exitstatus) != 0:
        image = "https://i7.pngguru.com/preview/1015/544/835/thumb-signal-red-clip-art-thumbs-down.jpg"
        status = "FAILED"

    else:
        image = "https://i7.pngguru.com/preview/508/990/339/thumb-signal-computer-icons-emoji-clip-art-thumbs-up.jpg"
        status = "PASSED"

    # Arrange your data in pre-defined format. See an example here:
    # https://developers.google.com/hangouts/chat/reference/message-formats/cards
    bot_message = {
        "cards": [
            {
                "header": {
                    "title": project_title,
                    "subtitle": "built on Jenkins server",
                    "imageUrl": image
                },
                "sections": [
                    {
                        "widgets": [
                            {
                                "keyValue": {
                                    "topLabel": "Status",
                                    "content": status
                                }
                            }
                        ]
                    },
                    {
                        "widgets": [
                            {
                                "textParagraph": {
                                    "text": test_data
                                }
                            }
                        ]
                    },
                    {
                        "widgets": [
                            {
                                "buttons": [
                                    {
                                        "textButton": {
                                            "text": "CHECK THE LOGS",
                                            "onClick": {
                                                "openLink": {
                                                    "url": pytest_log_jenkins_url
                                                }
                                            }
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }

    body = json.dumps(bot_message)
    response = requests.post(url=webhook_url, data=body, headers={"Content-type": "application/json"})
    if response.text == 'ok':
        print('\n Successfully posted pytest report on google chat')
    else:
        print('\n Something went wrong. Unable to post pytest report on google chat. Response:', response)

    # ---USAGE EXAMPLES


if __name__ == '__main__':
    post_reports_to_google_chat(exitstatus=0)
