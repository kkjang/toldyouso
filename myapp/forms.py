from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Statement

class SubmitForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(SubmitForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper(self)

		self.helper.add_input(Submit('submit', 'Submit'))

	class Meta:
		model = Statement
		exclude = ['date_created', 'user']
