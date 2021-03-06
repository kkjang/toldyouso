from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from djangular.forms import NgModelFormMixin, NgModelForm
from djangular.styling.bootstrap3.forms import Bootstrap3FormMixin
from .models import Bet, Wager
from django.contrib import auth
from collections import OrderedDict

def horizontal_helper(form):
    """ Adds the horizontal form classes
    to the given form"""
    form.helper = FormHelper(form)
    form.helper.form_class = 'form-horizontal'
    form.helper.label_class = 'col-md-2'
    form.helper.field_class = 'col-md-10'

class SubmitBetForm(NgModelFormMixin, NgModelForm, Bootstrap3FormMixin):
	condition1 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'UNC beats Duke, KMP takes 426 class to Topo, etc.'}))
	amount1 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '$5, a beer, etc.'}))
	condition2 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Duke beats UNC, KMP takes 426 class to Spanky's, etc."}))
	amount2 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '$2, a bottle of wine, etc.'}))
	email = forms.EmailField()

	def __init__(self, *args, **kwargs):
		kwargs.update(scope_prefix='bet_data')
		super(SubmitBetForm, self).__init__(*args, **kwargs)
		
	class Meta:
		model = Bet
		fields = ['title']

class SubmitWagerForm(NgModelFormMixin, NgModelForm, Bootstrap3FormMixin):
	def __init__(self, *args, **kwargs):
		kwargs.update(scope_prefix='room_data')
		super(SubmitWagerForm, self).__init__(*args, **kwargs)
	class Meta:
		model = Wager
		exclude = ['user_id']

class UserRegisterForm(UserCreationForm):
	def __init__(self, *args, **kwargs):
		super(UserRegisterForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
			'username',
			'password1',
			'password2',
		)
		self.helper.add_input(Submit('submit', 'Submit'))

class UserLoginForm(AuthenticationForm):
	def __init__(self, *args, **kwargs):
		super(UserLoginForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
			'username',
			'password',
		)
		self.helper.add_input(Submit('submit', 'Submit'))

