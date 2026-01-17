import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

ADMIN_EMAIL = "admin@company.com"

def send_email(event_type, payload):
    if event_type not in ["LEAVE_MARKED", "EMPLOYEE_CREATED"]:
        return

    message = Mail(
        from_email="noreply@company.com",
        to_emails=ADMIN_EMAIL,
        subject=f"Alert: {event_type}",
        html_content=f"""
        <b>Event:</b> {event_type}<br>
        <b>Employee:</b> {payload.get('emp_id')}<br>
        <b>Details:</b> {payload}
        """
    )

    sg = SendGridAPIClient(os.environ["SENDGRID_API_KEY"])
    sg.send(message)
