import streamlit as st
import numpy as np
import joblib

import streamlit as st
import pandas as pd
import joblib  # 또는 pickle (모델을 로드하기 위해 필요합니다)

st.title("스마트팜 착과율 예측 머신러닝 모델")
st.write("내부 환경 정보를 입력하면 착과율을 예측합니다.")

rf_model = joblib.load("tomato_model.pkl")
st.image("https://m.health.chosun.com/site/data/img_dir/2014/03/27/2014032702818_0.jpg")
st.sidebar.header("환경 데이터 입력 (랜덤포레스트)")

# 2. Streamlit 슬라이더로 사용자 입력 받기 (최소값, 최대값, 기본값 설정)
temp = st.slider("내부온도 입력 (°C)", -10.0, 45.0, 25.0, step=0.5)
humidity = st.slider("내부습도 입력 (%)", 0.0, 100.0, 60.0, step=1.0)
soil_temp = st.slider("지온 입력 (°C)", 0.0, 35.0, 20.0, step=0.5)

# 3. DataFrame으로 변환(2차원 배열 형태로 입력)
input_data = pd.DataFrame([[temp, humidity, soil_temp]], columns=['내부온도', '내부습도', '지온'])

# 4. 버튼을 누르면 예측 수행 및 출력
if st.button("착과율 예측하기"):
    # rf_model이 사전에 로드되어 있어야 작동합니다.
    predicted = rf_model.predict(input_data)
    st.success(f"예측 착과율 : {predicted[0]:.1f}%")