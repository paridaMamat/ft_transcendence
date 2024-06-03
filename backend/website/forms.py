from .models.CustomUser import CustomUser
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'two_factor_enabled')  # You can customize the fields as needed
