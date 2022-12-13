from django.db.models import Sum
from django.shortcuts import render
from django.utils import timezone

from .models import Balance


# Create your views here.
def home(request):
    template_name = 'balancecontrol/pages/home.html'
    datebalance = Balance.objects.all().order_by('-datecreate')
    # calcula o total diario
    DailyAmountEntry = Balance.objects.all().filter(
        typeoperation='P', datecreate__day=timezone.now().day).aggregate(Sum('value'))  # noqa
    if DailyAmountEntry['value__sum'] is None:
        DailyAmountEntry['value__sum'] = 0
    print(DailyAmountEntry)

    DailyValueOutput = Balance.objects.all().filter(
        typeoperation='E', datecreate__day=timezone.now().day).aggregate(Sum('value'))  # noqa
    if DailyValueOutput['value__sum'] is None:
        DailyValueOutput['value__sum'] = 0

    DailyTotal = DailyAmountEntry['value__sum'] -\
        DailyValueOutput['value__sum']

    # calcula o total mensal
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

    # calcula o total anual
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
        'datebalance': datebalance,
        'DailyTotal': DailyTotal,
        'MonthlyTotal': MonthlyTotal,
        'YearlyTotal': YearlyTotal,

    }

    return render(request, template_name, context)
