from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from posts.models import Profile

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'اسم المستخدم'
        self.fields['password'].label = 'كلمة المرور'

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password', 'email')
        widgets = {
            'password': forms.PasswordInput(),
        }

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].label = 'كلمة السر القديمة'
        self.fields['new_password1'].label = 'كلمة السر الجديدة'
        self.fields['new_password2'].label = 'أعد كتابة كلمة السر الجديدة'
        self.fields['new_password1'].help_text = 'كلمة السر الجديدة يجب ان تتكون من 8 رموز ولا تحتوي على اسم المستخدم ولا تتشابه مع كلمة السر القديمة*'

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('books', 'user')