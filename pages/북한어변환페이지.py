
import json
import re
import streamlit as st

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None


# -------------------------
# 페이지 설정
# -------------------------
st.set_page_config(
    page_title="북한어변환",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# -------------------------
# 예시 사전
# -------------------------
DICTIONARY = {
    "손전화": {
        "south": "휴대전화",
        "meaning": "가지고 다니며 통화하는 전화기",
        "difference": "남한에서는 휴대전화, 휴대폰이라고 표현합니다."
    },
    "얼음보숭이": {
        "south": "아이스크림",
        "meaning": "차갑게 얼려 만든 달콤한 디저트",
        "difference": "남한에서는 아이스크림이라는 표현이 일반적입니다."
    },
    "녀성": {
        "south": "여성",
        "meaning": "여자라는 성별을 가리키는 말",
        "difference": "남한에서는 두음 법칙에 따라 여성이라고 씁니다."
    },
    "로동": {
        "south": "노동",
        "meaning": "몸이나 정신을 사용하여 일하는 것",
        "difference": "남한에서는 두음 법칙에 따라 노동이라고 씁니다."
    },
    "랭면": {
        "south": "냉면",
        "meaning": "차게 먹는 국수 음식",
        "difference": "남한에서는 냉면이라고 표기합니다."
    },
    "인차": {
        "south": "곧, 이내, 바로",
        "meaning": "시간이 오래 지나지 않아",
        "difference": "문맥에 따라 곧, 이내, 바로 등으로 바꿉니다."
    },
    "꽝포": {
        "south": "거짓말, 허풍",
        "meaning": "사실과 다르거나 과장된 말을 하는 것",
        "difference": "문맥에 따라 거짓말하다, 허풍을 떨다 등으로 표현합니다."
    },
    "후라이": {
        "south": "거짓말, 허풍",
        "meaning": "일부 구어적 문맥에서 사실이 아닌 말을 뜻하는 표현",
        "difference": "사용되는 지역과 문맥에 따라 의미가 달라질 수 있습니다."
    },
    "살림집": {
        "south": "집, 주택",
        "meaning": "사람이 생활하며 거주하는 곳",
        "difference": "문맥에 따라 집 또는 주택으로 표현할 수 있습니다."
    },
}


SYSTEM_PROMPT = """
너는 북한어를 남한에서 자연스럽게 쓰는 한국어로 바꾸는 도우미다.

입력 문장의 의미를 바꾸거나 내용을 지어내지 마라.
단어의 뜻과 남북한 표현 차이를 쉬운 한국어로 설명하라.
문맥이 불확실하면 확실하지 않다고 밝혀라.
북한어에 대응하는 남한어가 없는 경우 억지로 바꾸지 마라.

반드시 JSON 객체로 답하라.
형식:
{
  "converted": "자연스러운 한국어 변환 결과",
  "summary": "쉬운 뜻풀이",
  "differences": [
    {
      "north": "북한어 표현",
      "south": "남한어 표현",
      "meaning": "뜻과 표현 차이"
    }
  ],
  "confidence": "높음/보통/낮음"
}
"""


# -------------------------
# 변환 기능
# -------------------------
def offline_convert(text):
    converted = text
    differences = []

    for word in sorted(DICTIONARY, key=len, reverse=True):
        if word in text:
            item = DICTIONARY[word]
            converted = converted.replace(word, item["south"])

            differences.append({
                "north": word,
                "south": item["south"],
                "meaning": item["difference"]
            })

    if differences:
        summary = (
            "예시 사전에 등록된 단어를 바꿨습니다. "
            "실제 의미는 문맥에 따라 달라질 수 있습니다."
        )
        confidence = "보통"
    else:
        summary = (
            "예시 사전에서 일치하는 단어를 찾지 못했습니다. "
            "AI 기능을 이용하면 문맥을 분석할 수 있습니다."
        )
        confidence = "낮음"

    return {
        "converted": converted,
        "summary": summary,
        "differences": differences,
        "confidence": confidence
    }


def parse_json(text):
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("AI 응답을 읽을 수 없습니다.")

    data = json.loads(text[start:end + 1])

    if not isinstance(data, dict):
        raise ValueError("AI 응답 형식이 올바르지 않습니다.")

    if not isinstance(data.get("converted"), str):
        raise ValueError("변환 결과가 없습니다.")

    data.setdefault("summary", "뜻풀이가 없습니다.")
    data.setdefault("differences", [])
    data.setdefault("confidence", "보통")

    if not isinstance(data["differences"], list):
        data["differences"] = []

    return data


def ai_convert(text, api_key):
    if genai is None:
        raise RuntimeError("AI 라이브러리를 불러올 수 없습니다.")

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=SYSTEM_PROMPT + "\n입력 문장:\n" + text,
        config=types.GenerateContentConfig(
            temperature=0.2,
            response_mime_type="application/json"
        )
    )

    if not response.text:
        raise ValueError("AI 응답이 비어 있습니다.")

    return parse_json(response.text)


# -------------------------
# 디자인
# -------------------------
st.markdown("""
<style>
    .stApp {
        background-color: #ffffff;
    }

    .block-container {
        max-width: 1250px;
        padding-top: 1rem;
        padding-bottom: 2rem;
    }

    .main-title {
        font-size: 30px;
        font-weight: 700;
        text-align: center;
        color: #111111;
        margin-bottom: 18px;
    }

    .outer-frame {
        border: 1px solid #333333;
        padding: 12px;
        background: white;
    }

    .member-box {
        border-right: 1px solid #333333;
        min-height: 540px;
        padding: 8px;
        color: #111111;
        font-size: 16px;
        line-height: 2;
    }

    .language-label {
        background-color: #cfe2f3;
        border: 1px solid #333333;
        color: #111111;
        text-align: center;
        padding: 5px 8px;
        font-size: 20px;
        margin: 0 auto 18px auto;
        max-width: 250px;
    }

    .arrow {
        text-align: center;
        font-size: 38px;
        line-height: 1.1;
        color: #111111;
        margin-bottom: 10px;
    }

    .example-box {
        background-color: #cfe2f3;
        border: 1px solid #333333;
        color: #111111;
        padding: 12px;
        font-size: 18px;
        line-height: 1.5;
        margin: 18px 12px 5px 12px;
    }

    div[data-testid="stTextArea"] textarea {
        background-color: #cfe2f3 !important;
        color: #111111 !important;
        border: 1px solid #333333 !important;
        border-radius: 0 !important;
        font-size: 18px !important;
        min-height: 190px;
    }

    div[data-testid="stTextArea"] label {
        display: none;
    }

    div.stButton > button {
        border-radius: 0;
        border: 1px solid #333333;
        min-height: 42px;
    }

    div.stButton > button[kind="primary"] {
        background-color: #cfe2f3;
        color: #111111;
        font-weight: 600;
    }

    .result-heading {
        background-color: #cfe2f3;
        border: 1px solid #333333;
        padding: 8px;
        text-align: center;
        font-size: 18px;
        color: #111111;
        margin-bottom: 10px;
    }

    div[data-testid="stAlert"] {
        border-radius: 0;
    }
</style>
""", unsafe_allow_html=True)


# -------------------------
# 페이지 제목
# -------------------------
st.markdown(
    '<div class="main-title">북한어변환</div>',
    unsafe_allow_html=True
)


# -------------------------
# 전체 표 레이아웃
# -------------------------
member_col, content_col = st.columns(
    [1, 6],
    gap="small"
)

with member_col:
    st.markdown("""
    <div class="member-box">
        조원 3:<br>
        11306 김슬지
    </div>
    """, unsafe_allow_html=True)


with content_col:

    # 북한어 / 화살표 / 남한어
    label1, arrow_col, label2 = st.columns(
        [1, 0.45, 1],
        gap="small"
    )

    with label1:
        st.markdown(
            '<div class="language-label">북한어</div>',
            unsafe_allow_html=True
        )

    with arrow_col:
        st.markdown(
            '<div class="arrow">➜</div>',
            unsafe_allow_html=True
        )

    with label2:
        st.markdown(
            '<div class="language-label">남한어</div>',
            unsafe_allow_html=True
        )

    # 입력 칸 / 결과 칸
    input_col, output_col = st.columns(
        2,
        gap="large"
    )

    with input_col:
        north_text = st.text_area(
            "북한어 입력",
            placeholder="북한어 단어나 문장을 입력하세요.",
            height=190,
            key="north_text",
            max_chars=5000
        )

    with output_col:
        if "converted_text" not in st.session_state:
            st.session_state.converted_text = ""

        st.text_area(
            "남한어 변환 결과",
            value=st.session_state.converted_text,
            height=190,
            key="south_text",
            disabled=True
        )

    # 예시 영역
    st.markdown("""
    <div class="example-box">
        예) 꽝포, 대포, 후라이 → 거짓말
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    # AI 설정
    use_ai = st.checkbox(
        "AI를 사용하여 문맥까지 분석하기",
        value=True
    )

    convert_button = st.button(
        "북한어 변환하기",
        type="primary",
        use_container_width=True
    )

    if convert_button:
        if not north_text.strip():
            st.warning("북한어를 먼저 입력해 주세요.")

        else:
            try:
                api_key = str(
                    st.secrets.get("GEMINI_API_KEY", "")
                ).strip()
            except Exception:
                api_key = ""

            result = None

            if use_ai and api_key:
                try:
                    with st.spinner("북한어를 분석하고 있습니다..."):
                        result = ai_convert(
                            north_text.strip(),
                            api_key
                        )

                    st.success("AI 변환이 완료되었습니다.")

                except Exception as error:
                    st.warning(
                        "AI 요청에 실패하여 예시 사전으로 변환합니다."
                    )
                    st.caption(
                        "오류 유형: " + type(error).__name__
                    )

            elif use_ai and not api_key:
                st.info(
                    "API 키가 없어 예시 사전으로 변환합니다. "
                    "AI 기능을 사용하려면 Secrets를 설정하세요."
                )

            if result is None:
                result = offline_convert(north_text.strip())

            st.session_state.converted_text = result["converted"]

            # 결과 칸 즉시 갱신
            st.rerun()


    # 변환 결과 설명
    if st.session_state.get("converted_text"):
        st.divider()

        st.markdown("### 단어 뜻과 표현 차이")

        result_data = st.session_state.get(
            "last_result",
            None
        )

        # 변환 결과와 설명은 아래 저장 로직을 통해 표시됩니다.
        if result_data:
            st.info(result_data.get("summary", ""))

            for item in result_data.get("differences", []):
                with st.container(border=True):
                    c1, c2 = st.columns(2)

                    with c1:
                        st.markdown("**북한어**")
                        st.write(item.get("north", "-"))

                    with c2:
                        st.markdown("**남한어**")
                        st.write(item.get("south", "-"))

                    st.caption(item.get("meaning", ""))

        else:
            st.write(
                "변환 결과를 확인하세요. "
                "표현 차이는 문맥에 따라 달라질 수 있습니다."
            )


st.divider()

st.caption(
    "북한어변환 | 북한어와 남한어의 뜻과 표현 차이를 알아보는 학습 도구"
)
