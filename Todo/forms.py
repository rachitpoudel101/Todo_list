from django.forms import ModelForm
from . models import Todo
class Todoform(ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'memo', 'important']