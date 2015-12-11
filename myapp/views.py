import django_filters
import datetime
import uuid
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, DetailView, ListView, FormView
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.core.mail import send_mail

from .models import Bet, Wager
from rest_framework import viewsets, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from .serializers import BetSerializer, WagerSerializer
from .forms import UserLoginForm, SubmitWagerForm, SubmitBetForm
from rest_framework.exceptions import PermissionDenied


def send_invite_email(email, request, bet):
	key = bet.key
	username = request.user.get_username()
	subject = "SetInStone Bet Invitation"
	email_body = "Hello! You have received an invitation to a bet from %s.  Please follow this link to get started! http://www.setinstone.com:8000/bet/%s/accept?key=%s" % (username, bet.id, key)

	send_mail(subject, email_body, None, [email], fail_silently=False)

# Create your views here.
class DetailRoomList(TemplateView):
	template_name = "detail_list.html"

class DetailRoom(TemplateView):
	template_name = 'detail.html'

class AcceptDetailRoom(TemplateView):
	template_name = 'accept_detail.html'

class SubmitBetFormView(FormView):
	template_name = 'submit_bet.html'
	form_class = SubmitBetForm

	def get_context_data(self, **kwargs):
		context = super(SubmitBetFormView, self).get_context_data(**kwargs)
		context.update(title="Please submit your bet.")
		return context

class WagerSetView(viewsets.ViewSet, ListAPIView):
	model = Wager
	serializer_class = WagerSerializer
	queryset = Wager.objects.all()

class BetSetView(viewsets.ModelViewSet):
	serializer_class = BetSerializer

	def destroy(self, *args, **kwargs):
		instance = self.get_object()
		print instance.creator_id
		if instance.creator_id == self.request.user and instance.date_accepted is None:
			instance.delete()
			return Response(status=status.HTTP_204_NO_CONTENT) 
		else:
			raise PermissionDenied

	def partial_update(self,*args, **kwargs):
		instance = self.get_object()
		bet = BetSerializer(instance, data = self.request.data, partial=True)
		if bet.is_valid():
			created_bet = bet.save()
			wager_id = bet.data['wagers'][1]['id']
			update_wager = Wager.objects.get(pk=wager_id)
			wager_data = {'user_id':User.objects.get(pk=self.request.user.id)}
			print wager_data
			wager = WagerSerializer(update_wager, data=wager_data, partial=True)
			if wager.is_valid():
				wager.save(user_id=self.request.user)
				wager.save()
			return Response(bet.data, status=status.HTTP_201_CREATED)
		else:
			return Response(bet.errors, status=status.HTTP_400_BAD_REQUEST)


	def retrieve(self, *args, **kwargs):
		super(BetSetView, self).retrieve(self, *args, **kwargs)
		bet_id = kwargs['pk']
		bet = Bet.objects.get(pk=bet_id)
		key = self.request.query_params.get('key', None)
		if key is None:
			bet = BetSerializer(bet)
			return Response(bet.data, status=status.HTTP_201_CREATED)
		else:
			if key != 'undefined' and key != 'true' and not None:
				try:
					key = uuid.UUID(key)
					if bet.key == key:
						bet = BetSerializer(bet)
						return Response(bet.data, status=status.HTTP_201_CREATED)
					else:
						raise PermissionDenied
				except:
					raise PermissionDenied
			raise PermissionDenied

	def create(self, request):
		wager_data = []
		email = request.data.pop('email')
		wager_data.append((request.data.pop('amount1'), request.data.pop('condition1')))
		wager_data.append((request.data.pop('amount2'), request.data.pop('condition2')))
		bet_data = request.data
		bet_data['wager_data'] = [{'amount':a,'condition':c} for a,c in wager_data]
		bet_data['wagers'] = []
		bet = BetSerializer(data=bet_data,context={'request':request})
		if bet.is_valid():
			bet.save(creator_id=request.user)
			created_bet = bet.save()
			send_invite_email(email, request, Bet.objects.get(pk=created_bet.id))
			return Response(bet.data, status=status.HTTP_201_CREATED)
		else:
			return Response(bet.errors, status=status.HTTP_400_BAD_REQUEST)

	def get_queryset(self):
		queryset = Bet.objects.all()
		title = self.request.query_params.get('title', None)
		creator = self.request.query_params.get('creator', None)
		condition = self.request.query_params.get('condition', None)
		amount = self.request.query_params.get('amount', None)
		date_created_start = self.request.query_params.get('date_created_start', None)
		date_created_end = self.request.query_params.get('date_created_end', None)
		date_accepted_start = self.request.query_params.get('date_accepted_start', None)
		date_accepted_end = self.request.query_params.get('date_accepted_start', None)
		if title is not None:
			queryset = queryset.filter(title__contains=title)
		elif condition is not None:
			wagers = Wager.objects.filter(condition__contains=condition)
			if creator == 'true':
				bet_list = []
				for bet in queryset:
					if bet.wagers.all()[0] in wagers:
						bet_list.append(bet)
				queryset = bet_list
			else:
				bet_list = []
				for bet in queryset:
					if bet.wagers.all()[1] in wagers:
						bet_list.append(bet)
				queryset = bet_list
		elif amount is not None:
			wagers = Wager.objects.filter(amount__contains=amount)
			print wagers
			if creator == 'true':
				bet_list = []
				for bet in queryset:
					if bet.wagers.all()[0] in wagers:
						bet_list.append(bet)
				queryset = bet_list
			else:
				bet_list = []
				for bet in queryset:
					if bet.wagers.all()[1] in wagers:
						bet_list.append(bet)
				queryset = bet_list
		elif date_created_start is not None:
			year, month, day = map(int, date_created_start.split('-'))
			date_created_start = datetime.date(year, month+1, day)
			year, month, day = map(int, date_created_end.split('-'))
			date_created_end = datetime.date(year, month+1, day)
			queryset = queryset.filter(date_created__range=(date_created_start, date_created_end))
		else:
			if date_accepted_start is not None or date_accepted_end is not None:
				year, month, day = map(int, date_accepted_start.split('-'))
				date_accepted_start = datetime.date(year, month+1, day)
				year, month, day = map(int, date_created_end.split('-'))
				date_accepted_end = datetime.date(year, month+1, day)
				print date_accepted_start, date_accepted_end
				queryset = queryset.filter(date_accepted__range=(date_accepted_start, date_accepted_end))
		print 'new queryset', queryset
		return queryset

def register_user(request):

	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.save()
			return HttpResponseRedirect(reverse('hello'))
	else:
		form = UserRegisterForm()
	title = "Enter your information here."
	return render(request, 'registration/registration.html', {'form': form, 'title': title})

def login_user(request):
	if request.method == 'POST':
		form = UserLoginForm(data=request.POST)
		if form.is_valid():
			login(request, form.get_user())
			return HttpResponseRedirect(reverse('index'))
	else:
		form = UserLoginForm()
	title = "Login Here."
	return render(request, 'registration/registration.html', {'form': form, 'title': title})

def logout_user(request):
	logout(request)
	return HttpResponseRedirect(reverse('bye'))

