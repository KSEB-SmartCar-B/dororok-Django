from django.shortcuts import render

from crawling.models import LastUpdate, crawling_genre_model
from crawling.app.update_all_genre import genre_code_map, update_all_genre
from spotify.app.search_for_item import search_all_genres
from ai import analyze_data
from datetime import datetime


def chart_view(request, genre):
    today = datetime.now().date()
    if today.weekday() == 2:
        try:
            last_update = LastUpdate.objects.get(genre=genre)
            if last_update.last_updated.date() < today:
                #update_all_genre()
                #last_update.last_updated = datetime.combine(today, datetime.min.time())
                #last_update.save()
                #print('clear update')
                search_all_genres()
                print('clear search')
                analyze_data.analyze_data()
                print('end')

        except LastUpdate.DoesNotExist:
            update_all_genre()
            LastUpdate.objects.create(genre=genre, last_updated=datetime.combine(today, datetime.min.time()))

    if genre not in genre_code_map:
        return render(request, 'crawling/error.html', {'message': 'Invalid genre'})

    model = crawling_genre_model[genre]
    chart_entries = model.objects.all()

    chart_data = [{'rank': entry.rank, 'title': entry.title, 'singer': entry.singer,
                   'album': entry.album, 'album_image': entry.album_image} for entry in chart_entries]

    return render(request, 'crawling/chart.html', {'chart_data': chart_data})
