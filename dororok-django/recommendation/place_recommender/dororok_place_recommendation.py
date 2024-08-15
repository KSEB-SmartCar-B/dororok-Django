import os
import django
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.compose import ColumnTransformer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from recommendation.models import DororokDestination

# 데이터베이스에서 데이터 가져오기 (Django ORM 사용)
# 데이터베이스에서 데이터 가져오기 (Django ORM 사용)
queryset = DororokDestination.objects.all().values('age_range', 'gender', 'region1depth_name', 'region2depth_name')
df = pd.DataFrame(list(queryset))

# 첫 번째 모델: region1depth_name 예측
X1 = df[['age_range', 'gender']]
y1 = df['region1depth_name']

# 범주형 데이터 인코딩
preprocessor1 = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(), [0, 1]),  # 열 이름 대신 인덱스 사용
    ],
    remainder='passthrough'
)

model1 = make_pipeline(preprocessor1, RandomForestClassifier(random_state=42))

X1_train, X1_test, y1_train, y1_test = train_test_split(X1, y1, test_size=0.2, random_state=42)

# 첫 번째 모델 학습
model1.fit(X1_train, y1_train)

# 첫 번째 예측 (region1depth_name)
df['predicted_region1'] = model1.predict(X1)

# 두 번째 모델: region2depth_name 예측
def train_region2_model(df):
    models = {}
    for region1 in df['predicted_region1'].unique():
        df_filtered = df[df['region1depth_name'] == region1]
        if len(df_filtered) < 2:  # 샘플 수가 2보다 적으면 건너뜁니다.
            continue

        X2 = df_filtered[['age_range', 'gender', 'region1depth_name']]
        y2 = df_filtered['region2depth_name']

        preprocessor2 = ColumnTransformer(
            transformers=[
                ('cat', OneHotEncoder(), [0, 1, 2]),  # 열 이름 대신 인덱스 사용
            ],
            remainder='passthrough'
        )

        model2 = make_pipeline(preprocessor2, RandomForestClassifier(random_state=42))

        X2_train, X2_test, y2_train, y2_test = train_test_split(X2, y2, test_size=0.2, random_state=42)

        if len(X2_train) > 0:  # 학습 데이터셋이 충분한 경우에만 학습합니다.
            model2.fit(X2_train, y2_train)
            df.loc[df['region1depth_name'] == region1, 'predicted_region2'] = model2.predict(X2)
            models[region1] = model2

    return df, models

df, model2_dict = train_region2_model(df)


# 예측 함수
def recommend_destination(age_range, gender, top_n=5):
    predicted_region1_probs = model1.predict_proba([[age_range, gender]])[0]
    top_regions1 = model1.classes_[predicted_region1_probs.argsort()[-top_n:][::-1]]  # 상위 N개 지역

    recommendations = []

    for region1 in top_regions1:
        # 두 번째 예측 (region2depth_name)
        model2 = model2_dict.get(region1)
        if model2 is None:
            continue

        X2 = [[age_range, gender, region1]]
        predicted_region2_probs = model2.predict_proba(X2)[0]
        top_regions2 = model2.classes_[predicted_region2_probs.argsort()[-top_n:][::-1]]

        for region2 in top_regions2:
            if df[(df['region1depth_name'] == region1) & (df['region2depth_name'] == region2)].empty:
                continue
            recommendations.append({
                'region1depth_name': region1,
                'region2depth_name': region2,
            })

        if len(recommendations) >= top_n:
            return recommendations[:top_n]

    return recommendations[:top_n]
