from django.shortcuts import render

def dashboard(request):
    cards = [
        {"title": "Total Complaints", "value": 120, "icon": "fa-solid fa-folder"},
        {"title": "Pending", "value": 35, "icon": "fa-solid fa-clock"},
        {"title": "Resolved", "value": 70, "icon": "fa-solid fa-circle-check"},
        {"title": "Rejected", "value": 15, "icon": "fa-solid fa-xmark"},
    ]

    return render(request, "dashboard/dashboard.html", {"cards": cards})
