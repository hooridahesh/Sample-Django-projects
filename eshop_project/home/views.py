from django.shortcuts import render
from django.views import View
from django.views.generic.base import TemplateView


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
    return render(request, 'shared/header_component.html', {})


def footer_component(request):
    return render(request, 'shared/footer_component.html', {})
