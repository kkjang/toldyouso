from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, DetailView, ListView
from django.utils import timezone

from .models import Statement
from .forms import SubmitForm

# Create your views here.
class DetailList(ListView):
	model = Statement
	template_name = "detail_list.html"

def detail(request, pid):
	statement = get_object_or_404(Statement, pk=pid)
	return render(request, 'detail.html', {'statement': statement})

def submit(request):
	if request.method == 'POST':
		form = SubmitForm(request.POST)
		if form.is_valid():
			statement = form.save(commit=False)
			statement.date_created = timezone.now()
			statement.user = request.user
			statement.save()
			return HttpResponseRedirect(reverse('thanks'))

	else:
		form = SubmitForm()

	return render(request, 'submit.html', {'form': form})