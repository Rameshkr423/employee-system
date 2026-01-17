def send_email(event_type, payload):
    if event_type == "LEAVE_MARKED":
        print("📧 Email sent to manager")
