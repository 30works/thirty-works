from .models import Day

def GetDate(request):
    days = Day.objects.all()
    return {"days":days}

def get_latest_day_number(request):
    day = Day.objects.last()
    day_number = day.number
    return {"day_number": day_number}