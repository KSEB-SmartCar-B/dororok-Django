import os
import django
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.compose import ColumnTransformer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # 'config.settings'를 실제 Django 설정 모듈로 변경
django.setup()

from recommendation.models import DororokDestination


def train_model():
    queryset = DororokDestination.objects.all().values('age_range', 'gender', 'region1depth_name', 'region2depth_name')
    df = pd.DataFrame(list(queryset))

    df['region_full_name'] = df['region1depth_name'] + ' ' + df['region2depth_name']

    x = df[['age_range', 'gender']]
    y = df['region_full_name']

    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(), [0, 1]),
        ],
        remainder='passthrough'
    )

    model = make_pipeline(
        preprocessor,
        RandomForestClassifier(
            n_estimators=500,
            min_samples_split=10,
            min_samples_leaf=2,
            max_features='sqrt',
            max_depth=30,
            bootstrap=True,
            random_state=42
        )
    )
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    model.fit(x_train, y_train)

    return model

def recommend_region(model, age_range, gender, top_n=10):
    X_input = pd.DataFrame([[age_range, gender]], columns=['age_range', 'gender'])
    predicted_probs = model.predict_proba(X_input)[0]
    top_regions = model.classes_[predicted_probs.argsort()][::-1]  # 상위 지역 우선순위로 정렬

    recommendations = []
    for region in top_regions:
        if len(recommendations) >= top_n:
            break
        region1depth_name, region2depth_name = region.split(' ', 1)
        recommendations.append({
            'region1depth_name': region1depth_name,
            'region2depth_name': region2depth_name
        })

    return recommendations[:top_n]