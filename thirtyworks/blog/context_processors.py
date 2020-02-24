from .models import Day

def GetDate(request):
    days = Day.objects.all()
    return {"days":days}
