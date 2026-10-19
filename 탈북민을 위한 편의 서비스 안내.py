import os
import streamlit as st
from google import genai

# ------------------------------------------------------------------------------
# 1. 페이지 기본 설정 및 세션 상태 초기화
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="탈북민을 위한 편의 서비스", page_icon="🇰🇷", layout="wide"
)

if "page" not in st.session_state:
    st.session_state.page = "홈"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# Gemini API 클라이언트 생성 함수
def get_gemini_client():
    api_key = None
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
    elif os.environ.get("GEMINI_API_KEY"):
        api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        return None
    try:
        return genai.Client(api_key=api_key)
    except Exception as e:
        st.error(f"API 연결 설정 중 오류가 발생했습니다: {e}")
        return None


# ------------------------------------------------------------------------------
# 2. 사이드바 네비게이션
# ------------------------------------------------------------------------------
st.sidebar.title("📌 메뉴 이동")
page_options = ["홈", "언어변환 페이지", "AI 남한어 연습 페이지", "주요문화 차이 페이지"]

selected_page = st.sidebar.radio(
    "원하는 서비스를 선택하세요:",
    page_options,
    index=page_options.index(st.session_state.page),
)

if selected_page != st.session_state.page:
    st.session_state.page = selected_page
    st.rerun()

# ------------------------------------------------------------------------------
# 3. 페이지별 화면 구현
# ------------------------------------------------------------------------------

# === [메인 홈 페이지] ===
if st.session_state.page == "홈":
    st.title("탈북민을 위한 편의 서비스 안내")

    st.info(
        "안녕하세요! 이 사이트는 2026년 10월에 만들어진 탈북민을 위한 사이트이며 "
        "남한과 북한언어 차이, 문화 차이 등 여러 요인 때문에 남한 생활에 어려움을 겪는 "
        "탈북민들을 돕기 위한 사이트입니다."
    )

    st.markdown("---")
    st.subheader("주요 기능 설명 및 바로가기")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 1. 언어변환 페이지")
        st.write(
            "남한어와 북한어의 단어 차이나 생소한 외래어, 일상 용어를 쉽게 비교하고 이해할 수 있도록 변환해 드립니다."
        )
        if st.button("바로가기 ➔", key="btn1"):
            st.session_state.page = "언어변환 페이지"
            st.rerun()

    with col2:
        st.markdown("### 2. AI 남한어 연습 페이지")
        st.write(
            "대중교통, 식당 주문, 주민센터 방문 등 다양한 남한의 일상 대화 상황을 AI와 실시간으로 연습할 수 있습니다."
        )
        if st.button("바로가기 ➔", key="btn2"):
            st.session_state.page = "AI 남한어 연습 페이지"
            st.rerun()

    with col3:
        st.markdown("### 3. 주요문화 차이 페이지")
        st.write(
            "남한과 북한의 일상생활, 행정, 금융, 대중교통 등 필수적인 문화 차이점과 생활 팁을 안내합니다."
        )
        if st.button("바로가기 ➔", key="btn3"):
            st.session_state.page = "주요문화 차이 페이지"
            st.rerun()

# === [1. 언어변환 페이지] ===
elif st.session_state.page == "언어변환 페이지":
    st.title("🔤 1. 언어변환 페이지")
    st.write(
        "북한 어휘나 생소한 남한의 외래어 및 줄임말을 입력하시면 뜻풀이와 함께 쉬운 표현으로 변환해 드립니다."
    )

    client = get_gemini_client()
    if not client:
        st.warning(
            "⚠️ Gemini API 키가 설정되지 않았습니다. Secrets에 GEMINI_API_KEY를 등록해주세요."
        )

    direction = st.radio(
        "변환 방향을 선택하세요:",
        ["북한어 ➔ 남한어 변환", "남한어/외래어 ➔ 북한어 및 쉬운 설명"],
    )

    user_input = st.text_area(
        "변환할 단어나 문장을 입력하세요:",
        placeholder="예: 곽밥, 원적지, 키오스크, 아메리카노 등",
    )

    if st.button("변환하기"):
        if not user_input.strip():
            st.warning("변환할 내용을 입력해주세요.")
        elif not client:
            st.error("Gemini API 키가 없어 AI 서비스를 이용할 수 없습니다.")
        else:
            with st.spinner("AI가 분석 중입니다..."):
                try:
                    prompt = f"""
                    당신은 탈북민의 남한 사회 적응을 돕는 친절하고 전문적인 언어 멘토입니다.
                    다음 입력을 바탕으로 사용자가 이해하기 쉽게 변환 및 설명해 주세요.

                    [요청 방향]: {direction}
                    [입력 내용]: {user_input}

                    [답변 형식]:
                    1. **변환 결과**: (남한 표준어 또는 북한 대응어)
                    2. **단어/문장 의미**: (친절한 뜻 풀이)
                    3. **실생활 활용 예문**: (실제 사용할 수 있는 예문 2개)
                    """
                    response = client.models.generate_content(
                        model="gemini-2.5-flash-lite", contents=prompt
                    )
                    st.success("변환이 완료되었습니다!")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"오류가 발생했습니다: {str(e)}")

# === [2. AI 남한어 연습 페이지] ===
elif st.session_state.page == "AI 남한어 연습 페이지":
    st.title("💬 2. AI 남한어 연습 페이지")
    st.write(
        "다양한 상황을 선택하고 AI와 대화를 주고받으며 남한의 일상 대화 표현을 연습해 보세요."
    )

    client = get_gemini_client()
    if not client:
        st.warning(
            "⚠️ Gemini API 키가 설정되지 않았습니다. Secrets에 GEMINI_API_KEY를 등록해주세요."
        )

    scenario = st.selectbox(
        "연습하고 싶은 상황을 선택하세요:",
        [
            "카페에서 음료 주문하기",
            "주민센터에서 서류 발급받기",
            "식당에서 메뉴 문의 및 주문하기",
            "부동산에서 집 구하기 상담하기",
            "회사에서 동료와 인사 및 업무 대화하기",
        ],
    )

    if st.button("대화 내용 초기화"):
        st.session_state.chat_history = []
        st.rerun()

    # 이전 대화 기록 표시
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # 입력 창
    user_chat = st.chat_input("AI에게 말해보세요...")
    if user_chat:
        st.session_state.chat_history.append(
            {"role": "user", "content": user_chat}
        )
        with st.chat_message("user"):
            st.write(user_chat)

        if not client:
            st.error("Gemini API 키가 설정되지 않아 응답을 생성할 수 없습니다.")
        else:
            with st.spinner("AI가 답변을 작성하는 중입니다..."):
                try:
                    conversation_text = "\n".join(
                        [
                            f"{m['role']}: {m['content']}"
                            for m in st.session_state.chat_history
                        ]
                    )
                    prompt = f"""
                    당신은 탈북민이 남한 사회에 자연스럽게 적응할 수 있도록 돕는 친절한 남한 대화 상대입니다.
                    현재 연습 대화 상황: [{scenario}]

                    대화 내역:
                    {conversation_text}

                    [지침]:
                    1. 선택된 상황에 맞추어 상호작용하는 답변을 자연스러운 남한 표준어로 작성하세요.
                    2. 만약 사용자가 북한식 어휘나 어색한 표현을 사용했다면, 대화 마지막 부분에 "💡 남한어 표현 팁:" 항목을 붙여 자연스러운 표준어 표현을 친절하게 추천해 주세요.
                    3. 대화를 원활하게 이어나갈 수 있도록 대화를 마무리하는 질문을 포함하세요.
                    """
                    response = client.models.generate_content(
                        model="gemini-2.5-flash-lite", contents=prompt
                    )
                    ai_reply = response.text

                    st.session_state.chat_history.append(
                        {"role": "assistant", "content": ai_reply}
                    )
                    with st.chat_message("assistant"):
                        st.write(ai_reply)
                except Exception as e:
                    st.error(f"오류가 발생했습니다: {str(e)}")

# === [3. 주요문화 차이 페이지] ===
elif st.session_state.page == "주요문화 차이 페이지":
    st.title("📚 3. 주요문화 차이 페이지")
    st.write(
        "남한 생활에서 꼭 알아야 할 주요 문화 및 제도의 차이점을 한눈에 확인하세요."
