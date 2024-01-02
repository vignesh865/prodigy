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

        authentication = st.session_state["authentication"]
        is_valid = StreamlitService.check_token_status(authentication.get("token"))
        return not is_valid

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
