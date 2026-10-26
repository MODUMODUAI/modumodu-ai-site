window.MODUMODU_SITE = {
  contactEmail: "wjmorning@naver.com",
  contactPhone: "010-9214-6997",
  contactKakao: "",
  contactBank: "안내 후 개별 전달",
  maxPcs: 5,
  /** 공개 주소. 링크 공유·FAQ 공유에 이 주소를 씁니다. */
  siteUrl: "https://modumoduai.github.io/modumodu-ai-site",
  /** 회원가입 주소. 비어 있으면 가입 버튼이 준비 중으로 남습니다. */
  memberApi: "https://49.247.136.222:8443",

  /**
   * 포트원(구 아임포트) 가맹점 식별코드.
   * 예: "imp00000000"
   * 비어 있으면 결제창 대신 안내만 보여 줍니다.
   * https://admin.portone.io 에서 발급·채널(카카오페이/네이버페이/토스페이)을 켠 뒤 넣으세요.
   */
  portoneImpCode: "",
  plans: {
    trial: { label: "프로그램 15일 무료", price: "0원", amount: 0, months: 0 },
    m1: { label: "프로그램 1개월", price: "80,000원", amount: 80000, was: "200,000원", months: 1 },
    m3: { label: "프로그램 3개월", price: "210,000원", amount: 210000, was: "600,000원", months: 3 },
    m6: { label: "프로그램 6개월", price: "360,000원", amount: 360000, was: "1,200,000원", months: 6 },
    y1: { label: "프로그램 1년", price: "600,000원", amount: 600000, was: "2,400,000원", months: 12 },
  },
  supplier: {
    freeCount: 10,
    packSize: 10,
    packMonthly: 50000,
    ownerclanMonthly: 30000,
  },
  payMethods: {
    kakaopay: { label: "카카오페이", pg: "kakaopay" },
    naverpay: { label: "네이버페이", pg: "naverpay" },
    tosspay: { label: "토스페이", pg: "tosspay" },
  },
};
