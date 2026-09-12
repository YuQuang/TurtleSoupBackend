import os
import time
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

from flask import redirect, session, request, jsonify
from google_auth_oauthlib.flow import Flow
from turtlesoup.logging import get_logger
from turtlesoup.services.auth_service import AuthService
from turtlesoup.services.google_service import GoogleService
from turtlesoup.services.user_service import UserService
from turtlesoup.api.google_oauth_store import OAUTH_SESSION_TTL, OAuthSession


load_dotenv()
logger = get_logger(__name__)


class GoogleController:

    def __init__(
        self,
        google_service: GoogleService,
        user_service: UserService,
        auth_service: AuthService
    ):
        self.GOOGLE_SCOPES = [
            "openid",
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
        ]
        self.google_service = google_service
        self.user_service = user_service
        self.auth_service = auth_service
        self.jwt = ""
        self.oauth_sessions = {}


    def _create_flow(self):
        return Flow.from_client_config(
            {
                "web": {
                    "client_id": os.environ["GOOGLE_CLIENT_ID"],
                    "client_secret": os.environ["GOOGLE_CLIENT_SECRET"],
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                }
            },
            scopes=self.GOOGLE_SCOPES,
            redirect_uri=os.environ["GOOGLE_REDIRECT_URI"],
        )


    def connect(self):
        flow = self._create_flow()

        authorization_url, state = flow.authorization_url(
            access_type="offline",
            include_granted_scopes="true",
        )

        self.oauth_sessions[state] = OAuthSession(
            code_verifier=flow.code_verifier,
            expires_at=time.time() + OAUTH_SESSION_TTL,
        )

        return redirect(authorization_url)


    def callback(self):
        returned_state = request.args.get("state")

        if not returned_state: return "Missing OAuth state", 400
        oauth_session = self.oauth_sessions.pop(returned_state, None)
        if oauth_session.expires_at < time.time(): return "OAuth session expired", 400
        code_verifier = oauth_session.code_verifier
        if not code_verifier: return "OAuth code verifier not found", 400
        session_state = returned_state

        flow = self._create_flow()
        flow.state = session_state
        flow.code_verifier = code_verifier
        flow.fetch_token( authorization_response=request.url )

        # 取得 Google user
        response = requests.get(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            headers={
                "Authorization": f"Bearer {flow.credentials.token}"
            },
        )

        logger.info("credentials %s", flow.credentials.__dict__)

        response.raise_for_status()

        user_data = response.json()
        if user_data == None: return "Google API error", 400

        #
        # 登入流程檢查
        # 1. 檢查是否有第三方紀錄 ( 有，登入 )
        # 2. 檢查 email 是否關聯 ( 有，綁定+登入 )
        # 3. 都沒有 創建新的 user ( 登入 )
        #
        if self.google_service.check_user_integration(
            user_data["sub"]
        ):
            self.google_service.partial_update_integration(
                user_data["sub"],
                str(flow.credentials.token),
                str(flow.credentials.token),
                user_data["picture"]
            )
        elif self.user_service.check_user_email_exist(
            user_data["email"]
        ):
            pass
        else:
            user = self.user_service.create_user(
                user_data["name"],
                user_data["email"],
                None
            )
            if user.user_id == None: return "Error"
            self.google_service.create_integration(
                user.user_id,
                "Google",
                user_data["sub"],
                str(flow.credentials.token),
                str(flow.credentials.token),
                user_data["picture"]
            )

        user = self.user_service.get_user_by_provider_id(user_data["sub"])
        if user == None: return "User not found", 400
        self.jwt = self.auth_service.create_jwt(
            {
                "name": user.user_name,
                "email": user.email,
                "user_id": user.user_id.__str__(),
                "avatar": user_data["picture"]
            },
            datetime.now(timezone.utc) + timedelta(hours=3)
        )

        response = redirect(
            os.getenv("FRONTEND_BASE_URL","")
        )

        response.set_cookie(
            "Authorization",
            self.jwt,
            httponly=True,
            secure=True,
            samesite="None; Secure; HttpOnly",
            max_age=60 * 60 * 3,  # 3 hours
        )

        return response