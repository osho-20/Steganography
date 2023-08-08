from django.shortcuts import render
# import stepic
# from PIL import Image
# Create your views here.

def index(request):
    return render(request,'index.html')

def encrypt(request):
    return render(request,'encrypt.html')

def decrypt(request):
    return render(request,'decrypt.html')
    