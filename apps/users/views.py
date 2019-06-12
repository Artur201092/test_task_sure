import pandas as pd
from django.http import JsonResponse
from rest_framework import status, mixins
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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

    def create(self, request, *args, **kwargs):
        file = request.FILES['file']
        df = pd.read_csv(file)
        if len(df) > User.objects.all().count():
            for index, row in df.iterrows():
                try:
                    user_obj = User.objects.filter(email=row["email"]).first()
                    if not user_obj:
                        User.objects.create(first_name=row['first_name'], last_name=row['last_name'], email=row['email'])
                except User.DoesNotExist:
                    raise ValidationError('User "%s" is already exist' % row["first_name"])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response({"success": "success", 'data': serializer.data}, status=status.HTTP_201_CREATED, headers=headers)

