import uuid

from authentication.utils.auth_utils import AuthUtils
from integration.models.oauth2_redirection import OAuth2Redirection


class OAuth2RedirectionService:

    @staticmethod
    def generate_redirection_code(request):
        redirect_code = uuid.uuid4()

        user = AuthUtils.get_user(request)
        tenant = AuthUtils.get_tenant(request)
        data = {
            "tenant_id": tenant.id,
            "user_id": user.id,
            "login_hint": user.email

        }

        oauth2_redirect = OAuth2Redirection.objects.create(redirect_code=redirect_code,
                                                           redirect_data=data)

        oauth2_redirect.save()

        return redirect_code

    @staticmethod
    def get_data(redirect_code):
        return OAuth2Redirection.objects.filter(redirect_code=redirect_code).values("redirect_data").first().get(
            "redirect_data")

    @staticmethod
    def delete_by_redirect_code(redirect_code):
        return OAuth2Redirection.objects.filter(redirect_code=redirect_code).delete()
