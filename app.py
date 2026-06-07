import streamlit as st


# 1. 페이지 기본 설정 및 타이틀 세팅 (정직하고 신뢰감 있는 타이틀로 변경)
st.set_page_config(page_title="Tax-Check: 청년창업 세법 시뮬레이터", layout="wide")
st.title("🚀 Tax-Check for 예비 청년사업자 세무 및 재무 시뮬레이터")
st.caption("📊현행세법 반영")

st.info("### 📌 사용자가 입력한 사업 계획 데이터를 기반으로 실제 세액 감면 및 리스크 금액을 연산합니다.")



st.header("📍 청년창업 예정지 주소 입력")
st.info("💡 [수도권정비계획법 시행령 별표1] 및 2026년 개정 세법 반영")

# 1단계: 전국 17개 시/도 선택창
sido = st.selectbox("시/도를 선택하세요", [
    "선택하세요", "서울특별시", "인천광역시", "경기도", 
    "부산광역시", "대구광역시", "광주광역시", "대전광역시", "울산광역시",
    "세종특별자치시", "충청남도", "충청북도", "전라남도", "전라북도", 
    "경상남도", "경상북도", "강원특별자치도", "제주특별자치도"
])

reduction_rate = 0.0
zone_name = ""
is_ready = False
location_status = "내"

# ==================== [1] 서울특별시 ====================
if sido == "서울특별시":
    sigungu = st.selectbox("시/군/구를 선택하세요", ["선택하세요","강남구", "강동구", "강북구", "강서구", "관악구", "광진구", "구로구", "금천구", "노원구", "도봉구", "동대문구", "동작구", "마포구", "서대문구", "서초구", "성동구", "성북구", "송파구", "양천구", "영등포구", "용산구", "은평구", "종로구", "중구", "중랑구"])
    if sigungu != "선택하세요":
        reduction_rate = 0.50
        zone_name = "수도권 과밀억제권역 (청년창업 50% 감면)"
        is_ready = True

# ==================== [2] 인천광역시 (송도·영종·청라 경제자유구역 완벽 반영) ====================
elif sido == "인천광역시":
    sigungu = st.selectbox("시/군/구를 선택하세요", ["선택하세요", "강화군", "옹진군", "서구", "연수구", "중구", "남동구", "부평구", "계양구", "미추홀구", "동구"])
    
    if sigungu in ["강화군", "옹진군"]:
        reduction_rate = 1.00
        zone_name = "수도권 내 인구감소지역 (청년창업 100% 전액 면제)"
        is_ready = True
        
    elif sigungu == "서구":
        # 청라국제도시(청라동) 및 수도권정비계획법상 제외동 포함
        seogu_zone = st.selectbox("창업지 해당 동을 선택하세요", [
            "선택하세요",
            "청라동", "대곡동", "불로동", "마전동", "금곡동", "오류동", "왕길동", "당하동", "원당동",
            "가좌동", "석남동", "가정동", "신현동", "원창동", "연희동", "심곡동", "공촌동", "경서동", "시천동", "검암동"
        ])
        if seogu_zone != "선택하세요":
            # 청라동(경제자유구역) 및 검단면 지역(대곡~원당)은 과밀억제 제외(75% 감면)
            if seogu_zone in ["청라동", "대곡동", "불로동", "마전동", "금곡동", "오류동", "왕길동", "당하동", "원당동"]:
                reduction_rate = 0.75
                zone_name = "수도권 과밀억제 제외지역 [인천경제자유구역 청라국제도시 및 특례구역] (75% 감면)"
            else:
                reduction_rate = 0.50
                zone_name = "수도권 과밀억제권역 (청년창업 50% 감면)"
            is_ready = True

    elif sigungu == "연수구":
        # 송도국제도시(송도동) 포함
        songdo_zone = st.selectbox("창업지 해당 동을 선택하세요", [
            "선택하세요", "송도동", "옥련동", "선학동", "연수동", "청학동", "동춘동"
        ])
        if songdo_zone != "선택하세요":
            # 송도동은 인천경제자유구역 핵심 지정 지역이므로 과밀억제 제외(75% 감면)가 맞습니다.
            if songdo_zone == "송도동":
                reduction_rate = 0.75
                zone_name = "수도권 과밀억제 제외지역 [인천경제자유구역 송도국제도시] (75% 감면)"
            else:
                reduction_rate = 0.50
                zone_name = "수도권 과밀억제권역 (청년창업 50% 감면)"
            is_ready = True

    elif sigungu == "중구":
        # 영종국제도시(운서~무의동) 포함
        junggu_zone = st.selectbox("창업지 해당 동을 선택하세요", [
            "선택하세요",
            "운서동", "운남동", "운북동", "중산동", "남북동", "덕교동", "을왕동", "무의동",
            "중앙동", "해안동", "관동", "항동", "선린동", "북성동", "송학동", "사동", "신생동", 
            "신포동", "답동", "신흥동", "선화동", "유동", "율목동", "도원동", "내동", "경동", 
            "용동", "인현동", "전동", "송월동", "만석동"
        ])
        if junggu_zone != "선택하세요":
            # 영종국제도시 및 용유/무의 지역은 과밀억제 제외(75% 감면)
            if junggu_zone in ["운서동", "운남동", "운북동", "중산동", "남북동", "덕교동", "을왕동", "무의동"]:
                reduction_rate = 0.75
                zone_name = "수도권 과밀억제 제외지역 [인천경제자유구역 영종국제도시] (청년창업 75% 감면)"
            else:
                reduction_rate = 0.50
                zone_name = "수도권 과밀억제권역 (청년창업 50% 감면)"
            is_ready = True

    elif sigungu == "남동구":
        namdong_zone = st.selectbox("창업지 해당 구역/동을 선택하세요", [
            "선택하세요",
            "남동국가산업단지 구역 내부 (산단 필지)",
            "논현동", "고잔동", "구월동", "간석동", "만수동", "장수동", "서창동", "운연동", "도림동", "수산동", "남촌동"
        ])
        if namdong_zone != "선택하세요":
            if "산업단지" in namdong_zone:
                reduction_rate = 0.75
                zone_name = "수도권 과밀억제 제외지역 (청년창업 75% 감면)"
            else:
                reduction_rate = 0.50
                zone_name = "수도권 과밀억제권역 (청년창업 50% 감면)"
            is_ready = True

    elif sigungu in ["부평구", "계양구", "미추홀구", "동구"]:
        reduction_rate = 0.50
        zone_name = "수도권 과밀억제권역 (청년창업 50% 감면)"
        is_ready = True

# ==================== [3] 경기도 ====================
elif sido == "경기도":
    sigungu = st.selectbox("시/군/구를 선택하세요", [
        "선택하세요", "수원시", "성남시", "안양시", "부천시", "광명시", "과천시", "의왕시", "군포시", 
        "의정부시", "구리시", "고양시", "하남시", "시흥시", "남양주시", "가평군", "연천군",
        "평택시", "파주시", "김포시", "광주시", "이천시", "오산시", "안성시", "포천시", "양주시", "여주시", "동두천시", "양평군", "용인시", "화성시", "안산시"
    ])
    
    if sigungu in ["가평군", "연천군"]:
        reduction_rate = 1.00
        zone_name = "수도권 내 인구감소지역 (청년창업 100% 전액 면제)"
        is_ready = True
        
    elif sigungu in ["수원시", "성남시", "안양시", "부천시", "광명시", "과천시", "의왕시", "군포시", "의정부시", "구리시", "고양시", "하남시"]:
        reduction_rate = 0.50
        zone_name = "수도권 과밀억제권역 (청년창업 50% 감면)"
        is_ready = True

    elif sigungu == "남양주시":
        dong = st.selectbox("세부 읍/면/동을 선택하세요", [
            "선택하세요",
            "호평동", "평내동", "금곡동", "일패동", "이패동", "삼패동", "가운동", "수석동", "지금동", "도농동",
            "와부읍", "진접읍", "화도읍", "진건읍", "오남읍", "퇴계원읍", "별내면", "수동면", "조안면", "별내동", "다산동", "양정동"
        ])
        if dong != "선택하세요":
            if dong in ["호평동", "평내동", "금곡동", "일패동", "이패동", "삼패동", "가운동", "수석동", "지금동", "도농동"]:
                reduction_rate = 0.50
                zone_name = "수도권 과밀억제권역 (청년창업 50% 감면)"
            else:
                reduction_rate = 0.75
                zone_name = "수도권 과밀억제 제외지역 (청년창업 75% 감면)"
            is_ready = True

    elif sigungu == "시흥시":
        dong = st.selectbox("세부 동/구역을 선택하세요", [
            "선택하세요",
            "반월특수지역 지정구역 (시화공단·MTV 내부)",
            "대야동", "신천동", "방산동", "포동", "미산동", "은행동", "안현동", "매화동", "도창동", 
            "금이동", "과림동", "계수동", "화정동", "능곡동", "하중동", "하상동", "광석동", "물왕동", 
            "산현동", "조남동", "논곡동", "목감동", "거모동", "군자동", "월곶동", "정왕동", "죽율동", 
            "무지내동", "신현동", "연성동", "장현동", "장곡동", "배곳동"
        ])
        if dong != "선택하세요":
            if "반월특수지역" in dong:
                reduction_rate = 0.75
                zone_name = "수도권 과밀억제 제외지역 (청년창업 75% 감면)"
            else:
                reduction_rate = 0.50
                zone_name = "수도권 과밀억제권역 (청년창업 50% 감면)"
            is_ready = True

    elif sigungu in ["평택시", "파주시", "김포시", "광주시", "이천시", "오산시", "안성시", "포천시", "양주시", "여주시", "동두천시", "양평군", "용인시", "화성시", "안산시"]:
        reduction_rate = 0.75
        zone_name = "수도권 과밀억제 제외지역 (청년창업 75% 감면)"
        is_ready = True

# ==================== [4] 지방 광역시 및 도 지역 ====================
elif sido in ["부산광역시", "대구광역시", "광주광역시", "대전광역시", "울산광역시"]:
    if sido == "부산광역시":
        sigungu = st.selectbox("구/군을 선택하세요", ["선택하세요", "중구", "서구", "동구", "영도구", "부산진구", "동래구", "남구", "북구", "해운대구", "사하구", "금정구", "강서구", "연제구", "수영구", "사상구", "기장군"])
    elif sido == "대구광역시":
        sigungu = st.selectbox("구/군을 선택하세요", ["선택하세요", "중구", "동구", "서구", "남구", "북구", "수성구", "달서구", "달성군", "군위군"])
    elif sido == "광주광역시":
        sigungu = st.selectbox("구를 선택하세요", ["선택하세요", "동구", "서구", "남구", "북구", "광산구"])
    elif sido == "대전광역시":
        sigungu = st.selectbox("구를 선택하세요", ["선택하세요", "동구", "중구", "서구", "유성구", "대덕구"])
    elif sido == "울산광역시":
        sigungu = st.selectbox("구/군을 선택하세요", ["선택하세요", "중구", "남구", "동구", "북구", "울주군"])
        
    if sigungu != "선택하세요":
        reduction_rate = 1.00
        zone_name = "수도권 외 지역 (청년창업 100% 전액 면제)"
        is_ready = True

elif sido == "세종특별자치시":
    reduction_rate = 1.00
    zone_name = "수도권 외 지역 (청년창업 100% 전액 면제)"
    is_ready = True

elif sido in ["충청남도", "충청북도", "전라남도", "전북특별자치도", "경상남도", "경상북도", "강원특별자치도", "제주특별자치도"]:
    if sido == "충청남도":
        sigungu = st.selectbox("시/군을 선택하세요", ["선택하세요", "천안시", "공주시", "보령시", "아산시", "서산시", "논산시", "계룡시", "당진시", "금산군", "부여군", "서천군", "청양군", "홍성군", "예산군", "태안군"])
    elif sido == "충청북도":
        sigungu = st.selectbox("시/군을 선택하세요", ["선택하세요", "청주시", "충주시", "제천시", "보은군", "옥천군", "영동군", "증평군", "진천군", "괴산군", "음성군", "단양군"])
    elif sido == "전라남도":
        sigungu = st.selectbox("시/군을 선택하세요", ["선택하세요", "목포시", "여수시", "순천시", "나주시", "광양시", "담양군", "곡성군", "구례군", "고흥군", "보성군", "화순군", "장흥군", "강진군", "해남군", "영암군", "무안군", "함평군", "영광군", "장성군", "완도군", "진도군", "신안군"])
    elif sido == "전북특별자치도":
        sigungu = st.selectbox("시/군을 선택하세요", ["선택하세요", "전주시", "군산시", "익산시", "정읍시", "남원시", "김제시", "완주군", "진안군", "무주군", "장수군", "임실군", "순창군", "고창군", "부안군"])
    elif sido == "경상남도":
        sigungu = st.selectbox("시/군을 선택하세요", ["선택하세요", "창원시", "진주시", "통영시", "사천시", "김해시", "밀양시", "거제시", "양산시", "의령군", "함안군", "창녕군", "고성군", "남해군", "하동군", "산청군", "함양군", "거창군", "합천군"])
    elif sido == "경상북도":
        sigungu = st.selectbox("시/군을 선택하세요", ["선택하세요", "포항시", "경주시", "김천시", "안동시", "구미시", "영주시", "영천시", "상주시", "문경시", "경산시", "의성군", "청송군", "영양군", "영덕군", "청도군", "고령군", "성주군", "칠곡군", "예천군", "봉화군", "울진군", "울릉군"])
    elif sido == "강원특별자치도":
        sigungu = st.selectbox("시/군을 선택하세요", ["선택하세요", "춘천시", "원주시", "강릉시", "동해시", "태백시", "속초시", "삼척시", "홍천군", "횡성군", "영월군", "평창군", "정선군", "철원군", "화천군", "양구군", "인제군", "고성군", "양양군"])
    elif sido == "제주특별자치도":
        sigungu = st.selectbox("행정시를 선택하세요", ["선택하세요", "제주시", "서귀포시"])

    if sigungu != "선택하세요":
        reduction_rate = 1.00
        zone_name = "수도권 외 지역 (청년창업 100% 전액 면제)"
        is_ready = True

# ==================== 결과 출력부 ====================
if is_ready and sido != "선택하세요":
    st.write(f"### 🔍 2026년 청년창업 세액감면 계산 결과")
    st.success(f"⚖️ 법적 적용 권역: **{zone_name}**")
    st.success(f"🎉 **선택하신 지역의 청년창업중소기업 최종 세액감면율은 {int(reduction_rate * 100)}% 입니다.**") 
    st.markdown("---")


# ==================== [수정] 기존 코드 연동을 위한 location_status 주입 ====================
if reduction_rate == 1.00:
    # 수도권 외 지역 또는 수도권 내 인구감소지역은 세법상 가장 높은 혜택을 받으므로 "비수도권" 등급 부여
    location_status = "비수도권"
elif reduction_rate == 0.75:
    # 과밀억제 제외 수도권, 특례 산단 등은 "외곽" 등급 부여
    location_status = "외곽"
elif reduction_rate == 0.50:
    # 서울 및 일반 과밀억제권역은 "내" 등급 부여
    location_status = "내"
else:
    location_status = "내" # 기본값 예외 처리



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

    

    
   # [대한민국 세법 고증 100%] 조특법(inc) - 지특법(tax) - 부가세(vat) 최종 마스터 테이블
    BUSINESS_TAX_MAP = {
    "선택하세요": {"inc": False, "tax": False, "vat": "간이"},
    
    # -------------------------------------------------------------------------
    # ZONE 1. 하이브리드 감면 구간 (소득세 O / 취득세 O / 국세청 고시에 의해 부가세 일반과세 강제)
    # -------------------------------------------------------------------------
    "수도, 하수 및 폐기물 처리, 원료 재생업": {"inc": True, "tax": True, "vat": "일반"}, # 고시 900200, 900300 등 명시됨
    "정보통신업 (SW개발, 게임, 호스팅, 데이터베이스 등)": {"inc": True, "tax": True, "vat": "일반"}, # 고시 722000, 723001 등 대거 명시됨
    "물류산업 (물류터미널 등)": {"inc": True, "tax": True, "vat": "일반"}, # 고시 630305 물류터미널 명시됨
    "창작 및 예술관련 서비스업 (영화·방송프로그램 제작 및 배급업 등 / 자영예술가 제외)": {"inc": True, "tax": True, "vat": "일반"}, # 지특법 7호 적격 & 고시 921100, 921304 명시됨
    "관광숙박업, 국제회의업, 테마파크업 및 관광객 이용시설업": {"inc": True, "tax": True, "vat": "일반"}, # 지특법 11호 적격 & 고시 551001(호텔), 921903(테마파크) 명시됨
    "직업기술 분야 학원 또는 직업능력개발훈련시설 (기술훈련 및 운전학원 등)": {"inc": True, "tax": True, "vat": "일반"}, # 지특법 10호 적격 & 고시 809001, 809011 명시됨

    # -------------------------------------------------------------------------
    # ZONE 2. 혜택 극대화 구간 (소득세 O / 취득세 O / 국세청 고시에 없어 간이과세 가능)
    # -------------------------------------------------------------------------
    "광업": {"inc": True, "tax": True, "vat": "간이"}, # 고시 종목기준 명단에 없음
    "제조업 (유사 사업 포함)": {"inc": True, "tax": True, "vat": "간이"}, # 고시 종목기준 명단에 없음 (사라진 항목 반영)
    "건설업": {"inc": True, "tax": True, "vat": "간이"}, # 고시 종목기준 명단에 없음
    "전문, 과학 및 기술 서비스업 (연구개발업, 광고업, 전문디자인, 시장조사 등)": {"inc": True, "tax": True, "vat": "간이"}, # 지특법 5호 적격이나 고시 명단에 없음
    "전시산업 (전시, 컨벤션 및 행사대행업 등)": {"inc": True, "tax": True, "vat": "간이"}, # 지특법 6호 마목 및 12호 적격이나 고시 명단에 부재

    # -------------------------------------------------------------------------
    # ZONE 3. 국세(소득세)만 감면되고 지방세(취득세)는 배제되는 서비스/유통 구간
    # -------------------------------------------------------------------------
    "전문, 과학 및 기술 서비스업 (위 연구개발·광고 등 외 일반 전문직 제외 분야)": {"inc": True, "tax": False, "vat": "간이"},
    "통신판매업 (온라인 쇼핑몰, 스마트스토어 등)": {"inc": True, "tax": False, "vat": "간이"}, # 고시 명단에 없음
    "음식점업 (식당, 카페 등 - 사업장 면적 50㎡ 미만 소형 창업)": {"inc": True, "tax": False, "vat": "간이"}, # 고시 552107 등 등록 (50㎡ 미만만 간이 인정)
    "음식점업 (식당, 카페 등 - 사업장 면적 50㎡ 이상 중대형 창업)": {"inc": True, "tax": False, "vat": "일반"}, # 고시 552107 등 등록 (50㎡ 이상은 일반과세)
    "금융 및 보험업 (정보통신 활용 핀테크·금융플랫폼 서비스 한정)": {"inc": True, "tax": False, "vat": "간이"}, # 고시 명단에 없음
    "사업시설 관리 및 조경 서비스업": {"inc": True, "tax": False, "vat": "간이"}, # 고시 명단에 없음
    "사업 지원 서비스업 (고용알선, 인력공급, 경비·경호, 보안시스템 등)": {"inc": True, "tax": False, "vat": "간이"}, # 고시 명단에 없음
    "스포츠 및 기타 여가관련 서비스업 (오락장 등 제외 스포츠시설, 경기장 등)": {"inc": True, "tax": False, "vat": "일반"}, # 고시 924200(경기장), 924303(골프장) 등 명시됨
    "개인 및 소비용품 수리업 (자동차 종합수리업 외 일반 수리)": {"inc": True, "tax": False, "vat": "간이"}, # 고시 명단에 없음
    "자동차 종합수리업": {"inc": True, "tax": False, "vat": "일반"}, # 고시 922201 명시됨
    "이용 및 미용업 (마사지 및 체형관리 외 일반 미용)": {"inc": True, "tax": False, "vat": "간이"}, # 고시 명단에 없음
    "마사지업 및 체형관리 서비스업 (※ 단, 체형관리는 사업장면적 40㎡ 이상 일반과세 강제)": {"inc": True, "tax": False, "vat": "일반"}, # 고시 930208, 930209 명시됨
    "노인복지시설 운영 사업 및 사회복지 서비스업": {"inc": True, "tax": False, "vat": "일반"}, # 고시 930914(노인양로복지시설) 명시됨

    # -------------------------------------------------------------------------
    # ZONE 4. 🚫 창업 감면 전면 비대상 (조특법X, 지특법X) -> 부가세 성격별 분류
    # -------------------------------------------------------------------------
    "🚫 법률/회계/세무 전문직, 오락장, 가상자산거래소, 예식장업 등": {"inc": False, "tax": False, "vat": "일반"}, # 고시 930901(예식장) 등 명시됨
    "🚫 기타 일반 오프라인 소매업, 옷가게, 잡화점 등 (고시 명시 품목 제외)": {"inc": False, "tax": False, "vat": "간이"},
    "🚫 백화점, 대형마트, 편의점, 가구·가전·귀금속·골프장비 오프라인 소매업": {"inc": False, "tax": False, "vat": "일반"} }

# Streamlit 업종 선택 컴포넌트 출력
    business_type = st.selectbox(
    "창업 예정인 사업의 종류(업종)를 선택하세요",
    list(BUSINESS_TAX_MAP.keys()))

# 2. 선택된 업종에 맞춰 소득세와 취득세의 감면 자격을 독립적으로 판정하는 엔진
    if business_type != "선택하세요":
    # 국세(종합소득세) 감면 대상 여부 판정 (조특법 제6조 제3항 기준)
      is_eligible_business = BUSINESS_TAX_MAP[business_type]["inc"]
    
    # 지방세(부동산 취득세) 감면 대상 여부 판정 (지특법 제58조의3 제4항 기준)
      is_eligible_property_tax = BUSINESS_TAX_MAP[business_type]["tax"]

      vat_style = BUSINESS_TAX_MAP[business_type]["vat"]

    


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
    
    # ========== [사전 단계: 장부 작성 여부 체크] ==========
    reporting_type = st.radio(
            "📋 올해 종합소득세 신고 방식을 선택해 주세요.",
            ["정식 장부 기장 신고 (간편장부 또는 복식부기)", "장부 없는 추계 신고 (단순경비율 또는 기준경비율)"])
    is_self_book = (reporting_type == "정식 장부 기장 신고 (간편장부 또는 복식부기)")



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
    is_self_book = (reporting_type == "정식 장부 기장 신고 (간편장부 또는 복식부기)")
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
    status_kr = {"내": "수도권 과밀억제권역", "외곽": "수도권 과밀억제권역 외의 수도권(인구감소지역 제외)", "비수도권": "비수도권 혹은 수도권 인구감소지역"}[location_status]
    st.success(f"📍 선택하신 주소는 세법상 [{status_kr}]으로 분류되었습니다.")



    res_col1, res_col2 = st.columns(2)
    
    with res_col1:
        st.subheader("1. 소득세 감면 및 특별 공제 (조세특례제한법/소득세법)")
        
    
    

        # A. 창업중소기업 세액감면 연산 (조특법 제6조)
        if not is_eligible_business:
            reduction_rate = 0.0
            st.error("❌ **[업종 제한] 창업세액감면 대상 제외 업종입니다.**")
            st.write("선택하신 업종은 조특법 제6조에 열거된 감면 대상이 아니므로 소득세 감면율은 0%입니다.")
        else:
        # 업종 코드가 통과된 경우, 주소(location_status)와 청년/소기업 여부에 따라 최종 감면율 산출
             if location_status == "비수도권":
        # 1번 조문 구역: 청년 100% / 일반(소기업 등) 50%
                 reduction_rate = 1.0 if is_young else (0.5 if is_small_business else 0.0)
        
             elif location_status == "외곽":
        # 2번·4번 조문 구역: 청년 75% / 일반(소기업 등) 25%
                reduction_rate = 0.75 if is_young else (0.25 if is_small_business else 0.0)
        
             else: # "내" (과밀억제권역)
        # 3번 조문 구역: 청년 50% / 일반 0% (과밀억제권역 내 일반 창업은 감면 없음)
                   reduction_rate = 0.5 if is_young else 0.0

        tax_savings = base_tax * reduction_rate
        
        st.success(f"🎉 **[조특법 제6조] 창업세액감면율: {int(reduction_rate * 100)}% 적용**")
        st.write(f"- 예상 순이익: **{int(estimated_income):,}원**")
        st.write(f"- 가상 산출소득세: **{int(base_tax):,}원**")
        st.write(f"- **최종 소득세 감면 혜택 액수: 약 {int(tax_savings):,}원 (5년간 매년 절세 가능)**")
        st.write(f"**최종 소득세 감면 적용 후 세액: {int(final_income_tax):,} 원**")
        st.write(f"**지방소득세(국세의 10%): {int(final_local_tax):,} 원**")
        st.success(f"💰 **최종 총 납부 세액: {int(total_tax):,} 원**")
        st.caption("⚠️ 본 감면 혜택은 법률상 **2027년 12월 31일 이전 창업자**에게만 유효하므로 기한 내 창업 및 사업자등록이 필수적입니다.")

        
        
















        # 3. 통합고용세액공제 (2026년 최신 개정 조특법 제29조의8 및 제132조 최저한세 반영)
        if employee_count > 0:
    # 지역별 단가 세팅 (A+B+C 누적 구조 고증)
          if location_status != "내":
             per_person_value = 10000000  # 수도권 밖: 인당 1,000만 원
             next_year_bonus = 19000000   
             third_year_bonus = 20000000  
          else:
             per_person_value = 7000000   # 수도권 내: 인당 700만 원
             next_year_bonus = 16000000   
             third_year_bonus = 17000000  
    
    # 1년 차 공제액 및 3년 누적액 산출
          annual_employment_savings = employee_count * per_person_value
          total_3years_savings = (
          (employee_count * per_person_value) + 
        (employee_count * next_year_bonus) + 
        (employee_count * third_year_bonus) )
    
          st.info(f"👥 **[조특법 제29조의8] 청년 개인사업자 통합고용세액공제 시뮬레이션**")
          st.warning("⚠️ **[세법 기준 고지]** 본 공제는 대표자 본인, 배우자 및 직계존비속을 제외한 **'4대보험 가입 정규직 직원(상시근로자)'** 채용 시에만 적용됩니다.")
    
          st.write(f"- 청년 채용 인원 (대표자 제외): **{employee_count}명** (최초 사업연도 인당 {per_person_value:,}원 적용)")
          st.write(f"- **이론상 금년도 세액공제액: {int(annual_employment_savings):,}원**")
    
    
    # [핵심 고증] 조특법 제132조에 따른 개인사업자 최저한세(35%) 한도 필터링 엔지니어링
    # 창업세액감면 등으로 이미 세금이 줄어든 상태의 남은 소득세 확인
          tax_savings = base_tax * reduction_rate
          remaining_tax_window = base_tax - tax_savings
    
    # 최저한세 기준선 산출: 감면 전 산출세액(base_tax)의 35%는 무조건 납부해야 함
          minimum_tax_limit = base_tax * 0.35
    
    # 최저한세를 고려하여 올해 최대로 공제받을 수 있는 실질 한도 금액 계산
    # (남은 소득세에서 최저한세 기준선만큼은 공제하지 못하고 남겨둬야 함)
          max_allowable_savings = max(0.0, remaining_tax_window - minimum_tax_limit)
    # -------------------------------------------------------------------------
    
          if annual_employment_savings > max_allowable_savings:
        # 최저한세 한도 또는 소득세 부족으로 인해 이월공제 발생
             actual_employment_savings = max_allowable_savings
             carried_over_savings = annual_employment_savings - actual_employment_savings
        
             st.error("🚨 **[조특법 제132조 최저한세 한도 도달 안내]**")
             st.write(f"  * 관련 법령에 따라 개인사업자는 산출세액의 최소 35%인 **{int(minimum_tax_limit):,}원**을 의무 납부해야 합니다.")
             st.write(f"  * 이에 따라 올해 소득세에서 실제로 감면되는 금액은 **{int(actual_employment_savings):,}원**으로 제한됩니다.")
             st.info(f"  * **다음 해로 이월되는 공제액: {int(carried_over_savings):,}원** (조특법 제144조에 따라 향후 10년간 이월하여 차감 가능)")
          else:
        # 최저한세 걸리지 않고 전액 당해 연도 차감 가능
             actual_employment_savings = annual_employment_savings
             carried_over_savings = 0
             st.success(f"  * **금년도 실제 소득세 차감액: {int(actual_employment_savings):,}원** (최저한세 범위 내 전액 차감 완료)")
    
          st.caption(f"💡 **[3개년 연동형 누적 특례 적용]** 고용 유지 시 향후 3년간 누적 총 **{int(total_3years_savings):,}원**의 세액공제 혜택을 받게 됩니다.")
    
    # 감면액의 20% 농어촌특별세 부과 처리
          nongtuk_tax = actual_employment_savings * 0.20
          if nongtuk_tax > 0:
              st.write(f"💸 **[농어촌특별세법 제5조 제1항 제1호] 부가 한도세:** 세액공제 혜택의 20%인 **{int(nongtuk_tax):,}원**은 농어촌특별세로 별도 고지되어 납부하셔야 합니다.")
        
    # 사후관리 리스크
          st.error(f"🚨 **[사후관리 의무 위반 추징 리스크]**")
          st.write(f"  * 본 세액공제를 적용받은 후, 차년도 및 차차년도 과세연도에 전체 상시근로자 수가 감소할 경우, **기 공제받은 세액({int(actual_employment_savings):,}원)의 상당액을 국세청에 다시 추징당하므로** 고용 유지 관리가 필수적입니다.")
        
        
        
        
        
        # C. 기부금 세액공제 연산 (소득세법 제59조의4)
    

       # ========== [C. 기부금 한도 및 절세액 정밀 연산 엔진] ==========
        # 소득세법 제34조 및 제59조의4 법리 고증 완료
        if donation_amount > 0:
            st.info(f"🕊️ **[소득세법 제34조] 기부금 필요경비 한도 및 절세 정밀 진단**")
            st.write(f"- 입력한 연간 예상 기부액: **{int(donation_amount):,}원**")
            st.caption("※ 본 시뮬레이터는 청년 창업자가 주로 이용하는 일반 지정기부금(공익·동물·환경단체 등)을 기준으로 간소화하여 연산합니다.")
            
            if is_self_book:
                # 1. 장부 기장 사업자: 필요경비(비용) 산입 한도 계산
                base_income = estimated_income 
                
                # 일반 지정기부금(종교단체 외 공익법인) 한도 범위 계산 (기준소득금액의 30%)
        
                donation_limit = max(0.0, base_income * 0.30)
                st.write(f"- 세법상 기부금 인정 한도액 (순이익의 30%): **{int(donation_limit):,}원**")
                
                if donation_amount > donation_limit:
                    actual_expense = donation_limit
                    over_limit_amount = donation_amount - donation_limit
                    
                    st.warning(f"⚠️ **[기부금 한도 초과]** 입력하신 기부금이 올해 비용 인정 한도를 초과했습니다.")
                    st.write(f"  * **금년도 실제 비용(필요경비) 반영액: {int(actual_expense):,}원**")
                    st.write(f"  * **다음 해로 이월되는 기부금: {int(over_limit_amount):,}원** (향후 10년간 이월하여 비용 처리 가능)")
                else:
                    actual_expense = donation_amount
                    st.success(f"✅ **[한도 내 전액 인정]** 기부금 {int(actual_expense):,}원 전액이 올해 사업 비용으로 정상 인정됩니다.")
                
                # 실질 절감액 정밀 환산
                if base_income > 0:
                    approx_tax_rate = base_tax / base_income
                    saved_tax = actual_expense * approx_tax_rate
                    st.write(f"  * **기부금 지출로 인한 올해 소득세 실질 절감액: 약 {int(saved_tax):,}원**")

            else:
                # 2. [세법 교정] 장부를 안 쓰는 추계신고 사업자: 혜택 전면 배제 고지
                st.error(f"❌ **[추계신고 시 기부금 혜택 전액 부인]**")
                st.write("장부를 작성하지 않고 추계신고를 하시는 경우, 소득세법상 기부금은 **비용(필요경비)으로 인정되지 않으며 세액공제(15%) 또한 적용 불가능**합니다.")
                st.caption("※ 소득세법 제59조의4에 따른 특별세액공제는 근로소득자(직장인) 대상 규정입니다. 사업소득만 있는 자가 추계신고를 하면 기부금 절세 효과는 **0원**이 됩니다.")

    
        # ========== [D. 장부 미기장 가산세 연산 수정] ==========
        # 소득세법 제160조 및 제81조의5 예외 조항 완벽 고증
        st.subheader("2. 장부 작성 및 가산세 리스크 (소득세법)")
        if is_self_book:
            st.success("✅ **[소득세법 제160조] 장부의 비치·기록 의무 이행 예정 (가산세 위험 없음)**")
            st.write("- 스스로 장부를 작성하여 정식 기장 신고를 진행하므로 세법상 무기장가산세 대상에서 제외됩니다.")
        else:
            # [세법 교정] 소규모 사업자 예외 변수 바인딩 (Upstream에서 해당 여부 체크 박스나 로직을 연동하는 것을 권장)
            is_small_business = st.checkbox("💡 올해 신규 개업하셨거나, 직전 연도 매출이 4,800만 원 미만인 '소규모 사업자'에 해당하나요?")
            
            if is_small_business:
                st.success("✅ **[가산세 면제] 소득세법 제81조의5 제2항에 따른 무기장가산세 제외 대상**")
                st.write("- 추계신고를 진행하더라도 세법상 '소규모 사업자' 조건에 부합하여 20% 무기장가산세가 전액 면제됩니다.")
            else:
                penalty_tax = base_tax * 0.20
                st.error("🚨 **[소득세법 제81조의5] 무기장가산세 처분 리스크 노출**")
                st.write(f"- 소규모 사업자에 해당하지 않는 기장 의무자가 장부 없이 신고하므로, 산출세액의 **20% 패널티**가 부과됩니다.")
                st.write(f"- **예상 부과 가산세 리스크 액수: 약 {int(penalty_tax):,}원 부과 주의**")

    with res_col2:


        st.subheader("3. 부가가치세 면제 및 환급 특례 (부가가치세법)")

# [STEP 1] 업종별 부가세 기본 유형(vat_style) 및 매출액 기준 매칭
        tax_type = ""

        if vat_style == "면세":
           st.info("🌸 **[부가세법 제26조] 본 업종은 부가가치세가 전액 면제되는 [면세사업자] 대상입니다.**")
           st.write("- 매출 발생 시 부가세 10%를 징수하지 않으며, 매출액 규모와 상관없이 면세가 유지됩니다.")
           tax_type = "면세"

        elif vat_style == "겸영":
             st.warning("⚠️ **[과세·면세 겸영] 과세 매출과 면세 매출이 공존하는 [겸영사업자] 대상입니다.**")
             st.write("- 의원의 미용시술(과세)/질병치료(면세), 약국의 일반약판매(과세)/처방조제(면세)처럼 사업 영역에 따라 부가세가 안분 적용됩니다.")
             tax_type = "겸영"

        elif vat_style == "일반":
             st.warning("🔶 **[일반과세자 강제] 매출액과 관계없이 무조건 [일반과세자]로 지정되는 업종입니다.**")
             st.write("- 간이과세 배제 업종(광업, 제조업, 전문직, 도매, 일부 정보통신업 등)에 해당하여 창업 즉시 일반과세가 적용됩니다.")
             tax_type = "일반"

        elif vat_style == "간이":
    # 간이과세가 가능한 업종만 매출액 분기를 태웁니다.
             if int(expected_sales) < 48000000:
                st.success("🎉 **[부가세법 제69조] 연 매출 4,800만 원 미만으로 부가가치세 납부 의무 전액 면제!**")
                tax_type = "간이_면제"
             elif int(expected_sales) < 140000000:
                  st.info(f"✅ **[부가세법 제61조 제1항] 연 매출 {int(expected_sales):,}원: 간이과세자 적용 권역**")
                  tax_type = "간이"

             else:
                st.warning("🔶 **[일반과세자 자동전환] 연 매출 1.4억 원 이상: 일반과세자 대상 (간이과세 배제)**")
                tax_type = "일반"



        if "해외 수출" in is_export:
          if tax_type == "면세":
              st.error("❌ **[영세율 적용 불가] 면세사업자는 부가세법상 영세율(0%) 제도를 적용받을 수 없습니다. (매입세액 환급 불가)**")
          else:
               st.success("✈️ **[부가세법 제24조] 외화 획득 사업자 영세율(0%) 적용 대상**")



# [STEP 3] 부가가치세 조기환급 조건부 렌더링 (면세, 겸영, 간이, 일반 완벽 분기)
        if initial_investment == "있음 (인테리어 및 시설 자금 대량 투입)" and investment_amount > 0:
            st.info(f"📐 **[부가세법 제59조] 초기 시설 투자 조기환급 검증**")
            st.write(f"- 초기 시설 투자/인테리어 예상액: **{int(investment_amount):,}원**")
    
            if tax_type == "면세":
             st.error("❌ **[환급 불가] 면세사업자는 매입 부가세 환급 자격이 없습니다. 인테리어비에 포함된 부가세 10%는 환급되지 않고 전액 자산 원가(비용)로 처리됩니다.**")
        
            elif tax_type == "겸영":
        # 과세 매출 비중만큼만 환급되므로 안내 문구 수정
                  expected_refund = investment_amount * (10 / 110) # 부가세 포함 금액이므로 10/110 공식을 써야 팩트에 맞습니다.
                  st.success(f"💰 **[조건부 조기환급] 예상 부가가치세 조기 환급액: 약 {int(expected_refund):,}원 (안분계산 필요)**")
                  st.write("💡 겸영사업자는 전체 매출 중 **'과세 매출이 차지하는 비율'만큼만 안분 계산**하여 제한적으로 환급됩니다.")
                  st.caption("※ 치료/조제 등 면세 매출 비율 부분은 환급되지 않습니다.")
        
            elif "간이" in tax_type:
                   st.error("❌ **[환급 불가] 현재 '간이과세자' 권역으로 설정되어 있어 부가가치세 환급 및 조기환급이 불가능합니다.**")
                   st.caption("💡 [세무 팁] 인테리어 비용에 대한 부가세 10%를 환급받고 싶다면, 사업자등록 시 초기 매출이 적더라도 '일반과세자'를 의도적으로 선택하여 등록해야 합니다.")
        
            elif tax_type == "일반":
        # 일반과세자는 100% 전액 조기환급 대상
                   expected_refund = investment_amount * (10 / 110) # 공급대가에서 부가세액만 추출하는 정확한 세법 수식
                   st.success(f"💰 **[조기환급 대상] 예상 부가가치세 조기 환급액: 약 {int(expected_refund):,}원**")
                   st.write("💡 일반 환급과 달리 확정/예정신고 후 **단 15일 이내**에 통장으로 즉시 조기 환급되어 초기 자금 융통에 매우 유리합니다.")
                   st.caption("※ 단, 세금계산서 또는 신용카드 매출전표 등 정규 증빙을 반드시 수취해야 합니다.")
        else:
            st.write("초기 대규모 시설 투자가 없으므로 조기환급 시뮬레이션을 종료합니다.")

       


       
        st.subheader("4. 창업 지방세 혜택 및 사후관리")

        if property_plan == "있음" and property_price > 0:
          if property_type == "상가/오피스텔/토지 유상 매입":
             tax_rate = 0.046       # 지방세법 제11조 제1항 제7호 (기본 4% + 지방교육세 0.4% + 농특세 0.2%)
          elif property_type == "사업용 건물 직접 신축 (원시취득)":
               tax_rate = 0.0316      # 지방세법 제11조 제1항 제3호 (기본 2.8% + 지방교육세 0.36% + 농특세 비과세 분기 반영)
          else:
              tax_rate = 0.046       # 그 외 기타 사업용 자산 매입 기본값 세팅
        
              
              
          normal_tax = property_price * tax_rate
    
    
          if is_eligible_property_tax:
       
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
        # [B그룹] 국세는 감면되나 취득세는 배제되는 업종인 경우 (음식점업, 통신판매업 등) 또는 완전 제외 업종
              normal_tax = property_price * tax_rate
              st.error(f"❌ **[취득세 감면 제외 업종 고지]**")
              st.write(f"- 선택하신 업종은 조특법상 소득세 감면 대상에는 해당할 수 있으나, **지방세특례제한법 제58조의3 제4항에 열거된 '취득세 감면 대상 한정 업종'에 포함되지 않습니다.**")
              st.warning(f"- 이에 따라 부동산 취득세 감면 혜택(75%)이 전액 배제되며, 기본 세율이 그대로 적용됩니다.")
              st.write(f"- 해당 사업용 부동산 법정 실효세율: **{round(tax_rate * 100, 2)}%**")
              st.error(f"💰 **최종 납부해야 할 취득세 총액: {int(normal_tax):,}원 (감면율 0%)**")

        else:
         st.write("부동산 매입 계획이 없으므로 취득세 시뮬레이션을 종료합니다.")

        



        # 창업자금 증여세 과세특례
        # 조특법 제30조의5 및 상증세법 제53조/제56조 법령 100% 검증 완료
        st.subheader("5. 창업자금 증여세 과세특례 (조특법 제30조의5)")
        
        if gift_plan == "있음" and gift_amount > 0:
            
            # [세법 교정] 업종 맵의 'inc' 항목을 통한 특례 적격 여부 사전 검증
            # upstream에서 선택된 업종 딕셔너리의 "inc" 결과값을 변수로 받아와 판정합니다.
            is_inc_eligible = is_eligible_business
            
            if not is_inc_eligible:
                st.error("❌ **[특례 적용 불가 업종] 선택하신 업종은 창업세액감면(조특법 제6조) 대상이 아니므로 본 특례를 적용할 수 없습니다.**")
                st.write("창업자금 증여세 과세특례는 감면 대상 업종에 한해서만 지원됩니다. 이에 따라 **일반 증여세율**이 전액 적용됩니다.")
                
                # 일반 증여세 기본 연산 (대한민국 상증세법 최고세율 50% 반영)
                normal_tax_base = max(0.0, gift_amount - 50000000)
                if normal_tax_base <= 100000000: normal_gift_tax = normal_tax_base * 0.10
                elif normal_tax_base <= 500000000: normal_gift_tax = (normal_tax_base * 0.20) - 10000000
                elif normal_tax_base <= 1000000000: normal_gift_tax = (normal_tax_base * 0.30) - 60000000
                elif normal_tax_base <= 3000000000: normal_gift_tax = (normal_tax_base * 0.40) - 160000000
                else: normal_gift_tax = (normal_tax_base * 0.50) - 460000000 # 👈 최고세율 50% 교정 완료
                    
                normal_gift_tax = max(0.0, normal_gift_tax)
                st.warning(f"🔶 **최종 납부할 일반 증여세: 약 {int(normal_gift_tax):,}원**")
                
            else:
                # [세법 교정 1] 일반 증여세의 과세표준(증여가액 - 성인자녀공제 5천만 원) 선행 연산
                # 근거: 상증세법 제53조 및 제55조 (절세 효과 비교 목적 전체 금액 연산)
                normal_tax_base = max(0.0, gift_amount - 50000000)
                
                # [세법 교정 2] 정확한 법정 기본세율 매트릭스 및 누진공제액 적용 (상증세법 제56조 최고세율 50%)
                if normal_tax_base <= 100000000: normal_gift_tax = normal_tax_base * 0.10
                elif normal_tax_base <= 500000000: normal_gift_tax = (normal_tax_base * 0.20) - 10000000
                elif normal_tax_base <= 1000000000: normal_gift_tax = (normal_tax_base * 0.30) - 60000000
                elif normal_tax_base <= 3000000000: normal_gift_tax = (normal_tax_base * 0.40) - 160000000
                else: normal_gift_tax = (normal_tax_base * 0.50) - 460000000
                normal_gift_tax = max(0.0, normal_gift_tax)

                # [세법 교정 3] 요청하신 한도 과세가액 50억 원 기준 컷오프 및 초과분 일반 과세 안분 연산
                LIMIT_AMOUNT = 5000000000  # 법정 한도 50억 원 고정
                special_target_amount = min(gift_amount, LIMIT_AMOUNT)
                excess_amount = max(0.0, gift_amount - LIMIT_AMOUNT)
                
                # 특례 대상 금액(최대 50억)에 대한 특례 증여세 계산
                if special_target_amount <= 500000000:
                    special_gift_tax = 0.0  # 5억 원까지는 전액 공제
                else:
                    special_gift_tax = (special_target_amount - 500000000) * 0.10  # 5억 초과분은 10% 단일세율
                
                # 50억 원을 초과하는 금액이 있다면 초과분은 일반 증여세율(누진세율)로 정밀 계산 후 특례 세액에 합산
                if excess_amount > 0:
                    excess_tax_base = max(0.0, excess_amount - 50000000)  # 일반공제 5천만 원 차감
                    if excess_tax_base <= 100000000: excess_tax = excess_tax_base * 0.10
                    elif excess_tax_base <= 500000000: excess_tax = (excess_tax_base * 0.20) - 10000000
                    elif excess_tax_base <= 1000000000: excess_tax = (excess_tax_base * 0.30) - 60000000
                    elif excess_tax_base <= 3000000000: excess_tax = (excess_tax_base * 0.40) - 160000000
                    else: excess_tax = (excess_tax_base * 0.50) - 460000000
                    special_gift_tax += max(0.0, excess_tax)
                    
                # 3. 아낀 세금 (정밀 연산)
                gift_tax_savings = max(0.0, normal_gift_tax - special_gift_tax)

                # --- 결과 UI 출력 ---
                st.success(f"🎁 **[특례 활성화] 창업자금 증여세 과세특례 적용 결과**")
                st.write(f"- 총 증여 자금: **{int(gift_amount):,}원** (특례 인정 한도: 5,000,000,000원)")
                st.write(f"- **기본 면제 금액 (비과세): 500,000,000원 (5억 전액 공제)**")
                
                if excess_amount > 0:
                    st.error(f"⚠️ **[한도 초과 고지]** 특례 법정 한도인 50억 원을 **{int(excess_amount):,}원** 초과하였습니다. 초과분은 일반 누진세율로 합산되어 계산되었습니다.")
                
                if special_gift_tax == 0:
                    st.balloons()
                    st.success(f"🎉 **최종 납부할 증여세: 0원 (전액 면제!)**")
                else:
                    st.warning(f"🔶 **최종 납부할 특례 증여세: 약 {int(special_gift_tax):,}원** (5억 초과분 10% 및 한도 초과분 반영)")
                    
                if gift_tax_savings > 0:
                    st.info(f"📈 **일반 증여 대비 절세 효과: 약 {int(gift_tax_savings):,}원 절감 효과**")
                    st.caption("※ 일반 직계존속 증여 시 공제(5천만 원) 및 상증세법 제56조 기본 누진세율(최고세율 50%)과 대조한 결과입니다.")
                    
                st.error("⚠️ **[조특법 제30조의5 제4항 사후관리 의무 공지]**")
                st.write("- **창업 의무:** 증여받은 날로부터 **2년 이내**에 법정 창업을 완료해야 합니다.")
                st.write("- **자금 소진:** 증여받은 날로부터 **4년 이내**에 창업 목적으로 전액 사용(소진)해야 합니다.")
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


