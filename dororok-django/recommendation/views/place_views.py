import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import api_view
from recommendation.place_recommender.dororok_place_recommendation import recommend_region, train_model

@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('ageRange', openapi.IN_QUERY, description='Age range',
                          type=openapi.TYPE_STRING),
        openapi.Parameter('gender', openapi.IN_QUERY, description='Gender',
                          type=openapi.TYPE_STRING),
    ],
    operation_summary="장소 추천을 위한 사용자 정보 입력.",
    operation_description="나이대(10대/20대 etc), 성별(male/female) "

)
@api_view(['GET'])
@csrf_exempt
def get_user_place_info(request):
    if request.method == 'GET':
        try:
            ageRange = request.GET['ageRange']
            gender = request.GET['gender']

            response_data = generate_place_recommendations(
                ageRange, gender
            )
            return JsonResponse(response_data, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def generate_place_recommendations(age_range, gender):
    model = train_model()
    recommendations = recommend_region(model, age_range, gender, top_n=5)
    return {'recommendations': recommendations}


if __name__ == '__main__':
    generate_place_recommendations("TWENTIES", "MALE")

