import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

FROM_EMAIL = "pozhtechzone@gmail.com"   # must be verified
TO_EMAIL = "rameshkr423@gmail.com"

def send_email(event_type, payload):
    api_key = os.getenv("SENDGRID_API_KEY")
    if not api_key:
        print("⚠️ SENDGRID_API_KEY missing, skipping email")
        return

    if event_type not in ["EMPLOYEE_CREATED", "LEAVE_MARKED"]:
        return

    try:
        message = Mail(
            from_email=FROM_EMAIL,
            to_emails=TO_EMAIL,
            subject=f"[Employee System] {event_type}",
            html_content=f"""
                <h3>Event: {event_type}</h3>
                <p><b>Employee ID:</b> {payload.get("emp_id")}</p>
                <pre>{payload}</pre>
            """
        )

        sg = SendGridAPIClient(api_key)
        response = sg.send(message)

        print(f"📧 Email sent, status={response.status_code}")

    except Exception as e:
        print("❌ SendGrid error:", e)
