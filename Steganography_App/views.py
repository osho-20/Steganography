from django.shortcuts import render
# import stepic
# from PIL import Image
# Create your views here.

def index(request):
    return render(request,'index.html')