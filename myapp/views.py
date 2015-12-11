from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.mail import send_mail, BadHeaderError, EmailMessage

from django.views.generic import TemplateView, DetailView, ListView, FormView
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login

from .models import Room, Bet, Wager
from rest_framework import viewsets, status
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

class DetailProfile(TemplateView):
	template_name = 'profile.html'

def sendmail(request):
	# email = EmailMessage('Hello', 'World', to=['pl@live.unc.edu'])
	# email.send()
	try:
		send_mail("asdf", "bodyofmessage", "uncsetinstone@gmail.com", ['PL@LIVE.UNC.EDU'])
		return HttpResponseRedirect('/faq/')
	except:
		return HttpResponseRedirect('/room/')

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


class BetSetView(viewsets.ModelViewSet, APIView):
	queryset = Bet.objects.all()
	serializer_class = BetSerializer

	def create(self, request):
		wager_data = []
		wager_data.append((request.data.pop('amount1'), request.data.pop('condition1')))
		wager_data.append((request.data.pop('amount2'), request.data.pop('condition2')))
		email = request.data.pop('email')
		print email

		bet_data = request.data
		bet_data['wager_data'] = [{'amount':a,'condition':c} for a,c in wager_data]
		bet_data['wagers'] = []
		bet = BetSerializer(data=bet_data,context={'request':request})
		if bet.is_valid():
			bet.save(creator_id=request.user)
			bet = bet.save()
			print 'email: ' + bet['email']
			print 'bet: ' + bet

			send_mail("asdf", "sent via room create", "uncsetinstone@gmail.com", [email])			
			return Response(bet.data, status=status.HTTP_201_CREATED)
		else:
			return Response(bet.errors, status=status.HTTP_400_BAD_REQUEST)

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
			print test.errors
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
			return HttpResponseRedirect(reverse('thanks'))
	else:
		form = UserRegisterForm()
	title = "Enter your information here."
	return render(request, 'registration/registration.html', {'form': form, 'title': title})

def login_user(request):
	if request.method == 'POST':
		form = UserLoginForm(data=request.POST)
		if form.is_valid():
			login(request, form.get_user())
			return HttpResponseRedirect(reverse('thanks'))
	else:
		form = UserLoginForm()
	title = "Login Here."
	return render(request, 'registration/registration.html', {'form': form, 'title': title})

def logout_user(request):
	logout(request)
	return HttpResponseRedirect(reverse('thanks'))

