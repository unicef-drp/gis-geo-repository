from django.views.generic import TemplateView


class UploaderView(TemplateView):
    template_name = 'uploader.html'
