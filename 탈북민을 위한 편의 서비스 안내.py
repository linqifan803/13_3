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
    margin-top: 1rem;
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

.phone-card {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 1.4rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
    margin-bottom: 1rem;
}

.phone-number {
    font-size: 1.25rem;
    font-weight: 800;
    color: #2563EB;
    margin-top: 0.3rem;
}

.phone-label {
    font-size: 1.05rem;
    font-weight: 700;
    color: #0F172A;
}

.phone-subtext {
    font-size: 0.88rem;
    color: #64748B;
    margin-top: 0.2rem;
}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# 1. 메인 타이틀
st.markdown('<div class="main-title">탈북민을 위한 편의 서비스 안내</div>', unsafe_allow_html=True)

# 2. 상단 안내 박스
banner_html = """
<div class="info-banner">
    👋 <strong>안녕하세요!</strong> 이 사이트는 2026년 10월에 만들어진 탈북민을 위한 사이트이며 
    남한과 북한언어 차이, 문화 차이 등 여러 요인 때문에 남한 생활에 어려움을 겪는 
    탈북민들을 돕기 위한 사이트입니다.
</div>
"""
st.markdown(banner_html, unsafe_allow_html=True)

# 3. 주요 기능 설명 섹션
st.markdown('<div class="section-title">주요 기능 설명</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    card1_html = """
    <div class="card-container">
        <div class="card-badge">기능 01</div>
        <div class="card-title">1. 언어변환 페이지</div>
        <div class="card-desc">남한에서 자주 쓰이는 외래어, 신조어 및 낯선 일상 용어를 이해하기 쉬운 단어와 표현으로 변환하고 해석해 드립니다.</div>
    </div>
    """
    st.markdown(card1_html, unsafe_allow_html=True)

with col2:
    card2_html = """
    <div class="card-container">
        <div class="card-badge">기능 02</div>
        <div class="card-title">2. AI 남한어 연습 페이지</div>
        <div class="card-desc">카페 주문, 관공서 방문, 취업 면접 등 남한 사회에서 겪게 되는 다양한 실제 상황을 AI와 맞춤형으로 대화하며 연습합니다.</div>
    </div>
    """
    st.markdown(card2_html, unsafe_allow_html=True)

with col3:
    card3_html = """
    <div class="card-container">
        <div class="card-badge">기능 03</div>
        <div class="card-title">3. 주요 문화 차이 페이지</div>
        <div class="card-desc">행정·금융, 분리수거·대중교통, 직장 비즈니스 매너 등 정착 초기에 꼭 알아두어야 할 필수 문화 정보를 보기 쉽게 정리했습니다.</div>
    </div>
    """
    st.markdown(card3_html, unsafe_allow_html=True)

st.write("")
st.write("")

# 4. 공공기관 주요 상담 및 긴급 전화번호 안내 섹션
st.markdown('<div class="section-title">📞 주요 공공기관 및 상담 콜센터 안내</div>', unsafe_allow_html=True)

p_col1, p_col2 = st.columns(2)

with p_col1:
    phone1_html = """
    <div class="phone-card">
        <div class="phone-label">🏛️ 남북하나재단 종합상담 콜센터</div>
        <div class="phone-subtext">초기 정착, 생활 안정, 일자리 및 정착금 통합 상담</div>
        <div class="phone-number">☎ 1577-6635 / 1855-0714</div>
    </div>
    """
    st.markdown(phone1_html, unsafe_allow_html=True)

    phone2_html = """
    <div class="phone-card">
        <div class="phone-label">🏥 보건복지상담센터</div>
        <div class="phone-subtext">긴급 생계 지원, 기초생활보장 및 의료·복지 상담</div>
        <div class="phone-number">☎ 129</div>
    </div>
    """
    st.markdown(phone2_html, unsafe_allow_html=True)

with p_col2:
    phone3_html = """
    <div class="phone-card">
        <div class="phone-label">⚖️ 대한법률구조공단</div>
        <div class="phone-subtext">남한 생활 중 발생하는 임대차계약, 법률 분쟁 무료 상담</div>
        <div class="phone-number">☎ 132</div>
    </div>
    """
    st.markdown(phone3_html, unsafe_allow_html=True)

    phone4_html = """
    <div class="phone-card">
        <div class="phone-label">👮 경찰청 민원상담 / 신변보호</div>
        <div class="phone-subtext">신변보호관 연결 및 경찰 민원 문의 (긴급 신고: 112)</div>
        <div class="phone-number">☎ 182</div>
    </div>
    """
    st.markdown(phone4_html, unsafe_allow_html=True)
