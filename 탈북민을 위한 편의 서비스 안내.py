import os
import streamlit as st
from google import genai

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="탈북민을 위한 편의 서비스 안내",
    page_icon="🤝",
    layout="wide"
)

# 2. Gemini API 키 안전하게 불러오기 (Secrets -> 환경변수 -> 사이드바 입력 순)
api_key = ""
try:
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

if not api_key:
    api_key = os.environ.get("GEMINI_API_KEY", "")

# 사이드바 설정 및 메뉴
st.sidebar.title("📌 메뉴 및 설정")

# Secrets 미설정 시를 대비한 백업 API 키 입력란 (오류 방지용)
if not api_key:
    user_key = st.sidebar.text_input("Gemini API Key (Secrets 미설정 시 입력)", type="password")
    if user_key:
        api_key = user_key

def generate_ai_response(prompt: str) -> str:
    if not api_key:
        return "⚠️ `GEMINI_API_KEY`가 설정되지 않았습니다. Streamlit Secrets에 키를 등록하거나 사이드바에 입력해 주세요."
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model='gemini-2.5-flash-lite',
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"⚠️ AI 서비스 호출 중 오류가 발생했습니다: {str(e)}"

# 3. 내비게이션 세션 관리 (Streamlit 오류 방지용 안전한 콜백 방식)
menu_options = ["홈", "1. 언어변환 페이지", "2. AI 남한어 연습 페이지", "3. 주요 문화 차이 페이지"]

if "nav" not in st.session_state or st.session_state["nav"] not in menu_options:
    st.session_state["nav"] = "홈"

def set_page(page_name):
    st.session_state["nav"] = page_name

# 라디오 버튼 내비게이션
selected_page = st.sidebar.radio("페이지 이동", menu_options, key="nav")

# -----------------------------------------------------------------------------
# PAGE 1: 홈 (안내 및 바로가기)
# -----------------------------------------------------------------------------
if selected_page == "홈":
    st.title("탈북민을 위한 편의 서비스 안내")
    
    st.info(
        "안녕하세요! 이사이트는 2026년 10월에 만들어진 탈북민을 위한 사이트이며 "
        "남한과 북한언어 차이, 문화 차이 등 여러 요인 때문에 남한 생활에 어려움을 겪는 탈북민들을 돕기 위한 사이트입니다."
    )
    
    st.markdown("---")
    st.subheader("주요 기능 설명 및 바로가기")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 1. 언어변환 페이지")
        st.write("생소한 남한의 외래어, 신조어, 전문 용어를 북한 어휘와 쉬운 뜻풀이로 변환해 드립니다.")
        st.button("바로가기 ➔", key="btn_p1", on_click=set_page, args=("1. 언어변환 페이지",))

    with col2:
        st.markdown("### 2. AI 남한어 연습 페이지")
        st.write("은행, 병원, 관공서 등 남한 생활에 필요한 실전 대화를 AI와 자유롭게 연습할 수 있습니다.")
        st.button("바로가기 ➔", key="btn_p2", on_click=set_page, args=("2. AI 남한어 연습 페이지",))

    with col3:
        st.markdown("### 3. 주요 문화 차이 페이지")
        st.write("금융, 의료, 행정 제도 등 남북한 생활 문화 차이를 비교 표와 AI Q&A로 알기 쉽게 정리해 드립니다.")
        st.button("바로가기 ➔", key="btn_p3", on_click=set_page, args=("3. 주요 문화 차이 페이지",))

# -----------------------------------------------------------------------------
# PAGE 2: 언어변환 페이지
# -----------------------------------------------------------------------------
elif selected_page == "1. 언어변환 페이지":
    st.title("🔤 1. 언어변환 페이지")
    st.write("남한 생활 중 뜻을 잘 모르겠거나 생소한 단어 및 문장을 입력해 보세요.")

    example_choice = st.selectbox(
        "자주 쓰이는 남한 표현 예시 선택:",
        [
            "직접 입력",
            "아이스 아메리카노 테이크아웃으로 키오스크에서 주문해 주세요.",
            "모바일 뱅킹으로 공과금을 자동이체 신청하려고 합니다.",
            "주민센터에서 주민등록등본 발급받으려면 신분증이 필요합니다."
        ]
    )

    default_value = "" if example_choice == "직접 입력" else example_choice
    user_input = st.text_area("변환할 남한어 문장/단어 입력:", value=default_value, placeholder="예: 패스트푸드점에서 키오스크로 결제하세요.", height=120)

    if st.button("언어 변환하기", type="primary"):
        if not user_input.strip():
            st.warning("변환할 문장이나 단어를 입력해 주세요.")
        else:
            with st.spinner("AI가 분석 및 변환 중입니다..."):
                prompt = f"""
                당신은 탈북민의 남한 사회 정착을 돕는 친절한 언어 튜터입니다.
                아래 남한어 문장이나 단어에 대해 다음 항목으로 친절히 해설해 주세요:

                1. **알기 쉬운 뜻풀이**: 핵심 의미를 쉬운 말로 요약해 주세요.
                2. **외래어 및 어휘 비교**: 남한 표현과 상응하는 북한 어휘 또는 쉬운 우리말 설명.
                3. **실생활 팁**: 해당 상황에서 알아두면 좋은 행동 요령이나 에티켓.

                [입력 문장]: {user_input}
                """
                result = generate_ai_response(prompt)
                st.markdown("### 💡 변환 결과")
                st.markdown(result)

# -----------------------------------------------------------------------------
# PAGE 3: AI 남한어 연습 페이지
# -----------------------------------------------------------------------------
elif selected_page == "2. AI 남한어 연습 페이지":
    st.title("💬 2. AI 남한어 연습 페이지")
    st.write("실전 상황별로 AI 직원과 가상 대화를 나누며 자연스러운 남한 표현을 연습해 보세요.")

    scenario = st.selectbox(
        "연습할 상황을 선택하세요:",
        ["은행 창구에서 계좌 개설하기", "주민센터에서 서류 발급받기", "병원 접수 및 증상 설명하기", "카페에서 음료 주문하기"]
    )

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "last_scenario" not in st.session_state or st.session_state.last_scenario != scenario:
        st.session_state.last_scenario = scenario
        st.session_state.chat_history = [
            {"role": "assistant", "content": f"안녕하세요! **[{scenario}]** 대화 연습입니다.\n\n'어서 오세요! 무엇을 도와드릴까요?'"}
        ]

    for msg in st.session_state.chat_history:
        st.chat_message(msg["role"]).write(msg["content"])

    if user_chat := st.chat_input("답변을 입력하세요..."):
        st.session_state.chat_history.append({"role": "user", "content": user_chat})
        st.chat_message("user").write(user_chat)

        with st.spinner("AI 답변 생성 중..."):
            prompt = f"""
            당신은 탈북민의 남한 언어적응을 돕는 친절한 AI 대화 상대입니다.
            현재 상황: [{scenario}]

            사용자의 말: "{user_chat}"

            다음 구성을 따라 응답을 제공해 주세요:
            1. [직원 응답]: 상황에 맞는 자연스럽고 친절한 남한 직원 역할 대화 (2~3문장).
            2. [표현 팁]: 사용자가 쓴 표현 중 남한에서 더 자연스럽게 쓰이는 높임말이나 용어 피드백.
            """
            ai_reply = generate_ai_response(prompt)
            st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})
            st.chat_message("assistant").write(ai_reply)

# -----------------------------------------------------------------------------
# PAGE 4: 주요 문화 차이 페이지
# -----------------------------------------------------------------------------
elif selected_page == "3. 주요 문화 차이 페이지":
    st.title("📚 3. 주요 문화 차이 페이지")
    st.write("남한과 북한의 생활 분야별 주요 제도 및 문화 차이점을 확인하세요.")

    tab1, tab2, tab3, tab4 = st.tabs(["💰 금융/상거래", "🏥 의료/사회복지", "🏢 행정/주거", "🔍 AI 문화 Q&A"])

    with tab1:
        st.subheader("금융 및 상거래 문화 차이")
        st.markdown("""
        | 구분 | 남한 생활 특징 | 안내 및 주의사항 |
        | :--- | :--- | :--- |
        | **결제 수단** | 신용카드, 체크카드, 간편결제 위주 | 대부분 현금 없는 매장 운영 (카드 지참 필수) |
        | **신용점수** | 대출, 카드 발급의 기준이 되는 개인 신용평가 | 연체 없이 꾸준히 정산하는 금융 습관 중요 |
        | **자동이체** | 월세, 통신비, 공과금 등이 지정일에 자동 출금 | 계좌 잔액이 부족하면 연체 이자 발생 가능 |
        """)

    with tab2:
        st.subheader("의료 및 보건 시스템")
        st.markdown("""
        | 구분 | 남한 생활 특징 | 안내 및 주의사항 |
        | :--- | :--- | :--- |
        | **의료보험** | 국민건강보험 적용으로 진료비 일부 본인 부담 | 병원 진료 후 창구에서 결제 진행 |
        | **약국 이용** | 처방전 필요 약품과 일반 의약품 분리 | 감기약, 진통제 등은 약국/편의점에서 바로 구매 가능 |
        | **응급 신고** | 응급환자 발생 시 119 구급차 무료 이용 | 긴급상황 발생 시 국번 없이 119 전화 |
        """)

    with tab3:
        st.subheader("행정 및 주거 체계")
        st.markdown("""
        | 구분 | 남한 생활 특징 | 안내 및 주의사항 |
        | :--- | :--- | :--- |
        | **민원 서류** | 주민센터 방문 또는 '정부24' 무인발급기 이용 | 신분증(주민등록증) 지참 필수 |
        | **주거 계약** | 전세(보증금) 및 월세(보증금+월세) 제도 | 집 계약 후 반드시 '전입신고' 및 '확정일자' 받아야 함 |
        | **쓰레기 배출** | 규격 봉투(종량제) 사용 및 분리수거 | 쓰레기 종류별, 요일별 배출 규정 준수 |
        """)

    with tab4:
        st.subheader("🔍 AI 문화 궁금증 해결사")
        st.write("남한 생활 문화 중 궁금한 점이 있다면 무엇이든 물어보세요!")
        
        culture_q = st.text_input("질문 입력 (예: 남한에서 '밥 한번 먹자'는 인사는 실제 약속인가요?)")
        if st.button("질문하기", key="btn_ask_culture"):
            if culture_q.strip():
                with st.spinner("AI가 문화 배경을 설명해 드립니다..."):
                    prompt = f"""
                    탈북민이 궁금해하는 남한 문화 질문입니다.
                    질문: "{culture_q}"

                    탈북민 입장에서 이해하기 쉽도록 친절하고 명확하게 남한 사회의 문화적 맥락과 팁을 설명해 주세요.
                    """
                    ans = generate_ai_response(prompt)
                    st.markdown("### 💡 AI 답변")
                    st.markdown(ans)
            else:
                st.warning("질문을 입력해 주세요.")
