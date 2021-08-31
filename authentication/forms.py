from django import forms
from django.contrib.auth.models import User
from authentication.models import Usuario
from django.contrib.auth.forms import PasswordResetForm, UserCreationForm, PasswordChangeForm, SetPasswordForm


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Usuario:',
                               widget=forms.TextInput(attrs={'placeholder': 'Ingrese su usuario', 'id': 'user'}),
                               max_length=50, required=True)
    password = forms.CharField(label='Contraseña',
                               widget=forms.PasswordInput(attrs={'placeholder': 'Ingrese su contraseña', 'id': 'pwd'}),
                               required=True)

    class Meta:
        model = User
        fields = ['username', 'password']


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=50, required=True, help_text='Required.add valid email address')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserrecoverpwForm(PasswordResetForm):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'placeholder': 'Enter email'}),
                             max_length=50, required=True)

    class Meta:
        model = PasswordResetForm
        fields = ['email']

    # #View2


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old password',
                                   widget=forms.PasswordInput(attrs={'placeholder': 'Enter your old password'}),
                                   max_length=10, min_length=2, required=True)
    new_password1 = forms.CharField(label='New password',
                                    widget=forms.PasswordInput(attrs={'placeholder': 'Enter your old password'}),
                                    max_length=10, min_length=2, required=True)
    new_password2 = forms.CharField(label='Confirm new password',
                                    widget=forms.PasswordInput(attrs={'placeholder': 'Enter your old password'}),
                                    max_length=10, min_length=2, required=True)

    class Meta:
        model = PasswordChangeForm
        fields = ['old_password', 'new_password1', 'new_password2']


class ResetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='New password',
                                    widget=forms.PasswordInput(attrs={'placeholder': 'Enter your old password'}),
                                    max_length=10, min_length=2, required=True)
    new_password2 = forms.CharField(label='Confirm new password',
                                    widget=forms.PasswordInput(attrs={'placeholder': 'Enter your old password'}),
                                    max_length=10, min_length=2, required=True)

    class Meta:
        model = SetPasswordForm
        fields = ['new_password1', 'new_password2']


class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = '__all__'
        exclude = ['imagen', 'last_login', 'password']
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese su correo',
                }
            ),
            'nombres': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese sus nombres',
                }
            ),
            'apellidos': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese sus apellidos',
                }
            ),
            'identificacion': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese su No. de identificación',
                    'maxlength': '10'
                }
            ),
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Generado por el sistema',
                    'maxlength': '10',
                    'readonly': 'true'
                }
            ),
            'direccion': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese la dirección domiciliaria',
                }
            ),
            'telefono': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el No. de teléfono o celular',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['username'].required = False
        if 'identificacion' in self.data:
            _mutable = self.data._mutable
            self.data._mutable = True
            self.data['username'] = self.data['identificacion']
            self.data._mutable = _mutable

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['identificacion'])
        if commit:
            user.save()
        return user


class UsuarioPerfilForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['email','nombres','apellidos','identificacion','direccion','telefono']
        exclude = ['usuario_activo', 'usuario_administrador']
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'nombres': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'apellidos': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'identificacion': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'maxlength': '10'
                }
            ),
            'direccion': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'maxlength': '10'
                }
            ),
            'telefono': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'maxlength': '10'
                }
            ),
        }