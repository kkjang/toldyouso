from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, DetailView, ListView
from django.utils import timezone

from .models import Room
from .forms import SubmitRoomForm, RequestRoomForm, ResponseRoomForm

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
				room.date_created = timezone.now()
				room.ready = False
				room.save()
				return HttpResponseRedirect(reverse('thanks'))
		else:
			form = SubmitRoomForm()
	else:
		form = SubmitRoomForm()

	return render(request, 'submit.html', {'form': form})

def find_room_from_key(request):
	if request.method == 'POST':
		form = RequestRoomForm(request.POST)
		if form.is_valid():
			room_key = form.cleaned_data['room_key'].encode('utf8')
			return HttpResponseRedirect(reverse('edit', kwargs={'room_key':room_key}))
	else:
		form = RequestRoomForm()

	return render(request, 'submit.html', {'form': form})

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

	return render(request, 'submit.html', {'form': form})

