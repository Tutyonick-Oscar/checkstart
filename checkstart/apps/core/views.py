from django.views.generic import TemplateView


class MacAccessCodeMailView(TemplateView):
    template_name = "mails/mac_access_code.html"
