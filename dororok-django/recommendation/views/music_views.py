from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('genre', openapi.IN_QUERY, description="Music genres",
                          type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING)),  # 타입 설정 수정
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
        openapi.Parameter('dayPart', openapi.IN_QUERY, description="Day part", type=openapi.TYPE_STRING)
    ],
    operation_summary='뮤직 추천을 위한 사용자 정보 입력.',
    operation_description="장르(리스트), 위도/경도(현재 위치), 도/시/군구(현재위치), "
                          "날씨(맑음/흐림/구름많음), 강수(없음/비/눈/소나기), "
                          "뮤직모드(도로록PICK, 일상, 출근, 퇴근, 여행, 드라이브, 데이트, 친구들과)."
)
@api_view(['GET'])
@csrf_exempt
def get_user_music_info(request):
    if request.method == 'GET':
        try:
            genre = request.GET.getlist('genre', [])  # Query Parameters로 데이터 추출
            lat = request.GET.get('lat')
            lng = request.GET.get('lng')
            region1depthName = request.GET.get('region1depthName')
            region2depthName = request.GET.get('region2depthName')
            region3depthName = request.GET.get('region3depthName')
            skyCondition = request.GET.get('skyCondition')
            precipitationType = request.GET.get('precipitationType')
            MusicMode = request.GET.get('MusicMode')
            DayPart = request.GET.get('dayPart')

            response_data = generate_music_recommendations(
                genre, lat, lng, region1depthName, region2depthName, region3depthName,
                skyCondition, precipitationType, MusicMode, DayPart
            )

            return JsonResponse(response_data, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def generate_music_recommendations(genre, lat, lng, region1depth_name,
                                   region2depth_name, region3depth_name,
                                   sky_condition, precipitation_type, music_mode, Daypart):
    print(genre, lat, lng, region1depth_name, region2depth_name,
          region3depth_name, sky_condition, precipitation_type, music_mode, Daypart)

    test = 'test'
    return {'recommendations': test}
