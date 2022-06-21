from .models import Settings

def counter(request):
    settings_count = Settings.objects.all().count()
    if settings_count == 1:
        flag = False
    else:
        flag = True
    return dict(settings_count=flag)