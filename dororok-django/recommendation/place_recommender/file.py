import os
import django
import pandas as pd

# Django 프로젝트의 설정 파일을 환경 변수로 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Django 모델 임포트
from recommendation.models import DororokDestination

# Django ORM을 사용하여 모든 데이터를 쿼리합니다
queryset = DororokDestination.objects.all()

# 쿼리셋에서 데이터를 추출하여 Pandas DataFrame으로 변환합니다
data = []
for obj in queryset:
    data.append({
        'age_range': obj.age_range,
        'gender': obj.gender,
        'region1depth_name': obj.region1depth_name,
        'region2depth_name': obj.region2depth_name,
        'region3depth_name': obj.region3depth_name,
    })

df = pd.DataFrame(data)

# DataFrame을 Excel 파일로 저장합니다
df.to_excel('output.xlsx', index=False)

print("데이터가 Excel 파일로 성공적으로 저장되었습니다.")
