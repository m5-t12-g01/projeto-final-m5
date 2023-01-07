from .models import User
from .serializers import UserSerializer
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsSuperUser, UserPermissions


class UserView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSuperUser]

    serializer_class = UserSerializer
    queryset = User.objects.get_queryset().order_by('id')


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [UserPermissions]

    serializer_class = UserSerializer
    queryset = User.objects.all()

    lookup_url_kwarg = 'user_id'
