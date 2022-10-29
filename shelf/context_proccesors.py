from datetime import datetime


def date(request):
    date = datetime.now()
    return {'date':date}