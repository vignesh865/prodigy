import os
from http import HTTPStatus

import google_auth_oauthlib.flow
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from integration.service.source_credential_service import SourceCredentialService

os.environ['AUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


class GoogleIntegrationView(APIView):
    CLIENT_SECRETS_FILE = "resources/secrets/client_secret.json"
    SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
    API_SERVICE_NAME = 'drive'
    API_VERSION = 'v3'

    #
    # authentication_classes = [SessionAuthentication, TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request):

        action = request.query_params.get('action')

        if action == "authorize":
            return GoogleIntegrationView.authorize(request)
        if action == "callback":
            return GoogleIntegrationView.oauth2callback(request)
        if action == "callback_complete":
            return redirect(f"{reverse('integration_index')}?action=callback_complete&source_type=google_drive")

        return Response({"code": HTTPStatus.UNAUTHORIZED,
                         "message": f"Google Drive Authorization Failed"})

    @staticmethod
    def authorize(request):

        redirect_data = request.session["redirect_data"]

        if redirect_data is None:
            raise PermissionDenied()

        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            GoogleIntegrationView.CLIENT_SECRETS_FILE, scopes=GoogleIntegrationView.SCOPES)

        redirect_uri = reverse('google-drive')
        flow.redirect_uri = request.build_absolute_uri(redirect_uri) + f"?action=callback"
        # 'http://127.0.0.1:8080/integration/google-drive?action=callback'
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            login_hint=redirect_data.get("login_hint"),
            include_granted_scopes='true')

        request.session['state'] = state

        # return Response(authorization_url)
        return Response({"code": HTTPStatus.TEMPORARY_REDIRECT,
                         "message": authorization_url})
        # return redirect(authorization_url)

    @staticmethod
    def oauth2callback(request):

        redirect_data = request.session["redirect_data"]

        if redirect_data is None:
            raise PermissionDenied()

        state = request.session['state']

        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            GoogleIntegrationView.CLIENT_SECRETS_FILE, scopes=GoogleIntegrationView.SCOPES, state=state)
        redirect_uri = reverse('google-drive')
        flow.redirect_uri = request.build_absolute_uri(redirect_uri) + f"?action=callback"

        authorization_response = request.build_absolute_uri()
        flow.fetch_token(authorization_response=authorization_response)

        credentials = flow.credentials
        SourceCredentialService.save_google_drive_credentials(redirect_data.get("tenant_id"),
                                                              redirect_data.get("user_id"), credentials)

        return redirect(reverse('google-drive') + "?action=callback_complete")
