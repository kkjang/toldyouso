from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, DetailView, ListView, FormView
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login

from .models import Bet, Wager, BetWager, Room
from rest_framework import viewsets
from .serializers import RoomSerializer
from .forms import SubmitRoomForm, RequestRoomForm, ResponseRoomForm, UserRegisterForm, UserLoginForm

# Create your views here.
class DetailRoomList(ListView):
	model = Room
	template_name = "detail_list.html"

def room_detail(request, pid):
	room = get_object_or_404(Room, pk=pid)
	return render(request, 'detail.html', {'room': room})

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

class RoomSetView(viewsets.ModelViewSet):
	queryset = Room.objects.all().order_by('-date_created')
	serializer_class = RoomSerializer

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
	return render(request, 'submit.html', {'form': form, 'title': title})

def login_user(request):
	if request.method == 'POST':
		form = UserLoginForm(data=request.POST)
		if form.is_valid():
			login(request, form.get_user())
			return HttpResponseRedirect(reverse('thanks'))
	else:
		form = UserLoginForm()
	title = "Login Here."
	return render(request, 'submit.html', {'form': form, 'title': title})

def logout_user(request):
	logout(request)
	return HttpResponseRedirect(reverse('thanks'))
