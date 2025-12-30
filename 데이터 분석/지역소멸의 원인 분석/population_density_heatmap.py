import pandas as pd
import folium
from folium.plugins import HeatMap
import json
import requests
import io
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os

# 데이터 읽기
df = pd.read_csv('(완료)연도v4.csv')

# 연령대가 '합계'인 데이터만 사용하고, 전국 제외
filtered = df[(df['연령대'] == '합계') & (df['시도'] != '전국')]

# 2023년 데이터만 사용
latest_data = filtered[filtered['연도'] == 2023].copy() # SettingWithCopyWarning 방지를 위해 .copy() 사용

# 인구밀도 최대값 계산 (2023년 데이터 기준)
max_density_2023 = latest_data['인구밀도'].max()

# 시도별 중심 좌표 (위도, 경도)
sido_coords = {
    '서울특별시': [37.5665, 126.9780],
    '부산광역시': [35.1796, 129.0756],
    '대구광역시': [35.8714, 128.6014],
    '인천광역시': [37.4563, 126.7052],
    '광주광역시': [35.1595, 126.8526],
    '대전광역시': [36.3504, 127.3845],
    '울산광역시': [35.5384, 129.3114],
    '세종특별자치시': [36.4801, 127.2892],
    '경기도': [37.4138, 127.5183],
    '강원도': [37.8228, 128.1555],
    '충청북도': [36.6357, 127.4915],
    '충청남도': [36.6588, 126.6728],
    '전라북도': [35.8242, 127.1480],
    '전라남도': [34.8161, 126.4629],
    '경상북도': [36.5760, 128.5059],
    '경상남도': [35.2382, 128.6924],
    '제주특별자치도': [33.4996, 126.5312]
}

# 히트맵 데이터 준비
heat_data = []
for _, row in latest_data.iterrows():
    sido = row['시도']
    if sido in sido_coords:
        lat, lon = sido_coords[sido]
        density = row['인구밀도']
        # 인구밀도에 따라 가중치 조정 (최대값 기준 스케일링)
        weight = density / max_density_2023
        heat_data.append([lat, lon, weight])

# 대한민국 중심으로 지도 생성
m = folium.Map(location=[36.5, 127.5], zoom_start=7)

# 히트맵 레이어 추가
HeatMap(heat_data, 
        min_opacity=0.3,
        max_val=1.0, # 가중치가 0~1 사이로 스케일링되었으므로 max_val=1.0
        radius=25, 
        blur=15, 
        gradient={0.0: 'blue', 0.4: 'lime', 0.65: 'yellow', 1.0: 'red'} # 그라데이션 조정
).add_to(m)

# 시도별 마커와 팝업 추가
for _, row in latest_data.iterrows():
    sido = row['시도']
    if sido in sido_coords:
        lat, lon = sido_coords[sido]
        density = row['인구밀도']
        folium.CircleMarker(
            location=[lat, lon],
            radius=8,
            popup=f'{sido}<br>인구밀도: {density:.1f}명/km²',
            color='black',
            fill=True,
            fill_color='white',
            fill_opacity=0.7
        ).add_to(m)

# 지도 저장 (HTML)
html_file_path = 'korea_population_density_heatmap.html'
m.save(html_file_path)

# Selenium을 사용하여 HTML을 PNG로 변환
png_file_path = 'korea_population_density_heatmap.png'

# Chrome headless 모드 설정
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox') # Linux 환경에서 필요할 수 있음
options.add_argument('--disable-dev-shm-usage') # Linux 환경에서 필요할 수 있음

# 웹 드라이버 설정 및 실행
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# HTML 파일 열기
# 로컬 파일 경로를 URL 형식으로 변환해야 함
html_url = 'file://' + os.path.abspath(html_file_path).replace('\\', '/')
driver.get(html_url)

# 페이지 로딩 대기 (필요에 따라 조정)
driver.implicitly_wait(10) 

# 스크린샷 저장
driver.save_screenshot(png_file_path)

# 드라이버 종료
driver.quit()

print(f"HTML 파일 저장됨: {html_file_path}")
print(f"PNG 파일 저장됨: {png_file_path}") 