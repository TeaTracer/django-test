from django import forms
import re

class DataForm(forms.Form):
    data = forms.CharField(label='Data',  max_length=140)

    def clean(self):
        data = self.cleaned_data.get('data')

        if len(data) > 140:
	    raise ValidationError("Write up to 140 characters.")

	numbers_len = len(re.findall(r"\d+", ))

        if numbers_len == 0:
	    raise ValidationError("This field can't be empty.")

        if numbers_len % 2 != 0:
	    raise ValidationError("Write even number of numbers.")

	return self.cleaned_data
