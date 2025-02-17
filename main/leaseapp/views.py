from django.shortcuts import render

# Create your views here.
def main(request):
    return render(request, 'landing.html')


def base(request):
    return render(request, 'base.html')

def detail(request):
    return render(request, 'detail.html')

def home(request):
    return render(request, 'index.html')