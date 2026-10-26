import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="탈북민을 위한 편의 서비스 안내",
    page_icon="🇰🇷",
    layout="wide"
)

# 세련된 CSS 디자인 적용 (폰트, 카드 스타일, 컬러 하이라이트)
st.markdown("""
    <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

    /* 전체 폰트 및 배경 설정 */
    html, body, [class*="css"] {
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
    }

    /* 메인 타이틀 디자인 */
    .main-title {
        font-size: 2.3rem;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: -0.03em;
        margin-bottom: 1.2rem;
        text-align: center;
    }

    /* 상단 안내 박스 디자인 */
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
        margin-bottom: 2.5rem;
    }

    /* 서브 타이틀 디자인 */
    .section-title {
        font-size: 1.35rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 1rem;
        letter-spacing: -0.02em;
    }

    /* 카드 컨테이너 디자인 */
    .card-container {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 1.8rem 1.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
        height: 100%;
        min-height: 180px;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
    }

    /* 카드 내부 태그 라벨 */
    .card-badge {
        display: inline-block;
        background-color: #EFF6FF;
        color: #2563EB;
        font-size: 0.8rem;
        font-weight: 700;
        padding: 0.3rem 0.7rem;
        border-radius: 20px;
        width: fit-content;
        margin-bottom: 0.8rem;
    }

    /*
