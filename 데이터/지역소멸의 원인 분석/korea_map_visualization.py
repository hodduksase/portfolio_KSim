import pandas as pd
import folium
from folium import plugins
import json
import requests
import io
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 데이터 읽기
df = pd.read_csv('연도별_시군구_전입률_전출률_2013_2024 - 완료.csv')

# 수도권 지역 정의
capital_area = ['서울특별시', '경기도', '인천광역시']

# 수도권/비수도권 구분
df['region_type'] = df['시도'].apply(lambda x: '수도권' if x in capital_area else '비수도권')

# 2024년 데이터만 선택
df_2024 = df[df['연도'] == 2024].copy()

# 시도별 데이터 집계
region_data = df_2024.groupby('시도')[['전입', '전출']].sum().reset_index()
region_data['순이동'] = region_data['전입'] - region_data['전출']

# 대한민국 시도 경계 데이터 다운로드
url = "https://raw.githubusercontent.com/southkorea/southkorea-maps/master/kostat/2013/json/skorea-provinces-2013-geo.json"
response = requests.get(url)
korea_geo = json.loads(response.text)

# 지도 생성
m = folium.Map(location=[36.5, 127.5], zoom_start=7)

# 색상 스케일 생성
max_value = region_data['순이동'].abs().max()
min_value = -max_value

# 시도별 색상 매핑
def get_color(value):
    if value > 0:
        return '#ff9999'  # 양수: 빨간색 계열
    else:
        return '#99ccff'  # 음수: 파란색 계열

# 시도별 데이터 시각화
for feature in korea_geo['features']:
    sido_name = feature['properties']['name']
    sido_data = region_data[region_data['시도'] == sido_name]
    
    if not sido_data.empty:
        value = sido_data['순이동'].values[0]
        color = get_color(value)
        
        # 팝업 내용 생성
        popup_text = f"""
        <b>{sido_name}</b><br>
        전입: {sido_data['전입'].values[0]:,.0f}명<br>
        전출: {sido_data['전출'].values[0]:,.0f}명<br>
        순이동: {value:,.0f}명
        """
        
        # 지도에 시도 경계 추가
        folium.GeoJson(
            feature,
            style_function=lambda x, color=color: {
                'fillColor': color,
                'color': 'black',
                'weight': 1,
                'fillOpacity': 0.7
            },
            popup=folium.Popup(popup_text, max_width=300)
        ).add_to(m)

# 범례 추가
legend_html = """
<div style="position: fixed; 
            bottom: 50px; right: 50px; width: 150px; height: 90px; 
            border:2px solid grey; z-index:9999; background-color:white;
            padding: 10px;
            font-size:14px;
            ">
    <p><strong>순이동 인구</strong></p>
    <p><span style="color:#ff9999;">■</span> 순유입</p>
    <p><span style="color:#99ccff;">■</span> 순유출</p>
</div>
"""
m.get_root().html.add_child(folium.Element(legend_html))

# 지도 저장
m.save('korea_migration_map.html')

# 추가: 시도별 순이동 막대 그래프
plt.figure(figsize=(15, 8))
sns.barplot(data=region_data.sort_values('순이동', ascending=False), 
            x='시도', y='순이동', 
            palette=['#ff9999' if x > 0 else '#99ccff' for x in region_data.sort_values('순이동', ascending=False)['순이동']])

plt.title('2024년 시도별 순이동 인구', fontsize=14, pad=20)
plt.xticks(rotation=45)
plt.ylabel('순이동 인구 수')
plt.grid(True, axis='y', linestyle='--', alpha=0.7)

# 막대 위에 값 표시
for i, v in enumerate(region_data.sort_values('순이동', ascending=False)['순이동']):
    plt.text(i, v, f'{v:,.0f}', ha='center', va='bottom' if v > 0 else 'top')

plt.tight_layout()
plt.savefig('region_migration_bar.png', dpi=300, bbox_inches='tight')
plt.close() 