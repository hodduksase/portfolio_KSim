"""
인스타그램 수집 데이터 분석 스크립트
크롤링으로 수집한 인스타그램 데이터를 분석하고 시각화합니다.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import re
import warnings

warnings.filterwarnings('ignore')
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False


class InstagramDataAnalyzer:
    """인스타그램 데이터 분석 클래스"""
    
    def __init__(self, data_path='data/instagram_posts.csv'):
        """
        초기화
        
        Parameters:
        -----------
        data_path : str
            인스타그램 데이터 파일 경로
        """
        self.df = pd.read_csv(data_path, encoding='utf-8-sig')
        self.df['collected_date'] = pd.to_datetime(self.df['timestamp'])
        print(f"데이터 로드 완료: {len(self.df)}개 게시물")
    
    def clean_numeric_data(self, column):
        """
        숫자 데이터 정제 (좋아요, 댓글 수 등)
        
        Parameters:
        -----------
        column : str
            정제할 컬럼명
        
        Returns:
        --------
        pd.Series
            정제된 숫자 데이터
        """
        def extract_number(text):
            if pd.isna(text) or text == 'N/A':
                return 0
            # 텍스트에서 숫자만 추출
            numbers = re.findall(r'[\d,]+', str(text))
            if numbers:
                # 쉼표 제거 후 숫자로 변환
                return int(numbers[0].replace(',', ''))
            return 0
        
        return self.df[column].apply(extract_number)
    
    def analyze_engagement(self):
        """게시물 참여도 분석"""
        # 좋아요 수 정제
        self.df['likes_numeric'] = self.clean_numeric_data('likes')
        self.df['comments_numeric'] = self.clean_numeric_data('comments')
        
        # 참여도 계산 (좋아요 + 댓글)
        self.df['engagement'] = self.df['likes_numeric'] + self.df['comments_numeric']
        
        print("\n" + "="*60)
        print("게시물 참여도 분석")
        print("="*60)
        print(f"평균 좋아요: {self.df['likes_numeric'].mean():.0f}")
        print(f"평균 댓글: {self.df['comments_numeric'].mean():.0f}")
        print(f"평균 참여도: {self.df['engagement'].mean():.0f}")
        print(f"최고 좋아요 게시물: {self.df['likes_numeric'].max()}")
        print(f"최저 좋아요 게시물: {self.df['likes_numeric'].min()}")
    
    def analyze_caption_length(self):
        """게시물 본문 길이 분석"""
        self.df['caption_length'] = self.df['caption'].str.len()
        
        print("\n" + "="*60)
        print("게시물 본문 길이 분석")
        print("="*60)
        print(f"평균 본문 길이: {self.df['caption_length'].mean():.0f}자")
        print(f"최대 본문 길이: {self.df['caption_length'].max()}자")
        print(f"최소 본문 길이: {self.df['caption_length'].min()}자")
    
    def create_visualization_dashboard(self, save_dir='results'):
        """시각화 대시보드 생성"""
        import os
        os.makedirs(save_dir, exist_ok=True)
        
        # 데이터 정제
        self.df['likes_numeric'] = self.clean_numeric_data('likes')
        self.df['comments_numeric'] = self.clean_numeric_data('comments')
        self.df['engagement'] = self.df['likes_numeric'] + self.df['comments_numeric']
        self.df['caption_length'] = self.df['caption'].str.len()
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # 1. 좋아요 분포
        axes[0, 0].hist(self.df['likes_numeric'], bins=20, edgecolor='black', alpha=0.7, color='steelblue')
        axes[0, 0].set_title('좋아요 수 분포', fontsize=14, fontweight='bold')
        axes[0, 0].set_xlabel('좋아요 수')
        axes[0, 0].set_ylabel('게시물 수')
        axes[0, 0].axvline(self.df['likes_numeric'].mean(), color='red', 
                          linestyle='--', linewidth=2, label=f'평균: {self.df["likes_numeric"].mean():.0f}')
        axes[0, 0].legend()
        
        # 2. 댓글 수 분포
        axes[0, 1].hist(self.df['comments_numeric'], bins=20, edgecolor='black', alpha=0.7, color='coral')
        axes[0, 1].set_title('댓글 수 분포', fontsize=14, fontweight='bold')
        axes[0, 1].set_xlabel('댓글 수')
        axes[0, 1].set_ylabel('게시물 수')
        axes[0, 1].axvline(self.df['comments_numeric'].mean(), color='red', 
                          linestyle='--', linewidth=2, label=f'평균: {self.df["comments_numeric"].mean():.0f}')
        axes[0, 1].legend()
        
        # 3. 참여도 추이 (게시물 순서 기준)
        axes[1, 0].plot(range(len(self.df)), self.df['engagement'], marker='o', linewidth=2, markersize=4)
        axes[1, 0].set_title('게시물별 참여도 추이', fontsize=14, fontweight='bold')
        axes[1, 0].set_xlabel('게시물 순서')
        axes[1, 0].set_ylabel('참여도 (좋아요 + 댓글)')
        axes[1, 0].grid(True, alpha=0.3)
        
        # 4. 본문 길이 vs 참여도 산점도
        axes[1, 1].scatter(self.df['caption_length'], self.df['engagement'], 
                          alpha=0.6, s=50, color='purple')
        axes[1, 1].set_title('본문 길이 vs 참여도', fontsize=14, fontweight='bold')
        axes[1, 1].set_xlabel('본문 길이 (자)')
        axes[1, 1].set_ylabel('참여도')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.suptitle('인스타그램 게시물 분석 대시보드', fontsize=16, fontweight='bold', y=0.995)
        plt.tight_layout()
        plt.savefig(f'{save_dir}/instagram_analysis_dashboard.png', dpi=300, bbox_inches='tight')
        print(f"\n시각화 대시보드 저장: {save_dir}/instagram_analysis_dashboard.png")
        plt.show()
    
    def generate_summary_report(self, save_path='results/instagram_analysis_report.txt'):
        """분석 요약 리포트 생성"""
        import os
        os.makedirs(os.path.dirname(save_path) if os.path.dirname(save_path) else '.', exist_ok=True)
        
        # 데이터 정제
        self.df['likes_numeric'] = self.clean_numeric_data('likes')
        self.df['comments_numeric'] = self.clean_numeric_data('comments')
        self.df['engagement'] = self.df['likes_numeric'] + self.df['comments_numeric']
        self.df['caption_length'] = self.df['caption'].str.len()
        
        report = f"""
인스타그램 게시물 분석 리포트
생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*60}

1. 기본 통계
   - 총 게시물 수: {len(self.df)}개
   - 계정명: {self.df['account'].iloc[0] if 'account' in self.df.columns else 'N/A'}

2. 좋아요 분석
   - 평균 좋아요: {self.df['likes_numeric'].mean():.0f}
   - 최대 좋아요: {self.df['likes_numeric'].max()}
   - 최소 좋아요: {self.df['likes_numeric'].min()}
   - 중앙값: {self.df['likes_numeric'].median():.0f}

3. 댓글 분석
   - 평균 댓글: {self.df['comments_numeric'].mean():.0f}
   - 최대 댓글: {self.df['comments_numeric'].max()}
   - 최소 댓글: {self.df['comments_numeric'].min()}
   - 중앙값: {self.df['comments_numeric'].median():.0f}

4. 참여도 분석
   - 평균 참여도: {self.df['engagement'].mean():.0f}
   - 최고 참여도: {self.df['engagement'].max()}
   - 최저 참여도: {self.df['engagement'].min()}

5. 본문 분석
   - 평균 본문 길이: {self.df['caption_length'].mean():.0f}자
   - 최대 본문 길이: {self.df['caption_length'].max()}자
   - 최소 본문 길이: {self.df['caption_length'].min()}자

6. 상위 5개 게시물 (참여도 기준)
{self.df.nlargest(5, 'engagement')[['post_url', 'engagement', 'likes_numeric', 'comments_numeric']].to_string(index=False)}
"""
        
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n분석 리포트 저장: {save_path}")
        print(report)


def main():
    """메인 실행 함수"""
    try:
        # 분석기 초기화
        analyzer = InstagramDataAnalyzer('data/instagram_posts.csv')
        
        # 데이터 분석
        analyzer.analyze_engagement()
        analyzer.analyze_caption_length()
        
        # 시각화
        analyzer.create_visualization_dashboard()
        
        # 리포트 생성
        analyzer.generate_summary_report()
        
        print("\n✅ 인스타그램 데이터 분석이 완료되었습니다!")
        
    except FileNotFoundError:
        print("❌ 데이터 파일을 찾을 수 없습니다. 먼저 04_Instagram_Data_Collection.py를 실행하여 데이터를 수집해주세요.")
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")


if __name__ == '__main__':
    main()

