import pandas as pd
import matplotlib.pyplot as plt

# 한글 폰트 설정
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False

# 데이터 로드
empty_df = pd.read_csv('01_빈집 데이터/연도별 빈집 수와 비율 (수도권_비수도권, 2015-2023).csv', encoding='utf-8')

# 수도권과 비수도권 데이터 분리
capital_data = empty_df[empty_df['지역구분'] == '수도권']
noncapital_data = empty_df[empty_df['지역구분'] == '비수도권']

# 선 그래프 생성
plt.figure(figsize=(15, 8))

# 선 그래프 그리기
plt.plot(capital_data['연도'], capital_data['빈집비율(%)'], 
         marker='o', linewidth=2, markersize=8, 
         color='skyblue', label='수도권')
plt.plot(noncapital_data['연도'], noncapital_data['빈집비율(%)'], 
         marker='s', linewidth=2, markersize=8, 
         color='lightcoral', label='비수도권')

# 그래프 스타일링
plt.title('연도별 수도권/비수도권 빈집 비율 (2015-2023)', pad=20, size=14)
plt.xlabel('연도', size=12)
plt.ylabel('빈집 비율(%)', size=12)

# 범례 추가
plt.legend(loc='upper left')

# 격자 추가
plt.grid(True, linestyle='--', alpha=0.7)

# 각 포인트에 값 표시
for year, ratio in zip(capital_data['연도'], capital_data['빈집비율(%)']):
    plt.text(year, ratio-0.3, f'{ratio}%', ha='center', va='top')
for year, ratio in zip(noncapital_data['연도'], noncapital_data['빈집비율(%)']):
    plt.text(year, ratio+0.3, f'{ratio}%', ha='center', va='bottom')

# y축 범위 설정
plt.ylim(0, 15)

# 여백 조정
plt.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.9)

# 그래프 저장
plt.savefig('연도별_수도권_비수도권_빈집비율_선그래프.png', dpi=300, bbox_inches='tight')

# 결과 출력
print("\n연도별 수도권/비수도권 빈집 비율(%):")
print(empty_df.pivot_table(index='연도', columns='지역구분', values='빈집비율(%)', aggfunc='first')) 