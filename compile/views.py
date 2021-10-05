from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@require_http_methods(["POST"])
@csrf_exempt
def index(request):
    try:
        file = request.FILES['filename']
        print(file.name)
    except Exception as e:
        raise e
    return HttpResponse("response here")
