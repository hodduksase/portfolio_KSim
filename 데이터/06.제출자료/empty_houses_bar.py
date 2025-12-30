import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 한글 폰트 설정
plt.rcParams['font.family'] = 'AppleGothic'

# 데이터 파일 경로
empty_houses_file = '01_빈집 데이터/연도별 빈집 수와 비율 (수도권_비수도권, 2015-2023).csv'

# 데이터 로드
df = pd.read_csv(empty_houses_file, encoding='utf-8')
df.rename(columns={'지역구분': '구분'}, inplace=True)

# 그래프 설정
plt.figure(figsize=(12, 6))

# 연도 데이터
years = df[df['구분'] == '수도권']['연도'].values
x = np.arange(len(years))
width = 0.35  # 막대 너비

# 수도권과 비수도권 데이터
capital_data = df[df['구분'] == '수도권']['빈집수(호)'].values
non_capital_data = df[df['구분'] == '비수도권']['빈집수(호)'].values

# 막대 그래프 생성
bars1 = plt.bar(x - width/2, capital_data, width, label='수도권', color='skyblue')
bars2 = plt.bar(x + width/2, non_capital_data, width, label='비수도권', color='lightcoral')

# 그래프 꾸미기
plt.xlabel('연도')
plt.ylabel('빈집 수 (호)')
plt.title('연도별 수도권/비수도권 빈집 수')
plt.xticks(x, years, rotation=45)
plt.legend()
plt.grid(True, alpha=0.3)

# 막대 위에 값 표시
def autolabel(bars):
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height):,}',
                ha='center', va='bottom')

autolabel(bars1)
autolabel(bars2)

# 여백 조정
plt.tight_layout()

# 그래프 저장
plt.savefig('empty_houses_bar.png', dpi=300, bbox_inches='tight')

# 통계 출력
print("\n=== 빈집 수 통계 ===")
for region in ['수도권', '비수도권']:
    region_data = df[df['구분'] == region]
    print(f"\n{region}:")
    print(f"평균 빈집 수: {region_data['빈집수(호)'].mean():.0f}호")
    print(f"최대 빈집 수: {region_data['빈집수(호)'].max():.0f}호 ({region_data.loc[region_data['빈집수(호)'].idxmax(), '연도']}년)")
    print(f"최소 빈집 수: {region_data['빈집수(호)'].min():.0f}호 ({region_data.loc[region_data['빈집수(호)'].idxmin(), '연도']}년)") 