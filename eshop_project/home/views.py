from django.shortcuts import render
from django.views import View
from django.views.generic.base import TemplateView
from site_module.models import siteSetting


# Create your views here.

# class homeView(View):
#     def get(self, request):
#         context = {
#             'data': 'this is data'
#         }
#         return render(request, 'home/index_page.html', context)

class homeView(TemplateView):
    template_name = 'home/index_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = 'this is dataaa'
        return context


def header_component(request):
    setting: siteSetting = siteSetting.objects.filter(is_main_setting=True).first()
    return render(request, 'shared/header_component.html', {'site_setting': setting})


def footer_component(request):
    setting: siteSetting = siteSetting.objects.filter(is_main_setting=True).first()
    return render(request, 'shared/footer_component.html', {'site_setting': setting})
