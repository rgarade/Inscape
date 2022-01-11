from django.forms import ModelForm
from .models import *


class userMasterMapping(ModelForm):
    class Meta:
        model = User
        fields = "__all__"
