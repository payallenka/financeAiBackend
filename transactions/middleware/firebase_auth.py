import os
import json
import firebase_admin
from firebase_admin import auth, credentials
from django.http import JsonResponse

# Load Firebase credentials from environment variable
firebase_credentials_json = os.getenv("FIREBASE_CREDENTIALS")

if firebase_credentials_json:
    firebase_credentials = json.loads(firebase_credentials_json)
    cred = credentials.Certificate(firebase_credentials)

    # Initialize Firebase only if not already initialized
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
else:
    raise ValueError("FIREBASE_CREDENTIALS environment variable is not set")


class FirebaseAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.headers.get("Authorization")

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]  
            try:
                decoded_token = auth.verify_id_token(token)
                request.user = type("User", (), {"uid": decoded_token["uid"]})  
            except Exception:
                return JsonResponse({"error": "Invalid authentication token"}, status=401)

        return self.get_response(request)
