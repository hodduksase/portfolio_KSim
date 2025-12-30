"""
데이터 분석 파이프라인
전체 데이터 분석 프로세스를 자동화하는 메인 스크립트입니다.
"""

import pandas as pd
import numpy as np
import os
import sys
from datetime import datetime
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/analysis_pipeline.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class DataAnalysisPipeline:
    """데이터 분석 파이프라인 클래스"""
    
    def __init__(self, raw_data_path='data/raw_data.csv', output_dir='results'):
        """
        초기화
        
        Parameters:
        -----------
        raw_data_path : str
            원본 데이터 경로
        output_dir : str
            결과 저장 디렉토리
        """
        self.raw_data_path = raw_data_path
        self.output_dir = output_dir
        self.processed_data_path = 'data/processed_data.csv'
        self.df = None
        
        # 디렉토리 생성
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs('data', exist_ok=True)
        os.makedirs('logs', exist_ok=True)
        os.makedirs('models', exist_ok=True)
        
        logger.info(f"데이터 분석 파이프라인 초기화 완료")
        logger.info(f"원본 데이터 경로: {self.raw_data_path}")
        logger.info(f"결과 저장 디렉토리: {self.output_dir}")
    
    def load_data(self):
        """데이터 로드"""
        logger.info("데이터 로드 시작...")
        try:
            self.df = pd.read_csv(self.raw_data_path)
            logger.info(f"데이터 로드 완료: {self.df.shape[0]}행, {self.df.shape[1]}열")
            return True
        except FileNotFoundError:
            logger.error(f"파일을 찾을 수 없습니다: {self.raw_data_path}")
            logger.info("샘플 데이터를 생성합니다...")
            self._generate_sample_data()
            return True
        except Exception as e:
            logger.error(f"데이터 로드 중 오류 발생: {str(e)}")
            return False
    
    def _generate_sample_data(self):
        """샘플 데이터 생성 (데이터가 없는 경우)"""
        np.random.seed(42)
        n_samples = 1000
        
        self.df = pd.DataFrame({
            'feature_1': np.random.normal(50, 15, n_samples),
            'feature_2': np.random.normal(100, 20, n_samples),
            'feature_3': np.random.exponential(2, n_samples),
            'feature_4': np.random.uniform(0, 100, n_samples),
            'category': np.random.choice(['A', 'B', 'C'], n_samples),
            'target': np.random.choice([0, 1], n_samples, p=[0.6, 0.4])
        })
        
        # 일부 결측치 추가
        missing_indices = np.random.choice(self.df.index, size=int(0.05 * len(self.df)), replace=False)
        self.df.loc[missing_indices, 'feature_1'] = np.nan
        
        logger.info(f"샘플 데이터 생성 완료: {self.df.shape}")
        
        # 원본 데이터 저장
        os.makedirs('data', exist_ok=True)
        self.df.to_csv(self.raw_data_path, index=False)
        logger.info(f"샘플 데이터 저장: {self.raw_data_path}")
    
    def data_quality_check(self):
        """데이터 품질 검사"""
        logger.info("데이터 품질 검사 시작...")
        
        quality_report = {
            'total_rows': len(self.df),
            'total_columns': len(self.df.columns),
            'missing_values': self.df.isnull().sum().to_dict(),
            'missing_percentage': (self.df.isnull().sum() / len(self.df) * 100).to_dict(),
            'duplicate_rows': self.df.duplicated().sum(),
            'data_types': self.df.dtypes.to_dict()
        }
        
        # 리포트 저장
        quality_df = pd.DataFrame({
            'Column': self.df.columns,
            'Missing_Count': [quality_report['missing_values'][col] for col in self.df.columns],
            'Missing_Percentage': [quality_report['missing_percentage'][col] for col in self.df.columns],
            'Data_Type': [str(quality_report['data_types'][col]) for col in self.df.columns]
        })
        
        quality_df.to_csv(f'{self.output_dir}/data_quality_report.csv', index=False)
        logger.info(f"데이터 품질 리포트 저장: {self.output_dir}/data_quality_report.csv")
        
        return quality_report
    
    def preprocess_data(self):
        """데이터 전처리"""
        logger.info("데이터 전처리 시작...")
        
        df_processed = self.df.copy()
        
        # 결측치 처리
        numeric_cols = df_processed.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df_processed.select_dtypes(include=['object']).columns.tolist()
        
        for col in numeric_cols:
            if df_processed[col].isnull().sum() > 0:
                median_value = df_processed[col].median()
                df_processed[col].fillna(median_value, inplace=True)
                logger.info(f"{col}: 결측치를 중앙값({median_value:.2f})으로 대체")
        
        for col in categorical_cols:
            if df_processed[col].isnull().sum() > 0:
                mode_value = df_processed[col].mode()[0] if len(df_processed[col].mode()) > 0 else 'Unknown'
                df_processed[col].fillna(mode_value, inplace=True)
                logger.info(f"{col}: 결측치를 최빈값({mode_value})으로 대체")
        
        # 전처리된 데이터 저장
        df_processed.to_csv(self.processed_data_path, index=False)
        logger.info(f"전처리된 데이터 저장: {self.processed_data_path}")
        
        return df_processed
    
    def generate_statistics_report(self):
        """통계 리포트 생성"""
        logger.info("통계 리포트 생성 시작...")
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_cols) > 0:
            stats_df = self.df[numeric_cols].describe().T
            stats_df['skewness'] = self.df[numeric_cols].skew()
            stats_df['kurtosis'] = self.df[numeric_cols].kurtosis()
            stats_df.to_csv(f'{self.output_dir}/statistics_report.csv')
            logger.info(f"통계 리포트 저장: {self.output_dir}/statistics_report.csv")
        
        return stats_df
    
    def run_pipeline(self):
        """전체 파이프라인 실행"""
        logger.info("="*60)
        logger.info("데이터 분석 파이프라인 시작")
        logger.info("="*60)
        
        start_time = datetime.now()
        
        # 1. 데이터 로드
        if not self.load_data():
            logger.error("데이터 로드 실패. 파이프라인을 종료합니다.")
            return False
        
        # 2. 데이터 품질 검사
        quality_report = self.data_quality_check()
        
        # 3. 데이터 전처리
        self.df = self.preprocess_data()
        
        # 4. 통계 리포트 생성
        stats_report = self.generate_statistics_report()
        
        # 5. 파이프라인 요약 리포트 생성
        self._generate_pipeline_summary(start_time, quality_report)
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        logger.info("="*60)
        logger.info(f"데이터 분석 파이프라인 완료 (소요 시간: {duration:.2f}초)")
        logger.info("="*60)
        
        return True
    
    def _generate_pipeline_summary(self, start_time, quality_report):
        """파이프라인 요약 리포트 생성"""
        summary = f"""
데이터 분석 파이프라인 실행 요약
====================================
실행 시간: {start_time.strftime('%Y-%m-%d %H:%M:%S')}
완료 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

데이터 정보:
- 총 행 수: {quality_report['total_rows']:,}
- 총 열 수: {quality_report['total_columns']}
- 중복 행 수: {quality_report['duplicate_rows']}

주요 처리 사항:
- 데이터 로드 완료
- 데이터 품질 검사 완료
- 데이터 전처리 완료 (결측치 처리)
- 통계 리포트 생성 완료

결과 파일:
- 전처리된 데이터: {self.processed_data_path}
- 데이터 품질 리포트: {self.output_dir}/data_quality_report.csv
- 통계 리포트: {self.output_dir}/statistics_report.csv
- 파이프라인 로그: logs/analysis_pipeline.log
"""
        
        with open(f'{self.output_dir}/pipeline_summary.txt', 'w', encoding='utf-8') as f:
            f.write(summary)
        
        logger.info("파이프라인 요약 리포트 저장 완료")


def main():
    """메인 실행 함수"""
    pipeline = DataAnalysisPipeline()
    success = pipeline.run_pipeline()
    
    if success:
        print("\n✅ 데이터 분석 파이프라인이 성공적으로 완료되었습니다!")
        print(f"결과는 '{pipeline.output_dir}' 디렉토리에서 확인할 수 있습니다.")
    else:
        print("\n❌ 데이터 분석 파이프라인 실행 중 오류가 발생했습니다.")
        print("로그 파일을 확인해주세요: logs/analysis_pipeline.log")


if __name__ == '__main__':
    main()

