def notify_manager(event_type, payload):
    if event_type == "LEAVE_MARKED":
        print("🔔 HR notified for leave")
    elif event_type == "EMPLOYEE_CREATED":
        print("👤 New employee registered")
