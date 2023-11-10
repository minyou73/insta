from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        # fields = UserCreationForm.Meta.fields
        fields = ('username', 'profile_image', )


class CustomAuthenticationForm(AuthenticationForm):
    pass