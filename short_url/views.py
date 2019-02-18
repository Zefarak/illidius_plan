from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.contrib import messages
from django.views import View

from .models import *
from .forms import *
# Create your views here.


class ShortHomepage(View):
    template = 'tim/shorting_url.html'

    def get(self, request, *args, **kwargs):
        # ShortingURL.objects.all().delete()
        form = ShortURLForm()
        context = locals()
        return render(request, self.template, context)

    def post(self, request, *args, **kwargs):
        if request.POST:
            print(request.POST)
            form = ShortURLForm(request.POST)
            if form.is_valid():
                print(request.POST)
                form.save()
                new_url = ShortingURL.objects.last()
                get_url = 'www.simply-chris.com/s/%s/' % new_url.shortcode
                messages.success(request, '%s' % get_url)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        context = locals()
        return render(request, self.template, context)


def redirect_view(request, slug):
    get_url = get_object_or_404(ShortingURL, shortcode=slug)
    return HttpResponseRedirect(get_url.url)


