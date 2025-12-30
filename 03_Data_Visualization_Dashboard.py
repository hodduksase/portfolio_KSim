"""
데이터 시각화 대시보드
인터랙티브한 차트와 그래프를 생성하여 데이터 인사이트를 시각적으로 표현합니다.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings

warnings.filterwarnings('ignore')
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False


class DataVisualizationDashboard:
    """데이터 시각화 대시보드 클래스"""
    
    def __init__(self, data_path='data/processed_data.csv'):
        """
        초기화
        
        Parameters:
        -----------
        data_path : str
            데이터 파일 경로
        """
        self.df = pd.read_csv(data_path)
        self.numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_cols = self.df.select_dtypes(include=['object']).columns.tolist()
        print(f"데이터 로드 완료: {self.df.shape[0]}행, {self.df.shape[1]}열")
    
    def create_summary_statistics_chart(self, save_path='results/summary_statistics.png'):
        """요약 통계량 차트 생성"""
        if len(self.numeric_cols) == 0:
            print("수치형 변수가 없습니다.")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # 1. 박스플롯
        data_to_plot = [self.df[col].dropna() for col in self.numeric_cols[:6]]
        axes[0, 0].boxplot(data_to_plot, labels=self.numeric_cols[:6])
        axes[0, 0].set_title('주요 변수 박스플롯', fontsize=14, fontweight='bold')
        axes[0, 0].set_ylabel('값')
        axes[0, 0].tick_params(axis='x', rotation=45)
        
        # 2. 히스토그램 (첫 번째 수치형 변수)
        if len(self.numeric_cols) > 0:
            axes[0, 1].hist(self.df[self.numeric_cols[0]].dropna(), bins=30, 
                           edgecolor='black', alpha=0.7, color='steelblue')
            axes[0, 1].set_title(f'{self.numeric_cols[0]} 분포', fontsize=14, fontweight='bold')
            axes[0, 1].set_xlabel(self.numeric_cols[0])
            axes[0, 1].set_ylabel('빈도')
            axes[0, 1].axvline(self.df[self.numeric_cols[0]].mean(), 
                              color='red', linestyle='--', label='평균')
            axes[0, 1].axvline(self.df[self.numeric_cols[0]].median(), 
                              color='green', linestyle='--', label='중앙값')
            axes[0, 1].legend()
        
        # 3. 상관관계 히트맵
        if len(self.numeric_cols) > 1:
            corr_matrix = self.df[self.numeric_cols].corr()
            sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                       center=0, square=True, ax=axes[1, 0], 
                       cbar_kws={"shrink": .8}, linewidths=1)
            axes[1, 0].set_title('변수 간 상관관계', fontsize=14, fontweight='bold')
        
        # 4. 통계량 요약 테이블
        stats_summary = self.df[self.numeric_cols].describe().T
        axes[1, 1].axis('tight')
        axes[1, 1].axis('off')
        table = axes[1, 1].table(cellText=stats_summary.values.round(2),
                                 rowLabels=stats_summary.index,
                                 colLabels=stats_summary.columns,
                                 cellLoc='center',
                                 loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1.2, 1.5)
        axes[1, 1].set_title('요약 통계량', fontsize=14, fontweight='bold', pad=20)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"요약 통계량 차트 저장: {save_path}")
        plt.show()
    
    def create_interactive_plotly_dashboard(self, save_path='results/interactive_dashboard.html'):
        """인터랙티브 Plotly 대시보드 생성"""
        if len(self.numeric_cols) < 2:
            print("인터랙티브 대시보드를 생성하기에 충분한 수치형 변수가 없습니다.")
            return
        
        # 서브플롯 생성
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('변수 분포', '상관관계', '시계열 추세', '변수 비교'),
            specs=[[{"secondary_y": False}, {"type": "heatmap"}],
                   [{"type": "scatter"}, {"type": "box"}]]
        )
        
        # 1. 히스토그램
        for i, col in enumerate(self.numeric_cols[:3]):
            fig.add_trace(
                go.Histogram(x=self.df[col], name=col, opacity=0.7),
                row=1, col=1
            )
        
        # 2. 상관관계 히트맵
        if len(self.numeric_cols) > 1:
            corr_matrix = self.df[self.numeric_cols[:10]].corr()
            fig.add_trace(
                go.Heatmap(z=corr_matrix.values,
                          x=corr_matrix.columns,
                          y=corr_matrix.columns,
                          colorscale='RdBu',
                          zmid=0,
                          text=corr_matrix.values.round(2),
                          texttemplate='%{text}',
                          textfont={"size": 10}),
                row=1, col=2
            )
        
        # 3. 산점도 (첫 두 변수)
        if len(self.numeric_cols) >= 2:
            fig.add_trace(
                go.Scatter(x=self.df[self.numeric_cols[0]],
                          y=self.df[self.numeric_cols[1]],
                          mode='markers',
                          name='관계',
                          marker=dict(size=5, opacity=0.6)),
                row=2, col=1
            )
        
        # 4. 박스플롯
        for col in self.numeric_cols[:3]:
            fig.add_trace(
                go.Box(y=self.df[col], name=col),
                row=2, col=2
            )
        
        # 레이아웃 업데이트
        fig.update_layout(
            title_text="데이터 분석 대시보드",
            title_x=0.5,
            height=900,
            showlegend=True
        )
        
        fig.update_xaxes(title_text="값", row=1, col=1)
        fig.update_yaxes(title_text="빈도", row=1, col=1)
        fig.update_xaxes(title_text=self.numeric_cols[0] if len(self.numeric_cols) >= 2 else "", row=2, col=1)
        fig.update_yaxes(title_text=self.numeric_cols[1] if len(self.numeric_cols) >= 2 else "", row=2, col=1)
        
        fig.write_html(save_path)
        print(f"인터랙티브 대시보드 저장: {save_path}")
        return fig
    
    def create_time_series_analysis(self, date_col=None, value_col=None, 
                                    save_path='results/time_series.png'):
        """시계열 분석 차트"""
        # 날짜 컬럼이 있는 경우 시계열 분석 수행
        if date_col and date_col in self.df.columns:
            self.df[date_col] = pd.to_datetime(self.df[date_col])
            self.df = self.df.sort_values(date_col)
            
            if value_col and value_col in self.df.columns:
                plt.figure(figsize=(14, 6))
                plt.plot(self.df[date_col], self.df[value_col], linewidth=2, alpha=0.7)
                plt.title(f'{value_col} 시계열 추세', fontsize=14, fontweight='bold')
                plt.xlabel('날짜')
                plt.ylabel(value_col)
                plt.grid(True, alpha=0.3)
                plt.tight_layout()
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                print(f"시계열 차트 저장: {save_path}")
                plt.show()
        else:
            print("시계열 분석을 위한 날짜 컬럼이 없습니다.")
    
    def create_distribution_comparison(self, save_path='results/distribution_comparison.png'):
        """분포 비교 차트"""
        if len(self.numeric_cols) == 0:
            return
        
        n_cols = min(4, len(self.numeric_cols))
        n_rows = (len(self.numeric_cols[:12]) + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(16, 4*n_rows))
        axes = axes.flatten() if n_rows > 1 else [axes] if n_cols == 1 else axes
        
        for idx, col in enumerate(self.numeric_cols[:12]):
            if idx < len(axes):
                self.df[col].hist(bins=30, ax=axes[idx], edgecolor='black', alpha=0.7)
                axes[idx].set_title(f'{col}', fontweight='bold')
                axes[idx].set_xlabel('값')
                axes[idx].set_ylabel('빈도')
                axes[idx].axvline(self.df[col].mean(), color='red', 
                                 linestyle='--', linewidth=1, label='평균')
                axes[idx].legend()
        
        # 빈 subplot 제거
        for idx in range(len(self.numeric_cols[:12]), len(axes)):
            fig.delaxes(axes[idx])
        
        plt.suptitle('변수별 분포 비교', fontsize=16, fontweight='bold', y=1.02)
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"분포 비교 차트 저장: {save_path}")
        plt.show()


def main():
    """메인 실행 함수"""
    import os
    os.makedirs('results', exist_ok=True)
    
    # 대시보드 생성
    dashboard = DataVisualizationDashboard()
    
    # 다양한 시각화 생성
    print("\n1. 요약 통계량 차트 생성 중...")
    dashboard.create_summary_statistics_chart()
    
    print("\n2. 인터랙티브 대시보드 생성 중...")
    dashboard.create_interactive_plotly_dashboard()
    
    print("\n3. 분포 비교 차트 생성 중...")
    dashboard.create_distribution_comparison()
    
    print("\n모든 시각화가 완료되었습니다!")


if __name__ == '__main__':
    main()

