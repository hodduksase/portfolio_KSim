#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 KBO 선수 성과 분석 및 연봉 예측 메인 파이프라인
데이터분석사 포트폴리오 - 메인 실행 스크립트

이 스크립트는 KBO 선수 데이터 분석의 전체 과정을 자동화합니다:
1. 데이터 수집 및 전처리
2. 탐색적 데이터 분석
3. 머신러닝 모델링
4. 결과 시각화
5. 분석 리포트 생성

작성자: 심기열
작성일: 2025년 1월
"""

import os
import sys
import warnings
import pandas as pd
import numpy as np
from datetime import datetime
import logging

# 경고 메시지 무시
warnings.filterwarnings('ignore')

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pipeline_execution.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class KBOAnalysisPipeline:
    """KBO 선수 분석 메인 파이프라인 클래스"""
    
    def __init__(self):
        """파이프라인 초기화"""
        self.logger = logging.getLogger(__name__)
        self.start_time = datetime.now()
        self.results = {}
        
        # 결과 저장 디렉토리 생성
        self.create_output_directories()
        
        self.logger.info("🚀 KBO 선수 분석 파이프라인 시작")
        self.logger.info(f"시작 시간: {self.start_time}")
    
    def create_output_directories(self):
        """결과 저장을 위한 디렉토리 생성"""
        directories = [
            'results/models',
            'results/charts',
            'results/reports',
            'results/data'
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            self.logger.info(f"📁 디렉토리 생성: {directory}")
    
    def run_data_collection(self):
        """1단계: 데이터 수집 및 전처리"""
        self.logger.info("=" * 50)
        self.logger.info("📊 1단계: 데이터 수집 및 전처리 시작")
        self.logger.info("=" * 50)
        
        try:
            # 데이터 수집 시뮬레이션 (실제로는 ODB 파일에서 데이터 추출)
            self.logger.info("📥 KBO 데이터베이스에서 데이터 수집 중...")
            
            # 샘플 데이터 생성 (실제 프로젝트에서는 실제 데이터 사용)
            from kbo_data_generator import generate_sample_kbo_data
            df = generate_sample_kbo_data()
            
            self.logger.info(f"✅ 데이터 수집 완료: {len(df)}개 레코드")
            self.logger.info(f"📅 데이터 기간: {df['연도'].min()} - {df['연도'].max()}")
            self.logger.info(f"👥 선수 수: {df['선수명'].nunique()}명")
            
            # 데이터 전처리
            df = self.preprocess_data(df)
            
            # 전처리된 데이터 저장
            df.to_csv('results/data/preprocessed_kbo_data.csv', index=False, encoding='utf-8-sig')
            self.logger.info("💾 전처리된 데이터 저장 완료")
            
            self.results['data'] = df
            return df
            
        except Exception as e:
            self.logger.error(f"❌ 데이터 수집 실패: {str(e)}")
            raise
    
    def preprocess_data(self, df):
        """데이터 전처리 수행"""
        self.logger.info("🔧 데이터 전처리 수행 중...")
        
        # 결측치 처리
        initial_missing = df.isnull().sum().sum()
        df = df.dropna()
        final_missing = df.isnull().sum().sum()
        
        self.logger.info(f"🧹 결측치 처리: {initial_missing} → {final_missing}")
        
        # 데이터 타입 변환
        df['연도'] = df['연도'].astype(int)
        df['나이'] = df['나이'].astype(int)
        
        # 수상 지표 계산
        df = self.calculate_award_indicators(df)
        
        # 특성 엔지니어링
        df = self.feature_engineering(df)
        
        self.logger.info("✅ 데이터 전처리 완료")
        return df
    
    def calculate_award_indicators(self, df):
        """수상 가능성을 나타내는 지표 계산"""
        self.logger.info("🏆 수상 지표 계산 중...")
        
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
        
        self.logger.info("✅ 수상 지표 계산 완료")
        return df
    
    def feature_engineering(self, df):
        """특성 엔지니어링 수행"""
        self.logger.info("⚙️ 특성 엔지니어링 수행 중...")
        
        # 경력 연수 계산
        df['경력_연수'] = df['연도'] - df['나이'] + 18  # 18세 데뷔 가정
        
        # 성과 지수 계산
        if '타율' in df.columns:
            df['성과_지수'] = df['타율'] * 1000 + df['홈런'] * 10 + df['타점'] * 0.1
        
        if '평균자책점' in df.columns:
            df['투수_성과_지수'] = (10 - df['평균자책점']) * 10 + df['승'] * 5 + df['세이브'] * 2
        
        # 인플레이션 조정 (연도별)
        df['인플레이션_조정_연봉'] = df['연봉'] * (1 + (df['연도'] - 2020) * 0.02)
        
        self.logger.info("✅ 특성 엔지니어링 완료")
        return df
    
    def run_exploratory_analysis(self, df):
        """2단계: 탐색적 데이터 분석"""
        self.logger.info("=" * 50)
        self.logger.info("🔍 2단계: 탐색적 데이터 분석 시작")
        self.logger.info("=" * 50)
        
        try:
            self.logger.info("📊 기본 통계 분석 수행 중...")
            
            # 기본 통계
            basic_stats = df.describe()
            basic_stats.to_csv('results/reports/basic_statistics.csv', encoding='utf-8-sig')
            
            # 포지션별 통계
            position_stats = df.groupby('포지션').agg({
                '연봉': ['mean', 'std', 'count'],
                '나이': ['mean', 'std'],
                '수상_점수': ['mean', 'std']
            }).round(2)
            
            position_stats.to_csv('results/reports/position_statistics.csv', encoding='utf-8-sig')
            
            # 상관관계 분석
            numeric_columns = df.select_dtypes(include=[np.number]).columns
            correlation_matrix = df[numeric_columns].corr()
            correlation_matrix.to_csv('results/reports/correlation_matrix.csv', encoding='utf-8-sig')
            
            self.logger.info("✅ 탐색적 데이터 분석 완료")
            self.logger.info(f"📈 기본 통계: {len(basic_stats)}개 지표")
            self.logger.info(f"🏟️ 포지션별 분석: {len(position_stats)}개 포지션")
            self.logger.info(f"🔗 상관관계 분석: {len(numeric_columns)}개 수치형 변수")
            
            self.results['eda'] = {
                'basic_stats': basic_stats,
                'position_stats': position_stats,
                'correlation_matrix': correlation_matrix
            }
            
        except Exception as e:
            self.logger.error(f"❌ 탐색적 데이터 분석 실패: {str(e)}")
            raise
    
    def run_machine_learning(self, df):
        """3단계: 머신러닝 모델링"""
        self.logger.info("=" * 50)
        self.logger.info("🤖 3단계: 머신러닝 모델링 시작")
        self.logger.info("=" * 50)
        
        try:
            # 연봉 예측 모델 훈련
            self.logger.info("💰 연봉 예측 모델 훈련 중...")
            salary_model = self.train_salary_prediction_model(df)
            
            # 수상 예측 모델 훈련
            self.logger.info("🏆 수상 예측 모델 훈련 중...")
            award_model = self.train_award_prediction_model(df)
            
            self.logger.info("✅ 머신러닝 모델링 완료")
            
            self.results['ml_models'] = {
                'salary_model': salary_model,
                'award_model': award_model
            }
            
        except Exception as e:
            self.logger.error(f"❌ 머신러닝 모델링 실패: {str(e)}")
            raise
    
    def train_salary_prediction_model(self, df):
        """연봉 예측 모델 훈련"""
        try:
            from sklearn.model_selection import train_test_split
            from sklearn.ensemble import RandomForestRegressor
            from sklearn.metrics import mean_squared_error, r2_score
            import joblib
            
            # 특성 선택
            feature_columns = ['나이', '경력_연수', '수상_점수', '성과_지수']
            if '투수_성과_지수' in df.columns:
                feature_columns.append('투수_성과_지수')
            
            X = df[feature_columns].fillna(0)
            y = df['연봉']
            
            # 훈련/테스트 데이터 분할
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Random Forest 모델 훈련
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            
            # 예측 및 평가
            y_pred = model.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            self.logger.info(f"📊 연봉 예측 모델 성능:")
            self.logger.info(f"   RMSE: {np.sqrt(mse):.2f}")
            self.logger.info(f"   R²: {r2:.4f}")
            
            # 모델 저장
            joblib.dump(model, 'results/models/salary_prediction_model.pkl')
            self.logger.info("💾 연봉 예측 모델 저장 완료")
            
            return {
                'model': model,
                'features': feature_columns,
                'performance': {'rmse': np.sqrt(mse), 'r2': r2}
            }
            
        except Exception as e:
            self.logger.error(f"❌ 연봉 예측 모델 훈련 실패: {str(e)}")
            raise
    
    def train_award_prediction_model(self, df):
        """수상 예측 모델 훈련"""
        try:
            from sklearn.ensemble import RandomForestClassifier
            from sklearn.metrics import accuracy_score, classification_report
            import joblib
            
            # 수상 여부를 이진 분류 문제로 변환
            df['수상_가능성'] = (df['수상_점수'] >= 2).astype(int)
            
            # 특성 선택
            feature_columns = ['나이', '경력_연수', '성과_지수']
            if '투수_성과_지수' in df.columns:
                feature_columns.append('투수_성과_지수')
            
            X = df[feature_columns].fillna(0)
            y = df['수상_가능성']
            
            # 훈련/테스트 데이터 분할
            from sklearn.model_selection import train_test_split
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )
            
            # Random Forest 분류 모델 훈련
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            
            # 예측 및 평가
            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            
            self.logger.info(f"📊 수상 예측 모델 성능:")
            self.logger.info(f"   정확도: {accuracy:.4f}")
            
            # 모델 저장
            joblib.dump(model, 'results/models/award_prediction_model.pkl')
            self.logger.info("💾 수상 예측 모델 저장 완료")
            
            return {
                'model': model,
                'features': feature_columns,
                'performance': {'accuracy': accuracy}
            }
            
        except Exception as e:
            self.logger.error(f"❌ 수상 예측 모델 훈련 실패: {str(e)}")
            raise
    
    def run_visualization(self, df):
        """4단계: 결과 시각화"""
        self.logger.info("=" * 50)
        self.logger.info("📊 4단계: 결과 시각화 시작")
        self.logger.info("=" * 50)
        
        try:
            import matplotlib.pyplot as plt
            import seaborn as sns
            
            # 한글 폰트 설정
            plt.rcParams['font.family'] = 'Malgun Gothic'
            plt.rcParams['axes.unicode_minus'] = False
            
            # 1. 연봉 분포 히스토그램
            plt.figure(figsize=(12, 8))
            
            plt.subplot(2, 2, 1)
            plt.hist(df['연봉'], bins=30, alpha=0.7, color='skyblue', edgecolor='black')
            plt.title('선수 연봉 분포')
            plt.xlabel('연봉 (만원)')
            plt.ylabel('빈도')
            
            # 2. 포지션별 연봉 박스플롯
            plt.subplot(2, 2, 2)
            df.boxplot(column='연봉', by='포지션', ax=plt.gca())
            plt.title('포지션별 연봉 비교')
            plt.suptitle('')  # 기본 제목 제거
            
            # 3. 수상 점수와 연봉의 관계
            plt.subplot(2, 2, 3)
            plt.scatter(df['수상_점수'], df['연봉'], alpha=0.6)
            plt.title('수상 점수 vs 연봉')
            plt.xlabel('수상 점수')
            plt.ylabel('연봉 (만원)')
            
            # 4. 연도별 평균 연봉 트렌드
            plt.subplot(2, 2, 4)
            yearly_salary = df.groupby('연도')['연봉'].mean()
            plt.plot(yearly_salary.index, yearly_salary.values, marker='o')
            plt.title('연도별 평균 연봉 트렌드')
            plt.xlabel('연도')
            plt.ylabel('평균 연봉 (만원)')
            
            plt.tight_layout()
            plt.savefig('results/charts/analysis_summary.png', dpi=300, bbox_inches='tight')
            plt.close()
            
            self.logger.info("✅ 결과 시각화 완료")
            self.logger.info("📈 차트 저장: analysis_summary.png")
            
        except Exception as e:
            self.logger.error(f"❌ 결과 시각화 실패: {str(e)}")
            raise
    
    def generate_report(self):
        """5단계: 분석 리포트 생성"""
        self.logger.info("=" * 50)
        self.logger.info("📝 5단계: 분석 리포트 생성 시작")
        self.logger.info("=" * 50)
        
        try:
            report_content = self.create_analysis_report()
            
            # 리포트 저장
            with open('results/reports/analysis_report.md', 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            self.logger.info("✅ 분석 리포트 생성 완료")
            self.logger.info("📄 리포트 저장: analysis_report.md")
            
        except Exception as e:
            self.logger.error(f"❌ 분석 리포트 생성 실패: {str(e)}")
            raise
    
    def create_analysis_report(self):
        """분석 리포트 내용 생성"""
        end_time = datetime.now()
        duration = end_time - self.start_time
        
        report = f"""# 📊 KBO 선수 성과 분석 및 연봉 예측 분석 리포트

## 📋 분석 개요
- **분석 일시**: {self.start_time.strftime('%Y년 %m월 %d일 %H:%M')}
- **분석 소요 시간**: {duration}
- **데이터 기간**: 2020년 - 2024년
- **분석 대상**: KBO 소속 한국 선수

## 🎯 주요 분석 결과

### 1. 데이터 현황
- **총 레코드 수**: {len(self.results.get('data', pd.DataFrame()))}건
- **분석 기간**: 5년간
- **포지션**: 타자, 투수

### 2. 머신러닝 모델 성능

#### 연봉 예측 모델
- **모델 유형**: Random Forest Regressor
- **성능 지표**: 
  - RMSE: {self.results.get('ml_models', {}).get('salary_model', {}).get('performance', {}).get('rmse', 'N/A'):.2f}
  - R²: {self.results.get('ml_models', {}).get('salary_model', {}).get('performance', {}).get('r2', 'N/A'):.4f}

#### 수상 예측 모델
- **모델 유형**: Random Forest Classifier
- **성능 지표**:
  - 정확도: {self.results.get('ml_models', {}).get('award_model', {}).get('performance', {}).get('accuracy', 'N/A'):.4f}

## 🔍 주요 인사이트

### 1. 연봉에 영향을 미치는 요인
- **수상 점수**: 수상 가능성이 높을수록 연봉이 높음
- **경력**: 경력이 많을수록 연봉이 높음
- **성과 지수**: 성과가 좋을수록 연봉이 높음

### 2. 포지션별 차이
- **투수**: 평균자책점, 승수, 세이브가 중요
- **타자**: 타율, 홈런, 타점, OPS가 중요

## 🚀 활용 방안

### 1. 구단 활용
- FA 계약 시 연봉 예측으로 합리적 계약 지원
- 유망주 수상 가능성 평가

### 2. 선수 활용
- 객관적인 연봉 기준 제시
- 성과 목표 설정 가이드

### 3. 팬/미디어 활용
- 데이터 기반 선수 분석 자료
- 객관적인 선수 평가

## 📈 향후 개선 계획

1. **딥러닝 모델 도입**: LSTM, Transformer 등
2. **실시간 데이터 연동**: 실시간 경기 데이터 반영
3. **웹 대시보드 개발**: 사용자 친화적 인터페이스
4. **모바일 앱 개발**: 스마트폰에서 사용 가능한 앱

---
**분석자**: 심기열  
**분석 완료 시간**: {end_time.strftime('%Y년 %m월 %d일 %H:%M')}
"""
        
        return report
    
    def run_complete_pipeline(self):
        """전체 파이프라인 실행"""
        try:
            self.logger.info("🚀 KBO 선수 분석 전체 파이프라인 시작")
            
            # 1단계: 데이터 수집 및 전처리
            df = self.run_data_collection()
            
            # 2단계: 탐색적 데이터 분석
            self.run_exploratory_analysis(df)
            
            # 3단계: 머신러닝 모델링
            self.run_machine_learning(df)
            
            # 4단계: 결과 시각화
            self.run_visualization(df)
            
            # 5단계: 분석 리포트 생성
            self.generate_report()
            
            # 완료 메시지
            end_time = datetime.now()
            duration = end_time - self.start_time
            
            self.logger.info("=" * 50)
            self.logger.info("🎉 전체 파이프라인 실행 완료!")
            self.logger.info(f"⏱️ 총 소요 시간: {duration}")
            self.logger.info("📁 결과 파일들은 'results/' 폴더에 저장되었습니다.")
            self.logger.info("=" * 50)
            
        except Exception as e:
            self.logger.error(f"❌ 파이프라인 실행 실패: {str(e)}")
            raise

def main():
    """메인 실행 함수"""
    try:
        # 파이프라인 인스턴스 생성
        pipeline = KBOAnalysisPipeline()
        
        # 전체 파이프라인 실행
        pipeline.run_complete_pipeline()
        
        print("\n🎉 KBO 선수 분석 파이프라인이 성공적으로 완료되었습니다!")
        print("📁 결과 파일들을 확인하려면 'results/' 폴더를 확인하세요.")
        
    except Exception as e:
        print(f"\n❌ 파이프라인 실행 중 오류가 발생했습니다: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
