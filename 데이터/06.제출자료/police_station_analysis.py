import pandas as pd

# 한글 폰트 설정
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False

# 데이터 로드
police_df = pd.read_csv('경찰청_전국 경찰서 명칭 및 주소_20230627.csv', encoding='cp949')

# 위치 데이터 정제
location_mapping = {
    '경기도 수원시': '경기도',
    '경기도 의정부시': '경기도',
    '강원특별자치도 춘천시': '강원특별자치도',
    '충청북도 청주시': '충청북도',
    '충청북도청주시': '충청북도',
    '충청남도 예산군': '충청남도',
    '전라북도 전주시': '전북특별자치도',
    '전라남도 무안군': '전라남도',
    '경상북도 안동시': '경상북도',
    '경상남도 창원시': '경상남도',
    '제주특별자치도 제주시': '제주특별자치도'
}

# 위치 데이터 변경
police_df['위치'] = police_df['위치'].replace(location_mapping)

# 위치별 경찰서 수 계산
location_counts = police_df.groupby('위치')['경찰서명칭'].count().sort_values(ascending=False)

# 결과 출력
print("\n위치별 경찰서 수:")
print(location_counts)

# 정제된 데이터를 CSV 파일로 저장
police_df.to_csv('정제된_경찰서_데이터.csv', encoding='cp949', index=False)

# 위치별 경찰서 수 데이터를 CSV 파일로 저장
location_counts.to_frame(name='경찰서_수').to_csv('위치별_경찰서_수.csv', encoding='cp949') 