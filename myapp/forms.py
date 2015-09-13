from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from .models import Room

def horizontal_helper(form):
    """ Adds the horizontal form classes
    to the given form"""
    form.helper = FormHelper(form)
    form.helper.form_class = 'form-horizontal'
    form.helper.label_class = 'col-md-2'
    form.helper.field_class = 'col-md-10'

class SubmitRoomForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(SubmitRoomForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper(self)
		horizontal_helper(self)
		self.helper.add_input(Submit('submit', 'Submit'))
		self.helper.add_input(Submit('clear', 'Clear'))

	class Meta:
		model = Room
		exclude = ['date_created', 'challenged_bet', 'ready']

class RequestRoomForm(forms.Form):
	room_key = forms.CharField(label="Room Key")
	def __init__(self, *args, **kwargs):
		super(RequestRoomForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper(self)
		horizontal_helper(self)
		self.helper.add_input(Submit('submit', 'Submit'))

	def clean_room_key(self):
		room_key = self.cleaned_data['room_key'].encode('utf8')
		if Room.objects.get(room_key=room_key).ready:
			raise forms.ValidationError('This room is already complete! Please enter another key.')
		return room_key


class ResponseRoomForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(ResponseRoomForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper(self)
		horizontal_helper(self)
		self.helper.add_input(Submit('submit', 'Submit'))

	class Meta:
		model = Room
		exclude = ['date_created', 'challenger_bet', 'ready', 'title']
