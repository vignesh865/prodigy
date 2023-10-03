class AuthUtils:

    @staticmethod
    def get_tenant(request):
        return request.auth.user.tenant

    @staticmethod
    def get_user(request):
        return request.auth.user
