from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from .models import Car, Rent


class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password1', 'password2']



    def save(self, commit=True):
        user = super().save(commit=False)
        # ავტომატურად შეივსოს username როგორც ტელეფონის ნომერი
        user.username = self.cleaned_data['phone_number']
        if commit:
            user.save()
        return user

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Phone Number",
        widget=forms.TextInput(attrs={'autofocus': True})
    )

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        exclude = ['added_by']
        widgets = {
            'transmission': forms.Select(choices=Car._meta.get_field('transmission').choices),
        }
class RentForm(forms.ModelForm):
    class Meta:
        model = Rent
        fields = ['rent_start_date', 'rent_end_date']
        widgets = {
            'rent_start_date': forms.DateInput(attrs={'type': 'date'}),
            'rent_end_date': forms.DateInput(attrs={'type': 'date'}),
        }


class EmailResetRequestForm(forms.Form):
    email = forms.EmailField(label="შეიყვანეთ ელ-ფოსტა")

class EmailCodeResetForm(forms.Form):
    code = forms.CharField(label="კოდი")
    new_password = forms.CharField(label="ახალი პაროლი", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="დაადასტურე პაროლი", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("new_password") != cleaned_data.get("confirm_password"):
            raise forms.ValidationError("პაროლები არ ემთხვევა")
        return cleaned_data