import streamlit as st

# 1. 페이지 기본 설정 및 보안/공신력 타이틀 세팅
st.set_page_config(page_title="Tax-Check: 청년창업 최종 마스터피스", layout="wide")
st.title("🚀 Tax-Check: 예비 청년사업자 4대 세법 종합 진단 시스템")
st.caption("🔥 2026년 현행세법 기준 ")

st.info("### 📌 청년 개인사업자 맞춤형 세제 혜택 및 리스크 스크리닝")

# -------------------------------------------------------------------------
# [원천 데이터 1] 대한민국 전 지역 행정구역 및 세법상 권역 매핑 데이터베이스
# -------------------------------------------------------------------------
REGION_DATA = {
    "서울특별시": {"districts": ["강남구", "강동구", "강북구", "강서구", "관악구", "마포구", "서초구", "성동구", "종로구", "중구", "기타 서울 전 지역"], "default_zone": "내"},
    "인천광역시": {"districts": ["부평구", "남동구", "미추홀구", "서구", "강화군 (외곽특례)", "옹진군 (외곽특례)", "송도/청라/영종 경제자유구역"], "mapping": {"강화군 (외곽특례)": "외곽", "옹진군 (외곽특례)": "외곽", "송도/청라/영종 경제자유구역": "외곽"}, "default_zone": "내"},
    "경기도": {
        "districts": ["수원시", "성남시", "고양시", "부천시", "안양시", "화성시 (외곽지)", "김포시 (외곽지)", "용인시 (외곽지)", "파주시 (외곽지)", "평택시 (외곽지)", "가평군/양평군"],
        "mapping": {"수원시": "내", "성남시": "내", "고양시": "내", "부천시": "내", "안양시": "내", "화성시 (외곽지)": "외곽", "김포시 (외곽지)": "외곽", "용인시 (외곽지)": "외곽", "파주시 (외곽지)": "외곽", "평택시 (외곽지)": "외곽"},
        "default_zone": "외곽"
    },
    "지방 광역시 및 도 지역 (비수도권)": {"districts": ["부산광역시", "대구광역시", "대전광역시", "광주광역시", "울산광역시", "세종특별자치시", "제주특별자치도", "기타 지방 시/군"], "default_zone": "비수도권"}
}

# 2. 사용자 입력 섹션 (UI 구성)
st.header("👤 창업 및 사업 계획 입력")

col1, col2 = st.columns(2)

with col1:
    st.subheader("[1] 기본 정보 및 창업 지역/업종")
    age = st.number_input("현재 만 나이를 입력하세요 (군 복무 기간은 최대 6년 차감 가능)", min_value=0, max_value=100, value=25)
    
    # 주소 자동 연동 시스템
    sido = st.selectbox("창업 예정 지역의 '시/도'를 선택하세요", list(REGION_DATA.keys()))
    sigungu = st.selectbox("상세 시/군/구를 선택하세요", REGION_DATA[sido]["districts"])
    
    # 내부 행정구역 권역 판별 알고리즘
    sido_db = REGION_DATA[sido]
    location_status = sido_db["mapping"][sigungu] if "mapping" in sido_db and sigungu in sido_db["mapping"] else sido_db["default_zone"]

    # 조세특례제한법 제6조 제3항 기반 세법 표준 대분류 업종 스키마
    business_type = st.selectbox(
        "창업 예정인 사업의 종류(업종)를 선택하세요 (★조특법 세법 표준 대분류 적용)",
        [
            "광업 / 제조업 (제품 생산, 식품 제조, 의류 제작 등)",
            "건설업 (인테리어, 건축 공사 등)",
            "통신판매업 (온라인 쇼핑몰, 해외직구 대행, 스마트스토어 등)",
            "정보통신업 (소프트웨어 개발, 게임 제작, 앱 개발, IT 플랫폼 등)",
            "연구개발업 / 전문·과학·기술 서비스업 (디자인, 광고대행, 경영컨설팅 등)",
            "음식점업 (일반식당, 카페, 제과점, 베이커리 등)",
            "물류산업 / 운수업 (창업 배송, 여객운송, 물류창고 등)",
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
    st.subheader("[2] 사업 규모 및 고용/자산/기부 계획")
    
    # [UX 업그레이드] 콤마(,) 입력을 지원하는 매출액 텍스트 인풋창
    sales_input = st.text_input("예상되는 연간 매출액을 입력하세요",)
    # 사용자가 입력한 문자열에서 콤마를 제거하고 숫자로 변환하는 예외 처리 파싱
    try:
        expected_sales = float(sales_input.replace(",", ""))
    except ValueError:
        expected_sales = 0.0
        st.error(" 매출액에는 숫자와 콤마(,)만 입력할 수 있습니다.")
        
    bookkeeping = st.radio("사업 장부를 스스로 작성하여 신고하실 계획인가요?", ["네, 스스로 작성하겠습니다.", "아니오, 장부 없이 간편하게 신고하겠습니다."])
    employee_plan = st.radio("나 외에 직원을 정규직(청년)으로 채용할 계획이 있으신가요?", ["혼자 일할 예정(1인 기업)", "직원을 채용할 예정"])
    initial_investment = st.radio("초기에 대규모 인테리어나 고가 장비 구입 계획이 있으신가요?", ["없음 (소자본 창업)", "있음 (인테리어 및 시설 자금 대량 투입)"])
    
    # 소득세법 제34조 기부금 세연 연동 인풋
    donation_plan = st.radio("지역사회 기부 및 사회공헌(ESG) 기부금 지출 계획이 있으신가요?", ["계획 없음", "연간 일정 금액 기부 계획 있음"])
    
    donation_amount = 0.0
    if donation_plan == "연간 일정 금액 기부 계획 있음":
        # [UX 업그레이드] 콤마(,) 입력을 지원하는 기부금 텍스트 인풋창
        donation_input = st.text_input("예상하는 연간 총 기부 금액을 입력하세요",)
        try:
            donation_amount = float(donation_input.replace(",", ""))
        except ValueError:
            donation_amount = 0.0
            st.error(" 기부 금액에는 숫자와 콤마(,)만 입력할 수 있습니다.")
            
    property_plan = st.radio("창업 후 4년 이내에 사업용 부동산(사무실 등)을 매입할 계획이 있으신가요?", ["있음", "없음"])

st.markdown("---")

# 3. 매칭 알고리즘 및 결과 연산
if st.button("📊 나의 현행세법 종합 혜택 및 리스크 진단하기"):
    st.header("📋 세법별 진단 결과 보고서 (청년 개인사업자 전용)")
    
    is_young = age <= 34
    is_self_book = "네" in bookkeeping
    is_small_business = expected_sales <= 104000000
    is_eligible_business = "🚫" not in business_type 
    
    status_kr = {"내": "수도권 과밀억제권역 내(핵심지)", "외곽": "수도권 과밀억제권역 외곽(성장관리지역 등)", "비수도권": "비수도권 지방지역"}[location_status]
    st.success(f"📍 **시스템 자동 권역 판별:** 선택하신 주소는 세법상 **[{status_kr}]**으로 자동 분류되었습니다.")
    
    res_col1, res_col2 = st.columns(2)
    
    with res_col1:
        # A. 소득세 감면 및 고용/기부 특례 (조특법 및 소득세법)
        st.subheader("1. 소득세 감면 및 특별 공제 (조세특례제한법/소득세법)")
        if not is_eligible_business:
            st.error("❌ **[업종 제한] 창업세액감면 대상 제외 업종입니다.**")
            st.write(f"선택하신 업종은 **조세특례제한법 제6조 제3항**이 규정하는 감면 열거 업종에 해당하지 않아, 청년창업 소득세 100% 감면 혜택을 적용받을 수 없습니다.")
        else:
            if location_status == "비수도권":
                if is_young or is_small_business:
                    st.success("🎉 **[조특법 제6조 제1항] 5년간 소득세 100% 전액 감면 대상**")
                else:
                    st.warning("🔶 **[조특법 제6조] 5년간 소득세 50% 감면 대상**")
            elif location_status == "외곽":
                if is_young or is_small_business:
                    st.success("🎉 **[2026 개정세법] 5년간 소득세 75% 감면 대상**")
                else:
                    st.warning("🔶 **[조특법 제6조] 5년간 소득세 25% 감면 대상**")
            else: 
                if is_young or is_small_business:
                    st.warning("🔶 **[조특법 제6조 제2항] 5년간 소득세 50% 감면 대상**")
                else:
                    st.error("❌ **청년 창업 세액감면 대상 제외**")
                    
        # 고용증대세액공제 (통합고용세액공제) 연계 연산
        if "채용" in employee_plan:
            bonus_amt = "1,450만 원" if location_status == "비수도권" else "1,100만 원"
            st.info(f"👥 **[조특법 제29조의7] 통합고용세액공제 연계 혜택**\n\n청년 개인사업자가 청년 정규직 직원을 채용할 경우, 국가에서 **인당 연간 최대 {bonus_amt}**의 소득세를 추가로 직접 공제해 줍니다.")

        # 소득세법 제34조 기부금 세법 매칭 알고리즘
        if donation_plan == "연간 일정 금액 기부 계획 있음" and donation_amount > 0:
            est_saving_15 = int(donation_amount * 0.15)
            st.success(f"🕊️ **[소득세법 제34조] 기부금 절세 특례 매칭**\n\n지출한 기부금은 복식/간편장부 작성 시 **'필요경비(사업 비용)'로 산입**하여 종합소득세 과세표준 자체를 낮추거나, 장부 미작성 시에도 기부 금액의 15%에 달하는 **약 {est_saving_15:,}원**을 최종 소득세액에서 직접 공제받을 수 있습니다.")

        # B. 소득세법 진단 (장부 의무)
        st.subheader("2. 장부 작성 및 가산세 리스크 (소득세법)")
        if is_self_book:
            st.success("✅ **[소득세법 제70조] 기장세액공제 혜택 가능**")
        else:
            st.error("🚨 **[소득세법 제81조의5] 무기장가산세 처분 주의**")

    with res_col2:
        # C. 부가가치세법 진단
        st.subheader("3. 부가가치세 면제 및 환급 특례 (부가가치세법)")
        if expected_sales < 48000000:
            st.success("🎉 **[부가세법 제69조 제1항] 부가가치세 납부 의무 전액 면제!**")
        elif expected_sales < 140000000:
            st.info("✅ **[부가세법 제61조 제1항] 간이과세자 적용 가능 권역**")
        else:
            st.warning("🔶 **일반과세자 자동 전환 대상**")
            
        if "해외 수출" in is_export:
            st.success("✈️ **[부가세법 제24조] 외화 획득 사업자 영세율(0%) 적용**")
        if "있음" in initial_investment:
            st.info("💰 **[부가세법 제59조] 초기 투자자산 부가가치세 조기환급 특례**")

        # D. 지방세특례제한법 진단
        st.subheader("4. 창업 지방세 혜택 및 사후관리 (지방세특례제한법)")
        if not is_eligible_business:
            st.error("❌ **[업종 제한] 지방세 특례 감면 제외 업종입니다.**")
        else:
            if is_young and location_status != "내":
                st.success("🎉 **[지특법 제58조의3 제1항] 창업 법인/사업자 등록면허세 75% 감면**")
                
            if property_plan == "있음":
                if (is_young or is_small_business) and location_status != "내":
                    st.success("🎉 **[지특법 제58조의3 제1항] 사업용 부동산 취득세 75% 및 재산세 50% 감면**")
                    st.error("🚨 **[지특법 제58조의3 제4항] 사후관리 조항 (추징 주의)**")
                else:
                    st.error("❌ **지방세 부동산 감면 대상 제외**")
            else:
                st.write("부동산 매입 계획이 없으므로 부동산 취득세 시뮬레이션을 종료합니다.")

    # 5. 하단 고정 확장 가이드라인 (성실신고 특례, 벤처인증, 카드이중공제 리스크)
    st.markdown("---")
    with st.expander("💡 2026년 현행법 기반 - 청년 개인사업자가 놓치기 쉬운 필수 세무 로드맵 및 카드 규제"):
        st.markdown("""
        * **🚨 [조특법 제126조의2] 대표자 신용카드 이중공제 원천 불가 (리스크)**
        * **🏥 [소득세법 제59조의4] 사업 확장 시 성실신고 의료비·교육비 특별세액공제 (혜택)**
        * **🚀 [조특법 제122조의3] 기술 기반 벤처기업 인증 시 추가 투자세액공제 (혜택)**
        """)

        # 백엔드 데이터 검증용 JSON 스키마 구조 시각화
        st.json({
            "service_name": "Tax-Check 청년창업편 콤마인풋 반영 최종본",
            "user_input_summary": {
                "user_age": age, "zone": location_status, "standard_business_category": business_type,
                "parsed_expected_sales": expected_sales, "parsed_donation_amount": donation_amount
            }
        })

