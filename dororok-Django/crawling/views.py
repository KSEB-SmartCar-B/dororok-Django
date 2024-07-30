from django.shortcuts import render
from crawling.models import genre_models, LastUpdate
from crawling.app.update_all_genre import genre_code_map, update_all_genre
from datetime import datetime


def chart_view(request, genre):
    today = datetime.now().date()
    if today.weekday() == 0:
        try:
            last_update = LastUpdate.objects.get(genre=genre)
            if last_update.last_updated.date() < today:
                update_all_genre()
                last_update.last_updated = datetime.combine(today, datetime.min.time())
                last_update.save()
        except LastUpdate.DoesNotExist:
            update_all_genre()
            LastUpdate.objects.create(genre=genre, last_updated=datetime.combine(today, datetime.min.time()))

    if genre not in genre_code_map:
        return render(request, 'crawling/error.html', {'message': 'Invalid genre'})

    model = genre_models[genre]
    chart_entries = model.objects.all()

    chart_data = [{'rank': entry.rank, 'title': entry.title, 'singer': entry.singer,
                   'album': entry.album, 'album_image': entry.album_image} for entry in chart_entries]

    return render(request, 'crawling/chart.html', {'chart_data': chart_data})
