import threading
from time import sleep
from django.conf import settings
import os

class ThreadGerarCsv(threading.Thread):
    def __init__(self,request, function, queryset):
        self.request = request
        self.function = function
        self.queryset = queryset
        self.path = ""
        threading.Thread.__init__(self)

    
    def run(self):
        path = os.path.join(settings.MEDIA_ROOT, f'extracoes/extracao_{self.request.user.username}.csv')
        self.function(self.queryset, path)
        self.path = path
