import React, { useState } from 'react';

const BACKEND_URL = 'http://localhost:8000';

const UnifiedWorkflow = () => {
  const [activeStep, setActiveStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);

  // 상품 정보
  const [productInfo, setProductInfo] = useState({
    product_name: '',
    category: '',
    keywords: '',
    target_customer: '',
    platforms: ['coupang', 'naver']
  });

  // SWOT 결과
  const [swotResult, setSwotResult] = useState(null);
  const [swotOptions, setSwotOptions] = useState({
    search_depth: 'advanced',
    days: 90,
    include_reviews: true,
    search_platforms: ['coupang', 'naver'],
    sort_by: 'popular'
  });

  // 상세페이지 결과
  const [detailResult, setDetailResult] = useState(null);

  // 편집 중인 마크다운
  const [editMode, setEditMode] = useState(false);
  const [editedMarkdown, setEditedMarkdown] = useState('');

  // 워크플로우 시작
  const handleStart = async () => {
    if (!productInfo.product_name || !productInfo.category) {
      alert('상품명과 카테고리를 입력하세요');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`${BACKEND_URL}/api/unified/start`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          product_name: productInfo.product_name,
          category: productInfo.category,
          keywords: productInfo.keywords.split(',').map(k => k.trim()).filter(k => k),
          target_customer: productInfo.target_customer,
          platforms: productInfo.platforms
        })
      });

      if (!response.ok) throw new Error('서버 오류');

      const data = await response.json();
      setSessionId(data.session_id);
      localStorage.setItem('current_session_id', data.session_id);
      setActiveStep(1);
    } catch (error) {
      alert('오류: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  // SWOT 분석 실행
  const handleExecuteSwot = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${BACKEND_URL}/api/unified/execute-swot`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionId,
          ...swotOptions
        })
      });

      if (!response.ok) throw new Error('SWOT 분석 실패');

      const data = await response.json();
      setSwotResult(data);

      // 마크다운 편집 준비 (HTML URL로부터 마크다운 가져오기)
      if (data.html_url) {
        fetchMarkdown(data.html_url.replace('.html', '.md'));
      }
    } catch (error) {
      alert('SWOT 분석 오류: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  // 마크다운 가져오기
  const fetchMarkdown = async (mdUrl) => {
    try {
      const response = await fetch(`${BACKEND_URL}${mdUrl}`);
      const text = await response.text();
      setEditedMarkdown(text);
    } catch (error) {
      console.error('마크다운 로드 실패:', error);
    }
  };

  // 마크다운 저장
  const handleSaveMarkdown = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${BACKEND_URL}/api/unified/update-markdown`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionId,
          markdown_content: editedMarkdown,
          step: activeStep === 1 ? 'swot' : 'detail'
        })
      });

      if (!response.ok) throw new Error('저장 실패');

      const data = await response.json();

      // 결과 업데이트
      if (activeStep === 1) {
        setSwotResult({ ...swotResult, html_url: data.html_url });
      } else if (activeStep === 2) {
        setDetailResult({ ...detailResult, html_url: data.html_url });
      }

      alert('✅ 수정 내용이 저장되었습니다');
      setEditMode(false);
    } catch (error) {
      alert('저장 오류: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  // 상세페이지 생성
  const handleExecuteDetail = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${BACKEND_URL}/api/unified/execute-detail`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionId,
          platform: 'coupang',
          tone: '친근한',
          image_style: 'real'
        })
      });

      if (!response.ok) throw new Error('상세페이지 생성 실패');

      const data = await response.json();
      setDetailResult(data);

      // 마크다운 편집 준비
      if (data.markdown_url) {
        fetchMarkdown(data.markdown_url);
      }
    } catch (error) {
      alert('상세페이지 생성 오류: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  // 챗봇으로 이동
  const goToChatbot = () => {
    window.location.href = '/chatbot';
  };

  const handleReset = () => {
    setActiveStep(0);
    setSessionId(null);
    setSwotResult(null);
    setDetailResult(null);
    setEditMode(false);
    setEditedMarkdown('');
    setProductInfo({
      product_name: '',
      category: '',
      keywords: '',
      target_customer: '',
      platforms: ['coupang', 'naver']
    });
  };

  return (
    <div style={{ background: '#fafdfb', minHeight: '100vh' }}>
      {/* 헤더 */}
      <header style={{
        width: '100%',
        background: 'linear-gradient(180deg, rgba(15,118,110,0.03), transparent)',
        borderBottom: '1px solid #e6eef0',
        position: 'sticky',
        top: 0,
        zIndex: 20,
        backgroundColor: '#fafdfb'
      }}>
        <div style={{
          maxWidth: '1100px',
          margin: '0 auto',
          padding: '12px 20px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between'
        }}>
          <div style={{
            fontSize: '20px',
            fontWeight: 800,
            color: '#0f766e',
            letterSpacing: '0.2px'
          }}>
            마케팅 AI 어시스턴트
          </div>
          <nav style={{ display: 'flex', gap: '20px', alignItems: 'center' }}>
            <a href="/" style={{
              textDecoration: 'none',
              color: '#0f1720',
              fontSize: '15px',
              padding: '8px 10px',
              borderRadius: '8px'
            }}>홈</a>
            <a href="/workflow" style={{
              textDecoration: 'none',
              color: '#0f766e',
              fontSize: '15px',
              padding: '8px 10px',
              borderRadius: '8px',
              background: 'rgba(15,118,110,0.06)'
            }}>워크플로우</a>
            <a href="/chatbot" style={{
              textDecoration: 'none',
              color: '#0f1720',
              fontSize: '15px',
              padding: '8px 10px',
              borderRadius: '8px'
            }}>챗봇</a>
          </nav>
        </div>
      </header>

      {/* 메인 컨텐츠 */}
      <main style={{ maxWidth: '1100px', margin: '40px auto', padding: '0 20px' }}>
        {/* 제목 카드 */}
        <div style={{
          background: '#ffffff',
          border: '1px solid #e6eef0',
          borderRadius: '12px',
          padding: '32px',
          marginBottom: '24px',
          boxShadow: '0 6px 18px rgba(15,118,110,0.03)'
        }}>
          <h1 style={{ margin: '0 0 8px', fontSize: '28px', fontWeight: 700, color: '#0f1720' }}>
            🚀 통합 워크플로우
          </h1>
          <p style={{ margin: 0, fontSize: '16px', color: '#6b7280' }}>
            상품 정보 입력 → SWOT 분석 → 상세페이지 생성 → 챗봇 상담까지 한 번에
          </p>
          {sessionId && (
            <div style={{
              marginTop: '16px',
              padding: '12px',
              background: 'rgba(5,150,105,0.08)',
              borderLeft: '3px solid #059669',
              borderRadius: '8px',
              fontSize: '14px',
              color: '#059669'
            }}>
              <strong>세션 ID:</strong> {sessionId}
            </div>
          )}
        </div>

        {/* 로딩 바 */}
        {loading && (
          <div style={{
            height: '4px',
            background: '#e6eef0',
            borderRadius: '2px',
            overflow: 'hidden',
            marginBottom: '24px'
          }}>
            <div style={{
              height: '100%',
              background: '#0f766e',
              width: '50%',
              animation: 'loading 1.5s infinite'
            }}></div>
          </div>
        )}

        {/* Step 0: 상품 정보 입력 */}
        {activeStep === 0 && (
          <div style={{
            background: '#ffffff',
            border: '1px solid #e6eef0',
            borderRadius: '12px',
            padding: '32px',
            marginBottom: '24px',
            boxShadow: '0 6px 18px rgba(15,118,110,0.03)'
          }}>
            <h2 style={{ margin: '0 0 8px', fontSize: '22px', fontWeight: 700, color: '#0f1720' }}>
              Step 1: 상품 정보 입력
            </h2>
            <p style={{ margin: '0 0 24px', fontSize: '14px', color: '#6b7280' }}>
              한 번만 입력하면 모든 단계에서 자동으로 사용됩니다
            </p>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '16px' }}>
              <div>
                <label style={{ display: 'block', fontSize: '13px', color: '#6b7280', marginBottom: '8px' }}>
                  상품명 *
                </label>
                <input
                  type="text"
                  value={productInfo.product_name}
                  onChange={(e) => setProductInfo({ ...productInfo, product_name: e.target.value })}
                  style={{
                    width: '100%',
                    padding: '12px',
                    borderRadius: '10px',
                    border: '1px solid #e6eef0',
                    background: '#fff',
                    fontSize: '15px'
                  }}
                  placeholder="예: 프리미엄 가죽 백팩"
                />
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '13px', color: '#6b7280', marginBottom: '8px' }}>
                  카테고리 *
                </label>
                <input
                  type="text"
                  value={productInfo.category}
                  onChange={(e) => setProductInfo({ ...productInfo, category: e.target.value })}
                  style={{
                    width: '100%',
                    padding: '12px',
                    borderRadius: '10px',
                    border: '1px solid #e6eef0',
                    background: '#fff',
                    fontSize: '15px'
                  }}
                  placeholder="예: 패션/가방"
                />
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '13px', color: '#6b7280', marginBottom: '8px' }}>
                  키워드 (쉼표로 구분)
                </label>
                <input
                  type="text"
                  value={productInfo.keywords}
                  onChange={(e) => setProductInfo({ ...productInfo, keywords: e.target.value })}
                  style={{
                    width: '100%',
                    padding: '12px',
                    borderRadius: '10px',
                    border: '1px solid #e6eef0',
                    background: '#fff',
                    fontSize: '15px'
                  }}
                  placeholder="예: 가죽, 직장인, 노트북"
                />
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '13px', color: '#6b7280', marginBottom: '8px' }}>
                  타겟 고객
                </label>
                <input
                  type="text"
                  value={productInfo.target_customer}
                  onChange={(e) => setProductInfo({ ...productInfo, target_customer: e.target.value })}
                  style={{
                    width: '100%',
                    padding: '12px',
                    borderRadius: '10px',
                    border: '1px solid #e6eef0',
                    background: '#fff',
                    fontSize: '15px'
                  }}
                  placeholder="예: 20-30대 직장인"
                />
              </div>
            </div>

            <button
              onClick={handleStart}
              disabled={loading}
              style={{
                marginTop: '24px',
                padding: '14px 28px',
                background: '#0f766e',
                color: '#fff',
                border: 'none',
                borderRadius: '10px',
                fontSize: '16px',
                fontWeight: 700,
                cursor: 'pointer',
                transition: 'background 0.15s'
              }}
              onMouseOver={(e) => e.target.style.background = '#115e59'}
              onMouseOut={(e) => e.target.style.background = '#0f766e'}
            >
              시작하기 →
            </button>
          </div>
        )}

        {/* Step 1: SWOT 분석 */}
        {activeStep === 1 && (
          <div style={{
            background: '#ffffff',
            border: '1px solid #e6eef0',
            borderRadius: '12px',
            padding: '32px',
            marginBottom: '24px',
            boxShadow: '0 6px 18px rgba(15,118,110,0.03)'
          }}>
            <h2 style={{ margin: '0 0 8px', fontSize: '22px', fontWeight: 700, color: '#0f1720' }}>
              Step 2: SWOT + 3C 분석
            </h2>
            <p style={{ margin: '0 0 16px', fontSize: '14px', color: '#6b7280' }}>
              <strong style={{ color: '#0f766e' }}>{productInfo.product_name}</strong> ({productInfo.category})의 시장 경쟁력을 분석합니다
            </p>

            {!swotResult && (
              <button
                onClick={handleExecuteSwot}
                disabled={loading}
                style={{
                  padding: '14px 28px',
                  background: '#0f766e',
                  color: '#fff',
                  border: 'none',
                  borderRadius: '10px',
                  fontSize: '16px',
                  fontWeight: 700,
                  cursor: 'pointer'
                }}
                onMouseOver={(e) => e.target.style.background = '#115e59'}
                onMouseOut={(e) => e.target.style.background = '#0f766e'}
              >
                {loading ? '분석 중...' : 'SWOT 분석 실행'}
              </button>
            )}

            {swotResult && !editMode && (
              <div>
                <div style={{
                  padding: '16px',
                  background: 'rgba(5,150,105,0.08)',
                  borderLeft: '3px solid #059669',
                  borderRadius: '8px',
                  marginBottom: '16px'
                }}>
                  ✅ SWOT 분석 완료! {swotResult.competitor_count}개 경쟁사 상품 분석됨
                </div>

                <div style={{ display: 'flex', gap: '12px', marginBottom: '16px' }}>
                  <button
                    onClick={() => window.open(`${BACKEND_URL}${swotResult.html_url}`, '_blank')}
                    style={{
                      flex: 1,
                      padding: '12px 20px',
                      background: '#ffffff',
                      color: '#0f766e',
                      border: '1px solid #0f766e',
                      borderRadius: '10px',
                      fontSize: '15px',
                      fontWeight: 600,
                      cursor: 'pointer'
                    }}
                  >
                    📊 분석 결과 보기
                  </button>
                  <button
                    onClick={() => {
                      setEditMode(true);
                      if (swotResult.html_url) {
                        fetchMarkdown(swotResult.html_url.replace('.html', '.md'));
                      }
                    }}
                    style={{
                      flex: 1,
                      padding: '12px 20px',
                      background: '#ffffff',
                      color: '#0f766e',
                      border: '1px solid #0f766e',
                      borderRadius: '10px',
                      fontSize: '15px',
                      fontWeight: 600,
                      cursor: 'pointer'
                    }}
                  >
                    ✏️ 내용 수정하기
                  </button>
                </div>

                <button
                  onClick={() => setActiveStep(2)}
                  style={{
                    width: '100%',
                    padding: '14px 28px',
                    background: '#0f766e',
                    color: '#fff',
                    border: 'none',
                    borderRadius: '10px',
                    fontSize: '16px',
                    fontWeight: 700,
                    cursor: 'pointer'
                  }}
                  onMouseOver={(e) => e.target.style.background = '#115e59'}
                  onMouseOut={(e) => e.target.style.background = '#0f766e'}
                >
                  다음 단계: 상세페이지 생성 →
                </button>
              </div>
            )}

            {editMode && (
              <div>
                <div style={{ marginBottom: '16px' }}>
                  <label style={{ display: 'block', fontSize: '13px', color: '#6b7280', marginBottom: '8px' }}>
                    마크다운 편집 (수정 후 저장하면 HTML이 자동으로 업데이트됩니다)
                  </label>
                  <textarea
                    value={editedMarkdown}
                    onChange={(e) => setEditedMarkdown(e.target.value)}
                    rows={20}
                    style={{
                      width: '100%',
                      padding: '12px',
                      borderRadius: '10px',
                      border: '1px solid #e6eef0',
                      background: '#fff',
                      fontSize: '14px',
                      fontFamily: 'monospace',
                      resize: 'vertical'
                    }}
                  />
                </div>

                <div style={{ display: 'flex', gap: '12px' }}>
                  <button
                    onClick={handleSaveMarkdown}
                    disabled={loading}
                    style={{
                      flex: 1,
                      padding: '12px 20px',
                      background: '#0f766e',
                      color: '#fff',
                      border: 'none',
                      borderRadius: '10px',
                      fontSize: '15px',
                      fontWeight: 600,
                      cursor: 'pointer'
                    }}
                  >
                    {loading ? '저장 중...' : '💾 저장'}
                  </button>
                  <button
                    onClick={() => setEditMode(false)}
                    style={{
                      flex: 1,
                      padding: '12px 20px',
                      background: '#ffffff',
                      color: '#6b7280',
                      border: '1px solid #e6eef0',
                      borderRadius: '10px',
                      fontSize: '15px',
                      fontWeight: 600,
                      cursor: 'pointer'
                    }}
                  >
                    취소
                  </button>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Step 2: 상세페이지 생성 */}
        {activeStep === 2 && (
          <div style={{
            background: '#ffffff',
            border: '1px solid #e6eef0',
            borderRadius: '12px',
            padding: '32px',
            marginBottom: '24px',
            boxShadow: '0 6px 18px rgba(15,118,110,0.03)'
          }}>
            <h2 style={{ margin: '0 0 8px', fontSize: '22px', fontWeight: 700, color: '#0f1720' }}>
              Step 3: 상세페이지 생성
            </h2>
            <p style={{ margin: '0 0 16px', fontSize: '14px', color: '#6b7280' }}>
              ESM+ 가이드라인 준수 HTML 템플릿 (G마켓/쿠팡/스마트스토어 호환)
            </p>

            {!detailResult && (
              <button
                onClick={handleExecuteDetail}
                disabled={loading}
                style={{
                  padding: '14px 28px',
                  background: '#0f766e',
                  color: '#fff',
                  border: 'none',
                  borderRadius: '10px',
                  fontSize: '16px',
                  fontWeight: 700,
                  cursor: 'pointer'
                }}
                onMouseOver={(e) => e.target.style.background = '#115e59'}
                onMouseOut={(e) => e.target.style.background = '#0f766e'}
              >
                {loading ? '생성 중...' : '상세페이지 생성'}
              </button>
            )}

            {detailResult && !editMode && (
              <div>
                <div style={{
                  padding: '16px',
                  background: 'rgba(5,150,105,0.08)',
                  borderLeft: '3px solid #059669',
                  borderRadius: '8px',
                  marginBottom: '16px'
                }}>
                  ✅ 상세페이지 생성 완료!
                </div>

                <div style={{ display: 'flex', gap: '12px', marginBottom: '16px' }}>
                  <button
                    onClick={() => window.open(`${BACKEND_URL}${detailResult.html_url}`, '_blank')}
                    style={{
                      flex: 1,
                      padding: '12px 20px',
                      background: '#ffffff',
                      color: '#0f766e',
                      border: '1px solid #0f766e',
                      borderRadius: '10px',
                      fontSize: '15px',
                      fontWeight: 600,
                      cursor: 'pointer'
                    }}
                  >
                    📄 상세페이지 보기
                  </button>
                  <button
                    onClick={() => {
                      setEditMode(true);
                      if (detailResult.markdown_url) {
                        fetchMarkdown(detailResult.markdown_url);
                      }
                    }}
                    style={{
                      flex: 1,
                      padding: '12px 20px',
                      background: '#ffffff',
                      color: '#0f766e',
                      border: '1px solid #0f766e',
                      borderRadius: '10px',
                      fontSize: '15px',
                      fontWeight: 600,
                      cursor: 'pointer'
                    }}
                  >
                    ✏️ 내용 수정하기
                  </button>
                </div>

                <div style={{ display: 'flex', gap: '12px' }}>
                  <button
                    onClick={goToChatbot}
                    style={{
                      flex: 1,
                      padding: '14px 28px',
                      background: '#0f766e',
                      color: '#fff',
                      border: 'none',
                      borderRadius: '10px',
                      fontSize: '16px',
                      fontWeight: 700,
                      cursor: 'pointer'
                    }}
                    onMouseOver={(e) => e.target.style.background = '#115e59'}
                    onMouseOut={(e) => e.target.style.background = '#0f766e'}
                  >
                    💬 챗봇으로 이동 →
                  </button>
                  <button
                    onClick={handleReset}
                    style={{
                      padding: '14px 28px',
                      background: '#ffffff',
                      color: '#6b7280',
                      border: '1px solid #e6eef0',
                      borderRadius: '10px',
                      fontSize: '16px',
                      fontWeight: 600,
                      cursor: 'pointer'
                    }}
                  >
                    🔄 새로 시작
                  </button>
                </div>
              </div>
            )}

            {editMode && (
              <div>
                <div style={{ marginBottom: '16px' }}>
                  <label style={{ display: 'block', fontSize: '13px', color: '#6b7280', marginBottom: '8px' }}>
                    마크다운 편집
                  </label>
                  <textarea
                    value={editedMarkdown}
                    onChange={(e) => setEditedMarkdown(e.target.value)}
                    rows={20}
                    style={{
                      width: '100%',
                      padding: '12px',
                      borderRadius: '10px',
                      border: '1px solid #e6eef0',
                      background: '#fff',
                      fontSize: '14px',
                      fontFamily: 'monospace',
                      resize: 'vertical'
                    }}
                  />
                </div>

                <div style={{ display: 'flex', gap: '12px' }}>
                  <button
                    onClick={handleSaveMarkdown}
                    disabled={loading}
                    style={{
                      flex: 1,
                      padding: '12px 20px',
                      background: '#0f766e',
                      color: '#fff',
                      border: 'none',
                      borderRadius: '10px',
                      fontSize: '15px',
                      fontWeight: 600,
                      cursor: 'pointer'
                    }}
                  >
                    {loading ? '저장 중...' : '💾 저장'}
                  </button>
                  <button
                    onClick={() => setEditMode(false)}
                    style={{
                      flex: 1,
                      padding: '12px 20px',
                      background: '#ffffff',
                      color: '#6b7280',
                      border: '1px solid #e6eef0',
                      borderRadius: '10px',
                      fontSize: '15px',
                      fontWeight: 600,
                      cursor: 'pointer'
                    }}
                  >
                    취소
                  </button>
                </div>
              </div>
            )}
          </div>
        )}
      </main>

      {/* CSS 애니메이션 */}
      <style>{`
        @keyframes loading {
          0% { transform: translateX(-100%); }
          100% { transform: translateX(300%); }
        }

        button:disabled {
          opacity: 0.5;
          cursor: not-allowed !important;
        }

        a:hover {
          background: rgba(15,118,110,0.06) !important;
          color: #0f766e !important;
        }
      `}</style>
    </div>
  );
};

export default UnifiedWorkflow;
