import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import numpy as np

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 데이터 읽기
df = pd.read_csv('★ 빈집과 범죄율 비교_2023.csv')

# 도시/농촌 구분
df['지역구분'] = df['행정구역'].apply(lambda x: '도시' if '시' in x else '농촌')

# 도시/농촌별 통계
urban_rural_stats = df.groupby('지역구분').agg({
    '빈집비율(%)': ['mean', 'std'],
    '범죄율(건/천명)': ['mean', 'std'],
    '행정구역': 'count'
}).round(2)

print("\n도시/농촌별 통계:")
print(urban_rural_stats)

# 도시/농촌별 T-검정
urban_crime = df[df['지역구분'] == '도시']['범죄율(건/천명)']
rural_crime = df[df['지역구분'] == '농촌']['범죄율(건/천명)']
t_stat, p_value = stats.ttest_ind(urban_crime, rural_crime)

print(f"\n도시/농촌 범죄율 차이 T-검정 결과:")
print(f"t-statistic: {t_stat:.3f}")
print(f"p-value: {p_value:.3f}")

# 산점도 그리기 (도시/농촌 구분)
plt.figure(figsize=(15, 10))
sns.scatterplot(data=df, x='빈집비율(%)', y='범죄율(건/천명)', 
                hue='지역구분', style='지역구분', alpha=0.6)

# 회귀선 추가 (도시/농촌별)
sns.regplot(data=df[df['지역구분'] == '도시'], 
            x='빈집비율(%)', y='범죄율(건/천명)', 
            scatter=False, color='blue', label='도시')
sns.regplot(data=df[df['지역구분'] == '농촌'], 
            x='빈집비율(%)', y='범죄율(건/천명)', 
            scatter=False, color='red', label='농촌')

# 각 점에 시도와 행정구역 표시
for idx, row in df.iterrows():
    plt.annotate(f"{row['시도']} {row['행정구역']}", 
                (row['빈집비율(%)'], row['범죄율(건/천명)']),
                xytext=(5, 5), textcoords='offset points',
                fontsize=8, alpha=0.7)

# 그래프 제목과 레이블 설정
plt.title('도시/농촌별 빈집률과 범죄율의 상관관계 분석', pad=20, fontsize=14)
plt.xlabel('빈집률 (%)', fontsize=12)
plt.ylabel('범죄율 (건/천명)', fontsize=12)

# 분석 결과 텍스트 추가
textstr = f'도시/농촌 범죄율 차이 p-value: {p_value:.3f}'
plt.text(0.05, 0.95, textstr, transform=plt.gca().transAxes, 
         bbox=dict(facecolor='white', alpha=0.8),
         verticalalignment='top', fontsize=12)

# 그래프 저장
plt.tight_layout()
plt.savefig('도시농촌_빈집률_범죄율_상관관계.png', dpi=300, bbox_inches='tight')
plt.close()

# 박스플롯 그리기
plt.figure(figsize=(12, 6))
sns.boxplot(data=df, x='지역구분', y='범죄율(건/천명)')
plt.title('도시/농촌별 범죄율 분포', pad=20, fontsize=14)
plt.xlabel('지역구분', fontsize=12)
plt.ylabel('범죄율 (건/천명)', fontsize=12)
plt.tight_layout()
plt.savefig('도시농촌_범죄율_분포.png', dpi=300, bbox_inches='tight')
plt.close()

# 결과 출력
print("\n도시/농촌별 상관계수:")
urban_corr = df[df['지역구분'] == '도시']['빈집비율(%)'].corr(df[df['지역구분'] == '도시']['범죄율(건/천명)'])
rural_corr = df[df['지역구분'] == '농촌']['빈집비율(%)'].corr(df[df['지역구분'] == '농촌']['범죄율(건/천명)'])
print(f"도시 지역 상관계수: {urban_corr:.3f}")
print(f"농촌 지역 상관계수: {rural_corr:.3f}") 