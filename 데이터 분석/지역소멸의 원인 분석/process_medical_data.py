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

def standardize_region_name(region):
    # Handle special cases
    if '경기도' in region:
        return '경기도'
    if '강원' in region:
        return '강원특별자치도'
    if '전북' in region:
        return '전북특별자치도'
    if '전라북도' in region:
        return '전북특별자치도'
    if '전라남도' in region:
        return '전라남도'
    if '충북' in region:
        return '충청북도'
    if '충남' in region:
        return '충청남도'
    if '경북' in region:
        return '경상북도'
    if '경남' in region:
        return '경상남도'
    return region

def process_medical_data():
    # Read the medical facility data
    df = pd.read_csv('의료기관_현황_2025년_3월_광역시도별.csv')
    
    # Standardize region names
    df['시도코드명'] = df['시도코드명'].apply(standardize_region_name)
    
    # Group by standardized region names and sum the values
    grouped_df = df.groupby('시도코드명').sum().reset_index()
    
    # Ensure all standard regions are present
    for region in STANDARD_REGIONS:
        if region not in grouped_df['시도코드명'].values:
            grouped_df = pd.concat([grouped_df, pd.DataFrame({
                '시도코드명': [region],
                '상급종합병원 수': [0],
                '종합병원 수': [0],
                '한의원 수': [0],
                '의원 수': [0]
            })], ignore_index=True)
    
    # Sort by the standard region order
    region_order = {region: idx for idx, region in enumerate(STANDARD_REGIONS)}
    grouped_df['order'] = grouped_df['시도코드명'].map(region_order)
    grouped_df = grouped_df.sort_values('order').drop('order', axis=1)
    
    # Save the processed data
    grouped_df.to_csv('의료기관_현황_2025년_3월_광역시도별_정리.csv', index=False, encoding='utf-8-sig')
    print("Data processing completed. Results saved to '의료기관_현황_2025년_3월_광역시도별_정리.csv'")

def load_medical_data(file_path):
    df = pd.read_csv(file_path)
    
    # 시도명 변환
    sido_mapping = {
        '강원도': '강원특별자치도',
        '전라북도': '전북특별자치도'
    }
    df['시도'] = df['시도'].replace(sido_mapping)
    
    return df

if __name__ == "__main__":
    process_medical_data() 