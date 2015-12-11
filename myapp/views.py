import django_filters
import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, DetailView, ListView, FormView
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login

from .models import Room, Bet, Wager
from rest_framework import viewsets, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from .serializers import RoomSerializer, BetSerializer, WagerSerializer
from .forms import SubmitRoomForm, RequestRoomForm, ResponseRoomForm, UserRegisterForm, UserLoginForm, SubmitWagerForm, SubmitBetForm

# Create your views here.
class DetailRoomList(TemplateView):
	template_name = "detail_list.html"

class DetailRoom(TemplateView):
	template_name = 'detail.html'

def room_detail(request, pid):
	# send request to django in json
	# send back info about room
	# let django figure out how to render page
	room = get_object_or_404(Room, pk=pid)
	# assertion error, has to do with {'room': room}	
	return render(request, 'detail.html', {'room': room})

def test_query_string (request):
	invite = request.GET.get('i')
	return render(request, 'test-for-string.html', {'invite': invite})

class SubmitRoomFormView(FormView):
	template_name = 'submit.html'
	form_class = SubmitRoomForm

	def get_context_data(self, **kwargs):
		context = super(SubmitRoomFormView, self).get_context_data(**kwargs)
		context.update(title="New Bet:")
		return context

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

	def create(self, request):
		wager_data = []
		wager_data.append((request.data.pop('amount1'), request.data.pop('condition1')))
		wager_data.append((request.data.pop('amount2'), request.data.pop('condition2')))
		bet_data = request.data
		bet_data['wager_data'] = [{'amount':a,'condition':c} for a,c in wager_data]
		bet_data['wagers'] = []
		bet = BetSerializer(data=bet_data,context={'request':request})
		if bet.is_valid():
			bet.save(creator_id=request.user)
			bet.save()
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
		print queryset
		return queryset

class RoomSetView(viewsets.ModelViewSet, APIView):
	queryset = Room.objects.all().order_by('-date_created')
	serializer_class = RoomSerializer

	def create(self, request):
		test = RoomSerializer(data=request.data)
		if test.is_valid():
			test.save(user=request.user)
			test.save()
			return Response(test.data, status=status.HTTP_201_CREATED)
		else:
			return Response(test.errors, status=status.HTTP_400_BAD_REQUEST)


def submit_room(request):

	if request.method == 'POST':
		if 'submit' in request.POST:
			form = SubmitRoomForm(request.POST)
			if form.is_valid():
				room = form.save(commit=False)
				room.user = request.user
				room.date_created = timezone.now()
				room.ready = False
				room.save()
				return HttpResponseRedirect(reverse('thanks'))
		else:
			form = SubmitRoomForm()
	else:
		form = SubmitRoomForm()
	title = "Welcome challenger... here is your room!"
	return render(request, 'submit.html', {'form': form, 'title': title})

def find_room_from_key(request):
	if request.method == 'POST':
		form = RequestRoomForm(request.POST)
		if form.is_valid():
			room_key = form.cleaned_data['room_key'].encode('utf8')
			return HttpResponseRedirect(reverse('edit', kwargs={'room_key':room_key}))
	else:
		form = RequestRoomForm()
	title = "Enter your room key to access the bet room."
	return render(request, 'submit.html', {'form': form, 'title': title})

def submit_challenged(request, room_key):
	room_instance = Room.objects.get(room_key = room_key)
	if Room.objects.get(room_key=room_key).ready:
		return redirect('room_ready_error')
	if request.method == 'POST':
		form = ResponseRoomForm(request.POST, instance=room_instance)
		if form.is_valid():
			room = form.save(commit=False)
			room.ready = True
			room.save()
			return HttpResponseRedirect(reverse('thanks'))
	else:
		form = ResponseRoomForm()
	title = "Success! Enter your side of the bet."
	return render(request, 'submit.html', {'form': form, 'title': title})

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

