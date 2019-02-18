from django.http import HttpResponse, JsonResponse

from newsletter.models import Join
from newsletter.utils import SendSubscriberMail


def subscribe(request):
    if request.POST:
        email = request.POST['email_id']
        email_qs = Join.objects.filter(email=email)
        if email_qs.exists():
            data = {"status": "404"}
            return JsonResponse(data)
        else:
            Join.objects.create(email=email)
            SendSubscriberMail(email)
    return HttpResponse("/")