#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 KBO 데이터 생성기
데이터분석사 포트폴리오 - 샘플 데이터 생성 모듈

이 모듈은 KBO 선수 데이터 분석을 위한 샘플 데이터를 생성합니다.
실제 프로젝트에서는 KBO 데이터베이스에서 실제 데이터를 추출합니다.

작성자: 심기열
작성일: 2025년 1월
"""

import pandas as pd
import numpy as np
from datetime import datetime
import random

def generate_sample_kbo_data(num_players=1000):
    """
    KBO 선수 샘플 데이터 생성
    
    Args:
        num_players (int): 생성할 선수 수
        
    Returns:
        pd.DataFrame: KBO 선수 데이터
    """
    
    # 시드 설정으로 재현 가능한 데이터 생성
    np.random.seed(42)
    random.seed(42)
    
    # 기본 정보 생성
    years = [2020, 2021, 2022, 2023, 2024]
    teams = ['LG', 'KT', 'SSG', '두산', '키움', '한화', '롯데', '삼성', 'NC', 'KIA']
    positions = ['타자', '투수']
    
    # 한국 성씨 리스트
    korean_surnames = ['김', '이', '박', '최', '정', '강', '조', '윤', '장', '임', '한', '오', '서', '신', '권', '황', '안', '송', '전', '고']
    korean_names = ['민준', '서준', '도윤', '예준', '시우', '주원', '하준', '지호', '지후', '준서', '준우', '현우', '도현', '지훈', '우진', '민재', '현준', '태현', '정현', '준혁']
    
    data = []
    
    for i in range(num_players):
        # 기본 정보
        year = random.choice(years)
        team = random.choice(teams)
        position = random.choice(positions)
        age = random.randint(20, 40)
        career_years = year - age + 18  # 18세 데뷔 가정
        
        # 선수명 생성
        surname = random.choice(korean_surnames)
        name = random.choice(korean_names)
        player_name = f"{surname}{name}"
        
        # 연봉 생성 (나이, 경력, 포지션에 따라 차등)
        base_salary = 5000  # 기본 연봉 5000만원
        age_bonus = (age - 20) * 200  # 나이 보너스
        career_bonus = career_years * 300  # 경력 보너스
        position_bonus = 1000 if position == '투수' else 500  # 포지션 보너스
        
        salary = base_salary + age_bonus + career_bonus + position_bonus
        salary += np.random.normal(0, 500)  # 랜덤 변동
        salary = max(3000, int(salary))  # 최소 3000만원
        
        # 연도별 인플레이션 조정
        inflation_factor = 1 + (year - 2020) * 0.02
        salary = int(salary * inflation_factor)
        
        if position == '타자':
            # 타자 성과 지표
            batting_avg = np.random.normal(0.280, 0.050)  # 타율
            batting_avg = max(0.150, min(0.400, batting_avg))
            
            home_runs = np.random.poisson(15)  # 홈런
            rbi = np.random.poisson(60)  # 타점
            stolen_bases = np.random.poisson(15)  # 도루
            
            # OPS 계산 (출루율 + 장타율)
            obp = batting_avg + np.random.normal(0.080, 0.020)  # 출루율
            obp = max(0.200, min(0.500, obp))
            
            slg = batting_avg + np.random.normal(0.150, 0.050)  # 장타율
            slg = max(0.200, min(0.700, slg))
            
            ops = obp + slg
            
            # 경기 수
            games = random.randint(100, 150)
            runs = int(home_runs * 0.8 + np.random.normal(0, 10))
            walks = int(np.random.normal(50, 15))
            strikeouts = int(np.random.normal(80, 20))
            
            # 투수 관련 컬럼은 NaN으로 설정
            innings = np.nan
            wins = np.nan
            losses = np.nan
            saves = np.nan
            holds = np.nan
            era = np.nan
            strikeouts_pitching = np.nan
            games_pitching = np.nan
            starts = np.nan
            complete_games = np.nan
            shutouts = np.nan
            
        else:  # 투수
            # 투수 성과 지표
            innings = np.random.normal(150, 30)  # 이닝
            innings = max(50, min(200, innings))
            
            wins = np.random.poisson(12)  # 승수
            losses = np.random.poisson(8)  # 패수
            saves = np.random.poisson(25) if random.random() < 0.3 else 0  # 세이브 (30% 확률로 세이브 투수)
            holds = np.random.poisson(20) if saves == 0 else 0  # 홀드 (세이브 투수가 아닌 경우)
            
            era = np.random.normal(3.50, 0.80)  # 평균자책점
            era = max(1.50, min(6.00, era))
            
            strikeouts_pitching = int(innings * np.random.normal(7.5, 1.5))  # 탈삼진
            games_pitching = random.randint(30, 70)
            starts = int(games_pitching * 0.8) if saves == 0 else 0  # 선발 (세이브 투수가 아닌 경우)
            complete_games = random.randint(0, 3) if starts > 0 else 0
            shutouts = random.randint(0, 1) if complete_games > 0 else 0
            
            # 타자 관련 컬럼은 NaN으로 설정
            batting_avg = np.nan
            home_runs = np.nan
            rbi = np.nan
            stolen_bases = np.nan
            obp = np.nan
            slg = np.nan
            ops = np.nan
            games = np.nan
            runs = np.nan
            walks = np.nan
            strikeouts = np.nan
        
        # 수상 지표 계산 (실제로는 calculate_award_indicators에서 계산)
        award_score = 0
        
        # 선수 데이터 생성
        player_data = {
            '연도': year,
            '선수명': player_name,
            '팀': team,
            '포지션': position,
            '나이': age,
            '연봉': salary,
            '경력_연수': career_years,
            '수상_점수': award_score,
            
            # 타자 지표
            '타율': batting_avg,
            '홈런': home_runs,
            '타점': rbi,
            '도루': stolen_bases,
            '출루율': obp,
            '장타율': slg,
            'OPS': ops,
            '경기수': games,
            '득점': runs,
            '볼넷': walks,
            '삼진': strikeouts,
            
            # 투수 지표
            '이닝': innings,
            '승': wins,
            '패': losses,
            '세이브': saves,
            '홀드': holds,
            '평균자책점': era,
            '탈삼진': strikeouts_pitching,
            '경기수_투수': games_pitching,
            '선발': starts,
            '완투': complete_games,
            '완봉': shutouts
        }
        
        data.append(player_data)
    
    # DataFrame 생성
    df = pd.DataFrame(data)
    
    # 수상 지표 계산
    df = calculate_award_indicators(df)
    
    # 특성 엔지니어링
    df = feature_engineering(df)
    
    return df

def calculate_award_indicators(df):
    """수상 가능성을 나타내는 지표 계산"""
    
    # 타자 수상 지표
    batter_mask = df['포지션'] == '타자'
    if batter_mask.any():
        # 타율 기준 상위 10%
        df.loc[batter_mask, '타율_상위10%'] = df.loc[batter_mask, '타율'].rank(pct=True) >= 0.9
        
        # 홈런 기준 상위 10%
        df.loc[batter_mask, '홈런_상위10%'] = df.loc[batter_mask, '홈런'].rank(pct=True) >= 0.9
        
        # 타점 기준 상위 10%
        df.loc[batter_mask, '타점_상위10%'] = df.loc[batter_mask, '타점'].rank(pct=True) >= 0.9
        
        # OPS 기준 상위 10%
        df.loc[batter_mask, 'OPS_상위10%'] = df.loc[batter_mask, 'OPS'].rank(pct=True) >= 0.9
        
        # 종합 수상 점수 (0-4점)
        df.loc[batter_mask, '수상_점수'] = (
            df.loc[batter_mask, '타율_상위10%'].astype(int) +
            df.loc[batter_mask, '홈런_상위10%'].astype(int) +
            df.loc[batter_mask, '타점_상위10%'].astype(int) +
            df.loc[batter_mask, 'OPS_상위10%'].astype(int)
        )
    
    # 투수 수상 지표
    pitcher_mask = df['포지션'] == '투수'
    if pitcher_mask.any():
        # 평균자책점 기준 하위 10%
        df.loc[pitcher_mask, 'ERA_상위10%'] = df.loc[pitcher_mask, '평균자책점'].rank(pct=True) <= 0.1
        
        # 승수 기준 상위 10%
        df.loc[pitcher_mask, '승수_상위10%'] = df.loc[pitcher_mask, '승'].rank(pct=True) >= 0.9
        
        # 세이브 기준 상위 10%
        df.loc[pitcher_mask, '세이브_상위10%'] = df.loc[pitcher_mask, '세이브'].rank(pct=True) >= 0.9
        
        # 탈삼진 기준 상위 10%
        df.loc[pitcher_mask, '탈삼진_상위10%'] = df.loc[pitcher_mask, '탈삼진'].rank(pct=True) >= 0.9
        
        # 종합 수상 점수 (0-4점)
        df.loc[pitcher_mask, '수상_점수'] = (
            df.loc[pitcher_mask, 'ERA_상위10%'].astype(int) +
            df.loc[pitcher_mask, '승수_상위10%'].astype(int) +
            df.loc[pitcher_mask, '세이브_상위10%'].astype(int) +
            df.loc[pitcher_mask, '탈삼진_상위10%'].astype(int)
        )
    
    return df

def feature_engineering(df):
    """특성 엔지니어링 수행"""
    
    # 성과 지수 계산
    batter_mask = df['포지션'] == '타자'
    if batter_mask.any():
        df.loc[batter_mask, '성과_지수'] = (
            df.loc[batter_mask, '타율'] * 1000 + 
            df.loc[batter_mask, '홈런'] * 10 + 
            df.loc[batter_mask, '타점'] * 0.1
        )
    
    pitcher_mask = df['포지션'] == '투수'
    if pitcher_mask.any():
        df.loc[pitcher_mask, '투수_성과_지수'] = (
            (10 - df.loc[pitcher_mask, '평균자책점']) * 10 + 
            df.loc[pitcher_mask, '승'] * 5 + 
            df.loc[pitcher_mask, '세이브'] * 2
        )
    
    # 인플레이션 조정 (연도별)
    df['인플레이션_조정_연봉'] = df['연봉'] * (1 + (df['연도'] - 2020) * 0.02)
    
    return df

def generate_specific_year_data(year, num_players=200):
    """특정 연도의 데이터만 생성"""
    df = generate_sample_kbo_data(num_players)
    return df[df['연도'] == year]

def generate_position_data(position, num_players=500):
    """특정 포지션의 데이터만 생성"""
    df = generate_sample_kbo_data(num_players)
    return df[df['포지션'] == position]

def generate_high_salary_data(min_salary=10000, num_players=200):
    """고연봉 선수 데이터만 생성"""
    df = generate_sample_kbo_data(num_players * 2)  # 더 많은 데이터 생성
    return df[df['연봉'] >= min_salary]

if __name__ == "__main__":
    # 샘플 데이터 생성 테스트
    print("📊 KBO 샘플 데이터 생성 테스트")
    print("=" * 50)
    
    # 전체 데이터 생성
    df = generate_sample_kbo_data(100)
    print(f"✅ 전체 데이터 생성 완료: {len(df)}개 레코드")
    print(f"📅 데이터 기간: {df['연도'].min()} - {df['연도'].max()}")
    print(f"👥 선수 수: {df['선수명'].nunique()}명")
    print(f"🏟️ 포지션: {df['포지션'].unique()}")
    print(f"💰 연봉 범위: {df['연봉'].min():,} - {df['연봉'].max():,}만원")
    
    # 포지션별 통계
    print("\n📊 포지션별 통계:")
    position_stats = df.groupby('포지션').agg({
        '연봉': ['mean', 'count'],
        '나이': 'mean',
        '수상_점수': 'mean'
    }).round(2)
    print(position_stats)
    
    # 수상 점수 분포
    print(f"\n🏆 수상 점수 분포:")
    award_distribution = df['수상_점수'].value_counts().sort_index()
    for score, count in award_distribution.items():
        print(f"   {score}점: {count}명 ({count/len(df)*100:.1f}%)")
    
    print("\n🎉 데이터 생성 테스트 완료!")
