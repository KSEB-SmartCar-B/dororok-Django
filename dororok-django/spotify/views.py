from asgiref.sync import async_to_sync
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from spotify.app.search_for_item import get_music_data
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import api_view


@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('title', openapi.IN_QUERY, description="Music title",
                          type=openapi.TYPE_STRING),
        openapi.Parameter('artist', openapi.IN_QUERY, description="Music artist",
                          type=openapi.TYPE_STRING)
    ],
    operation_summary='음악 검색(제목/가수)',
    operation_description='제목 or 가수 or 제목/가수 검색 가능'
)

@api_view(['GET'])
def search_music_or_artist(request):
    if request.method == 'GET':
        try:
            input_title = request.GET.get('title', '')
            input_artist = request.GET.get('artist' '')

            if not input_title and not input_artist:
                return JsonResponse({'error': 'Title or artist parameter is required.'}, status=400)

            response_data = async_to_sync(get_music_data)(input_title, input_artist)
            result = {
                'track_names': response_data[0],
                'artist_names': response_data[1],
                'track_ids': response_data[2],
                'track_images': response_data[3],
            }

            return JsonResponse(result, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
