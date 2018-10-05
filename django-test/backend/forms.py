from django import forms
from django.core.exceptions import ValidationError
import re

class DataForm(forms.Form):
    data = forms.CharField(label='Data',  max_length=140)

    def clean(self):
        data = self.cleaned_data.get('data', '')

        if len(data) > 140:
            raise ValidationError("Write up to 140 characters.")

        data_array = re.findall(r"\d+", data)
        numbers_len = len(data_array)

        if numbers_len == 0:
            raise ValidationError("This field can't be empty.")

        if numbers_len % 2 != 0:
            raise ValidationError("Write even number of numbers.")
        self.cleaned_data['data'] = data_array

        return self.cleaned_data
