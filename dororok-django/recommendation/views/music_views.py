import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from recommendation.music_recommender.params.params import MusicRecommendationParams
from recommendation.music_recommender.personalized_music_recommender import recommend_music


@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('member_id', openapi.IN_QUERY, description="Member ID", type=openapi.TYPE_INTEGER),
        openapi.Parameter('genre', openapi.IN_QUERY, description="Music genres",
                          type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING)),
        openapi.Parameter('lat', openapi.IN_QUERY, description="Latitude", type=openapi.TYPE_NUMBER),
        openapi.Parameter('lng', openapi.IN_QUERY, description="Longitude", type=openapi.TYPE_NUMBER),
        openapi.Parameter('region1depthName', openapi.IN_QUERY, description="Region 1 depth name",
                          type=openapi.TYPE_STRING),
        openapi.Parameter('region2depthName', openapi.IN_QUERY, description="Region 2 depth name",
                          type=openapi.TYPE_STRING),
        openapi.Parameter('region3depthName', openapi.IN_QUERY, description="Region 3 depth name",
                          type=openapi.TYPE_STRING),
        openapi.Parameter('skyCondition', openapi.IN_QUERY, description="Sky condition", type=openapi.TYPE_STRING),
        openapi.Parameter('precipitationType', openapi.IN_QUERY, description="Precipitation type",
                          type=openapi.TYPE_STRING),
        openapi.Parameter('MusicMode', openapi.IN_QUERY, description="Music mode", type=openapi.TYPE_STRING),
        openapi.Parameter('dayPart', openapi.IN_QUERY, description="Day part", type=openapi.TYPE_STRING),
        openapi.Parameter('is_first', openapi.IN_QUERY, description="Is first recommendation", type=openapi.TYPE_BOOLEAN)
    ],
    operation_summary='뮤직 추천을 위한 사용자 정보 입력.',
    operation_description="장르(리스트), 위도/경도(현재 위치), 도/시/군구(현재위치), "
                          "날씨(맑음/흐림/구름많음), 강수(없음/비/눈/소나기), "
                          "뮤직모드(dororok, daily, to_work, leave_work, travel, drive, with_lover, with_friends)."
)
@api_view(['GET'])
@csrf_exempt
def get_user_music_info(request):
    if request.method == 'GET':
        try:
            member_id = request.GET.get('member_id')
            genre = request.GET.getlist('genre', [])
            lat = request.GET.get('lat')
            lng = request.GET.get('lng')
            region1depthName = request.GET.get('region1depthName')
            region2depthName = request.GET.get('region2depthName')
            region3depthName = request.GET.get('region3depthName')
            skyCondition = request.GET.get('skyCondition')
            precipitationType = request.GET.get('precipitationType')
            MusicMode = request.GET.get('MusicMode')
            DayPart = request.GET.get('dayPart')
            is_first = request.GET.get('is_first').lower() == 'true'

            print(f"Member ID: {member_id}")
            print(f"Genre: {genre}")
            print(f"Latitude: {lat}")
            print(f"Longitude: {lng}")
            print(f"Region1: {region1depthName}")
            print(f"Region2: {region2depthName}")
            print(f"Region3: {region3depthName}")
            print(f"Sky Condition: {skyCondition}")
            print(f"Precipitation: {precipitationType}")
            print(f"Music Mode: {MusicMode}")
            print(f"Day Part: {DayPart}")
            print(f"Is First: {is_first}")

            params = MusicRecommendationParams(
                member_id=member_id,
                genre=genre,
                lat=float(lat),
                lng=float(lng),
                region1depth_name=region1depthName,
                region2depth_name=region2depthName,
                region3depth_name=region3depthName,
                sky_condition=skyCondition,
                precipitation=precipitationType,
                music_mode=MusicMode,
                day_part=DayPart,
                is_first=is_first
            )

            response_data = generate_music_recommendations(params, is_first)
            return JsonResponse(response_data, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def generate_music_recommendations(params: MusicRecommendationParams, is_first: bool):
    recommendations = recommend_music(params)
    num_songs = 2 if is_first else 1

    # 필요한 필드만 포함된 결과 리스트 생성
    filtered_recommendations = [
        {
            'title': rec['title'],
            'artist': rec['artist'],
            'track_id': rec['track_id'],
            'album_image': rec['album_image'],
        }
        for rec in recommendations[:num_songs]
    ]
    for rec in filtered_recommendations:
        print(f"Title: {rec['title']}")
        print(f"Artist: {rec['artist']}")
        print(f"Track ID: {rec['track_id']}")
        print(f"Album Image: {rec['album_image']}")
        print()
    return {'recommendations': filtered_recommendations}


