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
    margin-bottom: 1.2rem;
    text-align: center;
}

.info-banner {
    background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%);
    border: 1px solid #BAE6FD;
    border-left: 6px solid #0284C7;
    padding: 1.4rem 1.8rem;
    border-radius: 14px;
    color: #0369A1;
    font-size: 1.05rem;
    line-height: 1.65;
    font-weight: 500;
    box-shadow: 0 4px 12px rgba(2, 132, 199, 0.06);
    margin-bottom: 2rem;
}

.section-title {
    font-size: 1.35rem;
    font-weight: 700;
    color: #1E293B;
    margin-top: 1.5rem;
    margin-bottom: 0.8rem;
    letter-spacing: -0.02em;
}

.card-container {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 1.8rem 1.5rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
    height: 100%;
}

.card-badge {
    display: inline-block;
    background-color: #EFF6FF;
    color: #2563EB;
    font-size: 0.8rem;
    font-weight: 700;
    padding: 0.3rem 0.7rem;
    border-radius: 20px;
    margin-bottom: 0.8rem;
}

.card-title {
    font-size: 1.2rem;
    font-weight: 700;
    color: #0F172A;
    margin-bottom: 0.6rem;
}

.card-desc {
    font-size: 0.95rem;
    color: #64748B;
    line-height: 1.55;
}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# 1. 메인 타이틀
st.markdown('<div class="main-title">탈북민을 위한 편의 서비스 안내</div>', unsafe_allow_html=True)

# 2. 안내 박스
st.markdown(
    '<div class="info-banner">'
    '👋 <strong>안녕하세요!</strong> 이 사이트는 2026년 10월에 만들어진 탈북민을 위한 공간입니다.<br>'
    '남한과 북한의 언어 차이, 문화 차이 등 여러 요인으로 남한 생활에 어려움을 겪는 탈북민분들의 안정적인 정착을 돕고자 제작되었습니다.'
    '</div>', 
    unsafe_allow_html=True
)

# 3. 주요 기능 카드 (바로가기 버튼 및 상단 탭 제거)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        '<div class="card-container">'
        '<div class="card-badge">기능 01</div>'
        '<div class="card-title">1. 언어변환</div>'
        '<div class="card-desc">남한에서 자주 쓰이는 외래어, 신조어 및 낯선 일상 용어를 이해하기 쉬운 단어와 표현으로 변환하고 해석해 드립니다.</div>'
        '</div>',
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        '<div class="card-container">'
        '<div class="card-badge">기능 02</div>'
        '<div class="card-title">2. AI 남한어 연습</div>'
        '<div class="card-desc">카페 주문, 관공서 방문, 취업 면접 등 남한 사회에서 겪게 되는 다양한 실제 상황을 AI와 맞춤형으로 대화하며 연습합니다.</div>'
        '</div>',
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        '<div class="card-container">'
        '<div class="card-badge">기능 03</div>'
        '<div class="card-title">3. 주요 문화 차이</div>'
        '<div class="card-desc">행정·금융, 분리수거·대중교통, 직장 비즈니스 매너 등 정착 초기에 꼭 알아두어야 할 필수 문화 정보를 보기 쉽게 정리했습니다.</div>'
        '</div>',
        unsafe_allow_html=True
    )

st.write("")
st.write("")

# 4. 각 기능별 실행 화면
st.markdown('<div class="section-title">🔤 1. 언어변환 서비스</div>', unsafe_allow_html=True)
search_term = st.text_input("단어 입력", placeholder="예: 키오스크, 아메리카노, 주민센터")
if search_term:
    st.info(f"'{search_term}'에 대한 남한어 의미와 풀이가 표시되는 공간입니다.")

st.markdown('<div class="section-title">🗣️ 2. AI 남한어 연습</div>', unsafe_allow_html=True)
st.selectbox("연습할 상황을 선택하세요", ["☕ 카페 주문하기", "🏢 주민센터 방문", "💼 직장 면접"])
st.chat_input("메시지를 입력하세요...")

st.markdown('<div class="section-title">💡 3. 주요 문화 차이 안내</div>', unsafe_allow_html=True)
st.write("- **행정/금융**: 주민등록등본 발급, 체크카드 활용법")
st.write("- **일상/소비**: 키오스크 주문, 분리배출 방법")
st.write("- **직장/사회**: 직급 호칭 문화, 회식 에티켓")
