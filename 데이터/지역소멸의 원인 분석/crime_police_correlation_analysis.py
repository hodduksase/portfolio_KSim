import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns
import numpy as np

# 한글 폰트 설정
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False

# 범죄 데이터 로드
crime_df = pd.read_csv('06_5대 범죄 데이터/(완료)2023년 5대 주요범죄통계.csv', encoding='utf-8')

# 기타 제외하고 시도별 발생건수 합계 계산
crime_sum = crime_df[crime_df['시도'] != '기타'].groupby('시도')['발생건수'].sum().reset_index()
crime_sum = crime_sum.rename(columns={'발생건수': '총_발생건수'})

# 경찰서 수 데이터 로드
police_df = pd.read_csv('위치별_경찰서_수.csv', encoding='cp949')
police_df = police_df.rename(columns={'위치': '시도'})

# 데이터 전처리: 시도 이름 통일
name_mapping = {
    '서울특별시경찰청': '서울특별시',
    '부산광역시경찰청': '부산광역시',
    '대구광역시경찰청': '대구광역시',
    '인천광역시경찰청': '인천광역시',
    '광주광역시경찰청': '광주광역시',
    '대전광역시경찰청': '대전광역시',
    '울산광역시경찰청': '울산광역시',
    '세종특별자치시경찰청': '세종특별자치시',
    '경기도': '경기도',
    '강원특별자치도': '강원특별자치도',
    '충청북도': '충청북도',
    '충청남도': '충청남도',
    '전북특별자치도': '전라북도',
    '전라남도': '전라남도',
    '경상북도': '경상북도',
    '경상남도': '경상남도',
    '제주특별자치도': '제주특별자치도'
}

police_df['시도'] = police_df['시도'].replace(name_mapping)

# 데이터 병합
merged_df = pd.merge(crime_sum, police_df, on='시도', how='inner')

# 상관관계 계산
correlation = stats.pearsonr(merged_df['경찰서_수'], merged_df['총_발생건수'])

# 시각화
plt.figure(figsize=(12, 8))

# 산점도 그리기
sns.scatterplot(data=merged_df, x='경찰서_수', y='총_발생건수', s=100)

# 각 점에 시도 이름 표시
for idx, row in merged_df.iterrows():
    plt.annotate(row['시도'], 
                (row['경찰서_수'], row['총_발생건수']),
                xytext=(5, 5), 
                textcoords='offset points',
                fontsize=8)

# 추세선 추가
z = np.polyfit(merged_df['경찰서_수'], merged_df['총_발생건수'], 1)
p = np.poly1d(z)
plt.plot(merged_df['경찰서_수'], p(merged_df['경찰서_수']), "r--", alpha=0.8)

# 그래프 스타일링
plt.title('시도별 경찰서 수와 5대 범죄 발생건수의 상관관계 (2023년)', pad=20)
plt.xlabel('경찰서 수')
plt.ylabel('범죄 발생건수')

# 격자 추가
plt.grid(True, linestyle='--', alpha=0.7)

# 상관계수 텍스트 추가
plt.text(0.05, 0.95, 
         f'상관계수: {correlation[0]:.4f}\np-value: {correlation[1]:.4f}',
         transform=plt.gca().transAxes,
         bbox=dict(facecolor='white', alpha=0.8))

plt.tight_layout()

# 그래프 저장
plt.savefig('경찰서수_범죄발생_상관관계.png', dpi=300, bbox_inches='tight')

# 결과 출력
print("\n상관관계 분석 결과:")
print(f"상관계수: {correlation[0]:.4f}")
print(f"p-value: {correlation[1]:.4f}")

# 데이터 출력
print("\n시도별 경찰서 수와 범죄 발생건수:")
print(merged_df.sort_values('총_발생건수', ascending=False)) 