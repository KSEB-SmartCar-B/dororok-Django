import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.compose import ColumnTransformer

# CSV 파일에서 데이터 가져오기
df = pd.read_csv('augmented_output.csv')  # 'cp949' 또는 'ISO-8859-1'로 시도

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
def train_region2_model(input_df):
    models = {}
    # 각 region1depth_name별 region2depth_name의 데이터 분포 확인
    for region1 in df['region1depth_name'].unique():
        df_filtered = df[df['region1depth_name'] == region1]
        print(f"Region1: {region1}")
        print(df_filtered['region2depth_name'].value_counts())
        print("="*50)

        if len(df_filtered) < 1:
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

        if len(X2_train) > 0:
            model2.fit(X2_train, y2_train)
            input_df.loc[input_df['region1depth_name'] == region1, 'predicted_region2'] = model2.predict(X2)
            models[region1] = model2
            print(f"Trained model for region1: {region1}, Model classes: {model2.classes_}")
        else:
            print(f"Not enough data to train model for region1: {region1}")

    return input_df, models

# 모델 학습
df, model2_dict = train_region2_model(df)
print(f"Trained models: {model2_dict.keys()}")

# 예측 함수
def recommend_destination(age_range, gender, top_n=10):
    predicted_region1_probs = model1.predict_proba(pd.DataFrame([[age_range, gender]], columns=['age_range', 'gender']))[0]
    top_regions1 = model1.classes_[predicted_region1_probs.argsort()][::-1]  # 상위 지역 우선순위로 정렬

    recommendations = []

    for region1 in top_regions1:
        print(f"Processing region1: {region1}")
        model2 = model2_dict.get(region1)
        if model2 is None:
            print(f"No model found for region1: {region1}")
            continue
        else:
            print(f"Model found for region1: {region1}")

        X2 = pd.DataFrame([[age_range, gender, region1]], columns=['age_range', 'gender', 'region1depth_name'])
        predicted_region2_probs = model2.predict_proba(X2)[0]
        top_regions2 = model2.classes_[predicted_region2_probs.argsort()][::-1]
        print(f"Top regions2 for region1 {region1}: {top_regions2}")

        for region2 in top_regions2:
            print(f"Processing region2: {region2}")
            if df[(df['region1depth_name'] == region1) & (df['region2depth_name'] == region2)].empty:
                continue
            recommendations.append({
                'region1depth_name': region1,
                'region2depth_name': region2,
            })

            if len(recommendations) >= top_n:
                return recommendations[:top_n]

    # 여전히 10개를 채우지 못했을 경우 남은 지역들로 채우기
    if len(recommendations) < top_n:
        for region1 in top_regions1:
            model2 = model2_dict.get(region1)
            if model2 is None:
                continue

            X2 = pd.DataFrame([[age_range, gender, region1]], columns=['age_range', 'gender', 'region1depth_name'])
            predicted_region2_probs = model2.predict_proba(X2)[0]
            top_regions2 = model2.classes_[predicted_region2_probs.argsort()][::-1]

            for region2 in top_regions2:
                if len(recommendations) >= top_n:
                    break
                recommendations.append({
                    'region1depth_name': region1,
                    'region2depth_name': region2,
                })

    return recommendations[:top_n]

if __name__ == '__main__':
    # 예시 예측
    predicted_destinations = recommend_destination('TWENTIES', 'FEMALE', top_n=10)
    for i, destination in enumerate(predicted_destinations, 1):
        print(f"추천된 목적지 {i}: {destination}")
