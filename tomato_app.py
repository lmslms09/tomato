import streamlit as st
import pandas as pd
import joblib
import time

# 0. 페이지 설정 (귀여운 토마토 아이콘과 타이틀)
st.set_page_config(
    page_title="말랑말랑 토마토 예측기",
    page_icon="🍅",
    layout="centered"
)

# 귀여운 스타일링을 위한 간단한 CSS 주입 (폰트 및 배경 느낌 살리기)
st.markdown("""
    <style>
    .main-title {
        font-size: 30px !important;
        font-weight: bold;
        color: #FF4B4B;
    }
    .sub-title {
        font-size: 16px !important;
        color: #555555;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 1. 헤더 및 타이틀
st.markdown('<p class="main-title">🍅 말랑말랑 토마토 착과율 예측기 🍅</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">온실 안의 날씨를 알려주면, 토마토가 얼마나 잘 자랄지 예측해 줄게! ✨</p>', unsafe_allow_html=True)

# 귀여운 토마토 이미지
st.image("https://m.health.chosun.com/site/data/img_dir/2014/03/27/2014032702818_0.jpg", width=400)

# 모델 로드 (에러 방지를 위해 캐싱 처리)
@st.cache_resource
def load_model():
    return joblib.load("tomato_model.pkl")

try:
    rf_model = load_model()
except:
    rf_model = None
    st.warning("⚠️ `tomato_model.pkl` 파일을 찾을 수 없어서 테스트 모드로 작동해요!")

# 2. 귀여운 입력 공간 (사이드바 대신 메인 화면에 예쁘게 배치)
st.write("---")
st.subheader("🌱 지금 온실 환경은 어떤가요?")

# 2단 레이아웃으로 공간을 아기자기하게 분할
col1, col2 = st.columns(2)

with col1:
    temp = st.slider("🌡️ 온실 안 온도 (°C)", -10.0, 45.0, 25.0, step=0.5)
    soil_temp = st.slider("🪴 땅 속 온도 (지온, °C)", 0.0, 35.0, 20.0, step=0.5)

with col2:
    humidity = st.slider("💧 촉촉한 습도 (%)", 0.0, 100.0, 60.0, step=1.0)
    # 빈 공간을 채우거나 데코레이션용 텍스트
    st.write("")
    st.caption("💡 슬라이더를 밀어서 토마토방의 환경을 맞춰주세요!")

# Dataframe 변환
input_data = pd.DataFrame([[temp, humidity, soil_temp]], columns=['내부온도', '내부습도', '지온'])

st.write("---")

# 3. 예측 버튼 및 귀여운 효과
if st.button("✨ 토마토야 얼마나 자랄래? 예측해줘! ✨", use_container_width=True):
    
    # 귀여운 로딩 애니메이션
    with st.spinner("🤔 토마토가 열심히 생각하고 있어요... 잠시만 기다려줘! ⏳"):
        time.sleep(1) # 살짝 로딩 느낌 주기
        
        if rf_model is not None:
            predicted = rf_model.predict(input_data)[0]
        else:
            # 모델이 없을 때를 위한 가상 결과 (테스트용)
            predicted = (temp * 0.5) + (humidity * 0.3) + 20 
            predicted = min(max(predicted, 0), 100) # 0~100 사이 제한
    
    # 4. 깜찍한 결과 출력 및 축하 효과
    st.balloons() # 화면에 풍선이 팡팡 터집니다 🎈
    
    # 착과율 수치에 따른 귀여운 코멘트 추가
    if predicted >= 70:
        status_emoji = "🥳 대성공! 토마토가 주렁주렁 열릴 거예요! 🎉"
    elif predicted >= 40:
        status_emoji = "🌱 오호라! 무럭무럭 잘 자라고 있네요! 👍"
    else:
        status_emoji = "🥺 힝, 토마토가 조금 힘든가봐요 ㅠㅠ. 조금만 신경 써주세요! 💧"
        
    st.success(f"## 📊 예측 착과율 결과: **{predicted:.1f}%**")
    st.info(status_emoji)
