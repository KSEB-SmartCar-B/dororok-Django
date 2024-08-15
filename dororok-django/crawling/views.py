from django.shortcuts import render

from ai.DL.train_triplet_loss_model import train_and_save_model
from crawling.models import LastUpdate, crawling_genre_model
from crawling.app.update_all_genre import genre_code_map, update_all_genre
from spotify.app.search_for_track_id import search_all_genres
from ai import analyze_data
from datetime import datetime
from django.http import JsonResponse
import threading

def chart_view(request, genre):
    today = datetime.now().date()
    if today.weekday() == 3:
         try:
             last_update = LastUpdate.objects.get(genre=genre)
             if last_update.last_updated.date() < today:
                 perform_update_and_analysis(genre, today)
         except LastUpdate.DoesNotExist:
             perform_update_and_analysis(genre, today)

    if genre not in genre_code_map:
        return render(request, 'crawling/error.html', {'message': 'Invalid genre'})

    model = crawling_genre_model[genre]
    chart_entries = model.objects.all()

    chart_data = [
        {
            'rank': entry.rank,
            'title': entry.title,
            'singer': entry.singer,
            'album': entry.album,
            'album_image': entry.album_image
        } for entry in chart_entries
    ]

    return render(request, 'crawling/chart.html', {'chart_data': chart_data})


progress = 0
model_training_done = False


def model_train(request):
    global progress, model_training_done

    def run_training():
        global progress, model_training_done
        train_and_save_model()
        progress = 100
        model_training_done = True

    progress = 0
    model_training_done = False
    threading.Thread(target=run_training).start()

    return render(request, 'crawling/train.html')


def training_progress(request):
    return JsonResponse({'progress': progress, 'done': model_training_done})


def perform_update_and_analysis(genre, today):
    update_all_genre()
    last_update, created = LastUpdate.objects.get_or_create(genre=genre)
    last_update.last_updated = datetime.combine(today, datetime.min.time())
    last_update.save()

    search_all_genres()
    print('clear search')

    analyze_data.analyze_data()
    print('end')
    train_and_save_model()