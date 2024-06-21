from .models.CustomUser import CustomUser
from django.contrib.auth.forms import UserCreationForm
from django import forms
class CustomClearableFileInput(forms.ClearableFileInput):
    template_name = 'custom_clearable_file_input.html'
    class Media:
        css = {
            'all': ('css/custom_file_input.css',)
        }

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'two_factor_enabled')  # You can customize the fields as needed

       
class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'avatar']
        widgets = {
            'avatar': CustomClearableFileInput(attrs={'class': 'custom-file-input'})
         }
    def __init__(self, *args, **kwargs):
        super(CustomUserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['username'].disabled = True
        self.fields['email'].disabled = True