import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# 한글 폰트 설정
plt.rcParams['font.family'] = 'AppleGothic'

# 데이터 파일 경로
empty_houses_file = '01_빈집 데이터/연도별 빈집 수와 비율 (수도권_비수도권, 2015-2023).csv'
density_file = '02_인구 분포 데이터/인구밀도/연도별_수도권_비수도권_평균_인구밀도차이.csv'

# 데이터 로드
empty_df = pd.read_csv(empty_houses_file, encoding='utf-8')
density_df = pd.read_csv(density_file, encoding='utf-8')

# 전국 평균 인구밀도 계산 (수도권과 비수도권의 가중 평균)
density_df['전국_평균_인구밀도'] = (density_df['수도권'] + density_df['비수도권']) / 2

# 빈집 데이터에서 전국 총계 계산
empty_pivot = empty_df.pivot(index='연도', columns='지역구분', values='빈집수(호)')
empty_pivot['전국_빈집수'] = empty_pivot.sum(axis=1)
empty_pivot = empty_pivot.reset_index()

# 데이터 병합
merged_df = pd.merge(density_df[['연도', '전국_평균_인구밀도']], 
                    empty_pivot[['연도', '전국_빈집수']], 
                    on='연도')

# 상관계수 계산
correlation = stats.pearsonr(merged_df['전국_평균_인구밀도'], merged_df['전국_빈집수'])

# 그래프 생성
plt.figure(figsize=(10, 6))
sns.regplot(data=merged_df, x='전국_평균_인구밀도', y='전국_빈집수')

plt.title(f'전국 평균 인구밀도와 빈집수의 상관관계 분석 (2015-2023)\nCorrelation: {correlation[0]:.3f} (p-value: {correlation[1]:.3f})')
plt.xlabel('평균 인구밀도 (명/km²)')
plt.ylabel('빈집수 (호)')

# 연도 레이블 추가
for _, row in merged_df.iterrows():
    plt.annotate(str(int(row['연도'])), 
                (row['전국_평균_인구밀도'], row['전국_빈집수']),
                xytext=(5, 5), textcoords='offset points')

plt.tight_layout()
plt.savefig('density_empty_national_correlation.png', dpi=300, bbox_inches='tight')

# 연도별 데이터 출력
print("\n=== 연도별 상세 데이터 ===")
print("\n연도    평균인구밀도    빈집수")
print("--------------------------------")
for _, row in merged_df.sort_values('연도').iterrows():
    print(f"{int(row['연도'])}년: {row['전국_평균_인구밀도']:.1f}명/km²    {int(row['전국_빈집수']):,}호")

# 상관관계 분석 결과 출력
print("\n=== 상관관계 분석 결과 ===")
print(f"상관계수: {correlation[0]:.3f}")
print(f"P-value: {correlation[1]:.3f}")

# 상관관계 해석
print("해석:", end=" ")
if abs(correlation[0]) < 0.3:
    strength = "매우 약한"
elif abs(correlation[0]) < 0.5:
    strength = "약한"
elif abs(correlation[0]) < 0.7:
    strength = "중간 정도의"
elif abs(correlation[0]) < 0.9:
    strength = "강한"
else:
    strength = "매우 강한"
    
direction = "양의" if correlation[0] > 0 else "음의"
significance = "통계적으로 유의미한" if correlation[1] < 0.05 else "통계적으로 유의미하지 않은"

print(f"{significance} {strength} {direction} 상관관계가 있습니다.")

# 추가 통계 분석
print("\n=== 추가 통계 분석 ===")
density_mean = merged_df['전국_평균_인구밀도'].mean()
density_std = merged_df['전국_평균_인구밀도'].std()
empty_mean = merged_df['전국_빈집수'].mean()
empty_std = merged_df['전국_빈집수'].std()

print(f"평균 인구밀도: {density_mean:.1f}명/km² (표준편차: {density_std:.1f})")
print(f"평균 빈집수: {int(empty_mean):,}호 (표준편차: {int(empty_std):,})")

# 연간 변화율 계산
print("\n=== 연간 변화율 ===")
merged_df = merged_df.sort_values('연도')
merged_df['인구밀도_변화율'] = merged_df['전국_평균_인구밀도'].pct_change() * 100
merged_df['빈집수_변화율'] = merged_df['전국_빈집수'].pct_change() * 100

print("\n연도    인구밀도 변화율    빈집수 변화율")
print("----------------------------------------")
for _, row in merged_df.iterrows():
    if pd.notnull(row['인구밀도_변화율']):
        print(f"{int(row['연도'])}년: {row['인구밀도_변화율']:.2f}%    {row['빈집수_변화율']:.2f}%") 