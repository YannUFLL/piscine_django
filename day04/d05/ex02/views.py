from django.shortcuts import render
from .forms import MyForm
import os
from django.conf import settings
from django.utils import timezone

def form_view(request):
    path_log = settings.LOG_FILE

    if os.path.exists(path_log):
        with open(path_log, "r") as log_file:
            entries = log_file.readlines()

    with open(path_log, "a") as log_file:
        if request.method == "POST":
            form = MyForm(request.POST)
            if (form.is_valid()):
                data = form.cleaned_data["text"]
                time = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
                log = time + " " + data + '\n'
                log_file.write(log)
                entries.append(log)
        else: 
            form = MyForm()
        
    return (render(request, "ex02/history.html", {"form": form, "logs": entries}))