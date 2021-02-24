from io import BytesIO

import requests
from PIL import Image
from django.core.files import File
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.views.generic.base import View

from imageresizer.forms import NewImageForm, ResizeImageForm
from imageresizer.models import NewImage


def main_view(request):
    NewImage.objects.filter(is_copy=True).delete()
    images = NewImage.objects.all()
    context = {
        "images": images,
    }
    return render(request, "imageresizer/main.html", context=context)


class ResizeView(View):
    def get(self, request, pk):
        image = NewImage.objects.get(id=pk)
        return render(request, "imageresizer/resize-view.html",
                      context={"form": ResizeImageForm, "image": image})

    def post(self, request, pk):
        form = ResizeImageForm(request.POST, request.FILES)
        image = NewImage.objects.get(id=pk)
        if form.is_valid():
            width = request.POST.get('width')
            height = request.POST.get('height')
            im = Image.open(image.image)
            im.convert('RGB')
            width_orig, height_orig = im.size
            aspect_ratio = width_orig / height_orig if height_orig else 1
            print(f"width_orig - {width_orig}\nheight_orig - {height_orig}")
            if not (width and height):
                if aspect_ratio > 1:
                    if width:
                        height = int(width) * aspect_ratio if int(width) > width_orig else int(width) / aspect_ratio
                    elif height:
                        width = int(height) * aspect_ratio if int(height) < height_orig else int(height) / aspect_ratio
                else:
                    if width:
                        height = int(width) / aspect_ratio if int(width) < width_orig else int(width) * aspect_ratio
                    elif height:
                        width = int(height) / aspect_ratio if int(height) > height_orig else int(height) * aspect_ratio
            print(f"aspect_ratio - {aspect_ratio}\nwidth - {width}\nheight - {height}")
            size = (int(width), int(height))
            im = im.resize(size)
            thumb_io = BytesIO()
            im.save(thumb_io, 'PNG', quality=85)
            new_image = File(thumb_io, name=image.image.name)
            pk = NewImage.objects.create(image=new_image, is_copy=True).id
            return redirect("ResizeView", pk)
        else:
            form.add_error('width', 'Заполните только одно поле!')
        return render(request, "imageresizer/resize-view.html",
                      context={"form": form, "image": image})


class NewImageView(View):
    def get(self, request):
        return render(request, "imageresizer/add-image.html", context={"form": NewImageForm})

    def post(self, request):
        form = NewImageForm(request.POST, request.FILES)
        if form.is_valid():
            pk = -1
            url = form.cleaned_data.get('url')
            image = form.cleaned_data.get('image')
            if url:
                image = requests.get(url, stream=True).raw
                temp_image = NewImage.objects.create(image=image)
                pk = temp_image.id
            elif image:
                temp_image = NewImage.objects.create(image=image)
                pk = temp_image.id
            elif pk == -1:
                return redirect("AddView")
            return redirect("ResizeView", pk)
        else:
            form.data._mutable = True
            form.data['url'] = None
            form.add_error('url', 'Заполните только одно поле!')
        return render(request, "imageresizer/add-image.html", context={"form": form})


def custom_handler_404(request, exception):
    return HttpResponseNotFound('<center><h1>Ничего не нашлось! Ошибка 404!</h1></center>')


def custom_handler_500(request):
    return HttpResponseNotFound('<center><h1>Вы сломали сервер! Ошибка 500!</h1></center>')
