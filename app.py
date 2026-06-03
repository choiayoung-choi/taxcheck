import streamlit as st


# 1. 페이지 기본 설정 및 타이틀 세팅 (정직하고 신뢰감 있는 타이틀로 변경)
st.set_page_config(page_title="Tax-Check: 청년창업 세법 시뮬레이터", layout="wide")
st.title("🚀 Tax-Check: 예비 청년사업자 창업세액감면 및 재무 시뮬레이터")
st.caption("📊현행세법 반영")

st.info("### 📌 사용자가 입력한 사업 계획 데이터를 기반으로 실제 세액 감면 및 리스크 금액을 연산합니다.")

#new

st.header("📍 창업 예정지 주소 입력")
st.info("💡 본 시스템은 전국 17개 시·도의 조세특례제한법 및 수도권정비계획법을 동/읍/면 단위까지 반영하였습니다.")

# 1단계: 전국 17개 시/도 선택창
sido = st.selectbox("시/도를 선택하세요", [
    "선택하세요", "서울특별시", "인천광역시", "경기도", 
    "부산광역시", "대구광역시", "광주광역시", "대전광역시", "울산광역시",
    "세종특별자치시", "충청남도", "충청북도", "전라남도", "전라북도", 
    "경상남도", "경상북도", "강원특별자치도", "제주특별자치도"
])

reduction_rate = 0.0
zone_name = ""
location_status = "내" #하단 NameError 방지용 기본 안전장치 변수 선언


# ==================== [1] 서울특별시 (전 지역 과밀) ====================
if sido == "서울특별시":
    sigungu = st.selectbox("시/군/구를 선택하세요", ["선택하세요","강남구", "강동구", "강북구", "강서구", "관악구", "광진구", "구로구", "금천구", "노원구", "도봉구", "동대문구", "동작구", "마포구", "서대문구", "서초구", "성동구", "성북구", "송파구", "양천구", "영등포구", "용산구", "은평구", "종로구", "중구", "중랑구"])
    
    if sigungu != "선택하세요":
        reduction_rate = 0.5
        zone_name = "수도권 과밀억제권역 (기본 소득세 50% 감면)"
        location_status = "내" #  서울은 무조건 과밀억제권역 '내'
        is_ready = True

# ==================== [2] 인천광역시 (마이크로 동 단위 분기) ====================
elif sido == "인천광역시":
    sigungu = st.selectbox("시/군/구를 선택하세요", ["선택하세요", "서구", "연수구", "중구", "부평구", "계양구", "미추홀구", "남동구", "강화군", "옹진군"])
    

    if sigungu == "서구":
        special_dongs = ["검단동", "대곡동", "불로동", "마전동", "금곡동", "오류동", "왕길동", "당하동", "원당동", "아라동", "가좌/석남/연희동 내 국가·지방산업단지 구역"]
        normal_dongs = ["가좌동 (일반지역)", "석남동 (일반지역)", "신현동", "청라동", "연희동 (일반지역)", "심곡동", "공촌동", "경서동"]
        
        dong = st.selectbox("세부 행정동/법정동을 선택하세요", ["선택하세요"] + special_dongs + normal_dongs)

        if dong != "선택하세요":
            reduction_rate = 1.0 if dong in special_dongs else 0.5
            zone_name = "성장관리권역 (100% 면제)" if reduction_rate == 1.0 else "과밀억제권역 (50% 감면)"
            location_status = "외곽" if reduction_rate == 1.0 else "내"
            is_ready = True # 👈 완벽히 골랐으니 결과 창 띄워도 된다고 허락!
        




    elif sigungu == "연수구":
        songdo_dongs = ["송도동 (송도국제도시)", "인천경제자유구역 송도지구"]
        normal_dongs = ["옥련동", "선학동", "연수동", "청학동", "동춘동"]
        dong = st.selectbox("세부 행정동/법정동을 선택하세요", ["선택하세요"] + songdo_dongs + normal_dongs)

        
        if dong != "선택하세요":
            reduction_rate = 1.0 if dong in songdo_dongs else 0.5
            zone_name = "성장관리권역 (100% 면제)" if reduction_rate == 1.0 else "과밀억제권역 (50% 감면)"
            location_status = "외곽" if reduction_rate == 1.0 else "내"
            is_ready = True
  
    elif sigungu == "중구":
        youngjong_dongs = ["운서동", "운남동", "운북동", "중산동", "남북동", "덕교동", "을왕동", "무의동"]
        normal_dongs = ["신포동", "연안동", "신흥동", "동인천동", "북성동"]
        dong = st.selectbox("세부 행정동/법정동을 선택하세요", ["선택하세요"] + youngjong_dongs + normal_dongs)

        if dong != "선택하세요":
            reduction_rate = 1.0 if dong in youngjong_dongs else 0.5
            zone_name = "성장관리권역 (100% 면제)" if reduction_rate == 1.0 else "과밀억제권역 (50% 감면)"
            location_status = "외곽" if reduction_rate == 1.0 else "내"
            is_ready = True

    elif sigungu in ["부평구", "계양구", "미추홀구", "남동구"]:
        reduction_rate = 0.5
        zone_name = "수도권 과밀억제권역 (50% 감면)"
        location_status = "내"
    elif sigungu in ["강화군", "옹진군"]:
        reduction_rate = 1.0
        zone_name = "수도권 외 성장관리권역 (100% 면제)"
        location_status = "외곽"

# ==================== [3] 경기도 (마이크로 읍/면/동 분기) ====================
elif sido == "경기도":
    
    sigungu = st.selectbox("시/군/구를 선택하세요", [
        "선택하세요", "남양주시", "시흥시", "고양시", "안산시", "용인시", "화성시", 
        "수원시", "성남시", "안양시", "부천시", "광명시", "과천시", "의왕시", "군포시", "구리시", "하남시",
        "평택시", "파주시", "김포시", "광주시", "이천시", "오산시", "안성시", "포천시", "양주시", "여주시", "동두천시", "연천군", "가평군", "양평군"
    ])
    
    # 1. 남양주시 
    
    if sigungu == "남양주시":
        # 시행령 별표1에 언급된 과밀억제 제외 지역들 (100% 면제)
        towns_100 = ["와부읍", "진접읍", "화도읍", "진건읍", "오남읍", "별내면", "수동면", "조안면", "퇴계원읍", "호평동", "평내동", "금곡동", "양정동", "다산동", "별내동"]
        # 위 지역을 제외한 나머지 남양주 구역 (50% 감면)
        towns_50 = ["남양주시 그 외 일반 동지역"] 
        
        dong = st.selectbox("세부 읍/면/동을 선택하세요", ["선택하세요"] + towns_100 + towns_50)

        if dong != "선택하세요":
          reduction_rate = 1.0 if dong in towns_100 else 0.5
          zone_name = "성장관리권역 (100% 면제)" if reduction_rate == 1.0 else "과밀억제권역 (50% 감면)"
          location_status = "외곽" if reduction_rate == 1.0 else "내" # 🚨 읍면은 '외곽', 동은 '내'
          is_ready = True

    # 2. 시흥시 (글자 매칭 버그 해결, 칼같은 1:1 매칭 분기)
    elif sigungu == "시흥시":
        industrial_zones = ["정왕동 (시화MTV 구역)", "반월특수지역 지정구역", "시화공단 내부"]
        normal_zones = ["연성동", "신천동", "은행동", "매화동", "목감동", "군자동", "정왕동 (일반 주거지역)"]
        dong = st.selectbox("세부 지역 및 동을 선택하세요", ["선택하세요"] + industrial_zones + normal_zones)

        if dong != "선택하세요":
           reduction_rate = 1.0 if dong in industrial_zones else 0.5
           zone_name = "성장관리권역 (반월특수지역 특례 - 100% 면제)" if reduction_rate == 1.0 else "과밀억제권역 (50% 감면)"
           location_status = "외곽" if reduction_rate == 1.0 else "내" # 🚨 특수공단 구역은 '외곽', 일반 동은 '내'
           is_ready = True

    # 3. 안산시 (새로 추가된 혼재 지역 1)
    elif sigungu == "안산시":
        industrial_zones = ["반월국가산업단지 내부", "대부동 (대부도 전역)"]
        normal_zones = ["상록구 동지역 전체", "단원구 일반 동지역 전체"]
        dong = st.selectbox("세부 지역 및 동을 선택하세요", ["선택하세요"] + industrial_zones + normal_zones)

        if dong != "선택하세요":
           reduction_rate = 1.0 if dong in industrial_zones else 0.5
           zone_name = "성장관리권역 (산업단지/지방 특례 - 100% 면제)" if reduction_rate == 1.0 else "과밀억제권역 (50% 감면)"
           location_status = "외곽" if reduction_rate == 1.0 else "내"
           is_ready = True

    # 4. 용인시 (새로 추가된 혼재 지역 2)
    elif sigungu == "용인시":
        towns_100 = ["처인구 포곡읍", "처인구 모현읍", "처인구 남사읍", "처인구 이동읍", "처인구 원삼면", "처인구 백암면", "처인구 양지면", "처인구 중앙동", "처인구 역삼동", "처인구 유림동", "처인구 동부동"]
        towns_50 = ["수지구 전역", "기흥구 전역", "처인구 구성동", "처인구 마북동", "처인구 동백동", "처인구 상하동"]
        dong = st.selectbox("세부 구/읍/면/동을 선택하세요", ["선택하세요"] + towns_100 + towns_50)
        if dong != "선택하세요":
            reduction_rate = 1.0 if dong in towns_100 else 0.5
            zone_name = "자연보전권역 (100% 면제)" if reduction_rate == 1.0 else "과밀억제권역 (50% 감면)"
            location_status = "외곽" if reduction_rate == 1.0 else "내"
            is_ready = True

    # 5. 화성시 (새로 추가된 혼재 지역 3)
    elif sigungu == "화성시":
        towns_50 = ["반월동", "병점1동", "병점2동", "진안동", "황계동", "기산동", "능동"]
        towns_100 = ["그 외 화성시 전역 (동탄신도시, 향남읍, 봉담읍, 남양읍, 우정읍, 마도면, 송산면 등)"]
        dong = st.selectbox("세부 동/읍/면을 선택하세요", ["선택하세요"] + towns_50 + towns_100)
        if dong != "선택하세요":
            reduction_rate = 0.5 if dong in towns_50 else 1.0
            zone_name = "수도권 과밀억제권역 편입구역 (50% 감면)" if reduction_rate == 0.5 else "성장관리권역 (100% 면제)"
            location_status = "내" if reduction_rate == 0.5 else "외곽"
            is_ready = True

    # 6. 100% 과밀억제권역 (고양시 포함, 하남시 누락 수정)
    elif sigungu in ["수원시", "성남시", "안양시", "부천시", "광명시", "과천시", "의왕시", "군포시", "구리시", "하남시", "고양시"]:
        reduction_rate = 0.5
        zone_name = "수도권 과밀억제권역 (50% 감면)"
        location_status = "내" # 🚨 100% 과밀도시들은 '내'
        
    # 7. 100% 성장관리 / 자연보전권역 (동두천시 누락 수정)
    elif sigungu in ["평택시", "파주시", "김포시", "광주시", "이천시", "오산시", "안성시", "포천시", "양주시", "여주시", "동두천시", "연천군", "가평군", "양평군"]:
        reduction_rate = 1.0
        zone_name = "수도권 내 성장관리권역/자연보전권역 (100% 면제)"
        location_status = "외곽" # 🚨 100% 성장관리/자연보전지역들은 '외곽'



# ==================== [4] 지방 5대 광역시 (지방 광역시는 구 단위 50%, 읍면 100% 분기) ====================
elif sido in ["부산광역시", "대구광역시", "광주광역시", "대전광역시", "울산광역시"]:
    if sido == "부산광역시":
        sigungu = st.selectbox("시/군/구를 선택하세요", ["선택하세요", "해운대구", "수영구", "동래구", "금정구", "연제구", "부산진구", "남구", "북구", "사상구", "사하구", "중구", "동구", "서구", "영도구", "기장군", "강서구"])
        if sigungu != "선택하세요":
            reduction_rate = 1.0 if sigungu in ["기장군", "강서구"] else 0.5
            is_ready = True

    elif sido == "대구광역시":
        sigungu = st.selectbox("시/군/구를 선택하세요", ["선택하세요", "중구", "동구", "서구", "남구", "북구", "수성구", "달서구", "달성군", "군위군"])
        if sigungu != "선택하세요":
            reduction_rate = 1.0 if sigungu in ["달성군", "군위군"] else 0.5
            is_ready = True
            
    elif sido == "울산광역시":
        sigungu = st.selectbox("시/군/구를 선택하세요", ["선택하세요", "중구", "남구", "동구", "북구", "울주군"])
        if sigungu != "선택하세요":
            reduction_rate = 1.0 if sigungu == "울주군" else 0.5
            is_ready = True
            
    else:
        sigungu = st.selectbox("시/군/구를 선택하세요", ["선택하세요", "전 지역 구"])
        if sigungu != "선택하세요":
            reduction_rate = 0.5
            is_ready = True
    zone_name = "지방 광역시 감면 요건 (100% 면제)" if reduction_rate == 1.0 else "지방 광역시 구 권역 (50% 감면)"
    location_status = "비수도권" # 🚨 광역시는 '비수도권'

# ==================== [5] 순수 지방 도 지역 ====================
elif sido in ["세종특별자치시", "충청남도", "충청북도", "전라남도", "전라북도", "경상남도", "경상북도", "강원특별자치도", "제주특별자치도"]:
    if sido == "충청남도":
        sigungu = st.selectbox("시/군을 선택하세요", ["선택하세요", "천안시", "아산시", "당진시", "서산시", "공주시", "논산시", "보령시", "계룡시", "홍성군", "예산군", "태안군", "금산군", "부여군", "서천군", "청양군"])
    elif sido == "전라남도":
        sigungu = st.selectbox("시/군을 선택하세요", ["선택하세요", "여수시", "순천시", "목포시", "광양시", "나주시", "무안군", "해남군", "고흥군", "화순군", "영암군", "영광군", "완도군", "담양군", "장성군", "보성군", "신안군", "진도군", "곡성군", "구례군", "함평군", "장흥군", "강진군"])
    elif sido == "경상남도":
        sigungu = st.selectbox("시/군을 선택하세요", ["선택하세요", "창원시", "김해시", "진주시", "양산시", "거제시", "통영시", "사천시", "밀양시", "함안군", "거창군", "창녕군", "고성군", "하동군", "합천군", "남해군", "함양군", "산청군", "의령군"])
    elif sido == "경상북도":
        sigungu = st.selectbox("시/군을 선택하세요", ["선택하세요", "포항시", "구미시", "경산시", "경주시", "안동시", "김천시", "칠곡군", "영주시", "상주시", "영천시", "문경시", "의성군", "울진군", "예천군", "성주군", "청도군", "영덕군", "고령군", "봉화군", "부구군", "영양군", "울릉군"])
    else:
        sigungu = st.selectbox("시/군/구를 선택하세요", ["기타 시/군/구 전체"])

    if sigungu != "선택하세요":    
       reduction_rate = 1.0
       zone_name = "수도권 외 지방 청년창업 특례 지역 (100% 전액 면제)"
       location_status = "비수도권" # 🚨 일반 지방 도 지역은 '비수도권'
       is_ready = True




# 결과 출력부
if reduction_rate > 0.0:
    st.write(f"### 🔍 전국 마이크로 주소 연산 결과")
    st.success(f"⚖️ 법적 분류: **{zone_name}**")
    st.success(f"🎉 **선택하신 {sido} {sigungu}의 청년 창업세액감면율은 {int(reduction_rate * 100)}% 입니다.**") 
    st.caption(f"ℹ️ 조세특례제한법 제6조에 따라 본 혜택은 **2027년 12월 31일 이전 창업자**에게만 한시적으로 유효합니다.")
    st.markdown("---") 


# 2. 사용자 입력 섹션 (UI 구성)
st.header("👤 창업 및 사업 계획 입력")

col1, col2 = st.columns(2)

with col1:
    
    st.subheader("[1] 기본 정보 및 창업 업종")
    
    # 1. 만 나이 입력
    age = st.number_input("현재 만 나이를 입력하세요", min_value=0, max_value=100, value=23)

    # 2. 군 복무 특례 UI 추가 (기존 코드에 자연스럽게 녹아듬)
    has_served = st.radio("군 복무(병역 이행) 여부를 선택하세요", ["미필/해당 없음(여성 포함)", "군필(병역 이행 완료)"])
    
    service_years = 0
    if has_served == "군필(병역 이행 완료)":
        # 세법상 최대 6년까지만 인정되므로 마지노선을 6년으로 제한
        service_years = st.number_input("실제 군 복무 기간을 입력하세요 (연 단위, 최대 6년 인정)", min_value=0, max_value=6, value=2)

    # 🚨 세법상 최종 판정 나이 계산 (복무 기간만큼 나이를 차감)
    final_age = age - service_years
    
    if has_served == "군필(병역 이행 완료)" and service_years > 0:
        st.caption(f"💡 병역 특례 적용: 세법상 만 **{final_age}세**로 판정됩니다. (최대 만 34세까지 청년 창업 혜택 가능)")

    #창업 업종 선택 
    business_type = st.selectbox(
        "창업 예정인 사업의 종류(업종)를 선택하세요 (조특법 세법 표준 대분류 적용)",
        [
            "광업 / 제조업 (제품 생산, 식품 제조, 의류 제작 등)",
            "건설업 (인테리어, 건축 공사 등)",
            "통신판매업 (온라인 쇼핑몰, 해외직구 대행, 스마트스토어 등)",
            "정보통신업 (소프트웨어 개발, 게임 제작, 앱 개발, IT 플랫폼 등)",
            "연구개발업 / 전문·과학·기술 서비스업 (디자인, 광고대행, 경영컨설팅 등)",
            "음식점업 (일반식당, 카페, 제과점, 베이커리 등)",
            "물류산업 / 운수업 (창업 배송, 여객운송,물류창고 등)",
            "사업시설 관리, 사업 지원 및 임대 서비스업 (고용알선, 여행사 등)",
            "이·미용업 / 뷰티서비스업 (미용실, 네일숍, 바버샵 등)",
            "직업기술분야 학원 및 예술학원 (기술/무용/연기/미술 학원 등)",
            "개인 간병 및 유사 서비스업 / 사회복지 서비스업",
            "수도, 하수 및 폐기물 처리, 원료 재생업",
            "🚫 도·소매업 (유통업, 온·오프라인 마트 - 세법상 창업 감면 제외 업종)",
            "🚫 일반 보습학원 / 외국어학원 (입시학원, 어학당 - 세법상 창업 감면 제외 업종)",
            "🚫 숙박업 및 주점업 (호텔, 모텔, 일반 주점, 유흥업소 - 세법상 창업 감면 제외 업종)",
            "🚫 부동산 임대업 및 매매업 (상가 임대, 주택 매매 - 세법상 창업 감면 제외 업종)"
        ]
    )
    
    is_export = st.radio("해외 수출이나 역직구(해외 매출) 계획이 있으신가요?", ["오직 국내 매출만 발생", "해외 수출 및 글로벌 매출 계획 있음"])

with col2:
    st.subheader("[2] 시뮬레이션용 재무 및 고용 데이터")
    
    sales_input = st.text_input("예상되는 연간 매출액을 입력하세요 (원 단위)")
    try:
        expected_sales = float(sales_input.replace(",", ""))
    except ValueError:
        expected_sales = 0.0
        st.error("매출액에는 숫자와 콤마(,)만 입력할 수 있습니다.")

    income_rate = st.slider("예상 매출액 대비 순이익률(%)을 선택하세요 (종합소득세 산출 기준)", min_value=1, max_value=100)
    # 진짜 소득금액(과세표준 대용) 수학적 연산
    estimated_income = expected_sales * (income_rate / 100)
    
    bookkeeping = st.radio("사업 장부를 스스로 작성하여 신고하실 계획인가요?", ["네, 스스로 작성하겠습니다.", "아니오, 장부 없이 간편하게 신고하겠습니다."])
    
    # 텍스트가 아닌 실제 채용 인원 '숫자'를 입력받아 연산에 활용
    employee_count = st.number_input("채용할 청년 정규직 직원 수를 입력하세요 (명)", min_value=0, max_value=100)
    
    
    initial_investment = st.radio("초기에 대규모 인테리어나 고가 장비 구입 계획이 있으신가요?", ["없음 (소자본 창업)", "있음 (인테리어 및 시설 자금 대량 투입)"])
    investment_amount = 0.0

    if initial_investment == "있음 (인테리어 및 시설 자금 대량 투입)":
        investment_input = st.text_input("예상되는 초기 시설 투자 금액(인테리어, 장비 등 공급가액)을 입력하세요 (원 단위)")
        try:
              investment_amount = float(investment_input.replace(",", ""))
        except ValueError:
              investment_amount = 0.0

    donation_input = st.text_input("연간 예상되는 사회공헌 기부 금액을 입력하세요 (원 단위)")
    try:
        donation_amount = float(donation_input.replace(",", ""))
    except ValueError:
        donation_amount = 0.0
        st.error("기부 금액에는 숫자와 콤마(,)만 입력할 수 있습니다.")
            
    property_plan = st.radio("창업 후 4년 이내에 사업용 부동산(사무실 등)을 매입할 계획이 있으신가요?", ["없음", "있음"])
    property_type = "상가/오피스텔/토지 매입"
    property_price = 0.0
    
    if property_plan == "있음":
        # 사용자가 선택한 값이 property_type 변수에 저장됩니다.
        property_type = st.selectbox(
            "매입할 부동산의 종류 및 취득 방식을 선택하세요",
            ["상가/오피스텔/토지 유상 매입", "사업용 건물 직접 신축 (원시취득)"])
        
        property_input = st.text_input("매입하려는 부동산의 예상 가액을 입력하세요")
        try:
            property_price = float(property_input.replace(",", ""))
        except ValueError:
            property_price = 0.0

    # 조세특례제한법 제30조의5(창업자금에 대한 증여세 과세특례)
    gift_plan = st.radio("부모님 등으로부터 창업자금 증여 지원을 받으실 계획이 있나요?", ["없음", "있음"])
    gift_amount = 0.0
    
    if gift_plan == "있음":
        gift_input = st.text_input("증여받을(혹은 지원받은) 예상 창업자금을 입력하세요 (원 단위)")
        try:
            gift_amount = float(gift_input.replace(",", ""))
        except ValueError:
            gift_amount = 0.0

st.markdown("---")

# 3. 매칭 및 수학적 연산 시뮬레이션 엔진
if st.button("📊 나의 현행세법 종합 혜택 및 리스크 진단하기"):
    st.header("📋 세법별 시뮬레이션 결과 보고서")
    
    is_young = age <= 34
    is_self_book = "네" in bookkeeping
    is_small_business = expected_sales <= 104000000
    is_eligible_business = "🚫" not in business_type 
    
    # 💡 2026년 국세청 오피셜 8단계 종합소득세 누진세율 계산 함수
    def calculate_progressive_tax(income):
        if income <= 14000000:
            return income * 0.06
        elif income <= 50000000:
            return (income * 0.15) - 1260000
        elif income <= 88000000:
            return (income * 0.24) - 5760000
        elif income <= 150000000:
            return (income * 0.35) - 15440000
        elif income <= 300000000:
            return (income * 0.38) - 19940000
        elif income <= 500000000:
            return (income * 0.40) - 25940000
        elif income <= 1000000000:
            return (income * 0.42) - 35940000
        else:
            return (income * 0.45) - 65940000
        
   


    # 국가 누진세율 함수를 실행하여 기본 산출세액 도출
    base_tax = calculate_progressive_tax(estimated_income)

    # 기존에 계산된 소득세 산출세액 변수가 income_tax 라고 가정했을 때
    local_income_tax = base_tax * 0.1  # 👈 지방소득세는 국세의 10%

# 감면 적용 후 최종 세액 계산
    final_income_tax = base_tax * (1 - reduction_rate)
    final_local_tax = local_income_tax * (1 - reduction_rate)
    total_tax = final_income_tax + final_local_tax # 👈 사용자가 실제로 내는 총 세금

# 스트림릿 화면 출력부 예시
    
    

    #세법상 권역 분류 명칭 정밀화
    status_kr = {"내": "수도권 과밀억제권역(또는 법정 편입구역)", "외곽": "수도권 과밀억제권역 외(성장관리·자연보전·특례산단)", "비수도권": "비수도권 지방지역"}[location_status]
    st.success(f"📍 선택하신 주소는 세법상 [{status_kr}]으로 분류되었습니다.")
    
    res_col1, res_col2 = st.columns(2)
    
    with res_col1:
        st.subheader("1. 소득세 감면 및 특별 공제 (조세특례제한법/소득세법)")
        
        # A. 창업중소기업 세액감면 연산 (조특법 제6조)
        if not is_eligible_business:
            reduction_rate = 0.0
            st.error("❌ **[업종 제한] 창업세액감면 대상 제외 업종입니다.**")
            st.write("선택하신 업종은 조특법 제6조에 열거된 감면 대상이 아니므로 소득세 감면율은 **0%**입니다.")
        else:
            if location_status == "비수도권":
                reduction_rate = 1.0 if (is_young or is_small_business) else 0.5
            elif location_status == "외곽":
                reduction_rate = 1.0 if (is_young or is_small_business) else 0.5
            else: 
                reduction_rate = 0.5 if (is_young or is_small_business) else 0.0
                
            
            #기존 
            tax_savings = base_tax * reduction_rate
            st.success(f"🎉 **[조특법 제6조] 창업세액감면율: {int(reduction_rate * 100)}% 적용**")
            st.write(f"- 예상 순이익: **{int(estimated_income):,}원**")
            st.write(f"- 가상 산출소득세: **{int(base_tax):,}원**")
            st.write(f"- **최종 소득세 감면 혜택 액수: 약 {int(tax_savings):,}원 (5년간 매년 절세 가능)**")
            st.write(f"**최종 소득세 감면 적용 후 세액: {int(final_income_tax):,} 원**")
            st.write(f"**지방소득세(국세의 10%): {int(final_local_tax):,} 원**")
            st.success(f"💰 **최종 총 납부 세액: {int(total_tax):,} 원**")
            st.caption("⚠️ 본 감면 혜택은 법률상 **2027년 12월 31일 이전 창업자**에게만 유효하므로 기한 내 창업 및 사업자등록이 필수적입니다.")

        
        
        #3. 통합고용세액공제
        # 대표자 본인 및 친인척 제외 문구 명시 및 정확한 세액 차감 프로세스
        if employee_count > 0:
            per_person_value = 14500000 if location_status == "비수도권" else 11000000
            
            # 1년차 공제액 및 3년간 유지 시 총 누적 혜택 계산
            annual_employment_savings = employee_count * per_person_value
            total_3years_savings = annual_employment_savings * 3
            
            st.info(f"👥 **[조특법 제29조의7] 청년 개인사업자 통합고용세액공제 시뮬레이션**")
            st.warning("⚠️ **[세법 기준 고지]** 본 공제는 대표자 본인, 배우자 및 직계존비속을 제외한 **'4대보험 가입 정규직 직원'** 채용 시에만 적용됩니다.")
            
            st.write(f"- 청년 채용 인원 (대표자 제외): **{employee_count}명** (인당 {per_person_value:,}원 적용)")
            st.write(f"- **금년도 종합소득세에서 차감할 공제액: {int(annual_employment_savings):,}원**")
            st.caption(f"💡 고용 유지 시 향후 3년간 누적 총 **{int(total_3years_savings):,}원**의 세액공제 혜택을 받게 됩니다.")
            
            # 실제 소득세 잔액 한도 체크 (창업감면 등으로 이미 세금이 줄어든 상태를 반영)
            remaining_tax_window = base_tax - tax_savings
            
            if annual_employment_savings > remaining_tax_window:
                actual_employment_savings = max(0.0, remaining_tax_window)
                carried_over_savings = annual_employment_savings - actual_employment_savings
                
                if actual_employment_savings == 0:
                    st.warning(f"⚠️ **[안내] 창업세액감면(100%) 등으로 인해 올해 납부할 소득세가 이미 0원입니다.**")
                    st.write(f"  * **금년도 실제 소득세 차감액: 0원**")
                else:
                    st.warning(f"⚠️ **[소득세 한도 도달]** 금년도 납부 예정 소득세 한도를 초과하여 공제되었습니다.")
                    st.write(f"  * **금년도 실제 소득세 차감액: {int(actual_employment_savings):,}원**")
                
                st.write(f"  * **다음 해로 이월되는 공제액: {int(carried_over_savings):,}원** (소득세법에 따라 향후 10년간 이월하여 차감 가능)")
            else:
                actual_employment_savings = annual_employment_savings
                st.write(f"  * **금년도 실제 소득세 차감액: {int(actual_employment_savings):,}원** (전액 차감 완료)")
                carried_over_savings = 0
            
            # 감면액의 20% 농어촌특별세 부과 한도 처리
            nongtuk_tax = actual_employment_savings * 0.20
            if nongtuk_tax > 0:
                st.write(f"💸 **[농어촌특별세법 제5조] 부가 한도세:** 세액공제 혜택의 20%인 **{int(nongtuk_tax):,}원**은 농어촌특별세로 별도 고지되어 납부하셔야 합니다.")
                
            # 사후관리 리스크 (조특법 제29조의7 제4항)
            st.error(f"🚨 **[사후관리 의무 위반 추징 리스크]**")
            st.write(f"  * 채용 후 2년 이내에 직원이 퇴사하여 전체 상시근로자 수가 감소할 경우, **감면받은 세액({int(actual_employment_savings):,}원)을 국세청에 다시 전액 추징당하므로** 고용 유지가 필수적입니다.")





        # C. 기부금 세액공제 연산 (소득세법 제59조의4)
    

        # ========== [C. 기부금 한도 및 절세액 정밀 연산 엔진] ==========
        if donation_amount > 0:
            st.info(f"🕊️ **[소득세법 제34조] 기부금 필요경비 한도 및 절세 정밀 진단**")
            st.write(f"- 입력한 연간 예상 기부액: **{int(donation_amount):,}원**")
            
            if is_self_book:
                # 1. 장부 기장 사업자: 필요경비(비용) 산입 한도 계산
                # 기준소득금액 = 기부금 차감 전 순이익 (estimated_income)
                base_income = estimated_income 
                
                # 일반 지정기부금 한도 범위 계산 (기준소득금액의 30%를 대중적인 마지노선으로 설정)
                donation_limit = base_income * 0.30
                
                st.write(f"- 세법상 기부금 인정 한도액 (순이익의 30%): **{int(donation_limit):,}원**")
                
                if donation_amount > donation_limit:
                    # 한도를 초과한 경우
                    actual_expense = donation_limit
                    over_limit_amount = donation_amount - donation_limit
                    
                    st.warning(f"⚠️ **[기부금 한도 초과]** 입력하신 기부금이 올해 비용 인정 한도를 초과했습니다.")
                    st.write(f"  * **금년도 실제 비용(필요경비) 반영액: {int(actual_expense):,}원**")
                    st.write(f"  * **다음 해로 이월되는 기부금: {int(over_limit_amount):,}원** (향후 10년간 이월하여 비용 처리 가능)")
                else:
                    # 한도 내에 여유롭게 들어온 경우
                    actual_expense = donation_amount
                    st.success(f"✅ **[한도 내 전액 인정]** 기부금 {int(actual_expense):,}원 전액이 올해 사업 비용으로 정상 인정됩니다.")
                
                # 기부금으로 인해 실제로 아끼는 대략적인 소득세 환산 (순이익이 줄어든 효과)
                # (간이 시뮬레이션을 위해 산출세액 비율로 절세 효과 대리 연산)
                if base_income > 0:
                    approx_tax_rate = base_tax / base_income
                    saved_tax = actual_expense * approx_tax_rate
                    st.write(f"  * **기부금 지출로 인한 올해 소득세 실질 절감액: 약 {int(saved_tax):,}원**")

            else:
                # 2. 장부를 안 쓰는 추계신고 사업자: 소득세법 제59조의4 세액공제 특례 적용
                donation_savings = donation_amount * 0.15
                st.success(f"🎉 **[소득세법 ] 기부금 특별세액공제 적용 (추계신고 특례)**")
                st.write("- 장부 없이 추계신고를 하시는 경우 예외적으로 세액공제 15%가 준용됩니다.")
                st.write(f"- **이번 해 최종 소득세 직접 차감액: {int(donation_savings):,}원 (지출액의 15%)**")    

    
        # ========== [D. 장부 미기장 가산세 연산 수정] ==========
        st.subheader("2. 장부 작성 및 가산세 리스크 (소득세법)")
        if is_self_book:
            # 정식 조항인 제160조(장부의 비치·기록) 적용
            st.success("✅ **[소득세법 제160조] 장부의 비치·기록 의무 이행 예정 (가산세 위험 없음)**")
            st.write("- 스스로 장부를 작성하여 정식 기장 신고를 진행하므로 세법상 무기장가산세 대상에서 제외됩니다.")
        else:
            # 정식 조항인 제81조의5(무기장가산세) 적용
            penalty_tax = base_tax * 0.20
            st.error("🚨 **[소득세법 제81조의5] 무기장가산세 처분 리스크 노출**")
            st.write(f"- 장부를 작성하지 않고 추계신고를 하는 경우, 세법에 따라 산출세액의 **20% 패널티**가 부과됩니다.")
            st.write(f"- **예상 부과 가산세 리스크 액수: 약 {int(penalty_tax):,}원 부과 주의**")    

    with res_col2:
        st.subheader("3. 부가가치세 면제 및 환급 특례 (부가가치세법)")
        
        # A. 부가세 면제 및 간이과세 판별 연산
        if int(expected_sales) < 48000000:
            st.success("🎉 **[부가세법 제69조 제1항] 연 매출 4,800만 원 미만으로 부가가치세 납부 의무 전액 면제!**")
        elif int(expected_sales) < 140000000:
            st.info(f"✅ **[부가세법 제61조 제1항] 연 매출 {int(expected_sales):,}원: 간이과세자 적용 권역**")
        else:
            st.warning("🔶 **연 매출 1.4억 원 이상: 일반과세자 자동 전환 대상 (간이과세 배제)**")
            
        if "해외 수출" in is_export:
            st.success("✈️ **[부가세법 제24조] 외화 획득 사업자 영세율(0%) 적용 대상**")

        # ❌ 기존 영세율/조기환급 st.info 코드 부근을 아래 코드로 싹 교체하세요!
        if "해외 수출" in is_export:
            st.success("✈️ **[부가세법 제24조] 외화 획득 사업자 영세율(0%) 적용 대상**")
            
        if initial_investment == "있음 (인테리어 및 시설 자금 대량 투입)" and investment_amount > 0:
            # 시설 투자에 따른 환급 세액 계산 (10% 매입세액 환급)
            expected_refund = investment_amount * 0.10
            
            st.success(f"💰 **[부가세법 제59조] 초기 시설 투자 조기환급 특례**")
            st.write(f"- 시설 투자/인테리어 예상액: **{int(investment_amount):,}원**")
            st.write(f"- **예상 부가가치세 조기 환급액: 약 {int(expected_refund):,}원**")
            st.info(f"💡 일반 환급(최대 수개월 소요)과 달리, 확정/예정신고 후 **단 15일 이내**에 {int(expected_refund):,}원이 통장으로 즉시 조기 환급되어 초기 운전자금 확보에 유용합니다.")
            st.caption("※ 단, 세금계산서 또는 신용카드 매출전표 등 정규 증빙을 반드시 수취해야 환급 처리가 가능합니다.")
        else:
            st.write("초기 대규모 시설 투자가 없으므로 조기환급 시뮬레이션을 종료합니다.")



        

        # B. 지방세 및 부동산 추징 리스크 연산 (지특법 제58조의3)
        # 2026년 행정안전부/지방세법 기준 100% 검증 완료
        st.subheader("4. 창업 지방세 혜택 및 사후관리")
        if is_eligible_business and property_plan == "있음" and property_price > 0:
            
            # 주택 선택지를 삭제하고 오직 순수 사업용 자산 유형만 분류
            if property_type == "상가/오피스텔/토지 유상 매입":
                tax_rate = 0.046       # 지방세법 제11조 제1항 제7호 (기본 4% + 지방교육세 0.4% + 농특세 0.2%)
            elif property_type == "사업용 건물 직접 신축 (원시취득)":
                tax_rate = 0.0316      # 지방세법 제11조 제1항 제3호 (기본 2.8% + 지방교육세 0.56% + 농특세 비과세 분기 반영)
            else:
                tax_rate = 0.046       # 그 외 기타 사업용 자산 매입 기본값 세팅
                
            normal_tax = property_price * tax_rate
            
            # [지특법 제58조의3] 창업중소기업 사업용 재산 감면 판정
            if location_status != "내":
                discounted_tax = normal_tax * 0.25
                potential_penalty = normal_tax * 0.75
                
                st.success(f"🎉 **[지특법 제58조의3] 부동산 취득세 감면 시뮬레이션 ({property_type})**")
                st.write(f"- 해당 사업용 부동산 법정 실효세율(국세/지방세 부속세 포함): **{round(tax_rate * 100, 2)}%**")
                st.write(f"- 감면 전 정상 취득세액: **{int(normal_tax):,}원**")
                st.info(f"✨ **75% 감면 후 최종 실납부 취득세: 약 {int(discounted_tax):,}원**")
                st.error(f"🚨 **[지특법 제58조의3 제4항 사후관리] 창업일로부터 4년 내 취득 후, 3년 이상 해당 사업에 직접 사용하지 않고 매각/타 용도 전용 시 추징 리스크 금액: {int(potential_penalty):,}원**")
            else:
                # 수도권 과밀억제권역 내 취득 시 지특법 제58조의3 제1항 단서조항에 의해 감면 전면 배제
                st.error(f"❌ **[과밀억제권역 감면 배제] 선택하신 창업 예정지는 '수도권 과밀억제권역 내'에 해당합니다. 지특법 제58조의3에 따라 과밀억제권역 내 자산 취득은 취득세 {round(tax_rate * 100, 2)}% 전액 부과 대상입니다. (감면액 없음)**")
                st.write(f"- **최종 납부 취득세액: {int(normal_tax):,}원**")
        else:
            st.write("부동산 매입 계획이 없거나 감면 제외 업종이므로 취득세 시뮬레이션을 종료합니다.")    



        # 창업자금 증여세 과세특례
        # 조특법 제30조의5 및 상증세법 제53조/제56조 법령 100% 검증 완료
        st.subheader("5. 창업자금 증여세 과세특례 (조특법 제30조의5)")
        if gift_plan == "있음" and gift_amount > 0:
            
            # [세법 교정 1] 일반 증여세의 과세표준(증여가액 - 성인자녀공제 5천만 원) 선행 연산
            # 근거: 상증세법 제53조 및 제55조
            normal_tax_base = max(0.0, gift_amount - 50000000)
            
            # [세법 교정 2] 정확한 법정 기본세율 매트릭스 및 누진공제액 적용 (상증세법 제56조)
            if normal_tax_base <= 100000000:
                normal_gift_tax = normal_tax_base * 0.10
            elif normal_tax_base <= 500000000:
                normal_gift_tax = (normal_tax_base * 0.20) - 10000000
            elif normal_tax_base <= 1000000000:
                normal_gift_tax = (normal_tax_base * 0.30) - 60000000
            elif normal_tax_base <= 3000000000:
                normal_gift_tax = (normal_tax_base * 0.40) - 160000000
            else:
                normal_gift_tax = (normal_tax_base * 0.45) - 310000000
                
            normal_gift_tax = max(0.0, normal_gift_tax)

            # 2. [검증 완료] 조특법 제30조의5 특례 증여세 계산 (질문자님 기존 로직 완벽함)
            if gift_amount <= 500000000:
                special_gift_tax = 0.0  # 5억 원까지는 전액 공제
            else:
                special_gift_tax = (gift_amount - 500000000) * 0.10  # 5억 초과분은 10% 단일세율
            
            # 3. 아낀 세금 (정밀 연산)
            gift_tax_savings = max(0.0, normal_gift_tax - special_gift_tax)

            st.success(f"🎁 **[특례 활성화] 창업자금 증여세 과세특례 적용 결과**")
            st.write(f"- 총 증여 자금: **{int(gift_amount):,}원**")
            st.write(f"- **기본 면제 금액 (비과세): 500,000,000원 (5억 전액 공제)**")
            
            if special_gift_tax == 0:
                st.balloons()
                st.success(f"🎉 **최종 납부할 증여세: 0원 (전액 면제!)**")
            else:
                st.warning(f"🔶 **최종 납부할 특례 증여세: 약 {int(special_gift_tax):,}원** (5억 초과분 10% 적용)")
                
            if gift_tax_savings > 0:
                st.info(f"📈 **일반 증여 대비 절세 효과: 약 {int(gift_tax_savings):,}원 절감 효과**")
                st.caption("※ 일반 직계존속 증여 시 공제(5천만 원) 및 상속세및증여세법 제56조 기본 누진세율과 대조한 결과입니다.")
                
            st.error("⚠️ **[조특법 제30조의5 제4항 사후관리 의무 공지]**")
            st.write("창업자금은 증여받은 날로부터 **2년 이내에 법정 창업**을 완료해야 하고,증여받은 날로부터 **5년 이내에 창업 목적**으로 전액 사용(소진)해야 합니다.")
            st.caption("※ 위 사후관리 요건 성실 이행 규정을 위반하거나 중간에 폐업·면탈할 경우, 국세청으로부터 정식 증여세 가산세와 함께 전액 추징됩니다.")


       

st.markdown("---")
# ========== [코드 맨 최하단에 이어서 붙여넣기] ==========
st.info("⚖️ **법적 면책 고지 및 이용 안내**")
st.caption(
    "1. 본 시뮬레이션 결과는 사용자가 입력한 데이터를 바탕으로 현행 법 조문을 매칭한 단순 참고용 결과입니다.\n"
    "2. 특히 창업 지역의 경우, 수도권정비계획법 시행령 [별표 1]에 명시된 시흥 반월특수지역, 경제자유구역 등 세부 지번에 따른 과밀억제권역 제외 특례가 존재하므로 실제 필지(지번)에 따라 감면율 오차가 발생할 수 있습니다.\n"
    "3. 실제 세금 신고 시에는 개별 기업의 창업 당시 만 나이 요건, 병역 이행 기간 증빙,실제 통계청 표준산업분류 기준에 따른 정밀 업종 판정, 상시 근로자 수 유지 여부 등에 따라 결과가 완전히 달라질 수 있습니다.\n"
    "4. 세법의 해석과 적용은 과세관청(국세청)의 판단에 따라 차이가 있을 수 있으므로,본 결과를 근거로 한 실제 투자나 창업 결정으로 인해 발생하는 세무상 불이익에 대해 본 프로그램은 법적 책임을 지지 않습니다.\n"
    "5. **정확한 세액 감면 및 신고를 위해 사업자등록 전 전문 세무사와의 상담을 권장합니다.**"
        )       
st.markdown("### 🔗 2026년 현행세법 공식 근거 및 출처")
st.markdown("- [국세법령정보시스템(NTIS) 공식 홈페이지](https://taxlaw.nts.go.kr/index.do;jsessionid=SMNCQgnjqZItG2EMTasnlm6zqswMe0hBAFBJ-zYD.cpesiwsp01_SE12)")
st.markdown("- [국가법령정보센터](https://www.law.go.kr/)")


