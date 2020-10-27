from django.views.generic import DetailView

from .models import GFile


class GfileDetailView(DetailView):

    model = GFile
