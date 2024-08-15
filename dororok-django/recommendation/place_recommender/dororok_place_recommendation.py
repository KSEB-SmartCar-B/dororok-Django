import os
import django
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.compose import ColumnTransformer

# Django 설정 초기화
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # 'config.settings'를 실제 Django 설정 모듈로 변경
django.setup()

from recommendation.models import DororokDestination  # DororokDestination 모델 가져오기

# 데이터베이스에서 데이터 가져오기 (Django ORM 사용)
queryset = DororokDestination.objects.all().values('age_range', 'gender', 'region1depth_name', 'region2depth_name')
df = pd.DataFrame(list(queryset))

# region1depth_name과 region2depth_name을 공백으로 합친 새로운 컬럼 생성
df['region_full_name'] = df['region1depth_name'] + ' ' + df['region2depth_name']

# 첫 번째 모델: region_full_name 예측
X = df[['age_range', 'gender']]
y = df['region_full_name']

# 범주형 데이터 인코딩
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(), [0, 1]),  # 열 이름 대신 인덱스 사용
    ],
    remainder='passthrough'
)

model = make_pipeline(preprocessor, RandomForestClassifier(random_state=42))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 모델 학습
model.fit(X_train, y_train)

# 예측 함수
def recommend_full_region(age_range, gender, top_n=10):
    X_input = pd.DataFrame([[age_range, gender]], columns=['age_range', 'gender'])
    predicted_probs = model.predict_proba(X_input)[0]
    top_regions = model.classes_[predicted_probs.argsort()][::-1]  # 상위 지역 우선순위로 정렬

    recommendations = []
    for region in top_regions:
        if len(recommendations) >= top_n:
            break
        recommendations.append(region)

    return recommendations[:top_n]

if __name__ == '__main__':
    # 예시 예측
    predicted_destinations = recommend_full_region('TWENTIES', 'MALE', top_n=10)
    for i, destination in enumerate(predicted_destinations, 1):
        print(f"추천된 목적지 {i}: {destination}")
