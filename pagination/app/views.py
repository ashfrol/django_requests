from urllib.parse import urlencode

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
import csv

from pagination.app import settings


def index(request):
    return redirect(reverse(bus_stations))


def bus_stations(request):
    items_by = 10
    list_of_stations = []
    with open(settings.BUS_STATION_CSV, encoding='cp1251',  newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            station_data = {'Name': row['Name'], 'Street': row['Street'], 'District': row['District']}
            list_of_stations.append(station_data)
        print(list_of_stations)
        paginator = Paginator(list_of_stations, items_by)
        page_number = request.GET.get('page', 1)
        current_page_obj = paginator.get_page(page_number)

        next_page, previous_page = None, None
        if current_page_obj.has_next():
            next_page = reverse('bus_stations') + '?' + urlencode({'page': current_page_obj.next_page_number()})
        if current_page_obj.has_previous():
            previous_page = reverse('bus_stations') + '?' + urlencode({'page': current_page_obj.previous_page_number()})


    return render(request, 'index.html', context={
        'bus_stations': current_page_obj,
        'current_page': page_number,
        'prev_page_url': previous_page,
        'next_page_url': next_page
    })

