from django import forms
from .models import CV


class CVForm(forms.ModelForm):
    class Meta:
        model = CV
        fields = ['title', 'education', 'experience', 'skills']
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'e.g. Software Engineer CV'
                }
            ),
            'education': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            ),
            'experience': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 5}
            ),
            'skills': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            ),
        }
