import requests


class StreamlitService:
    BASE_PATH = "http://127.0.0.1:8080"

    @staticmethod
    def build_url(relative_path):
        return f"{StreamlitService.BASE_PATH}{relative_path}"

    @staticmethod
    def call_login(username, user_password, user_email):
        api_response = requests.post(StreamlitService.build_url("/auth/login"), {
            "username": username,
            "tenant": 1,
            "password": user_password,
            "email": user_email})

        if api_response.status_code != 200:
            raise LoginError(api_response.text)

        return api_response.json()

    @staticmethod
    def call_google_integration(st):

        headers = {
            "Authorization": f"token {StreamlitService.get_token(st)}"
        }

        url = "/integration/integrate?source_type=GOOGLE_DRIVE&redirect_url=http://localhost:8501/User"
        return requests.post(StreamlitService.build_url(url),
                             headers=headers).json()

    @staticmethod
    def call_get_google_integration_status(st):

        headers = {
            "Authorization": f"token {StreamlitService.get_token(st)}"
        }

        url = "/integration/integrate?source_type=GOOGLE_DRIVE"
        api_response = requests.get(StreamlitService.build_url(url),
                                    headers=headers)

        if api_response.status_code != 200:
            return False

        sources = api_response.json().get("sources")
        return "GOOGLE_DRIVE" in [source.upper() for source in sources]

    @staticmethod
    def call_signup(username, user_password, user_email):
        api_response = requests.post(StreamlitService.build_url("/auth/signup"), {
            "username": username,
            "tenant": 1,
            "password": user_password,
            "email": user_email})

        if api_response.status_code != 200:
            raise LoginError(api_response.text)

        json_response = api_response.json()
        return {
            "token": json_response.get("token"),
            "user": json_response.get("user").get("username"),
            "is_new_token": True,
            "tenant": json_response.get("user").get("tenant")
        }

    @staticmethod
    def check_token_status(token):
        headers = {
            "Authorization": f"token {token}"
        }
        api_response = requests.get(StreamlitService.build_url("/auth/me"), headers=headers)

        if api_response.status_code != 200:
            return False

        return True

    @staticmethod
    def should_authenticate(st):
        if "authentication" not in st.session_state.keys():
            return True

        token = StreamlitService.get_token(st)
        is_valid = StreamlitService.check_token_status(token)
        return not is_valid

    @staticmethod
    def get_token(st):
        authentication = st.session_state["authentication"]
        return authentication.get("token")

    @staticmethod
    def get_answers(token, query):
        headers = {
            "Authorization": f"token {token}"
        }
        api_response = requests.post(StreamlitService.build_url("/api/chat"),
                                     data={
                                         "query": query
                                     },
                                     headers=headers)

        if api_response.status_code != 200:
            raise ValueError(api_response.text)

        return api_response.json().get("message")


class LoginError(ValueError):
    pass
