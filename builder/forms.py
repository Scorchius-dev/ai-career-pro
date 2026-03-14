from django import forms
from .models import CV


class CVForm(forms.ModelForm):
    class Meta:
        model = CV
        fields = [
            'title', 'summary', 'phone_number', 'location',
            'education', 'experience', 'skills',
        ]
        labels = {
            'title': 'CV Profile Name',
            'summary': 'Personal Statement',
            'phone_number': 'Phone Number',
            'location': 'Location',
            'education': 'Education',
            'experience': 'Work Experience',
            'skills': 'Skills',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Retail CV, Developer CV',
            }),
            'summary': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': (
                    'e.g. Results-driven software engineer with 3 years '
                    'of experience building web APIs. Passionate about '
                    'clean code and mentoring junior developers.'
                ),
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. +44 7700 900000',
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. London, UK',
            }),
            'education': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': (
                    'e.g.\n'
                    'BSc Computer Science, University of Manchester '
                    '(2019\u20132022)\n'
                    'A-Levels: Maths (A), Physics (B), Computing (A*)'
                ),
            }),
            'experience': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': (
                    'e.g.\n'
                    'Junior Developer, Acme Ltd (2022\u2013present)\n'
                    '\u2013 Built REST APIs used by 10,000+ daily users\n'
                    '\u2013 Reduced page load time by 40% via caching\n\n'
                    'Retail Assistant, Starbucks (2020\u20132022)\n'
                    '\u2013 Managed stock and peak-hour customer operations'
                ),
            }),
            'skills': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': (
                    'e.g. Python, Django, React, PostgreSQL, Git, '
                    'Agile, communication, problem-solving'
                ),
            }),
        }

    def _clean_non_empty_text(self, field_name):
        value = self.cleaned_data.get(field_name, '')
        cleaned_value = value.strip()
        if not cleaned_value:
            raise forms.ValidationError('This field cannot be empty.')
        return cleaned_value

    def clean_title(self):
        return self._clean_non_empty_text('title')

    def clean_education(self):
        return self._clean_non_empty_text('education')

    def clean_experience(self):
        return self._clean_non_empty_text('experience')

    def clean_skills(self):
        return self._clean_non_empty_text('skills')
