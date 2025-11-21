from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, Http404
from django.urls import reverse
from django.template.loader import render_to_string

# Create your views here.


days = {
    'Saturday': 'today is Saturday',
    'Sunday': 'today is Sunday',
    'Monday': 'today is Monday',
    'Tuesday': 'today is Tuesday',
    'Wednesday': 'today is Wednesday',
    'Thursday': 'today is Thursday',
    'Friday': 'today is Friday',
}


def days_list(request):
    day_list = list(days.keys())
    context = {
        'days': day_list
    }
    return render(request, 'days/days_list.html', context)

    '''
    item = ""
    for day in day_list:
        url_day = reverse('day_unic', args=[day])
        item += f'<li><a href="{url_day}"> {day} </a></li>\n'
    finally_day = f'<ul>\n{item}</ul>'
    return HttpResponse(finally_day)
    '''


def check_int(request, day):
    day_str = list(days.keys())
    if day > len(day_str):
        return HttpResponseNotFound("Does not exist")
    day_new = day_str[day - 1]
    return HttpResponseRedirect(day_new)


def check_str(request, day):
    test_data = days.get(day)
    if test_data is None:
        # raise Http404()
        response = render_to_string('404.html')
        return HttpResponse(response)

    data = {
        "day_data": test_data,
        "day": day
    }
    return render(request, "days/day_detail.html", context=data)

    # DTL-->dajango template language--> توی کد اچ تی ام ال می تونیم با این جنگو بیاریم

    # if test_data is not None:
    #     data = {
    #         "day_data": test_data,
    #         "day": day
    #     }
    #     return render(request, "days/day_detail.html", context=data)

    # responsday = render_to_string("days/day_detail.html")
    # responsday = f'<h2 style="color:purple">day : {day}\n , day2 : {test_data}</h2>'
    # return HttpResponse(responsday)

    # return HttpResponseNotFound('Does not exist')
