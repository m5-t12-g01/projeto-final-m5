from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from .models import Diary
from .serializers import DiarySerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsPermissionDiary

class DiaryView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = DiarySerializer

    def get_queryset(self):
        return Diary.objects.filter(user_id = self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
    
        
class DiaryDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsPermissionDiary]

    serializer_class = DiarySerializer
    queryset = Diary.objects.all() 
    
    lookup_url_kwarg = "pk"    