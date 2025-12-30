import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import numpy as np

# 한글 폰트 설정
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False

# 데이터 로드
crime_df = pd.read_csv('06_5대 범죄 데이터/2023년 5대 주요범죄통계.csv')
police_df = pd.read_csv('05_범죄예방설계(CPTED) 데이터/경찰서 데이터/police_stations_stats.csv')

# 시도별 범죄 발생 건수 합계 계산
crime_by_region = crime_df.groupby('시도')['발생건수'].sum().reset_index()

# 경찰서 데이터의 컬럼명 변경
police_df.columns = ['시도', '경찰서수']

# 데이터 병합
merged_df = pd.merge(crime_by_region, police_df, on='시도', how='inner')

# 상관관계 계산
correlation = stats.pearsonr(merged_df['발생건수'], merged_df['경찰서수'])
print(f'상관계수: {correlation[0]:.4f}')
print(f'p-value: {correlation[1]:.4f}')

# 시각화
plt.figure(figsize=(12, 8))

# 산점도 그리기
sns.scatterplot(data=merged_df, x='경찰서수', y='발생건수', s=100)

# 각 점에 시도 이름 표시
for idx, row in merged_df.iterrows():
    plt.annotate(row['시도'], 
                (row['경찰서수'], row['발생건수']),
                xytext=(5, 5), 
                textcoords='offset points',
                fontsize=8)

# 추세선 추가
z = np.polyfit(merged_df['경찰서수'], merged_df['발생건수'], 1)
p = np.poly1d(z)
plt.plot(merged_df['경찰서수'], p(merged_df['경찰서수']), "r--", alpha=0.8)

# 그래프 스타일링
plt.title('시도별 경찰서 수와 5대 범죄 발생건수의 관계 (2023년)', pad=20)
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
plt.savefig('crime_police_correlation.png', dpi=300, bbox_inches='tight')

# 데이터 출력
print("\n시도별 경찰서 수와 범죄 발생건수:")
merged_df['범죄율'] = merged_df['발생건수'] / merged_df['경찰서수']
print(merged_df.sort_values('범죄율', ascending=False)[['시도', '발생건수', '경찰서수', '범죄율']]) 