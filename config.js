window.MODUMODU_SITE = {
  contactEmail: "modumoduai@gmail.com",
  contactPhone: "010-9214-6997",
  contactLandline: "070-7629-9306",
  contactKakao: "",
  contactBank: "안내 후 개별 전달",
  maxPcs: 0,
  /** 공개 주소. 링크 공유·FAQ 공유에 이 주소를 씁니다. */
  siteUrl: "https://modumoduai.github.io/modumodu-ai-site",
  /** 회원가입 주소. 비어 있으면 가입 버튼이 준비 중으로 남습니다. */
  memberApi: "https://43-200-32-76.sslip.io:8443",
  /** 프로그램 내려받기 (Windows). 업데이트를 게시하면 항상 최신 셀러용 설치 파일을 가리킵니다. */
  downloadUrl: "https://github.com/MODUMODUAI/smartstore-uploader/releases/latest/download/MODUMODU-seller-setup.zip",

  /**
   * 포트원(구 아임포트) 가맹점 식별코드.
   * 예: "imp00000000"
   * 비어 있으면 결제창 대신 안내만 보여 줍니다.
   * https://admin.portone.io 에서 발급·채널(카카오페이/네이버페이/토스페이)을 켠 뒤 넣으세요.
   */
  portoneImpCode: "",

  /**
   * 결제사 설정 (승인 메일이 오면 여기만 채우면 됩니다)
   * - inicisMid: KG이니시스 상점아이디(MID). 포트원에 이니시스 채널이 하나뿐이면 비워 둬도 됩니다.
   * - use: "inicis" 가 기본. 이니시스에 문제가 생기면 "kpn" 으로 바꾸면 한국결제네트워크로 결제합니다.
   * 포트원 REST API 키·시크릿은 여기 넣지 않습니다 (서버 /opt/modumodu/data/portone.json 에만).
   */
  pg: {
    use: "inicis",
    inicisMid: "",
    kpnMid: "",
  },
  plans: {
    trial: { label: "프로그램 7일 무료", price: "0원", amount: 0, months: 0 },
    m1: { label: "프로그램 1개월 + 무료 7일", price: "80,000원", amount: 80000, was: "200,000원", months: 1 },
    m3: { label: "프로그램 3개월 + 무료 7일", price: "210,000원", amount: 210000, was: "600,000원", months: 3 },
    m6: { label: "프로그램 6개월 + 무료 7일", price: "360,000원", amount: 360000, was: "1,200,000원", months: 6 },
    y1: { label: "프로그램 1년 + 무료 7일", price: "600,000원", amount: 600000, was: "2,400,000원", months: 12 },
    ownerclan: { label: "오너클랜만 추가", price: "30,000원", amount: 30000, months: 1, ownerclanOnly: true },
  },
  /** AI 포인트 충전 (프로그램 이용료와 따로). 서버 app/payments.py 의 AI_POINT_PACKS 와 금액을 맞춥니다. */
  aiPoints: {
    p1000: { label: "1,000포인트", points: 1000, amount: 9900 },
    p5000: { label: "5,000포인트", points: 5000, amount: 39000 },
    p10000: { label: "10,000포인트", points: 10000, amount: 69000 },
  },
  mallAccounts: {
    freeCount: 20,
    packSize: 10,
    packMonthly: 50000,
  },
  supplier: {
    freeCount: 10,
    packSize: 10,
    packMonthly: 50000,
    ownerclanMonthly: 30000,
  },
  /**
   * 결제: KG이니시스 (포트원 연동). 카드 결제창 안에서 카카오페이·네이버페이·토스페이 등 간편결제도 고를 수 있습니다.
   * 포트원 관리자에서 KG이니시스 채널을 켜고, 이니시스 상점아이디(MID)가 있으면 pg 를 "html5_inicis.MID값" 으로 바꿉니다.
   */
  payMethods: {
    card: { label: "카드·간편결제", method: "card" },
    trans: { label: "계좌이체", method: "trans" },
  },
};
