import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# CSV 파일들 읽기 (인코딩 지정)
crime_df = pd.read_csv('5대 범죄.csv', encoding='utf-8')
cctv_df = pd.read_csv('통합_시도별_CCTV_현황 (2024년 기준).csv', encoding='cp949')

# '기타' 시도 제외 및 제주특별자치도 이름 수정
crime_df = crime_df[crime_df['시도'] != '기타']
crime_df.loc[crime_df['시도'] == '제주특별자치도', '시도'] = '제주'
crime_df.loc[(crime_df['시도'] == '제주') & (crime_df['시군구'] == '시'), '시군구'] = '제주시'

# 두 데이터프레임을 시도와 시군구 기준으로 조인
merged_df = pd.merge(crime_df, cctv_df, 
                    on=['시도', '시군구'], 
                    how='inner')

# 상관관계 분석
correlation = merged_df['발생건수'].corr(merged_df['CCTV 수'])
r_squared = correlation ** 2

# 회귀분석
slope, intercept, r_value, p_value, std_err = stats.linregress(merged_df['CCTV 수'], merged_df['발생건수'])

# 시각화
plt.figure(figsize=(10, 6))
plt.scatter(merged_df['CCTV 수'], merged_df['발생건수'], alpha=0.5)
plt.plot(merged_df['CCTV 수'], intercept + slope * merged_df['CCTV 수'], 'r', label='회귀선')

plt.xlabel('CCTV 수')
plt.ylabel('범죄 발생건수')
plt.title('CCTV 수와 범죄 발생건수의 상관관계')

# 그래프에 도시 이름 표시
for i, txt in enumerate(merged_df['시군구']):
    plt.annotate(txt, (merged_df['CCTV 수'].iloc[i], merged_df['발생건수'].iloc[i]))

plt.legend()
plt.savefig('상관관계_분석.png')
plt.close()

# 결과 출력
print("\n=== 상관관계 분석 결과 ===")
print(f"1. Pearson 상관계수: {correlation:.4f}")
print(f"2. 결정계수(R²): {r_squared:.4f}")
print(f"3. P-value: {p_value:.4f}")

print("\n각 시군구별 CCTV 수와 범죄 발생건수:")
print(merged_df[['시도', '시군구', 'CCTV 수', '발생건수']].sort_values('발생건수', ascending=False))

# 결과를 새로운 CSV 파일로 저장
merged_df.to_csv('범죄_CCTV_통합.csv', index=False, encoding='utf-8-sig')

print("두 데이터가 통합되어 '범죄_CCTV_통합.csv' 파일로 저장되었습니다.")
print("\n통합된 데이터 미리보기:")
print(merged_df.head(10))

# 조인 결과 통계 출력
print("\n데이터 통합 결과:")
print(f"- 범죄 데이터 수: {len(crime_df)}개")
print(f"- CCTV 데이터 수: {len(cctv_df)}개")
print(f"- 통합된 데이터 수: {len(merged_df)}개") 