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

# 막대 그래프 생성
plt.figure(figsize=(15, 8))

# 쌓아올린 막대 그래프 생성
bars1 = plt.bar(capital_data['연도'], capital_data['빈집수(호)'], 
                color='skyblue', label='수도권')
bars2 = plt.bar(noncapital_data['연도'], noncapital_data['빈집수(호)'], 
                bottom=capital_data['빈집수(호)'], color='lightcoral', label='비수도권')

# 그래프 스타일링
plt.title('연도별 수도권/비수도권 빈집 수 (2015-2023)', pad=20, size=14)
plt.xlabel('연도', size=12)
plt.ylabel('빈집 수(호)', size=12)

# 범례 추가
plt.legend(loc='upper left')

# 격자 추가
plt.grid(True, linestyle='--', alpha=0.7, axis='y')

# 각 영역에 값 표시
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., bar.get_y() + height/2.,
                f'{int(height):,}',
                ha='center', va='center')

# 전체 합계 값 표시
for i in range(len(capital_data)):
    total = capital_data['빈집수(호)'].iloc[i] + noncapital_data['빈집수(호)'].iloc[i]
    plt.text(capital_data['연도'].iloc[i], total + 300, 
             f'총 {int(total):,}', ha='center', va='bottom')

# 여백 조정
plt.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.9)

# 그래프 저장
plt.savefig('연도별_수도권_비수도권_빈집수_그래프.png', dpi=300, bbox_inches='tight')

# 결과 출력
print("\n연도별 수도권/비수도권 빈집 수:")
print(empty_df.pivot_table(index='연도', columns='지역구분', values='빈집수(호)', aggfunc='sum'))

# CSV 파일로 저장
empty_df.to_csv('연도별_수도권_비수도권_빈집수.csv', encoding='utf-8-sig', index=False) 