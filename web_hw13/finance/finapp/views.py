from django.shortcuts import render, redirect
from .models import Record
from datetime import datetime

# Create your views here.
def main(request):
    return render(request, 'finapp/index.html', {})

def add_record(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        plan_plus = request.POST['plan_plus']
        unplan_plus = request.POST['unplan_plus']
        fart_plus = request.POST['fart_plus']
        plan_minus = request.POST['plan_minus']
        unplan_minus = request.POST['unplan_minus']
        idiotic_minus = request.POST['idiotic_minus']
        date = datetime.now()
        if bool(name) and bool(email):
            rec = Record(name=name,
                         email=email,
                         plan_plus=plan_plus,
                         unplan_plus=unplan_plus,
                         fart_plus=fart_plus,
                         plan_minus=plan_minus,
                         unplan_minus=unplan_minus,
                         idiotic_minus=idiotic_minus,
                         date=date)
            rec.save()
            return redirect(to='/')
    return render(request, 'finapp/record.html', {})

def see_report(request):
    if request.method == 'POST':
        email = request.POST['email']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        if start_date == '':
            start_date = datetime(1970, 1, 1)
        if end_date == '':
            end_date = datetime.now()
        records = Record.objects.filter(email=email).filter(date__gte=start_date).filter(date__lte=end_date)
        plan_plus, unplan_plus, fart_plus, plan_minus, unplan_minus, idiotic_minus = 0,0,0,0,0,0
        for item in records:
            name = item.name
            email = item.email
            plan_plus += int(item.plan_plus)
            unplan_plus += int(item.unplan_plus)
            fart_plus += int(item.fart_plus)
            plan_minus += int(item.plan_minus)
            unplan_minus += int(item.unplan_plus)
            idiotic_minus += int(item.idiotic_minus)
        debet = (plan_plus + unplan_plus + fart_plus)
        kredit = (plan_minus + unplan_minus + idiotic_minus)
        comment = "Фраер на фарте"
        if debet/3 > kredit:
            comment = "Адекватный чувак"
        if debet/2 > kredit:
            comment = "Транжира как девка"
        if idiotic_minus > 50:
            comment = "Просто идиот"
        record={"name": name,
                "email": email,
                "comment": comment,
                "debet": debet,
                "kredit": kredit,
                "plan_plus": plan_plus,
                "unplan_plus": unplan_plus,
                "fart_plus": fart_plus,
                "plan_minus": plan_minus,
                "unplan_minus": unplan_minus,
                "idiotic_minus": idiotic_minus
                }
        return render(request, 'finapp/report.html', {"record": record})
    records_all = Record.objects.all()
    return render(request, 'finapp/report.html', {"records_all":records_all})
