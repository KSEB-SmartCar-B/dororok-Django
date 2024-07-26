from django.http import JsonResponse
from rest_framework.decorators import api_view
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from spotify_app.authentication.spotify_auth import get_spotify_client

class SearchTrackId:
    def __init__(self):
        self.sp = get_spotify_client()

    def parse_track_id(self, title, artist):
        track_ids = []
        track_results = self.sp.search(q=f"track:{title} artist:{artist}", limit=1, type='track', market='KR')
        if track_results['tracks']['items']:
            track_id = track_results['tracks']['items'][0]['id']
            track_ids.append(track_id)
        else:
            track_ids.append(None)
        return track_ids

@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('title', openapi.IN_QUERY, description="Track title", type=openapi.TYPE_STRING),
        openapi.Parameter('artist', openapi.IN_QUERY, description="Artist name", type=openapi.TYPE_STRING),
    ],
    responses={
        200: openapi.Response(
            'Track IDs',
            openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'track_id': openapi.Schema(type=openapi.TYPE_STRING, description="Track ID"),
                }
            )
        )
    }
)

@api_view(['GET'])
def search_track(request):
    title = request.GET.get('title')
    artist = request.GET.get('artist')
    if not title or not artist:
        return JsonResponse({'error': 'Both title and artist parameters are required.'}, status=400)

    searcher = SearchTrackId()
    track_ids = searcher.parse_track_id(title, artist)
    return JsonResponse({'track_ids': track_ids})
