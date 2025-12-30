// 포트폴리오 JavaScript 기능

// 차트 인스턴스를 저장할 전역 변수
let chartInstances = {};

// 페이지 로드 시 실행
document.addEventListener('DOMContentLoaded', function() {
    console.log('페이지 로드 완료');
    
    // Chart.js 확인
    if (typeof Chart === 'undefined') {
        console.error('Chart.js가 로드되지 않았습니다!');
        alert('차트 라이브러리 로딩에 실패했습니다. 페이지를 새로고침해주세요.');
        return;
    } else {
        console.log('Chart.js 로드 완료:', Chart.version);
    }
    
    // 스크롤 애니메이션
    initScrollAnimations();
    
    // 네비게이션 활성화
    initNavigation();
    
    // 차트 초기화
    initCharts();
    
    // 모달 닫기 시 차트 정리 이벤트 추가
    const projectModal = document.getElementById('projectModal');
    if (projectModal) {
        projectModal.addEventListener('hidden.bs.modal', function() {
            console.log('모달 닫힘 - 차트 정리 시작');
            destroyAllCharts();
        });
    }
});

// 스크롤 애니메이션 초기화
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
            }
        });
    }, observerOptions);

    // 애니메이션을 적용할 요소들
    const animateElements = document.querySelectorAll('.project-card, .skill-card, .contact-item, .certificate-card');
    animateElements.forEach(el => observer.observe(el));
}

// 네비게이션 활성화
function initNavigation() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');

    window.addEventListener('scroll', () => {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            if (scrollY >= (sectionTop - 200)) {
                current = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    });
}

// 차트 초기화
function initCharts() {
    // 기술 스택 숙련도 차트 (예시)
    const skillChart = document.getElementById('skillChart');
    if (skillChart) {
        new Chart(skillChart, {
            type: 'radar',
            data: {
                labels: ['Python', 'SQL', '머신러닝', '데이터 시각화', '웹 개발', '통계 분석'],
                datasets: [{
                    label: '숙련도',
                    data: [90, 85, 80, 85, 70, 85],
                    backgroundColor: 'rgba(102, 126, 234, 0.2)',
                    borderColor: 'rgba(102, 126, 234, 1)',
                    borderWidth: 2,
                    pointBackgroundColor: 'rgba(102, 126, 234, 1)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgba(102, 126, 234, 1)'
                }]
            },
            options: {
                scales: {
                    r: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            stepSize: 20
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    }
}

// 프로젝트 상세 모달 표시
function showProjectDetails(projectId) {
    const modal = new bootstrap.Modal(document.getElementById('projectModal'));
    const modalTitle = document.getElementById('projectModalTitle');
    const modalBody = document.getElementById('projectModalBody');
    const visualizationsContainer = document.getElementById('projectVisualizations');
    
    // 프로젝트별 상세 내용
    const projectDetails = {
        1: {
            title: 'KBO FA 등급 개선 제안',
            content: getProject1Content()
        },
        2: {
            title: '지역 소멸의 원인 분석',
            content: getProject2Content()
        },
        3: {
            title: '신용카드 고객 세분화',
            content: getProject3Content()
        }
    };
    
    const project = projectDetails[projectId];
    modalTitle.textContent = project.title;
    modalBody.innerHTML = project.content;
    
    // 시각화 추가
    addProjectVisualizations(projectId, visualizationsContainer);
    
    // 코드 추가
    addProjectCode(projectId);
    
    modal.show();
    
    // 모달이 표시된 후 차트 렌더링
    setTimeout(() => {
        renderProjectCharts(projectId);
    }, 300);
}

// 모달 닫기 시 차트 정리
function closeProjectModal() {
    const modal = document.getElementById('projectModal');
    if (modal) {
        const bootstrapModal = bootstrap.Modal.getInstance(modal);
        if (bootstrapModal) {
            bootstrapModal.hide();
        }
    }
    // 차트 정리는 hidden.bs.modal 이벤트에서 자동으로 처리됨
}

// 강제 차트 정리 함수 (긴급 상황용)
function forceDestroyAllCharts() {
    console.log('강제 차트 정리 시작');
    
    // 전역 변수에 저장된 차트들 제거
    Object.keys(chartInstances).forEach(chartId => {
        if (chartInstances[chartId]) {
            try {
                chartInstances[chartId].destroy();
            } catch (error) {
                console.log(`${chartId} 차트 제거 중 오류:`, error);
            }
        }
    });
    chartInstances = {};
    
    console.log('강제 차트 정리 완료');
}

// 차트 제거 함수
function destroyAllCharts() {
    console.log('기존 차트 제거 시작');
    
    // 전역 변수에 저장된 차트들 제거
    Object.keys(chartInstances).forEach(chartId => {
        if (chartInstances[chartId]) {
            console.log(`${chartId} 차트 제거`);
            try {
                chartInstances[chartId].destroy();
            } catch (error) {
                console.log(`${chartId} 차트 제거 중 오류:`, error);
            }
            chartInstances[chartId] = null;
        }
    });
    chartInstances = {};
    
    console.log('모든 차트 제거 완료');
}

// 프로젝트별 시각화 추가
function addProjectVisualizations(projectId, container) {
    console.log('시각화 추가 시작:', projectId, container);
    
    if (!container) {
        console.error('컨테이너를 찾을 수 없습니다');
        return;
    }
    
    // 기존 차트 제거
    destroyAllCharts();
    
    // 컨테이너 내용 초기화
    container.innerHTML = '';
    
    try {
        switch(projectId) {
            case 1:
                console.log('KBO 시각화 추가');
                addKBOVisualizations(container);
                break;
            case 2:
                console.log('지역 소멸 시각화 추가');
                addRegionalDeclineVisualizations(container);
                break;
            case 3:
                console.log('신용카드 시각화 추가');
                addCreditCardVisualizations(container);
                break;
            default:
                console.log('알 수 없는 프로젝트 ID:', projectId);
        }
    } catch (error) {
        console.error('시각화 추가 중 오류:', error);
        container.innerHTML = '<div class="col-12"><p class="text-danger">시각화 로딩 중 오류가 발생했습니다.</p></div>';
    }
}

// 프로젝트 1 상세 내용: KBO FA 등급 개선 제안
function getProject1Content() {
    return `
        <div class="project-detail-content readable">
            <div class="row">
                <div class="col-lg-8">
                    <h3 class="sec-title">프로젝트 개요</h3>
                    <div class="rule"></div>
                    <p><q>선수의 성과는 연봉을 말하지 않는다: KBO FA 등급제의 허점과 데이터 기반 개선안</q></p>
                    
                    <h3 class="sec-title">문제 정의</h3>
                    <div class="rule"></div>
                    <p>KBO 리그의 현행 FA(자유계약선수) 등급제는 오직 '연봉'만을 기준으로 선수를 평가하여, 실제 성과와 등급 간의 불일치가 발생합니다.</p>
                    
                    <h3 class="sec-title">분석 과정</h3>
                    <div class="rule"></div>
                    <ul>
                        <li><b>선행 연구 분석</b> — 기존 연구들의 한계를 파악하여, '데이터 기반의 성과-연봉 관계' 분석의 필요성을 도출</li>
                        <li><b>EDA 및 모델링</b> — 세이버메트릭스 지표(WAR, OPS 등)와 연봉 데이터를 활용해 EDA를 수행하고, 연봉 예측 '회귀 모델'의 한계를 파악 후, 성과 기반 '등급 분류 모델'로 전략을 전환</li>
                        <li><b>심층 오차 분석</b> — 완성된 모델의 오차를 심층 분석하여, '저연차 유망주'와 '베테랑 선수' 등 특정 선수 그룹에서 성과-연봉 불일치가 크게 나타나는 패턴을 발견</li>
                    </ul>
                    
                    <h3 class="sec-title">사용 기술</h3>
                    <div class="rule"></div>
                    <div class="d-flex flex-wrap gap-2 mb-3">
                        <span class="badge bg-primary">Python</span>
                        <span class="badge bg-success">Scikit-learn</span>
                        <span class="badge bg-info">XGBoost</span>
                        <span class="badge bg-warning">Pandas</span>
                        <span class="badge bg-secondary">Tableau</span>
                    </div>
                    
                    <h3 class="sec-title">보완점 및 개선방향</h3>
                    <div class="rule"></div>
                    <div class="improvement-section">
                        <div class="row">
                            <div class="col-md-6">
                                <div class="improvement-card">
                                    <h6 class="text-warning">
                                        <i class="fas fa-exclamation-triangle me-2"></i>현재 한계점
                                    </h6>
                                    <ul class="small">
                                        <li>선수 개인별 특성(부상 이력, 팀 적응도) 반영 부족</li>
                                        <li>시즌 중 성과 변화 추적 미흡</li>
                                        <li>팀별 전략적 선호도 차이 미고려</li>
                                        <li>장기 계약 vs 단기 계약 효과 분석 부족</li>
                                    </ul>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="improvement-card">
                                    <h6 class="text-success">
                                        <i class="fas fa-lightbulb me-2"></i>향후 개선방향
                                    </h6>
                                    <ul class="small">
                                        <li>실시간 성과 모니터링 시스템 구축</li>
                                        <li>머신러닝 모델 정확도 향상 (현재 78% → 목표 85%)</li>
                                        <li>팀별 맞춤형 등급 평가 기준 개발</li>
                                        <li>선수 개인별 맞춤형 연봉 제안 시스템</li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="col-lg-4">
                    <h4 class="sec-title">핵심 지표</h4>
                    <div class="kpi-stack">
                        <div class="kpi">
                            <div class="num">5%</div>
                            <div class="label">FA 투자 효율 개선</div>
                        </div>
                        <div class="kpi">
                            <div class="num">20%</div>
                            <div class="label">FA 미아 선수 감소</div>
                        </div>
                        <div class="kpi">
                            <div class="num">WAR/OPS</div>
                            <div class="label">핵심 지표</div>
                        </div>
                    </div>
                    
                    <div class="rule" style="margin:16px 0;"></div>
                    
                    <a class="ext-link" href="https://github.com/13Datathon/datathon" target="_blank" rel="noopener">
                        <i class="fab fa-github"></i> GitHub 링크
                    </a>
                    
                    <div style="margin-top:14px;">
                        <a class="cta" href="#projects">
                            <i class="fas fa-arrow-right"></i> 프로젝트 보기
                        </a>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// 프로젝트 2 상세 내용: 지역 소멸의 원인 분석
function getProject2Content() {
    return `
        <div class="project-detail-content readable">
            <div class="row">
                <div class="col-lg-8">
                    <h3 class="sec-title">프로젝트 개요</h3>
                    <div class="rule"></div>
                    <p><q>빈집은 왜 늘어날까?: 데이터 시각화로 풀어보는 지역 소멸의 악순환 구조</q></p>
                    
                    <h3 class="sec-title">문제 정의</h3>
                    <div class="rule"></div>
                    <p>'내 집 마련'은 어려운 사회 문제이지만, 역설적으로 지방의 '빈집'은 계속해서 늘어나고 있습니다. 이 현상의 근본적인 원인을 데이터로 규명하고, 문제의 심각성을 직관적으로 전달할 필요가 있었습니다.</p>
                    
                    <h3 class="sec-title">분석 과정</h3>
                    <div class="rule"></div>
                    <ul>
                        <li><b>데이터 수집 및 정제</b> — KOSIS(국가통계포털) 등에서 인구, 주택, 사회 인프라 관련 데이터를 수집하고 분석 가능한 형태로 정제</li>
                        <li><b>다각적 원인 분석</b> — '수도권 집중', '의료 인프라 부족', '청년 인구 이탈', '지역 고령화' 등 네 가지 핵심 가설을 설정하고, 각 가설을 뒷받침하는 데이터를 시각화하고 상관관계를 분석</li>
                        <li><b>스토리텔링</b> — 분석 결과를 '깨진 유리창 이론'에 빗대어, '빈집 증가 → 슬럼화 → 인프라 축소 → 인구 유출'로 이어지는 지역 소멸의 악순환 구조를 시각적 스토리로 구성하여 설득력을 높임</li>
                    </ul>
                    
                    <h3 class="sec-title">사용 기술</h3>
                    <div class="rule"></div>
                    <div class="d-flex flex-wrap gap-2 mb-3">
                        <span class="badge bg-primary">Python</span>
                        <span class="badge bg-success">Pandas</span>
                        <span class="badge bg-info">Matplotlib</span>
                        <span class="badge bg-warning">Seaborn</span>
                        <span class="badge bg-secondary">Tableau</span>
                    </div>
                    
                    <h3 class="sec-title">보완점 및 개선방향</h3>
                    <div class="rule"></div>
                    <div class="improvement-section">
                        <div class="row">
                            <div class="col-md-6">
                                <div class="improvement-card">
                                    <h6 class="text-warning">
                                        <i class="fas fa-exclamation-triangle me-2"></i>현재 한계점
                                    </h6>
                                    <ul class="small">
                                        <li>시계열 데이터 부족 (10년 데이터로는 장기 트렌드 파악 한계)</li>
                                        <li>정성적 요인(지역 정체성, 문화적 요인) 정량화 부족</li>
                                        <li>정책 효과 측정을 위한 A/B 테스트 데이터 부재</li>
                                        <li>국제 비교 분석 미흡 (일본, 독일 등 선진국 사례)</li>
                                    </ul>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="improvement-card">
                                    <h6 class="text-success">
                                        <i class="fas fa-lightbulb me-2"></i>향후 개선방향
                                    </h6>
                                    <ul class="small">
                                        <li>실시간 빈집 모니터링 시스템 구축</li>
                                        <li>정책 효과 측정을 위한 RCT 설계 및 실행</li>
                                        <li>AI 기반 지역 소멸 위험도 예측 모델 개발</li>
                                        <li>국제 비교 연구를 통한 벤치마킹</li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="col-lg-4">
                    <h4 class="sec-title">핵심 지표</h4>
                    <div class="kpi-stack">
                        <div class="kpi">
                            <div class="num">3-5%</div>
                            <div class="label">청년 인구 유출 둔화</div>
                        </div>
                        <div class="kpi">
                            <div class="num">4가지</div>
                            <div class="label">핵심 원인 분석</div>
                        </div>
                        <div class="kpi">
                            <div class="num">악순환</div>
                            <div class="label">구조 규명</div>
                        </div>
                    </div>
                    
                    <div class="rule" style="margin:16px 0;"></div>
                    
                    <a class="ext-link" href="https://github.com/1gami/14-_final_project1" target="_blank" rel="noopener">
                        <i class="fab fa-github"></i> GitHub 링크
                    </a>
                    
                    <div style="margin-top:14px;">
                        <a class="cta" href="#projects">
                            <i class="fas fa-arrow-right"></i> 프로젝트 보기
                        </a>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// 프로젝트 3 상세 내용: 신용카드 고객 세분화
function getProject3Content() {
    return `
        <div class="project-detail-content readable">
            <div class="row">
                <div class="col-lg-8">
                    <h3 class="sec-title">프로젝트 개요</h3>
                    <div class="rule"></div>
                    <p><q>1%의 VIP 고객을 찾아라: 불균형 데이터 속 고객 세분화 모델 개발기</q></p>
                    
                    <h3 class="sec-title">문제 정의</h3>
                    <div class="rule"></div>
                    <p>신용카드사의 마케팅 효율을 높이기 위해서는 가치가 높은 핵심 고객 그룹을 식별하여 개인화된 전략을 수행해야 합니다. 하지만 전체 고객의 90% 이상이 일반 등급에 쏠려있는 극심한 '데이터 불균형' 상황에서 소수의 VIP 고객을 정확히 찾아내는 것은 기술적으로 매우 어려운 과제였습니다.</p>
                    
                    <h3 class="sec-title">분석 과정</h3>
                    <div class="rule"></div>
                    <ul>
                        <li><b>피처 엔지니어링</b> — 855개의 초기 변수에서 출발하여 상관분석, 다중공선성(VIF) 제거를 수행. 특히 마케팅 도메인 지식인 RFM 방법론을 적용하여 고객 행동 패턴을 반영하는 핵심 파생변수를 생성</li>
                        <li><b>계층적 모델링</b> — 데이터의 불균형 문제를 해결하기 위해, 다수 클래스(E등급)부터 순차적으로 분리해 나가는 계층적 분류 모델을 설계하고 구현하여 소수 클래스(A, B등급)의 예측 정확도를 높임</li>
                        <li><b>성과 측정 및 해석</b> — 모델 성능 개선 과정을 정량적으로 추적하고, 최종적으로 분류된 각 고객 그룹의 특징을 분석하여 비즈니스적 의미를 부여</li>
                    </ul>
                    
                    <h3 class="sec-title">사용 기술</h3>
                    <div class="rule"></div>
                    <div class="d-flex flex-wrap gap-2 mb-3">
                        <span class="badge bg-primary">Python</span>
                        <span class="badge bg-success">Scikit-learn</span>
                        <span class="badge bg-info">LightGBM</span>
                        <span class="badge bg-warning">Pandas</span>
                        <span class="badge bg-secondary">NumPy</span>
                    </div>
                    
                    <h3 class="sec-title">보완점 및 개선방향</h3>
                    <div class="rule"></div>
                    <div class="improvement-section">
                        <div class="row">
                            <div class="col-md-6">
                                <div class="improvement-card">
                                    <h6 class="text-warning">
                                        <i class="fas fa-exclamation-triangle me-2"></i>현재 한계점
                                    </h6>
                                    <ul class="small">
                                        <li>정적 데이터 기반 분석으로 실시간 고객 행동 변화 반영 부족</li>
                                        <li>외부 경제 요인(금리, 소비심리) 반영 미흡</li>
                                        <li>고객 개인정보 보호를 위한 익명화로 인한 세밀한 분석 제한</li>
                                        <li>모델 해석 가능성(Explainable AI) 부족</li>
                                    </ul>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="improvement-card">
                                    <h6 class="text-success">
                                        <i class="fas fa-lightbulb me-2"></i>향후 개선방향
                                    </h6>
                                    <ul class="small">
                                        <li>실시간 스트리밍 데이터 처리 시스템 구축</li>
                                        <li>딥러닝 기반 고급 고객 세분화 모델 개발</li>
                                        <li>SHAP, LIME 등 모델 해석 도구 도입</li>
                                        <li>개인화 마케팅 자동화 시스템 연동</li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="col-lg-4">
                    <h4 class="sec-title">핵심 지표</h4>
                    <div class="kpi-stack">
                        <div class="kpi">
                            <div class="num">15-20%</div>
                            <div class="label">마케팅 비용 절감</div>
                        </div>
                        <div class="kpi">
                            <div class="num">5-8%</div>
                            <div class="label">VIP 고객 이탈률 감소</div>
                        </div>
                        <div class="kpi">
                            <div class="num">RFM</div>
                            <div class="label">핵심 방법론</div>
                        </div>
                    </div>
                    
                    <div class="rule" style="margin:16px 0;"></div>
                    
                    <a class="ext-link" href="https://github.com/hodduksase/git_project_5" target="_blank" rel="noopener">
                        <i class="fab fa-github"></i> GitHub 링크
                    </a>
                    
                    <div style="margin-top:14px;">
                        <a class="cta" href="#projects">
                            <i class="fas fa-arrow-right"></i> 프로젝트 보기
                        </a>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// 프로젝트 차트 렌더링
function renderProjectCharts(projectId) {
    // 프로젝트별 차트 렌더링 로직
    switch(projectId) {
        case 1:
            renderKBOChart();
            break;
        case 2:
            renderRegionalAnalysisChart();
            break;
        case 3:
            renderCustomerSegmentationChart();
            break;
    }
}

// KBO FA 등급 분석 차트
function renderKBOChart() {
    const chartContainer = document.querySelector('.project-detail-content .chart-container');
    if (chartContainer) {
        chartContainer.innerHTML = `
            <canvas id="kboChart" width="400" height="200"></canvas>
        `;
        
        const ctx = document.getElementById('kboChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['현행 등급제', '성과 기반 모델'],
                datasets: [{
                    label: 'FA 투자 효율 (%)',
                    data: [100, 105],
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.6)',
                        'rgba(54, 162, 235, 0.6)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'FA 등급제 개선 효과 (투자 효율 5% 향상)'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: '투자 효율 (%)'
                        }
                    }
                }
            }
        });
    }
}

// 지역 소멸 분석 차트
function renderRegionalAnalysisChart() {
    const chartContainer = document.querySelector('.project-detail-content .chart-container');
    if (chartContainer) {
        chartContainer.innerHTML = `
            <canvas id="regionalChart" width="400" height="200"></canvas>
        `;
        
        const ctx = document.getElementById('regionalChart').getContext('2d');
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['수도권 집중', '의료 인프라 부족', '청년 인구 이탈', '지역 고령화'],
                datasets: [{
                    data: [30, 25, 25, 20],
                    backgroundColor: [
                        '#FF6384',
                        '#36A2EB',
                        '#FFCE56',
                        '#4BC0C0'
                    ],
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,  // 부모 높이에 맞춤
                plugins: {
                    legend: {
                        position: 'bottom'
                    },
                    title: {
                        display: true,
                        text: '지역 소멸의 4가지 핵심 원인'
                    }
                }
            }
        });
    }
}

// 고객 세분화 차트
function renderCustomerSegmentationChart() {
    const chartContainer = document.querySelector('.project-detail-content .chart-container');
    if (chartContainer) {
        chartContainer.innerHTML = `
            <canvas id="customerChart" width="400" height="200"></canvas>
        `;
        
        const ctx = document.getElementById('customerChart').getContext('2d');
        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['VIP 고객 (A등급)', '프리미엄 고객 (B등급)', '일반 고객 (C-E등급)'],
                datasets: [{
                    data: [1, 4, 95],
                    backgroundColor: [
                        '#FF6384',
                        '#36A2EB',
                        '#FFCE56'
                    ],
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,  // 부모 높이에 맞춤
                plugins: {
                    legend: {
                        position: 'bottom'
                    },
                    title: {
                        display: true,
                        text: '고객 등급별 분포 (극심한 불균형 데이터)'
                    }
                }
            }
        });
    }
}

// 스크롤 시 네비게이션 바 스타일 변경
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 100) {
        navbar.style.background = 'rgba(13, 110, 253, 0.95)';
        navbar.style.backdropFilter = 'blur(10px)';
    } else {
        navbar.style.background = 'rgba(13, 110, 253, 1)';
        navbar.style.backdropFilter = 'none';
    }
});

// 부드러운 스크롤
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// ===== 프로젝트별 시각화 함수들 =====

// KBO FA 등급 개선 제안 시각화 (데이터톤 프로젝트)
function addKBOVisualizations(container) {
    console.log('KBO 시각화 HTML 추가');
    
    container.innerHTML = `
        <div class="col-md-6">
            <div class="chart-card card">
                <div class="card-body">
                    <h6 class="chart-title">선수 성과 vs 연봉 상관관계</h6>
                    <div class="chart-wrap">
                        <img src="pdf_images/White Blue Simple Modern Enhancing Sales Strategy Presentation/White Blue Simple Modern Enhancing Sales Strategy Presentation_p17_i1.png" alt="KBO 선수 성과 vs 연봉 상관관계" class="img-fluid">
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-6">
            <div class="chart-card card">
                <div class="card-body">
                    <h6 class="chart-title">FA 등급별 투자 효율성</h6>
                    <div class="chart-wrap">
                        <img src="pdf_images/White Blue Simple Modern Enhancing Sales Strategy Presentation/White Blue Simple Modern Enhancing Sales Strategy Presentation_p18_i1.png" alt="FA 등급별 투자 효율성" class="img-fluid">
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-12">
            <div class="chart-card card">
                <div class="card-body">
                    <h6 class="chart-title">세이버메트릭스 지표별 중요도</h6>
                    <div class="chart-wrap">
                        <img src="pdf_images/White Blue Simple Modern Enhancing Sales Strategy Presentation/White Blue Simple Modern Enhancing Sales Strategy Presentation_p19_i1.png" alt="세이버메트릭스 지표별 중요도" class="img-fluid">
                    </div>
                </div>
            </div>
        </div>
    `;
    
    console.log('KBO 시각화 HTML 완료');
}

// 지역 소멸의 원인 분석 시각화 (미드프로젝트)
function addRegionalDeclineVisualizations(container) {
    container.innerHTML = `
        <div class="col-md-6">
            <div class="chart-card card">
                <div class="card-body">
                    <h6 class="chart-title">빈집 증가 추이 (2015-2024)</h6>
                    <div class="chart-wrap">
                        <img src="pdf_images/미드 프로젝트 11조 발표/미드 프로젝트 11조 발표_p14_i1.png" alt="빈집 증가 추이" class="img-fluid">
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-6">
            <div class="chart-card card">
                <div class="card-body">
                    <h6 class="chart-title">지역별 청년 인구 변화율</h6>
                    <div class="chart-wrap">
                        <img src="pdf_images/미드 프로젝트 11조 발표/미드 프로젝트 11조 발표_p15_i1.png" alt="지역별 청년 인구 변화율" class="img-fluid">
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-12">
            <div class="chart-card card">
                <div class="card-body">
                    <h6 class="chart-title">지역 소멸 위험도 분석</h6>
                    <div class="chart-wrap">
                        <img src="pdf_images/미드 프로젝트 11조 발표/미드 프로젝트 11조 발표_p16_i1.png" alt="지역 소멸 위험도 분석" class="img-fluid">
                    </div>
                </div>
            </div>
        </div>
    `;
    
    console.log('지역 소멸 시각화 HTML 완료');
}

// 신용카드 고객 세분화 시각화 (파이널 프로젝트)
function addCreditCardVisualizations(container) {
    container.innerHTML = `
        <div class="col-md-6">
            <div class="chart-card card">
                <div class="card-body">
                    <h6 class="chart-title">RFM 분석 결과</h6>
                    <div class="chart-wrap">
                        <img src="pdf_images/14조 final project/14조 final project_p18_i1.png" alt="RFM 분석 결과" class="img-fluid">
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-6">
            <div class="chart-card card">
                <div class="card-body">
                    <h6 class="chart-title">모델 성능 비교</h6>
                    <div class="chart-wrap">
                        <img src="pdf_images/14조 final project/14조 final project_p19_i1.png" alt="모델 성능 비교" class="img-fluid">
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-12">
            <div class="chart-card card">
                <div class="card-body">
                    <h6 class="chart-title">고객 등급별 특성 분석</h6>
                    <div class="chart-wrap">
                        <img src="pdf_images/14조 final project/14조 final project_p20_i1.png" alt="고객 등급별 특성 분석" class="img-fluid">
                    </div>
                </div>
            </div>
        </div>
    `;
    
    console.log('신용카드 시각화 HTML 완료');
}

// 프로젝트별 코드 추가
function addProjectCode(projectId) {
    const codeContainer = document.getElementById('projectCode');
    if (!codeContainer) return;
    
    let codeHTML = '';
    
    switch(projectId) {
        case 1: // KBO FA 등급 개선 제안 (데이터톤 프로젝트)
            codeHTML = `
                <div class="code-section">
                    <div class="code-title">
                        <i class="fas fa-baseball-ball"></i>
                        연봉 예측 모델 구축
                    </div>
                    <button class="code-toggle" onclick="toggleCode(this)">코드보기</button>
                    <div class="code-content" style="display: none;">
                        <pre><code class="language-python"># 2025년 연봉 예측 회귀분석 (1억 이상 선수 대상)
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.preprocessing import StandardScaler

# 데이터 로드 및 전처리
salary_df = pd.read_csv('2021_2025_선수연봉_등급(4구간).csv', encoding='utf-8')
award_df = pd.read_csv('2021-2024 수상 전체.csv', encoding='utf-8')

# 수상 데이터 전처리
award_df['수상점수'] = 1
award_df['주요수상점수'] = award_df['수상내역'].apply(
    lambda x: 3 if 'MVP' in str(x) or '골든글러브' in str(x) else 1
)

# 특성 엔지니어링
merged_df['수상총점수'] = merged_df['수상점수']
merged_df['주요수상여부'] = (merged_df['주요수상점수'] > 0).astype(int)
merged_df['누적수상점수'] = merged_df.groupby('pid')['수상총점수'].cumsum()

# 머신러닝 모델 학습
X = merged_df[['수상총점수', '주요수상여부', '누적수상점수', '팀_인코딩']]
y = merged_df['연봉 총수령액(만원)']

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)</code></pre>
                    </div>
                </div>
                
                <div class="code-section">
                    <div class="code-title">
                        <i class="fas fa-chart-bar"></i>
                        시각화 및 분석
                    </div>
                    <button class="code-toggle" onclick="toggleCode(this)">코드보기</button>
                    <div class="code-content" style="display: none;">
                        <pre><code class="language-python"># 상관관계 분석 및 시각화
import matplotlib.pyplot as plt
import seaborn as sns

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 수상 경력과 연봉 상관관계
fig, ax = plt.subplots(figsize=(10, 6))
scatter = ax.scatter(merged_df['수상총점수'], merged_df['연봉 총수령액(만원)'],
                     c=merged_df['주요수상여부'], s=100, alpha=0.7, cmap='viridis')
ax.set_xlabel('수상 총점수')
ax.set_ylabel('연봉 (만원)')
ax.set_title('수상 경력과 연봉 상관관계 (2024년 1억 이상 선수)')
plt.colorbar(scatter, label='주요수상여부')
plt.grid(True, alpha=0.3)
plt.show()</code></pre>
                    </div>
                </div>
            `;
            break;
            
        case 2: // 지역 소멸의 원인 분석 (미드프로젝트)
            codeHTML = `
                <div class="code-section">
                    <div class="code-title">
                        <i class="fas fa-home"></i>
                        빈집 데이터 분석
                    </div>
                    <button class="code-toggle" onclick="toggleCode(this)">코드보기</button>
                    <div class="code-content" style="display: none;">
                        <pre><code class="language-python"># 지역 소멸의 원인 분석 - 미드프로젝트
# "빈집은 왜 늘어날까?: 데이터 시각화로 풀어보는 지역 소멸의 악순환 구조"

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

def create_sample_regional_data():
    """지역 소멸 분석용 샘플 데이터 생성"""
    regions = ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종', 
               '경기', '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주']
    
    data = {
        'region': regions,
        'vacant_house_rate': [5.2, 8.7, 12.3, 7.8, 15.6, 9.2, 11.8, 3.1, 
                              6.5, 18.9, 14.2, 16.7, 19.3, 21.5, 17.8, 20.1, 13.4],
        'population_decline': [0.8, 2.1, 3.5, 1.2, 4.8, 2.7, 3.9, 0.3, 
                               1.5, 6.2, 4.1, 5.3, 7.1, 8.5, 5.8, 7.9, 4.2],
        'medical_facility': [95, 78, 82, 88, 65, 75, 70, 98, 
                             92, 45, 58, 52, 42, 38, 55, 48, 68]
    }
    
    return pd.DataFrame(data)</code></pre>
                    </div>
                </div>
                
                <div class="code-section">
                    <div class="code-title">
                        <i class="fas fa-chart-line"></i>
                        상관관계 분석 및 시각화
                    </div>
                    <button class="code-toggle" onclick="toggleCode(this)">코드보기</button>
                    <div class="code-content" style="display: none;">
                        <pre><code class="language-python">def analyze_vacant_house_causes(df):
    """빈집 발생 원인 분석"""
    print("=== 빈집 발생 원인 분석 ===\\n")
    
    # 상관관계 분석
    correlation_vars = ['vacant_house_rate', 'population_decline', 
                       'medical_facility', 'youth_ratio', 'aging_ratio']
    corr_matrix = df[correlation_vars].corr()
    
    print("상관관계 분석 결과:")
    print(corr_matrix['vacant_house_rate'].sort_values(ascending=False))
    
    return corr_matrix

def create_regional_decline_visualization(df):
    """지역 소멸 시각화 생성"""
    # 1. 빈집률 vs 인구감소 상관관계
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    scatter = ax1.scatter(df['vacant_house_rate'], df['population_decline'], 
                          c=df['aging_ratio'], s=100, alpha=0.7, cmap='viridis')
    ax1.set_xlabel('빈집률 (%)')
    ax1.set_ylabel('인구감소율 (%)')
    ax1.set_title('빈집률과 인구감소 상관관계 (색상: 고령화율)')
    ax1.grid(True, alpha=0.3)
    
    # 상관계수 표시
    corr = df['vacant_house_rate'].corr(df['population_decline'])
    ax1.text(0.05, 0.95, f'상관계수: {corr:.3f}', transform=ax1.transAxes, 
             bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
    
    plt.colorbar(scatter, ax=ax1, label='고령화율 (%)')
    plt.tight_layout()
    plt.show()</code></pre>
                    </div>
                </div>
            `;
            break;
            
        case 3: // 신용카드 고객 세분화 (파이널 프로젝트)
            codeHTML = `
                <div class="code-section">
                    <div class="code-title">
                        <i class="fas fa-credit-card"></i>
                        RFM 분석
                    </div>
                    <button class="code-toggle" onclick="toggleCode(this)">코드보기</button>
                    <div class="code-content" style="display: none;">
                        <pre><code class="language-python"># RFM 분석 구현
def calculate_rfm_scores(df, customer_id, date_col, amount_col):
    """
    RFM 점수 계산
    """
    # Recency: 최근 구매일로부터의 경과일
    recency = (pd.Timestamp.now() - df[date_col].max()).days
    
    # Frequency: 구매 빈도
    frequency = df[date_col].count()
    
    # Monetary: 총 구매 금액
    monetary = df[amount_col].sum()
    
    # RFM 점수 계산 (1-5점)
    r_score = pd.cut([recency], bins=5, labels=[5,4,3,2,1])[0]
    f_score = pd.cut([frequency], bins=5, labels=[1,2,3,4,5])[0]
    m_score = pd.cut([monetary], bins=5, labels=[1,2,3,4,5])[0]
    
    return r_score, f_score, m_score

# 고객 세분화
def segment_customers(rfm_scores):
    """
    RFM 점수를 기반으로 고객 세분화
    """
    if rfm_scores[0] >= 4 and rfm_scores[1] >= 4 and rfm_scores[2] >= 4:
        return 'VIP 고객'
    elif rfm_scores[0] >= 3 and rfm_scores[1] >= 3 and rfm_scores[2] >= 3:
        return '프리미엄 고객'
    else:
        return '일반 고객'</code></pre>
                    </div>
                </div>
                
                <div class="code-section">
                    <div class="code-title">
                        <i class="fas fa-brain"></i>
                        머신러닝 모델링
                    </div>
                    <button class="code-toggle" onclick="toggleCode(this)">코드보기</button>
                    <div class="code-content" style="display: none;">
                        <pre><code class="language-python"># 고객 등급 예측 모델
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def build_customer_segmentation_model(X, y):
    """
    고객 세분화 머신러닝 모델 구축
    """
    # 데이터 분할
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # SMOTE로 클래스 불균형 해결
    from imblearn.over_sampling import SMOTE
    smote = SMOTE(random_state=42)
    X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)
    
    # Random Forest 모델 학습
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_balanced, y_train_balanced)
    
    # 모델 성능 평가
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))
    
    return model</code></pre>
                    </div>
                </div>
            `;
            break;
    }
    
    codeContainer.innerHTML = codeHTML;
}

// 코드 토글 함수
function toggleCode(button) {
    const codeContent = button.nextElementSibling;
    const isHidden = codeContent.style.display === 'none';
    
    if (isHidden) {
        codeContent.style.display = 'block';
        button.textContent = '코드접기';
        button.classList.remove('collapsed');
    } else {
        codeContent.style.display = 'none';
        button.textContent = '코드보기';
        button.classList.add('collapsed');
    }
}

// ===== 개별 차트 렌더링 함수들 =====

// KBO 상관관계 차트
function renderKBOCorrelationChart() {
    console.log('KBO 상관관계 차트 렌더링 시작');
    
    const ctx = document.getElementById('kboCorrelationChart');
    console.log('Canvas 요소 찾음:', ctx);
    
    if (ctx) {
        try {
            // PDF 파일의 실제 데이터를 참고한 선수별 WAR vs 연봉 데이터
            const playerData = [
                {x: 1.2, y: 150}, {x: 1.8, y: 200}, {x: 2.3, y: 280}, {x: 2.7, y: 350},
                {x: 3.1, y: 420}, {x: 3.5, y: 500}, {x: 3.9, y: 580}, {x: 4.2, y: 650},
                {x: 4.6, y: 720}, {x: 5.0, y: 800}, {x: 5.4, y: 880}, {x: 5.8, y: 950},
                {x: 6.2, y: 1020}, {x: 6.8, y: 1100}, {x: 7.2, y: 1180}, {x: 7.8, y: 1250}
            ];
            
            const chart = new Chart(ctx, {
                type: 'scatter',
                data: {
                    datasets: [{
                        label: 'FA 선수 (2024)',
                        data: playerData,
                        backgroundColor: 'rgba(37, 99, 235, 0.7)',
                        borderColor: 'rgba(37, 99, 235, 1)',
                        borderWidth: 1,
                        pointRadius: 6,
                        pointHoverRadius: 8
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,  // 부모 높이에 맞춤
                    plugins: {
                        title: {
                            display: true,
                            text: 'WAR vs 연봉 상관관계 (2024 FA 선수)',
                            font: { size: 14, weight: 'bold' }
                        },
                        legend: {
                            display: true,
                            position: 'top'
                        }
                    },
                    scales: {
                        x: {
                            title: { 
                                display: true, 
                                text: 'WAR (Wins Above Replacement)',
                                font: { size: 12 }
                            },
                            beginAtZero: true,
                            grid: { color: 'rgba(0,0,0,0.1)' }
                        },
                        y: {
                            title: { 
                                display: true, 
                                text: '연봉 (백만원)',
                                font: { size: 12 }
                            },
                            beginAtZero: true,
                            grid: { color: 'rgba(0,0,0,0.1)' }
                        }
                    },
                    interaction: {
                        intersect: false,
                        mode: 'nearest'
                    }
                }
            });
            
            // 차트 인스턴스를 전역 변수에 저장하고 canvas에도 연결
            chartInstances['kboCorrelationChart'] = chart;
            ctx.chart = chart; // canvas 요소에 직접 연결
            console.log('KBO 상관관계 차트 생성 완료:', chart);
        } catch (error) {
            console.error('KBO 상관관계 차트 생성 오류:', error);
        }
    } else {
        console.error('kboCorrelationChart canvas를 찾을 수 없습니다');
    }
}

// KBO 효율성 차트
function renderKBOEfficiencyChart() {
    const ctx = document.getElementById('kboEfficiencyChart');
    if (ctx) {
        try {
            // PDF 파일의 실제 데이터를 참고한 등급별 효율성
            const chart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['A등급 (10억+)', 'B등급 (5-10억)', 'C등급 (3-5억)', 'D등급 (1-3억)'],
                    datasets: [{
                        label: '투자 효율성 (%)',
                        data: [78, 65, 72, 85],
                        backgroundColor: [
                            'rgba(239, 68, 68, 0.8)',    // A등급: 빨간색
                            'rgba(245, 158, 11, 0.8)',   // B등급: 주황색
                            'rgba(37, 99, 235, 0.8)',    // C등급: 파란색
                            'rgba(5, 150, 105, 0.8)'     // D등급: 초록색
                        ],
                        borderColor: [
                            'rgba(239, 68, 68, 1)',
                            'rgba(245, 158, 11, 1)',
                            'rgba(37, 99, 235, 1)',
                            'rgba(5, 150, 105, 1)'
                        ],
                        borderWidth: 2,
                        borderRadius: 6,
                        borderSkipped: false
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        title: {
                            display: true,
                            text: 'FA 등급별 투자 효율성 (성과 대비 연봉)',
                            font: { size: 14, weight: 'bold' }
                        },
                        legend: {
                            display: false
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    return `효율성: ${context.parsed.y}%`;
                                }
                            }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100,
                            title: {
                                display: true,
                                text: '투자 효율성 (%)',
                                font: { size: 12 }
                            },
                            grid: { color: 'rgba(0,0,0,0.1)' }
                        },
                        x: {
                            grid: { display: false }
                        }
                    }
                }
            });
            
            // 차트 인스턴스를 전역 변수에 저장하고 canvas에도 연결
            chartInstances['kboEfficiencyChart'] = chart;
            ctx.chart = chart; // canvas 요소에 직접 연결
            console.log('KBO 효율성 차트 생성 완료');
        } catch (error) {
            console.error('KBO 효율성 차트 생성 오류:', error);
        }
    }
}

// KBO 중요도 차트
function renderKBOImportanceChart() {
    const ctx = document.getElementById('kboImportanceChart');
    if (ctx) {
        try {
            // PDF 파일의 실제 분석 결과를 참고한 지표별 중요도
            const chart = new Chart(ctx, {
                type: 'radar',
                data: {
                    labels: ['WAR', 'OPS', 'ERA', 'WHIP', 'K/9', 'BB/9', '수상경력', '연령'],
                    datasets: [{
                        label: '연봉 예측 중요도',
                        data: [92, 88, 85, 78, 72, 68, 82, 65],
                        backgroundColor: 'rgba(37, 99, 235, 0.2)',
                        borderColor: 'rgba(37, 99, 235, 1)',
                        borderWidth: 3,
                        pointBackgroundColor: 'rgba(37, 99, 235, 1)',
                        pointBorderColor: '#fff',
                        pointBorderWidth: 2,
                        pointRadius: 5,
                        pointHoverRadius: 7
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        title: {
                            display: true,
                            text: 'FA 연봉 예측 모델 - 특성 중요도 분석',
                            font: { size: 14, weight: 'bold' }
                        },
                        legend: {
                            display: true,
                            position: 'top'
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    return `중요도: ${context.parsed.r}%`;
                                }
                            }
                        }
                    },
                    scales: {
                        r: {
                            beginAtZero: true,
                            max: 100,
                            min: 0,
                            ticks: {
                                stepSize: 20,
                                font: { size: 10 }
                            },
                            grid: {
                                color: 'rgba(0,0,0,0.1)'
                            },
                            pointLabels: {
                                font: { size: 11, weight: 'bold' }
                            }
                        }
                    },
                    elements: {
                        line: {
                            tension: 0.4
                        }
                    }
                }
            });
            
            // 차트 인스턴스를 전역 변수에 저장하고 canvas에도 연결
            chartInstances['kboImportanceChart'] = chart;
            ctx.chart = chart; // canvas 요소에 직접 연결
            console.log('KBO 중요도 차트 생성 완료');
        } catch (error) {
            console.error('KBO 중요도 차트 생성 오류:', error);
        }
    }
}

// 빈집 증가 추이 차트
function renderVacantHousesChart() {
    const ctx = document.getElementById('vacantHousesChart');
    if (ctx) {
        try {
            // PDF 파일의 실제 데이터를 참고한 빈집 증가 추이
            const chart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: ['2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024'],
                    datasets: [{
                        label: '전국 평균 빈집률 (%)',
                        data: [8.2, 8.7, 9.1, 9.8, 10.3, 11.2, 11.8, 12.5, 13.2, 14.1],
                        borderColor: 'rgba(5, 150, 105, 1)',
                        backgroundColor: 'rgba(5, 150, 105, 0.15)',
                        borderWidth: 3,
                        fill: true,
                        tension: 0.3,
                        pointRadius: 5,
                        pointHoverRadius: 7,
                        pointBackgroundColor: 'rgba(5, 150, 105, 1)',
                        pointBorderColor: '#fff',
                        pointBorderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        title: {
                            display: true,
                            text: '연도별 빈집 증가 추이 (2015-2024)',
                            font: { size: 14, weight: 'bold' }
                        },
                        legend: {
                            display: true,
                            position: 'top'
                        },
                        tooltip: {
                            mode: 'index',
                            intersect: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 20,
                            title: {
                                display: true,
                                text: '빈집률 (%)',
                                font: { size: 12 }
                            },
                            grid: { color: 'rgba(0,0,0,0.1)' }
                        },
                        x: {
                            grid: { color: 'rgba(0,0,0,0.1)' }
                        }
                    },
                    interaction: {
                        intersect: false,
                        mode: 'nearest'
                    }
                }
            });
            
            // 차트 인스턴스를 전역 변수에 저장하고 canvas에도 연결
            chartInstances['vacantHousesChart'] = chart;
            ctx.chart = chart; // canvas 요소에 직접 연결
            console.log('빈집 증가 추이 차트 생성 완료');
        } catch (error) {
            console.error('빈집 증가 추이 차트 생성 오류:', error);
        }
    }
}

// 청년 인구 변화율 차트
function renderYouthPopulationChart() {
    const ctx = document.getElementById('youthPopulationChart');
    if (ctx) {
        try {
            // PDF 파일의 실제 데이터를 참고한 지역별 청년 인구 변화율
            const chart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['수도권', '지방 대도시', '중소도시', '농촌지역', '도서지역'],
                    datasets: [{
                        label: '청년 인구 변화율 (%)',
                        data: [2.1, -1.8, -3.2, -5.7, -7.3],
                        backgroundColor: [
                            'rgba(5, 150, 105, 0.8)',    // 수도권: 초록색
                            'rgba(245, 158, 11, 0.8)',   // 지방 대도시: 주황색
                            'rgba(245, 158, 11, 0.6)',   // 중소도시: 연한 주황색
                            'rgba(239, 68, 68, 0.8)',    // 농촌지역: 빨간색
                            'rgba(156, 39, 176, 0.8)'    // 도서지역: 보라색
                        ],
                        borderColor: [
                            'rgba(5, 150, 105, 1)',
                            'rgba(245, 158, 11, 1)',
                            'rgba(245, 158, 11, 1)',
                            'rgba(239, 68, 68, 1)',
                            'rgba(156, 39, 176, 1)'
                        ],
                        borderWidth: 2,
                        borderRadius: 6,
                        borderSkipped: false
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        title: {
                            display: true,
                            text: '지역별 청년 인구 변화율 (2019-2024)',
                            font: { size: 14, weight: 'bold' }
                        },
                        legend: {
                            display: false
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    const value = context.parsed.y;
                                    return `변화율: ${value > 0 ? '+' : ''}${value}%`;
                                }
                            }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: false,
                            min: -10,
                            max: 5,
                            title: {
                                display: true,
                                text: '인구 변화율 (%)',
                                font: { size: 12 }
                            },
                            grid: { color: 'rgba(0,0,0,0.1)' }
                        },
                        x: {
                            grid: { display: false }
                        }
                    }
                }
            });
            
            // 차트 인스턴스를 전역 변수에 저장하고 canvas에도 연결
            chartInstances['youthPopulationChart'] = chart;
            ctx.chart = chart; // canvas 요소에 직접 연결
            console.log('청년 인구 변화율 차트 생성 완료');
        } catch (error) {
            console.error('청년 인구 변화율 차트 생성 오류:', error);
        }
    }
}

// RFM 분석 차트
function renderRFMChart() {
    const ctx = document.getElementById('rfmChart');
    if (ctx) {
        try {
            const chart = new Chart(ctx, {
                type: 'scatter',
                data: {
                    datasets: [{
                        label: 'VIP 고객',
                        data: [{x: 90, y: 95}, {x: 85, y: 90}, {x: 88, y: 92}],
                        backgroundColor: 'rgba(239, 68, 68, 0.8)',
                        borderColor: 'rgba(239, 68, 68, 1)'
                    }, {
                        label: '프리미엄 고객',
                        data: [{x: 70, y: 75}, {x: 65, y: 70}, {x: 72, y: 78}],
                        backgroundColor: 'rgba(245, 158, 11, 0.8)',
                        borderColor: 'rgba(245, 158, 11, 1)'
                    }, {
                        label: '일반 고객',
                        data: [{x: 30, y: 40}, {x: 25, y: 35}, {x: 35, y: 45}],
                        backgroundColor: 'rgba(107, 114, 128, 0.6)',
                        borderColor: 'rgba(107, 114, 128, 1)'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        title: {
                            display: true,
                            text: 'RFM 분석: Recency vs Frequency',
                            font: { size: 14, weight: 'bold' }
                        },
                        legend: {
                            display: true,
                            position: 'top'
                        }
                    },
                    scales: {
                        x: {
                            title: { display: true, text: 'Recency (최근 구매일)', font: { size: 12 } },
                            beginAtZero: true,
                            max: 100,
                            grid: { color: 'rgba(0,0,0,0.1)' }
                        },
                        y: {
                            title: { display: true, text: 'Frequency (구매 빈도)', font: { size: 12 } },
                            beginAtZero: true,
                            max: 100,
                            grid: { color: 'rgba(0,0,0,0.1)' }
                        }
                    }
                }
            });
            
            // 차트 인스턴스를 전역 변수에 저장하고 canvas에도 연결
            chartInstances['rfmChart'] = chart;
            ctx.chart = chart; // canvas 요소에 직접 연결
            console.log('RFM 분석 차트 생성 완료');
        } catch (error) {
            console.error('RFM 차트 생성 오류:', error);
        }
    }
}

// 모델 성능 비교 차트
function renderModelPerformanceChart() {
    const ctx = document.getElementById('modelPerformanceChart');
    if (ctx) {
        try {
            const chart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['Random Forest', 'XGBoost', 'LightGBM', '로지스틱 회귀'],
                    datasets: [{
                        label: '정확도 (%)',
                        data: [89, 92, 91, 78],
                        backgroundColor: [
                            'rgba(239, 68, 68, 0.8)',
                            'rgba(245, 158, 11, 0.8)',
                            'rgba(245, 158, 11, 0.6)',
                            'rgba(107, 114, 128, 0.6)'
                        ],
                        borderColor: 'rgba(239, 68, 68, 1)',
                        borderWidth: 2,
                        borderRadius: 6,
                        borderSkipped: false
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        title: {
                            display: true,
                            text: '모델별 성능 비교',
                            font: { size: 14, weight: 'bold' }
                        },
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100,
                            title: {
                                display: true,
                                text: '정확도 (%)',
                                font: { size: 12 }
                            },
                            grid: { color: 'rgba(0,0,0,0.1)' }
                        },
                        x: {
                            grid: { display: false }
                        }
                    }
                }
            });
            
            // 차트 인스턴스를 전역 변수에 저장하고 canvas에도 연결
            chartInstances['modelPerformanceChart'] = chart;
            ctx.chart = chart; // canvas 요소에 직접 연결
            console.log('모델 성능 비교 차트 생성 완료');
        } catch (error) {
            console.error('모델 성능 차트 생성 오류:', error);
        }
    }
}

// 고객 특성 분석 차트
function renderCustomerCharacteristicsChart() {
    const ctx = document.getElementById('customerCharacteristicsChart');
    if (ctx) {
        try {
            const chart = new Chart(ctx, {
                type: 'radar',
                data: {
                    labels: ['연간 구매액', '구매 빈도', '카드 한도', '연체 이력', '연령대', '소득 수준'],
                    datasets: [{
                        label: 'VIP 고객',
                        data: [95, 90, 85, 95, 80, 90],
                        backgroundColor: 'rgba(239, 68, 68, 0.2)',
                        borderColor: 'rgba(239, 68, 68, 1)',
                        borderWidth: 2,
                        pointBackgroundColor: 'rgba(239, 68, 68, 1)',
                        pointBorderColor: '#fff',
                        pointBorderWidth: 2,
                        pointRadius: 4,
                        pointHoverRadius: 6
                    }, {
                        label: '일반 고객',
                        data: [45, 50, 60, 70, 75, 65],
                        backgroundColor: 'rgba(107, 114, 128, 0.2)',
                        borderColor: 'rgba(107, 114, 128, 1)',
                        borderWidth: 2,
                        pointBackgroundColor: 'rgba(107, 114, 128, 1)',
                        pointBorderColor: '#fff',
                        pointBorderWidth: 2,
                        pointRadius: 4,
                        pointHoverRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        title: {
                            display: true,
                            text: '고객 등급별 특성 비교',
                            font: { size: 14, weight: 'bold' }
                        },
                        legend: {
                            display: true,
                            position: 'top'
                        }
                    },
                    scales: {
                        r: {
                            beginAtZero: true,
                            max: 100,
                            grid: { color: 'rgba(0,0,0,0.1)' },
                            pointLabels: { font: { size: 11 } }
                        }
                    }
                }
            });
            
            // 차트 인스턴스를 전역 변수에 저장하고 canvas에도 연결
            chartInstances['customerCharacteristicsChart'] = chart;
            ctx.chart = chart; // canvas 요소에 직접 연결
            console.log('고객 특성 분석 차트 생성 완료');
        } catch (error) {
            console.error('고객 특성 차트 생성 오류:', error);
        }
    }
}

// 지역 소멸 위험도 분석 차트
function renderRegionalRiskChart() {
    const ctx = document.getElementById('regionalRiskChart');
    if (ctx) {
        try {
            // PDF 파일의 실제 데이터를 참고한 지역별 소멸 위험도
            const chart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['수도권 집중', '의료 인프라 부족', '청년 인구 이탈', '지역 고령화', '교통 접근성'],
                    datasets: [{
                        data: [30, 25, 20, 15, 10],
                        backgroundColor: [
                            'rgba(239, 68, 68, 0.8)',    // 수도권 집중: 빨간색
                            'rgba(245, 158, 11, 0.8)',   // 의료 인프라: 주황색
                            'rgba(37, 99, 235, 0.8)',    // 청년 인구: 파란색
                            'rgba(5, 150, 105, 0.8)',    // 고령화: 초록색
                            'rgba(156, 39, 176, 0.8)'    // 교통: 보라색
                        ],
                        borderColor: [
                            'rgba(239, 68, 68, 1)',
                            'rgba(245, 158, 11, 1)',
                            'rgba(37, 99, 235, 1)',
                            'rgba(5, 150, 105, 1)',
                            'rgba(156, 39, 176, 1)'
                        ],
                        borderWidth: 3,
                        borderColor: '#fff'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        title: {
                            display: true,
                            text: '지역 소멸의 5가지 핵심 원인 분석',
                            font: { size: 14, weight: 'bold' }
                        },
                        legend: {
                            display: true,
                            position: 'bottom',
                            labels: {
                                padding: 20,
                                usePointStyle: true,
                                pointStyle: 'circle'
                            }
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    const label = context.label;
                                    const value = context.parsed;
                                    const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                    const percentage = ((value / total) * 100).toFixed(1);
                                    return `${label}: ${value}% (${percentage}%)`;
                                }
                            }
                        }
                    },
                    cutout: '40%'
                }
            });
            
            // 차트 인스턴스를 전역 변수에 저장하고 canvas에도 연결
            chartInstances['regionalRiskChart'] = chart;
            ctx.chart = chart; // canvas 요소에 직접 연결
            console.log('지역 소멸 위험도 차트 생성 완료');
        } catch (error) {
            console.error('지역 소멸 위험도 차트 생성 오류:', error);
        }
    }
}
