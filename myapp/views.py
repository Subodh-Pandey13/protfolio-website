from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, "home.html")

def cv(request):
    return render(request, "cv.html")

def research(request):
    return render(request, 'research.html')

def teaching(request):
    return render(request, 'teaching.html')

def blog(request):
    return render(request, 'blog.html')

def contact(request):
    return render(request, 'contact.html')