import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 데이터 읽기
df = pd.read_csv('연도별_시군구_전입률_전출률_2013_2024 - 완료.csv')

# 수도권 지역 정의
capital_area = ['서울특별시', '경기도', '인천광역시']

# 수도권/비수도권 구분
df['region_type'] = df['시도'].apply(lambda x: '수도권' if x in capital_area else '비수도권')

# 연도별 수도권-비수도권 간 이동 데이터 집계
migration_data = df.groupby(['연도', 'region_type'])[['전입', '전출']].sum().reset_index()

# 1. 수도권-비수도권 간 이동 현황 시각화
plt.figure(figsize=(15, 8))

# 수도권에서 비수도권으로의 이동
capital_to_non = migration_data[migration_data['region_type'] == '수도권']['전출'].values
# 비수도권에서 수도권으로의 이동
non_to_capital = migration_data[migration_data['region_type'] == '비수도권']['전출'].values

years = migration_data['연도'].unique()
x = np.arange(len(years))
width = 0.35

plt.bar(x - width/2, capital_to_non, width, label='수도권→비수도권', color='skyblue', alpha=0.7)
plt.bar(x + width/2, non_to_capital, width, label='비수도권→수도권', color='lightcoral', alpha=0.7)

plt.xlabel('연도', fontsize=12)
plt.ylabel('이동 인구 수', fontsize=12)
plt.title('수도권-비수도권 간 인구이동 현황 (2013-2024)', fontsize=14, pad=20)
plt.xticks(x, years, rotation=45)
plt.legend(fontsize=10)
plt.grid(True, axis='y', linestyle='--', alpha=0.7)

# 막대 위에 값 표시
for i, v in enumerate(capital_to_non):
    plt.text(i - width/2, v, f'{v:,.0f}', ha='center', va='bottom', fontsize=8)
for i, v in enumerate(non_to_capital):
    plt.text(i + width/2, v, f'{v:,.0f}', ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.savefig('population_migration.png', dpi=300, bbox_inches='tight')
plt.close()

# 2. 순이동 현황 시각화
migration_data['순이동'] = migration_data['전입'] - migration_data['전출']

plt.figure(figsize=(15, 8))

for region in ['수도권', '비수도권']:
    region_data = migration_data[migration_data['region_type'] == region]
    plt.plot(region_data['연도'], region_data['순이동'], 
             marker='o', label=f'{region} 순이동', linewidth=2)

plt.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
plt.xlabel('연도', fontsize=12)
plt.ylabel('순이동 인구 수', fontsize=12)
plt.title('수도권-비수도권 순이동 현황 (2013-2024)', fontsize=14, pad=20)
plt.xticks(rotation=45)
plt.legend(fontsize=10)
plt.grid(True, linestyle='--', alpha=0.7)

# 데이터 포인트에 값 표시
for region in ['수도권', '비수도권']:
    region_data = migration_data[migration_data['region_type'] == region]
    for x, y in zip(region_data['연도'], region_data['순이동']):
        plt.text(x, y, f'{y:,.0f}', ha='center', va='bottom' if y > 0 else 'top', fontsize=8)

plt.tight_layout()
plt.savefig('net_migration.png', dpi=300, bbox_inches='tight')
plt.close()

# 3. 이동률 추이 시각화
migration_data['이동률'] = (migration_data['순이동'] / migration_data['전입']) * 100

plt.figure(figsize=(15, 8))

for region in ['수도권', '비수도권']:
    region_data = migration_data[migration_data['region_type'] == region]
    plt.plot(region_data['연도'], region_data['이동률'], 
             marker='o', label=f'{region} 이동률', linewidth=2)

plt.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
plt.xlabel('연도', fontsize=12)
plt.ylabel('이동률 (%)', fontsize=12)
plt.title('수도권-비수도권 이동률 추이 (2013-2024)', fontsize=14, pad=20)
plt.xticks(rotation=45)
plt.legend(fontsize=10)
plt.grid(True, linestyle='--', alpha=0.7)

# 데이터 포인트에 값 표시
for region in ['수도권', '비수도권']:
    region_data = migration_data[migration_data['region_type'] == region]
    for x, y in zip(region_data['연도'], region_data['이동률']):
        plt.text(x, y, f'{y:.1f}%', ha='center', va='bottom' if y > 0 else 'top', fontsize=8)

plt.tight_layout()
plt.savefig('migration_rate.png', dpi=300, bbox_inches='tight')
plt.close() 