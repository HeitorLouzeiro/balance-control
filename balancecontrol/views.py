import os
from datetime import timedelta

from dateutil.parser import parse
from django.contrib import messages
from django.db.models import Sum
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from utils.pagination import make_pagination

from .models import Balance

PER_PAGE = int(os.environ.get('PER_PAGE', 6))

# Create your views here.


def home(request):
    template_name = 'balancecontrol/pages/home.html'
    datebalances = Balance.objects.all().order_by('-datecreate')

    page_obj, pagination_range = make_pagination(
        request, datebalances, PER_PAGE)

    # Search by date
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        end_date = parse(end_date) + timedelta(days=1)
        datebalances = datebalances.filter(
            datecreate__range=[start_date, end_date]
        )

    # calculate the daily total
    DailyAmountEntry = Balance.objects.all().filter(
        typeoperation='P', datecreate__day=timezone.now().day).aggregate(Sum('value'))  # noqa
    if DailyAmountEntry['value__sum'] is None:
        DailyAmountEntry['value__sum'] = 0

    DailyValueOutput = Balance.objects.all().filter(
        typeoperation='E', datecreate__day=timezone.now().day).aggregate(Sum('value'))  # noqa
    if DailyValueOutput['value__sum'] is None:
        DailyValueOutput['value__sum'] = 0

    DailyTotal = DailyAmountEntry['value__sum'] -\
        DailyValueOutput['value__sum']

    # calculate the monthly total
    MonthlyValueEntry = Balance.objects.all().filter(
        typeoperation='P', datecreate__month=timezone.now().month).aggregate(Sum('value'))  # noqa
    if MonthlyValueEntry['value__sum'] is None:
        MonthlyValueEntry['value__sum'] = 0
    MonthlyValueOutput = Balance.objects.all().filter(
        typeoperation='E', datecreate__month=timezone.now().month).aggregate(Sum('value'))  # noqa
    if MonthlyValueOutput['value__sum'] is None:
        MonthlyValueOutput['value__sum'] = 0

    MonthlyTotal = MonthlyValueEntry['value__sum'] - \
        MonthlyValueOutput['value__sum']

    # calculate the annual total
    YearlyValueEntry = Balance.objects.all().filter(
        typeoperation='P', datecreate__year=timezone.now().year).aggregate(Sum('value'))  # noqa
    if YearlyValueEntry['value__sum'] is None:
        YearlyValueEntry['value__sum'] = 0

    YearlyValueOutput = Balance.objects.all().filter(
        typeoperation='E', datecreate__year=timezone.now().year).aggregate(Sum('value'))  # noqa
    if YearlyValueOutput['value__sum'] is None:
        YearlyValueOutput['value__sum'] = 0

    YearlyTotal = YearlyValueEntry['value__sum'] - \
        YearlyValueOutput['value__sum']

    context = {
        'datebalances': page_obj,
        'pagination_range': pagination_range,
        'DailyTotal': DailyTotal,
        'MonthlyTotal': MonthlyTotal,
        'YearlyTotal': YearlyTotal,


    }

    return render(request, template_name, context)


def createfinance(request):
    if not request.POST:
        raise Http404()
    if request.method == 'POST':
        value = request.POST.get('value')
        typeoperation = request.POST.get('typeoperation')
        Balance.objects.create(value=value, typeoperation=typeoperation)
        messages.success(request, 'Data saved successfully!')
        return redirect('balancecontrol:home')
    else:
        messages.error(request, 'Data not saved!')
        return redirect(reverse('balancecontrol:home'))


def editfinance(request):
    if not request.POST:
        raise Http404()
    if request.method == 'POST':
        id = request.POST.get('id')
        value = request.POST.get('value')
        typeoperation = request.POST.get('typeoperation')
        balance = get_object_or_404(Balance, pk=id)
        balance.value = value
        balance.typeoperation = typeoperation
        balance.save()
        messages.success(request, 'Data edited successfully!')
        return redirect('balancecontrol:home')
    else:
        messages.error(request, 'Data not edited!')
        return redirect(reverse('balancecontrol:home'))


def deletefinance(request):
    if not request.POST:
        raise Http404()
    if request.method == 'POST':
        id = request.POST.get('id')
        balance = get_object_or_404(Balance, pk=id)
        balance.delete()
        messages.success(request, 'Data deleted successfully!')
        return redirect('balancecontrol:home')
    else:
        messages.error(request, 'Data not deleted!')
        return redirect(reverse('balancecontrol:home'))
