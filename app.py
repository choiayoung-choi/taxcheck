import streamlit as st

# 1. 페이지 기본 설정 및 타이틀 세팅 (정직하고 신뢰감 있는 타이틀로 변경)
st.set_page_config(page_title="Tax-Check: 청년창업 세법 시뮬레이터", layout="wide")
st.title("🚀 Tax-Check: 예비 청년사업자 창업세액감면 및 재무 시뮬레이터")
st.caption("📊 정부 조세특례제한법 제6조 및 현행세법 반영")

st.info("### 📌 사용자가 입력한 사업 계획 데이터를 기반으로 실제 세액 감면 및 리스크 금액을 연산합니다.")

# -------------------------------------------------------------------------
# [원천 데이터] 대한민국 행정구역 세법 권역 매핑 데이터베이스 (3단계 권역 완벽 반영)
# -------------------------------------------------------------------------
REGION_DATA = {
    "서울특별시": {
        "districts": [
            "강남구", "강동구", "강북구", "강서구", "관악구", "광진구", "구로구", "금천구", 
            "노원구", "도봉구", "동대문구", "동작구", "마포구", "서대문구", "서초구", "성동구", 
            "성북구", "송파구", "양천구", "영등포구", "용산구", "은평구", "종로구", "중구", "중랑구"
        ], 
        "default_zone": "내"
    },
    "인천광역시": {
        "districts": [
            "중구 (원도심 과밀권역)", "동구 (원도심 과밀권역)", "미추홀구 (원도심 과밀권역)", 
            "연수구 (송도국제도시 제외)", "남동구 (전 지역 과밀권역)", "부평구 (전 지역 과밀권역)", 
            "계양구 (전 지역 과밀권역)", "서구 (외곽 제외 검단·청라 외 지역)",
            "강화군 (수도권 외곽지 특례지역)", "옹진군 (수도권 외곽지 특례지역)", 
            "서구 (대곡동/불로동/마전동/금곡동/오류동/왕길동/당하동/원당동)", 
            "송도국제도시 (경제자유구역 특례)", "청라국제도시 (경제자유구역 특례)", "영종국제도시 (경제자유구역 특례)"
        ],
        "mapping": {
            "중구 (원도심 과밀권역)": "내", "동구 (원도심 과밀권역)": "내", "미추홀구 (원도심 과밀권역)": "내", 
            "연수구 (송도국제도시 제외)": "내", "남동구 (전 지역 과밀권역)": "내", "부평구 (전 지역 과밀권역)": "내", 
            "계양구 (전 지역 과밀권역)": "내", "서구 (외곽 제외 검단·청라 외 지역)": "내",
            "강화군 (수도권 외곽지 특례지역)": "외곽", "옹진군 (수도권 외곽지 특례지역)": "외곽", 
            "서구 (대곡동/불로동/마전동/금곡동/오류동/왕길동/당하동/원당동)": "외곽", 
            "송도국제도시 (경제자유구역 특례)": "외곽", "청라국제도시 (경제자유구역 특례)": "외곽", "영종국제도시 (경제자유구역 특례)": "외곽"
        },
        "default_zone": "내"
    },
    "경기도": {
        "districts": [
            "수원시 (장안구/권선구/팔달구/영통구)", "성남시 (수정구/중원구/분당구)", "고양시 (덕양구/일산동구/일산서구)", 
            "부천시 (원미구/소사구/오정구)", "안양시 (만안구/동안구)", "의왕시 (전 지역 과밀)", "군포시 (전 지역 과밀)", 
            "구리시 (전 지역 과밀)", "광명시 (전 지역 과밀)", "하남시 (전 지역 과밀)",
            "화성시 (동탄신도시 / 병점 / 진안 등 과밀 핵심지)", 
            "화성시 (동탄 외 남양/향남/봉담/우정/마도/송산/서신/팔탄/장안/양감/정남)", 
            "남양주시 (다산/호평/평내/금곡/일패/이패/삼패/수석/양정동)", 
            "남양주시 (와부읍/진접읍/화도읍/진건읍/오남읍/퇴계원읍/별내면/수동면/조안면/별내동)", 
            "시흥시 (대야/계수/은행/안현/매화/도창/금이/물왕/산현/조남/논곡/목감/포동/정왕동 일부)", 
            "시흥시 (시화MTV / 반월특구 / 정왕동 대부도 인근 공단지역)", 
            "안산시 (상록구/단원구 공단 제외 전 지역)", 
            "안산시 (단원구 원시동/목내동/성곡동 및 상록구 사동 일부 공단지역)",
            "광주시 (경안/쌍령/송정/탄벌/광남동 및 오포읍 일부 과밀지역)",
            "광주시 (초월읍/곤지암읍/도척면/퇴촌면/남종면/남한산성면)",
            "용인시 처인구", "용인시 기흥구", "용인시 수지구", "평택시", "파주시", "김포시", "안성시", 
            "오산시", "이천시", "포천시", "여주시", "양주시", "동두천시", "연천군", "가평군", "양평군"
        ],
        "mapping": {
            "수원시 (장안구/권선구/팔달구/영통구)": "내", "성남시 (수정구/중원구/분당구)": "내", "고양시 (덕양구/일산동구/일산서구)": "내", 
            "부천시 (원미구/소사구/오정구)": "내", "안양시 (만안구/동안구)": "내", "의왕시 (전 지역 과밀)": "내", "군포시 (전 지역 과밀)": "내", 
            "구리시 (전 지역 과밀)": "내", "광명시 (전 지역 과밀)": "내", "하남시 (전 지역 과밀)": "내",
            "화성시 (동탄신도시 / 병점 / 진안 등 과밀 핵심지)": "내", 
            "화성시 (동탄 외 남양/향남/봉담/우정/마도/송산/서신/팔탄/장안/양감/정남)": "외곽", 
            "남양주시 (다산/호평/평내/금곡/일패/이패/삼패/수석/양정동)": "내", 
            "남양주시 (와부읍/진접읍/화도읍/진건읍/오남읍/퇴계원읍/별내면/수동면/조안면/별내동)": "외곽", 
            "시흥시 (대야/계수/은행/안현/매화/도창/금이/물왕/산현/조남/논곡/목감/포동/정왕동 일부)": "내", 
            "시흥시 (시화MTV / 반월특구 / 정왕동 대부도 인근 공단지역)": "외곽", 
            "안산시 (상록구/단원구 공단 제외 전 지역)": "내", 
            "안산시 (단원구 원시동/목내동/성곡동 및 상록구 사동 일부 공단지역)": "외곽",
            "광주시 (경안/쌍령/송정/탄벌/광남동 및 오포읍 일부 과밀지역)": "내",
            "광주시 (초월읍/곤지암읍/도척면/퇴촌면/남종면/남한산성면)": "외곽",
            "용인시 처인구": "외곽", "용인시 기흥구": "외곽", "용인시 수지구": "외곽", "평택시": "외곽", "파주시": "외곽", 
            "김포시": "외곽", "안성시": "외곽", "오산시": "외곽", "이천시": "외곽", "포천시": "외곽", "여주시": "외곽", 
            "양주시": "외곽", "동두천시": "외곽", "연천군": "외곽", "가평군": "외곽", "양평군": "외곽"
        },
        "default_zone": "외곽"
    },
    "강원특별자치도": {
        "districts": ["춘천시", "원주시", "강릉시", "동해시", "태백시", "속초시", "삼척시", "홍천군", "횡성군", "영월군", "평창군", "정선군", "철원군", "화천군", "양구군", "인제군", "고성군", "양양군"],
        "default_zone": "비수도권"
    },
    "충청북도": {
        "districts": ["청주시 상당구", "청주시 서원구", "청주시 흥덕구", "청주시 청원구", "충주시", "제천시", "보은군", "옥천군", "영동군", "증평군", "진천군", "괴산군", "음성군", "단양군"],
        "default_zone": "비수도권"
    },
    "충청남도": {
        "districts": ["천안시 동남구", "천안시 서북구", "공주시", "보령시", "아산시", "서산시", "논산시", "계룡시", "당진시", "금산군", "부여군", "서천군", "청양군", "홍성군", "예산군", "태안군"],
        "default_zone": "비수도권"
    },
    "전북특별자치도": {
        "districts": ["전주시 완산구", "전주시 덕진구", "군산시", "익산시", "정읍시", "남원시", "김제시", "완주군", "진안군", "무주군", "장수군", "임실군", "순창군", "고창군", "부안군"],
        "default_zone": "비수도권"
    },
    "전라남도": {
        "districts": ["목포시", "여수시", "순천시", "나주시", "광양시", "담양군", "곡성군", "구례군", "고흥군", "보성군", "화순군", "장흥군", "강진군", "해남군", "영암군", "무안군", "함평군", "영광군", "장성군", "완도군", "진도군", "신안군"],
        "default_zone": "비수도권"
    },
    "경상북도": {
        "districts": ["포항시 남구", "포항시 북구", "경주시", "김천시", "안동시", "구미시", "영주시", "영천시", "상주시", "문경시", "경산시", "군위군", "의성군", "청송군", "영양군", "영덕군", "청도군", "고령군", "성주군", "칠곡군", "예천군", "봉화군", "울진군", "울릉군"],
        "default_zone": "비수도권"
    },
    "경상남도": {
        "districts": ["창원시 의창구", "창원시 성산구", "창원시 마산합포구", "창원시 마산회원구", "창원시 진해구", "진주시", "통영시", "사천시", "김해시", "밀양시", "거제시", "양산시", "의령군", "함안군", "창녕군", "고성군", "남해군", "하동군", "산청군", "함양군", "거창군", "합천군"],
        "default_zone": "비수도권"
    },
    "지방 대도시 및 특별자치시": {
        "districts": ["부산광역시 (전 구 군)", "대구광역시 (전 구 군)", "대전광역시 (전 구 군)", "광주광역시 (전 구 군)", "울산광역시 (전 구 군)", "세종특별자치시", "제주특별자치도 (제주시/서귀포시)"],
        "default_zone": "비수도권"
    }
}

# 2. 사용자 입력 섹션 (UI 구성)
st.header("👤 창업 및 사업 계획 입력")

col1, col2 = st.columns(2)

with col1:
    st.subheader("[1] 기본 정보 및 창업 지역/업종")
    age = st.number_input("현재 만 나이를 입력하세요 (군 복무 기간은 최대 6년 차감 가능)", min_value=0, max_value=100, value=25)
    
    sido = st.selectbox("창업 예정 지역의 '시/도'를 선택하세요", list(REGION_DATA.keys()))
    sigungu = st.selectbox("상세 시/군/구를 선택하세요", REGION_DATA[sido]["districts"])
    
    sido_db = REGION_DATA[sido]
    location_status = sido_db["mapping"][sigungu] if "mapping" in sido_db and sigungu in sido_db["mapping"] else sido_db["default_zone"]

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

    income_rate = st.slider("예상 매출액 대비 순이익률(%)을 선택하세요 (종합소득세 산출 기준)", min_value=1, max_value=100, value=30)
    # 진짜 소득금액(과세표준 대용) 수학적 연산
    estimated_income = expected_sales * (income_rate / 100)
    
    bookkeeping = st.radio("사업 장부를 스스로 작성하여 신고하실 계획인가요?", ["네, 스스로 작성하겠습니다.", "아니오, 장부 없이 간편하게 신고하겠습니다."])
    
    # 텍스트가 아닌 실제 채용 인원 '숫자'를 입력받아 연산에 활용
    employee_count = st.number_input("채용할 청년 정규직 직원 수를 입력하세요 (명)", min_value=0, max_value=100, value=0)
    
    initial_investment = st.radio("초기에 대규모 인테리어나 고가 장비 구입 계획이 있으신가요?", ["없음 (소자본 창업)", "있음 (인테리어 및 시설 자금 대량 투입)"])
    
    donation_input = st.text_input("연간 예상되는 사회공헌 기부 금액을 입력하세요 (원 단위)", value="0")
    try:
        donation_amount = float(donation_input.replace(",", ""))
    except ValueError:
        donation_amount = 0.0
        st.error("기부 금액에는 숫자와 콤마(,)만 입력할 수 있습니다.")
            
    property_plan = st.radio("창업 후 4년 이내에 사업용 부동산(사무실 등)을 매입할 계획이 있으신가요?", ["있음", "없음"])
    property_type = "상가/오피스텔/토지 매입"
    property_price = 0.0
    
    if property_plan == "있음":
        # 사용자가 선택한 값이 property_type 변수에 저장됩니다.
        property_type = st.selectbox(
            "매입할 부동산의 종류 및 취득 방식을 선택하세요",
            ["상가/오피스텔/토지 매입", "건물 직접 신축 (원시취득)", "6억 이하 주택 유상 매입", "6억 초과 ~ 9억 이하 주택 매입", "9억 초과 주택 매입"]
        )
        property_input = st.text_input("매입하려는 부동산의 예상 가액을 입력하세요", value="200,000,000")
        try:
            property_price = float(property_input.replace(",", ""))
        except ValueError:
            property_price = 0.0

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
            return (income * 0.24) - 576000
        elif income <= 150000000:
            return (income * 0.35) - 1544000
        elif income <= 300000000:
            return (income * 0.38) - 1994000
        elif income <= 500000000:
            return (income * 0.40) - 2594000
        elif income <= 1000000000:
            return (income * 0.42) - 3594000
        else:
            return (income * 0.45) - 6594000

    # 국가 누진세율 함수를 실행하여 기본 산출세액 도출
    base_tax = calculate_progressive_tax(estimated_income)
    
    status_kr = {"내": "수도권 과밀억제권역 내(핵심지)", "외곽": "수도권 과밀억제권역 외곽(성장관리지역 등)", "비수도권": "비수도권 지방지역"}[location_status]
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
                
            tax_savings = base_tax * reduction_rate
            st.success(f"🎉 **[조특법 제6조] 창업세액감면율: {int(reduction_rate * 100)}% 적용**")
            st.write(f"- 예상 순이익: **{int(estimated_income):,}원**")
            st.write(f"- 가상 산출소득세: **{int(base_tax):,}원**")
            st.write(f"- **최종 소득세 감면 혜택 액수: 약 {int(tax_savings):,}원 (5년간 매년 절세 가능)**")

        # B. 통합고용세액공제 연산 (조특법 제29조의7)
    
    # B. 통합고용세액공제 연산 및 리스크 모델링 (조특법 제29조의7)
        if employee_count > 0:
            per_person_value = 14500000 if location_status == "비수도권" else 11000000
            raw_employment_savings = employee_count * per_person_value
            
            st.info(f"👥 **[조특법 제29조의7] 통합고용세액공제 및 리스크 시뮬레이션**")
            st.write(f"- 청년 정규직 채용 인원: **{employee_count}명** (인당 {per_person_value:,}원 적용)")
            st.write(f"- 이론상 최대 공제 가능액: **{int(raw_employment_savings):,}원**")
            
            remaining_tax_window = base_tax - tax_savings
            
            if raw_employment_savings > remaining_tax_window:
                actual_employment_savings = max(0.0, remaining_tax_window)
                carried_over_savings = raw_employment_savings - actual_employment_savings
                
                # 💡 [UI 개선] 0원일 때와 아닐 때의 멘트를 분기하여 가독성 확보
                if actual_employment_savings == 0:
                    st.warning(f"⚠️ **[안내] 창업세액감면(100%) 적용으로 인해 올해 납부할 소득세가 이미 0원입니다.**")
                    st.write(f"  * **금년도 실제 반영 공제액: 0원** (이번 해에 차감할 세액이 없음)")
                else:
                    st.warning(f"⚠️ **[최저한세 및 소득세 한도 도달]** 올해 납부할 예상 소득세 한도를 초과했습니다.")
                    st.write(f"  * **금년도 실제 반영 공제액: {int(actual_employment_savings):,}원** (소득세 0원화 한도)")
                
                st.write(f"  * **다음 해로 이월되는 공제액: {int(carried_over_savings):,}원** (향후 10년간 이월공제 가능)")
            else:
                actual_employment_savings = raw_employment_savings
                st.write(f"  * **금년도 실제 반영 공제액: {int(actual_employment_savings):,}원** (전액 공제 가능)")
            
            st.error(f"🚨 **[조특법 제29조의7 제4항] 고용유지 의무 위반 추징 리스크**")
            st.write(f"  * **고용 유지 실패 시 최대 예상 추징 세액: {int(raw_employment_savings):,}원**")

        # C. 기부금 세액공제 연산 (소득세법 제59조의4)
        if donation_amount > 0:
            donation_savings = donation_amount * 0.15
            st.success(f"🕊️ **[소득세법 제59조의4] 기부금 절세 혜택 계산**")
            st.write(f"- 입력한 사회공헌 기부액: **{int(donation_amount):,}원**")
            st.write(f"- **추계신고 시 최종 소득세 직접 차감액: {int(donation_savings):,}원 (지출액의 15%)**")

        # D. 장부 미기장 가산세 연산 (소득세법 제81조의5)
        st.subheader("2. 장부 작성 및 가산세 리스크 (소득세법)")
        if is_self_book:
            st.success("✅ **[소득세법 제70조] 장부 기장 신고 예정 (가산세 위험 없음)**")
        else:
            penalty_tax = base_tax * 0.20
            st.error("🚨 **[소득세법 제81조의5] 무기장가산세 처분 리스크 노출**")
            st.write(f"- 장부 미작성 및 추계신고 시 소득세 산출세액의 **20% 패널티**가 부과됩니다.")
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
        if "있음" in initial_investment:
            st.info("💰 **[부가세법 제59조] 초기 시설 투자 자산 부가가치세 15일 이내 조기환급 특례 가능**")

        # B. 지방세 및 부동산 추징 리스크 연산 (지특법 제58조의3)
            st.subheader("4. 창업 지방세 혜택 및 사후관리")
        if is_eligible_business and property_plan == "있음" and property_price > 0:
            
            # 부동산 타입별 정확한 세법상 실효세율 주입
            if property_type == "상가/오피스텔/토지 매입":
                tax_rate = 0.046
            elif property_type == "건물 직접 신축 (원시취득)":
                tax_rate = 0.0316
            elif property_type == "6억 이하 주택 유상 매입":
                tax_rate = 0.011
            elif property_type == "6억 초과 ~ 9억 이하 주택 매입":
                tax_rate = 0.022  # 평균 실효세율 대리 위임
            else:
                tax_rate = 0.035
                
            normal_tax = property_price * tax_rate
            
            if location_status != "내":
                discounted_tax = normal_tax * 0.25
                potential_penalty = normal_tax * 0.75
                st.success(f"🎉 **[지특법 제58조의3] 부동산 취득세 감면 시뮬레이션 ({property_type})**")
                st.write(f"- 해당 부동산 법정 취득세율(부속세 포함): **{round(tax_rate * 100, 2)}%**")
                st.write(f"- 감면 전 정상 취득세액: **{int(normal_tax):,}원**")
                st.write(f"- **75% 감면 후 최종 납부 취득세: 약 {int(discounted_tax):,}원**")
                st.error(f"🚨 **[지특법 제58조의3 제4항] 3년 내 미사용/매각 시 추징 리스크 금액: {int(potential_penalty):,}원**")
            else:
                st.error(f"❌ **[과밀억제권역 감면 배제] 과밀억제권역 내 부동산 취득은 취득세 {round(tax_rate * 100, 2)}% 전액 부과 대상입니다. (감면액 없음)**")
                st.write(f"- 최종 납부 취득세액: **{int(normal_tax):,}원**")
        else:
            st.write("부동산 매입 계획이 없거나 감면 제외 업종이므로 취득세 시뮬레이션을 종료합니다.")