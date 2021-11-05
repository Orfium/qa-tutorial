import smtplib
import ssl
import pathlib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def get_test_report():
    # To generate report file add "> pytest_report.log" at end of py.test command
    test_report_file = pathlib.Path(__file__).parent / 'tests' / 'report.html'  # Add report file name here

    # Open report file and read data
    with open(test_report_file, "r") as in_file:
        test_data = ""
        for line in in_file:
            test_data = test_data + '\n' + line
    return str(test_data)


def send_test_report_to_email(receiver_email):
    port = 587
    smtp_server = "smtp.gmail.com"
    sender_email = "qa@orfium.com"
    password = "}fez3kSx)"
    message = MIMEMultipart("alternative")
    message["Subject"] = "Video Hunter 2 test report"
    message["From"] = "Orfium QA"
    message["To"] = receiver_email

    text = get_test_report()
    part1 = MIMEText(text, "html")

    message.attach(part1)

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        server.login(sender_email, password)
        server.sendmail(sender_email, message["To"].split(","), message.as_string())
