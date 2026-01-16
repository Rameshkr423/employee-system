from api.firestore_db import get_user

def login(user_id: str, role: str):
    user = get_user(user_id)
    if not user or user["role"] != role:
        return False
    return True
