import pandas as pd

# Define the standard regions
STANDARD_REGIONS = [
    '서울특별시',
    '부산광역시',
    '대구광역시',
    '인천광역시',
    '광주광역시',
    '대전광역시',
    '울산광역시',
    '세종특별자치시',
    '경기도',
    '강원특별자치도',
    '충청북도',
    '충청남도',
    '전북특별자치도',
    '전라남도',
    '경상북도',
    '경상남도',
    '제주특별자치도'
]

def get_sigungu_to_sido_map():
    # 시군구명 → 시도명 매핑 딕셔너리 생성
    sigungu_map = {}
    try:
        df = pd.read_csv('의료기관_현황_2025년_3월_시군구별.csv', encoding='utf-8')
        for _, row in df.iterrows():
            sido = row['시도코드명']
            sigungu = row['시군구코드명']
            sigungu_map[sigungu.replace(' ', '')] = sido.replace(' ', '')
    except FileNotFoundError:
        print("Error: 의료기관_현황_2025년_3월_시군구별.csv not found.")
        # Fallback or error handling if mapping file is missing
        pass # Or handle appropriately
    except Exception as e:
        print(f"Error reading mapping file: {e}")
        pass
    return sigungu_map

sigungu_to_sido = get_sigungu_to_sido_map()

# 시도명 표준화 함수

def standardize_region_name(region):
    if not isinstance(region, str):
        return ''
    region = region.strip()

    # 1. 표준 시도명 직접 매칭
    for std in STANDARD_REGIONS:
        if std.replace('특별자치도','').replace('광역시','').replace('특별시','').replace('도','') in region.replace(' ',''):
            return std
    
    # 2. 약어 처리 (예: 경기 -> 경기도)
    if '경기' in region: return '경기도'
    if '강원' in region: return '강원특별자치도'
    if '충북' in region: return '충청북도'
    if '충남' in region: return '충청남도'
    if '전북' in region or '전라북도' in region: return '전북특별자치도'
    if '전남' in region: return '전라남도'
    if '경북' in region: return '경상북도'
    if '경남' in region: return '경상남도'
    if '서울' in region: return '서울특별시'
    if '부산' in region: return '부산광역시'
    if '대구' in region: return '대구광역시'
    if '인천' in region: return '인천광역시'
    if '광주' in region: return '광주광역시'
    if '대전' in region: return '대전광역시'
    if '울산' in region: return '울산광역시'
    if '세종' in region: return '세종특별자치시' # 또는 '세종시'도 고려
    if '제주' in region: return '제주특별자치도'

    # 3. 시군구명으로 시도명 매핑
    region_key = region.replace(' ', '')
    if region_key in sigungu_to_sido:
        sido = sigungu_to_sido[region_key]
        # 매핑된 시도명 표준화
        for std in STANDARD_REGIONS:
            if std.startswith(sido[:2]): # 앞 두 글자로 매칭 (예: 전북 -> 전북특별자치도)
                return std

    return ''

def process_police_stations():
    # Read the police station data with proper encoding
    # Using the specified file: 경찰청_전국 지구대 파출소 주소 현황_20231231.csv
    df = pd.read_csv('경찰청_전국 지구대 파출소 주소 현황_20231231.csv', encoding='cp949')
    
    # Rename columns based on inspection:
    # Assuming columns are: [col1, col2, col3, col4, col5, '주소']
    # The last column is assumed to be '주소'.
    # We will extract region from the '주소' column.

    # Extract region from address (assuming address is the last column)
    # Use column index -1 to safely access the last column
    df['지역'] = df.iloc[:, -1].apply(lambda x: x.split()[0] if isinstance(x, str) else '')

    # 주소 기준으로 중복 제거 (경찰서 본청과 지구대/파출소 포함 데이터이므로 중복 제거 필요)
    # '주소' 컬럼명을 동적으로 가져오거나, 안전하게 인덱스 사용
    address_col_name = df.columns[-1]
    df = df.drop_duplicates(subset=[address_col_name])
    
    # Standardize region names using the existing function
    df['표준지역'] = df['지역'].apply(standardize_region_name)
    
    # Remove rows with empty or invalid standardized region names
    df = df[df['표준지역'].isin(STANDARD_REGIONS)]
    
    # Group by standardized region names and count the number of police stations
    grouped_df = df.groupby('표준지역').size().reset_index(name='경찰서 수')

    # Ensure all standard regions are present, even if count is 0
    for region in STANDARD_REGIONS:
        if region not in grouped_df['표준지역'].values:
            grouped_df = pd.concat([grouped_df, pd.DataFrame({
                '표준지역': [region],
                '경찰서 수': [0]
            })], ignore_index=True)
    
    # Sort by the standard region order
    region_order = {region: idx for idx, region in enumerate(STANDARD_REGIONS)}
    grouped_df['order'] = grouped_df['표준지역'].map(region_order)
    grouped_df = grouped_df.sort_values('order').drop('order', axis=1)
    
    # Save the processed data
    grouped_df.to_csv('경찰서_지역별_현황.csv', index=False, encoding='utf-8-sig')
    print("Data processing completed. Results saved to '경찰서_지역별_현황.csv'")

if __name__ == "__main__":
    # sigungu_to_sido = get_sigungu_to_sido_map() # 주소 파싱 안하므로 필요 없음
    process_police_stations() 