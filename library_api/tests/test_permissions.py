from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from library_api.permissions import IsReader

User = get_user_model()

class TestView(APIView):
    permission_classes = [IsReader]

    def get(self, request):
        return Response({"message": "You have access"})

class IsReaderPermissionTest(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

        self.reader_user = User.objects.create_user(
            username='reader',
            password='password123',
            role='RDR'
        )

        self.non_reader_user = User.objects.create_user(
            username='non_reader',
            password='password123',
            role='ADM'
        )

    def test_reader_has_permission(self):
        request = self.factory.get('/test-view/')
        request.user = self.reader_user

        view = TestView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"message": "You have access"})

    def test_non_reader_has_no_permission(self):
        request = self.factory.get('/test-view/')
        request.user = self.non_reader_user

        view = TestView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 403)

    def test_anonymous_user_has_no_permission(self):
        request = self.factory.get('/test-view/')
        request.user = None

        view = TestView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 403)