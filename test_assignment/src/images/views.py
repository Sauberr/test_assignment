from django.views.generic import ListView

from common.mixins import TitleMixin
from images.models import Images


class ImagesList(TitleMixin, ListView):
    template_name: str = "images/images_list.html"
    title: str = "Gallery"
    model = Images
    context_object_name: str = 'images'
    ordering = ['title']
