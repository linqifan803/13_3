import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="탈북민을 위한 편의 서비스 안내",
    page_icon="🇰🇷",
    layout="wide"
)

# 세련된 CSS 스타일 설정
custom_css = """
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

html, body, [class*="css"] {
    font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
}

.main-title {
    font-size: 2.2rem;
    font-weight: 800;
    color: #0F172A;
    letter-spacing: -0.03em;
    margin-bottom: 1.5rem;
    text-align: center;
}

.info-banner {
    background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%);
    border: 1px solid #BAE6FD;
    border-left: 6px solid #0284C7;
    padding: 1.5rem 2rem;
    border-radius: 14px;
    color: #0369A1;
    font-size: 1.05rem;
    line-height: 1.7;
    font-weight: 500;
    box-shadow: 0 4px 12px rgba(2, 132, 199, 0.06);
    margin-bottom: 2.5rem;
}

.section-title {
    font-size: 1.4rem;
    font-weight: 700;
    color: #1E293B;
    margin-bottom: 1.2rem;
    letter-spacing: -0.02em;
    text-align: center;
}

.card-container {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 2rem 1.6rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
    height: 100%;
}

.card-badge {
    display: inline-block;
    background-color: #EFF6FF;
    color: #2563EB;
    font-size: 0.8rem;
    font-weight: 700;
    padding: 0.35rem 0.75rem;
    border-radius: 20px;
    margin-bottom: 1rem;
}

.card-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #0F172A;
    margin-bottom: 0.7rem;
}

.card-desc {
    font-size: 0.95rem;
    color: #64748B;
    line-height: 1.6;
}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# 1. 메인 타이틀
st.markdown('<div class="main-title">탈북민을 위한 편의 서비스 안내</div>', unsafe_allow_html=True)

# 2. 상단 안내 박스
st.markdown(
    '<div class="info-banner">'
    '👋 <strong>안녕하세요!</strong> 이 사이트는 2026년 10월에 만들어진 탈북민을 위한 사이트이며 '
    '남한과 북한언어 차이, 문화 차이 등 여러 요인 때문에 남한 생활에 어려움을 겪는 '
    '탈북민들을 돕기 위한 사이트입니다.'
    '</div>', 
    unsafe_allow_html=True
)

# 3. 소제목
st.markdown('<div class="section-title">주요 기능 설명</div>', unsafe_allow_html=True)

# 4. 주요 기능 카드 (설명 제공)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        '<div class="card-container">'
        '<div class="card-badge">기능 01</div>'
        '<div class="card-title">1. 언어변환 페이지</div>'
        '<div class="card-desc">남한에서 자주 쓰이는 외래어, 신조어 및 낯선 일상 용어를 이해하기 쉬운 단어와 표현으로 변환하고 해석해 드립니다.</div>'
        '</div>',
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        '<div class="card-container">'
        '<div class="card-badge">기능
