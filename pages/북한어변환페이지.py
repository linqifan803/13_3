
import json
import re
import streamlit as st

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None


st.set_page_config(
    page_title="북한어변환",
    page_icon="🗣️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# 북한어 예시 사전
DICTIONARY = {
    "손전화": {
        "south": "휴대전화",
        "meaning": "가지고 다니며 통화하는 전화기",
        "difference": "남한에서는 휴대전화, 휴대폰 또는 핸드폰이라고 표현합니다."
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
        "meaning": "일부 구어적 문맥에서 거짓말을 뜻하는 표현",
        "difference": "정확한 의미는 사용된 문맥에 따라 달라질 수 있습니다."
    },
    "살림집": {
        "south": "집, 주택",
        "meaning": "사람이 생활하며 거주하는 곳",
        "difference": "문맥에 따라 집 또는 주택으로 표현할 수 있습니다."
    },
    "가락지빵": {
        "south": "도넛",
        "meaning": "고리 모양으로 만든 빵이나 과자",
        "difference": "남한에서는 도넛이라는 표현이 일반적입니다."
    }
}


SYSTEM_PROMPT = """
너는 북한어를 남한의 자연스러운 한국어로 바꾸는 언어 도우미다.
입력의 의미를 바꾸거나 내용을 지어내지 마라.
단어 뜻과 표현 차이를 쉬운 한국어로 설명하라.
문맥이 불확실하면 확실하지 않다고 밝혀라.
반드시 JSON 객체로 답하라.

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
            "문장 전체의 의미는 문맥에 따라 달라질 수 있습니다."
        )
        confidence = "보통"
    else:
        summary = (
            "예시 사전에서 일치하는 단어를 찾지 못했습니다. "
            "AI 분석을 이용하면 문맥에 맞는 변환을 시도할 수 있습니다."
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

    if start < 0 or end < 0:
        raise ValueError("AI 응답 형식이 올바르지 않습니다.")

    data = json.loads(text[start:end + 1])

    if not isinstance(data, dict):
        raise ValueError("AI 응답이 JSON 객체가 아닙니다.")

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
        raise RuntimeError("AI 라이브러리가 설치되지 않았습니다.")

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=SYSTEM_PROMPT + "\n\n입력 문장:\n" + text,
        config=types.GenerateContentConfig(
            temperature=0.2,
            response_mime_type="application/json"
        )
    )

    if not response.text:
        raise ValueError("AI 응답이 비어 있습니다.")

    return parse_json(response.text)


# 디자인 CSS
st.markdown("""
<style>
    .stApp {
        background: #f5f8fc;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .page-header {
        text-align: center;
        margin-bottom: 28px;
    }

    .page-title {
        font-size: 34px;
        font-weight: 800;
        color: #263f5c;
        margin-bottom: 5px;
    }

    .page-description {
        color: #65758a;
        font-size: 15px;
    }

    .language-label {
        background: #cfe2f3;
        border: 1px solid #9aafc2;
        border-radius: 8px;
        padding: 10px;
        text-align: center;
        color: #24384d;
        font-size: 20px;
        font-weight: 600;
    }

    .arrow-label {
        text-align: center;
        color: #456b91;
        font-size: 34px;
        padding-top: 1px;
    }

    .panel-label {
        color: #344c66;
        font-size: 17px;
        font-weight: 700;
        margin-top: 18px;
        margin-bottom: 8px;
    }

    div[data-testid="stTextArea"] textarea {
        background-color: #e4eff9;
        color: #26384a;
        border: 1px solid #b1c5d8;
        border-radius: 8px;
        font-size: 17px;
        line-height: 1.7;
    }

    div[data-testid="stTextArea"] label {
        color: #344c66;
        font-weight: 600;
    }

    div.stButton > button {
        border-radius: 8px;
        min-height: 44px;
        font-weight: 600;
    }

    div.stButton > button[kind="primary"] {
        background-color: #416f9f;
        color: white;
        border: none;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-color: #d7e2ee;
        border-radius: 10px;
    }

    .example-note {
        background: #e4eff9;
        border: 1px solid #c1d3e5;
        border-radius: 8px;
        padding: 12px 15px;
        color: #405a73;
        line-height: 1.8;
        font-size: 14px;
    }

    .footer-note {
        color: #78889a;
        font-size: 12px;
        text-align: center;
        margin-top: 25px;
    }
</style>
""", unsafe_allow_html=True)


# 페이지 제목
st.markdown("""
<div class="page-header">
    <div class="page-title">🗣️ 북한어변환</div>
    <div class="page-description">
        북한말을 자연스러운 한국어로 바꾸고 단어의 뜻과 표현 차이를 알아보세요.
    </div>
</div>
""", unsafe_allow_html=True)


# 변환 입력 영역
with st.container(border=True):
    north_col, arrow_col, south_col = st.columns(
        [1, 0.12, 1],
        gap="medium"
    )

    with north_col:
        st.markdown(
            '<div class="language-label">북한어</div>',
            unsafe_allow_html=True
        )

        north_text = st.text_area(
            "북한어 입력",
            placeholder="북한어 단어나 문장을 입력하세요.\n예: 인차 손전화로 알려주겠소.",
            height=220,
            max_chars=5000,
            label_visibility="collapsed",
            key="north_input"
        )

    with arrow_col:
        st.markdown(
            '<div class="arrow-label">→</div>',
            unsafe_allow_html=True
        )

    with south_col:
        st.markdown(
            '<div class="language-label">남한어</div>',
            unsafe_allow_html=True
        )

        st.text_area(
            "남한어 결과",
            placeholder="변환 결과가 여기에 표시됩니다.",
            height=220,
            disabled=True,
            label_visibility="collapsed",
            key="south_output"
        )

    st.markdown("""
    <div class="example-note">
        <b>변환 예시</b><br>
        꽝포 → 거짓말 또는 허풍<br>
        손전화 → 휴대전화<br>
        녀성 → 여성
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    option_col, button_col = st.columns([1, 1])

    with option_col:
        use_ai = st.checkbox(
            "AI 문맥 분석 사용",
            value=True,
            help="API 키가 없으면 예시 사전으로 변환합니다."
        )

    with button_col:
        convert_button = st.button(
            "한국어로 변환하기 →",
            type="primary",
            use_container_width=True
        )


# 결과 상태 관리
if "conversion_result" not in st.session_state:
    st.session_state.conversion_result = None

if convert_button:
    if not north_text.strip():
        st.warning("변환할 북한어 단어나 문장을 입력해 주세요.")
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
                with st.spinner("문맥과 표현 차이를 분석하고 있습니다..."):
                    result = ai_convert(north_text.strip(), api_key)
            except Exception as error:
                st.warning(
                    "AI 변환에 실패하여 예시 사전으로 변환합니다."
                )
                st.caption("오류 유형: " + type(error).__name__)

        elif use_ai and not api_key:
            st.info(
                "API 키가 등록되지 않아 예시 사전으로 변환합니다. "
                "AI를 사용하려면 Streamlit Secrets를 설정하세요."
            )

        if result is None:
            result = offline_convert(north_text.strip())

        st.session_state.conversion_result = result
        st.rerun()


# 변환 결과 표시
result = st.session_state.conversion_result

if result:
    st.markdown("## 변환 결과")

    result_col, meaning_col = st.columns([1, 1], gap="large")

    with result_col:
        st.markdown("### 🇰🇷 자연스러운 한국어")

        st.text_area(
            "변환된 문장",
            value=result.get("converted", ""),
            height=130,
            key="final_converted_text"
        )

        st.caption(
            "분석 신뢰도: "
            + str(result.get("confidence", "보통"))
        )

        st.download_button(
            "변환 결과 다운로드",
            data=result.get("converted", ""),
            file_name="북한어변환결과.txt",
            mime="text/plain",
            use_container_width=True
        )

    with meaning_col:
        st.markdown("### 💡 쉬운 뜻풀이")

        with st.container(border=True):
            st.write(
                result.get("summary", "뜻풀이가 없습니다.")
            )

    st.markdown("### 🔎 단어와 표현 차이")

    differences = result.get("differences", [])

    if differences:
        for item in differences:
            if not isinstance(item, dict):
                continue

            with st.container(border=True):
                left, right = st.columns(2)

                with left:
                    st.markdown("**북한어 표현**")
                    st.write(item.get("north", "-"))

                with right:
                    st.markdown("**남한어 표현**")
                    st.write(item.get("south", "-"))

                st.caption(item.get("meaning", ""))

    else:
        st.info(
            "별도의 표현 차이를 찾지 못했습니다. "
            "문맥에 따라 결과가 달라질 수 있습니다."
        )


# 하단 안내
st.markdown("""
<div class="footer-note">
    북한어변환 · 남북한 언어 차이를 배우는 학습 도구<br>
    자동 변환 결과는 참고용이며 문맥에 따라 정확도가 달라질 수 있습니다.
</div>
""", unsafe_allow_html=True)
