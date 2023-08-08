from django.shortcuts import render
import stepic
from PIL import Image
import io
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.storage import default_storage

def index(request):
    return render(request, 'index.html')

def encrypt_text(img_file, text):
    encrypted_text = text.encode('utf-8')
    
    # Convert the InMemoryUploadedFile to a PIL Image
    img = Image.open(img_file)
    img = img.convert("RGBA")
    
    # Encode the text within the image
    encoded_img = stepic.encode(img, encrypted_text)
    
    return encoded_img

# def encrypt(request):
#     message = ""
#     encoded_image = ""
#     if request.method == "POST":
#         img_file = request.FILES['image']
#         text = request.POST['message']
#         if img_file is not None:
#             new_img = encrypt_text(img_file, text)
#             encoded_image_io = io.BytesIO()
#             new_img.save(encoded_image_io,format="PNG")
#             # Create a new InMemoryUploadedFile from the BytesIO object
#             encoded_image = InMemoryUploadedFile(
#                 encoded_image_io, None, 'image.png', 'image/png',
#                 encoded_image_io.getbuffer().nbytes, None
#             )
            
#             image_path = 'images/' + encoded_image.name  # Construct the full path
#             saved_image_path = default_storage.save(image_path, encoded_image)
#             message = "Message is encrypted"
#             encoded_image=new_img
#         else:
#             message=""
    
#     # if encoded_image is not None:
#     context={'message': message,'encoded_image': encoded_image }
#     # else:
#     #     context={'message': message}
#     return render(request, 'encrypt.html', context)

def encrypt(request):
    message = ""
    encoded_image_url = ""
    
    if request.method == "POST":
        img_file = request.FILES.get('image')  # Use get() to handle missing key
        text = request.POST['message']
        
        if img_file is not None:
            new_img = encrypt_text(img_file, text)
            encoded_image_io = io.BytesIO()
            new_img.save(encoded_image_io, format="PNG")
            
            # Create a new InMemoryUploadedFile from the BytesIO object
            encoded_image = InMemoryUploadedFile(
                encoded_image_io, None, 'image.png', 'image/png',
                encoded_image_io.getbuffer().nbytes, None
            )
            
            # Save the image to the storage
            image_path = 'images/' + encoded_image.name
            saved_image_path = default_storage.save(image_path, encoded_image)
            
            # Construct the URL for displaying the image
            encoded_image_url = default_storage.url(saved_image_path)
            message = "Message is encrypted"
    context = {'message': message, 'encoded_image_url': encoded_image_url}
    return render(request, 'encrypt.html', context)

def decrypt_text(image):
    data=stepic.decode(image)
    if isinstance(data,bytes):
        return data.decode('utf-8')
    return data

def decrypt(request):
    text= ""
    if request.method=="POST":
        image_fil=request.FILES['image']
        image=Image.open(image_fil)
        text=decrypt_text(image)
        
    return render(request, 'decrypt.html',{'text':text})
