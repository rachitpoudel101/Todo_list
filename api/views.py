from rest_framework import generics,permissions
from .serializers import TodoSerializer
from todo.models import Todo

class TodoCompletedList(generics.ListAPIView):
    serializer_class = TodoSerializer
    permission_classes =[permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user, datecompleted__isnull=False).order_by('-datecompleted')


class TodoListCreate(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes =[permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user, datecompleted__isnull=True)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)