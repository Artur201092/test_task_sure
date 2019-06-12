import pandas as pd
from django.db import transaction
from django.http import JsonResponse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.users.filters import UsersFilter
from apps.users.models import User
from apps.users.serializers import SignUpSerializer, UsersSerializer, FileSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = ()
    search_fields = ('email',)
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    filter_class = UsersFilter


class SignUpViewSet(ModelViewSet):
    serializer_class = SignUpSerializer
    permission_classes = ()
    http_method_names = ('post',)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save_user(serializer.data)
            user = User.objects.get(email=request.data['email'])
            if user:
                return JsonResponse(
                    {
                        'result': 'success'
                    },
                    status=status.HTTP_201_CREATED,
                )
        return ValidationError(serializer.errors, status.HTTP_409_CONFLICT)


class FileViewSet(ModelViewSet):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = FileSerializer
    http_method_names = ('post',)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        file = request.FILES['file']
        df = pd.read_csv(file)
        current_users_emails = User.objects.all().values_list('email', flat=True)
        users_to_add = [
            User(
                first_name=row['first_name'],
                last_name=row['last_name'],
                email=row['email'],
            )
            for index, row in df.iterrows() if row['email'] not in current_users_emails
        ]
        if users_to_add:
            User.objects.bulk_create(users_to_add)
        return Response({"success": "success"}, status=status.HTTP_201_CREATED)

