# -*- coding: utf-8 -*-
"""현재 프로그램 화면을 가상 로그인·상품으로 찍어 홈페이지 샘플을 맞춥니다."""
import base64
from pathlib import Path

from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent
BASE = "http://127.0.0.1:8791"

HIDE = """
#appQuit, #backupWarning, .loading-overlay, #globalBusy, #toast, #menuTip, #settingsTabCustomers { display: none !important; }
#appEdition { display: none !important; }
"""

INJECT = r"""
() => {
  const productsData = [
    ['대용량 스텐 보온병 1L 텀블러 세트 캠핑용', 'BM-TUM100', 'SAMPLE-1000'],
    ['접이식 캠핑 테이블 휴대용 야외 탁자', 'CP-TBL200', 'SAMPLE-1001'],
    ['무선 미니 선풍기 USB 충전식 탁상형', 'FN-MINI30', 'SAMPLE-1002'],
    ['규조토 발매트 욕실 흡수 발판 대형', 'JM-MAT40', 'SAMPLE-1003'],
    ['실리콘 주방장갑 내열 오븐장갑 2개입', 'SL-GLV02', 'SAMPLE-1004'],
    ['LED 데스크램프 스탠드 조명 밝기조절', 'LD-DESK50', 'SAMPLE-1005'],
    ['진공 압축백 이불 옷 수납팩 10매', 'VC-BAG10', 'SAMPLE-1006'],
    ['원목 트레이 홈카페 티테이블 쟁반', 'WD-TRY01', 'SAMPLE-1007'],
    ['세라믹 머그컵 세트 선물용 350ml', 'CR-MUG03', 'SAMPLE-1008'],
    ['휴대용 넥밴드 선풍기 여름 캠핑', 'NB-FAN20', 'SAMPLE-1009'],
    ['다용도 수납 정리함 서랍형 3단', 'ST-BOX3', 'SAMPLE-1010'],
    ['주방 가위 세트 야채칼 포함 4종', 'KT-SC04', 'SAMPLE-1011'],
    ['충전식 미니 가습기 USB 무드등', 'HM-USB12', 'SAMPLE-1012'],
    ['접이식 세탁바구니 대용량 빨래통', 'LB-BSK08', 'SAMPLE-1013'],
    ['논슬립 욕실 발판 매트 미끄럼방지', 'BT-MAT22', 'SAMPLE-1014'],
    ['스테인리스 수저세트 가족용 10인', 'SP-SET10', 'SAMPLE-1015'],
    ['차량용 무선 충전기 거치대 고속', 'CR-CHG07', 'SAMPLE-1016'],
    ['방수 피크닉 매트 대형 돗자리', 'PK-MAT90', 'SAMPLE-1017'],
    ['유리 밀폐용기 세트 냉장고 보관', 'GL-BOX06', 'SAMPLE-1018'],
    ['블루투스 이어폰 노이즈캔슬링', 'BT-EAR01', 'SAMPLE-1019'],
    ['메모리폼 목베개 여행용 쿠션', 'NK-PIL03', 'SAMPLE-1020'],
    ['주방 칼도마 세트 항균 도마포함', 'KN-BRD05', 'SAMPLE-1021'],
  ];
  const brands = ['라이트홈', '캠프라이프', '홈디포', '리빙픽'];
  const suppliers = ['도매플러스', '공급마트', '오너클랜'];
  const malls = [
    ['demo-ss-1', '블루마켓'],
    ['demo-ss-2', '그린스토어'],
    ['demo-cp-1', '쿠팡홈샵'],
    ['demo-11-1', '일레븐샵'],
  ];
  const categories = [
    '생활/건강 > 주방용품 > 텀블러',
    '스포츠/레저 > 캠핑 > 테이블',
    '가전디지털 > 계절가전 > 선풍기',
    '생활/건강 > 욕실용품 > 발매트',
  ];
  const fakeMarkets = [
    { id: 'demo-ss-1', channel: 'smartstore', name: '블루마켓', login_id: 'seller-a', url: 'https://smartstore.naver.com/bluemarket', naver_account_id: 'ncp_sample_01', is_default: true, api_key_set: true, api_secret_set: true, login_password_set: true },
    { id: 'demo-ss-2', channel: 'smartstore', name: '그린스토어', login_id: 'seller-b', url: 'https://smartstore.naver.com/greenstore', naver_account_id: 'ncp_sample_02', api_key_set: true, api_secret_set: true, login_password_set: true },
    { id: 'demo-ss-3', channel: 'smartstore', name: '스카이홈', login_id: 'seller-c', url: 'https://smartstore.naver.com/skyhome', naver_account_id: 'ncp_sample_03', api_key_set: true, api_secret_set: true, login_password_set: true },
    { id: 'demo-ss-4', channel: 'smartstore', name: '라이트샵', login_id: 'seller-d', url: 'https://smartstore.naver.com/lightshop', naver_account_id: 'ncp_sample_04', api_key_set: true, api_secret_set: true, login_password_set: true },
    { id: 'demo-cp-1', channel: 'coupang', name: '쿠팡홈샵', login_id: 'coupang01', vendor_code: 'A00012345', api_key_set: true, api_secret_set: true, login_password_set: true },
    { id: 'demo-cp-2', channel: 'coupang', name: '로켓리빙', login_id: 'coupang02', vendor_code: 'A00067890', api_key_set: true, api_secret_set: true, login_password_set: true },
    { id: 'demo-au-1', channel: 'auction', name: '옥션리빙몰', login_id: 'auction01', esm_id: 'esm_sample_01', login_password_set: true },
    { id: 'demo-gm-1', channel: 'gmarket', name: '지마켓하우스', login_id: 'gmarket01', esm_id: 'esm_sample_02', login_password_set: true },
    { id: 'demo-11-1', channel: '11st', name: '일레븐샵', login_id: 'st11_01', login_password_set: true },
    { id: 'demo-11-2', channel: '11st', name: '엘레븐몰', login_id: 'st11_02', login_password_set: true },
    { id: 'demo-ts-1', channel: 'toss', name: '토스홈', login_id: 'toss01', login_password_set: true },
    { id: 'demo-lo-1', channel: 'lotteon', name: '롯데리빙', login_id: 'lotte01', login_password_set: true },
    { id: 'demo-kk-1', channel: 'kakao', name: '카카오홈샵', login_id: 'kakao01', login_password_set: true },
    { id: 'demo-ssg-1', channel: 'ssg', name: '쓱리빙', login_id: 'ssg01', login_password_set: true },
    { id: 'demo-tm-1', channel: 'temu', name: '테무리빙', login_id: 'temu01', login_password_set: true },
  ];
  markets.splice(0, markets.length, ...fakeMarkets);
  if (typeof channelExpanded !== 'undefined') {
    Object.keys(channelExpanded).forEach((key) => { channelExpanded[key] = true; });
    ['smartstore','coupang','auction','gmarket','11st','toss','lotteon','kakao','ssg','temu'].forEach((key) => { channelExpanded[key] = true; });
  }
  if (typeof sourceExpanded !== 'undefined') sourceExpanded = true;
  products = productsData.map((row, index) => {
    const mall = malls[index % malls.length];
    return {
      id: 'sample-' + index,
      name: row[0],
      model: row[1],
      seller_code: row[2],
      stock: 40 + (index % 8) * 10,
      cost: 8900 + (index % 12) * 700,
      price: 19800 + (index % 12) * 1500,
      brand: brands[index % brands.length],
      manufacturer: brands[(index + 1) % brands.length],
      origin: '상세설명참조',
      as_phone: '1588-0000',
      as_guide: '평일 10-17시 고객센터',
      wholesale_name: suppliers[index % suppliers.length],
      wholesale_soldout: false,
      market_id: mall[0],
      market_name: mall[1],
      category_name: categories[index % categories.length],
      created_at: '2026-10-' + String(10 + (index % 15)).padStart(2, '0'),
      status: index % 4 === 0 ? 'registered' : 'collected',
      options: [{ name: '색상', values: ['실버', '블랙'] }],
      attributes: [{ name: '소재', value: '스테인리스' }],
      tags: ['생활용품', '홈인테리어', '선물추천'],
      tax_type: 'TAX',
      minor_purchasable: true,
      source_url: 'https://example.com/p/' + row[2].toLowerCase(),
      images: [],
      extra_components: '',
      memo: '샘플 상품',
      summary: row[0],
      origin_product_no: 'ORG' + String(10000 + index),
      channel_product_no: 'CH' + String(20000 + index),
    };
  });
  selectedIds = new Set([products[0].id]);
  current = products[0];
  marketFilter = 'all';
  renderSheets();
  fillMarketTree();
  fillPreview();
  const preview = document.querySelector('#previewText');
  if (preview) preview.textContent = products[0].name + ' · ' + products[0].seller_code;
  const account = document.querySelector('#accountUse');
  if (account) {
    account.hidden = false;
    account.textContent = 'demo01 · 사용기한 2027-04-26';
  }
  const edition = document.querySelector('#appEdition');
  if (edition) edition.textContent = '';
  document.querySelectorAll('#marketTree .market-count, #orderMarketTree .market-count').forEach((el, idx) => {
    const n = [22, 8, 6, 4, 4, 3, 3, 2, 2, 2, 1, 1][idx % 12];
    el.textContent = '(' + n.toLocaleString('ko-KR') + ')';
  });
  document.querySelectorAll('#logList li, .job-log li').forEach((el) => {
    el.textContent = '샘플 화면입니다.';
  });
  const count = document.querySelector('#productFilterCount');
  if (count) count.textContent = products.length + '개';
  return products.length;
}
"""


def shot(page, name):
    page.mouse.move(12, 12)
    page.evaluate(
        """() => {
          const toast = document.querySelector('#toast');
          if (toast) toast.className = '';
          const tip = document.querySelector('#menuTip');
          if (tip) tip.hidden = true;
          document.querySelectorAll('#logList li, .job-log li').forEach((el) => {
            if (/비어 있습니다|data 폴더/.test(el.textContent || '')) el.textContent = '샘플 화면입니다.';
          });
        }"""
    )
    page.screenshot(path=str(OUT / name), full_page=False)


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
        page.goto(BASE + "/", wait_until="networkidle", timeout=90000)
        page.wait_for_function("() => typeof markets !== 'undefined' && typeof renderSheets === 'function'", timeout=30000)
        page.wait_for_timeout(400)
        page.add_style_tag(content=HIDE)
        page.evaluate(INJECT)
        page.evaluate(
            """() => {
              const wrap = document.querySelector('#viewProducts .grid-wrap');
              const nameTh = document.querySelector('#productGrid th');
              const headers = [...document.querySelectorAll('#productGrid thead th')];
              const target = headers.find((th) => (th.textContent || '').trim() === '상품명');
              if (wrap && target) wrap.scrollLeft = Math.max(0, target.offsetLeft - 240);
            }"""
        )
        page.wait_for_timeout(200)
        shot(page, "01-products.png")

        page.locator("#appTabOrders").click()
        page.wait_for_timeout(400)
        page.locator("#orderDateFrom").fill("2026-08-01")
        page.locator("#orderDateTo").fill("2026-10-26")
        page.evaluate(
            """() => {
              const names = ['김민수','이서연','박지훈','최유진','정하늘','한도윤'];
              const stores = ['블루마켓','쿠팡홈샵','일레븐샵','그린스토어','로켓리빙','스카이홈','옥션리빙몰','토스홈'];
              const products = [
                '대용량 스텐 보온병 1L 텀블러 세트',
                '무선 미니 선풍기 USB 충전식',
                '접이식 캠핑 의자 경량 낚시의자',
                '실리콘 수저통 주방 정리 홀더',
                '충전식 미니 가습기 USB 무드등',
                '규조토 발매트 욕실 흡수 발판',
              ];
              const suppliers = ['도매플러스','공급마트','오너클랜'];
              const marketIds = ['demo-ss-1','demo-cp-1','demo-11-1','demo-ss-2'];
              orders = [];
              for (let i = 0; i < 18; i++) {
                const day = String(12 + (i % 14)).padStart(2, '0');
                orders.push({
                  id: 'ord-' + i,
                  status: 'PAYED',
                  place_status: '',
                  market_id: marketIds[i % marketIds.length],
                  channel: 'smartstore',
                  mall_id: 'seller-a',
                  order_id: '202610' + String(10000 + i),
                  product_order_id: '202610' + String(10000 + i),
                  order_date: '2026-10-' + day + 'T10:12:00',
                  payment_date: '2026-10-' + day + 'T10:12:00',
                  buyer_name: names[i % names.length],
                  receiver_name: names[(i + 2) % names.length],
                  receiver_tel: '010-1000-' + String(1000 + i),
                  buyer_tel: '010-2000-' + String(1000 + i),
                  product_name: products[i % products.length],
                  option: '색상:실버',
                  quantity: (i % 3) + 1,
                  unit_price: 19800 + i * 500,
                  total_price: 19800 + i * 500,
                  payment_amount: 19800 + i * 500,
                  channel_product_no: String(10000000001 + i),
                  wholesale_name: suppliers[i % suppliers.length],
                  zipcode: '06000',
                  address1: '서울특별시 샘플구 예시로',
                  address2: String(10 + i),
                  shipping_memo: '',
                  delivery_fee: 0,
                  commission: 2000,
                });
              }
              ordersCollected = true;
              orderTab = 'new';
              orderMarketFilter = 'all';
              orderQuery = '';
              if (typeof fillOrderMarketTree === 'function') fillOrderMarketTree();
              renderOrders();
              const account = document.querySelector('#accountUse');
              if (account) {
                account.hidden = false;
                account.textContent = 'demo01 · 사용기한 2027-04-26';
              }
            }"""
        )
        page.wait_for_timeout(300)
        shot(page, "02-orders.png")

        page.locator("#appTabInquiries").click()
        page.wait_for_timeout(400)
        page.locator("#inquiryDateFrom").fill("2026-08-01")
        page.locator("#inquiryDateTo").fill("2026-10-26")
        page.evaluate(
            """() => {
              const products = [
                '대용량 스텐 보온병 1L 텀블러 세트',
                '충전식 미니 가습기 USB 무드등',
                '접이식 캠핑 의자 경량',
                '규조토 발매트 욕실 대형',
              ];
              inquiries = [0, 1, 2, 3].map((i) => ({
                id: 'inq-' + i,
                channel: 'smartstore',
                market_id: 'demo-ss-1',
                mall_id: 'seller-a',
                store_name: '블루마켓',
                order_id: 'ORD' + String(100000 + i),
                product_no: String(10000000001 + i),
                product_name: products[i],
                created_at: '2026-10-' + String(16 + i) + 'T10:04:00',
                writer: '김**',
                title: '배송 일정 문의',
                content: '배송 일정 문의 샘플입니다. 언제쯤 받을 수 있을까요?',
                status: '미답변',
                answer: '',
              }));
              currentInquiryId = inquiries[0].id;
              selectedInquiryIds = new Set([inquiries[0].id]);
              inquiryUpdatedAt = '2026.10.26 16:10';
              renderInquiryList();
              fillInquiryDetail(inquiries[0]);
              const content = document.querySelector('#inquiryContent');
              if (content) content.value = inquiries[0].content;
            }"""
        )
        page.wait_for_timeout(300)
        shot(page, "03-inquiries.png")

        page.locator("#appTabWholesalers").click()
        page.wait_for_timeout(300)
        page.evaluate(
            """() => {
              wholesalers = [
                { id: 'w1', name: '도매플러스', url: 'https://domeplus.example/', type: 'cafe24', type_label: '카페24', login_id: 'seller01@example.com', enabled: true, memo: '생활용품 샘플 공급처', login_password_set: true },
                { id: 'w2', name: '공급마트', url: 'https://supplymart.example/', type: 'cafe24', type_label: '카페24', login_id: 'seller02', enabled: true, memo: '주방용품 샘플 공급처', login_password_set: true },
                { id: 'w3', name: '오너클랜', url: 'https://domedome.example/', type: 'ownerclan', type_label: '오너클랜', login_id: 'hub01', enabled: true, memo: '전체 상품 샘플 연결', login_password_set: true },
              ];
              currentWholesalerId = 'w1';
              renderWholesalerSheet();
              fillWholesaleForm(wholesalers[0]);
              const form = document.querySelector('#wholesaleForm');
              if (form) {
                form.elements.login_password.value = 'sample-pass';
                form.elements.name.placeholder = '예: 도매플러스';
                form.elements.url.placeholder = 'https://domeplus.example/';
              }
            }"""
        )
        page.wait_for_timeout(200)
        shot(page, "06-wholesalers.png")

        page.locator("#appTabCollect").click()
        page.wait_for_timeout(400)
        product_images = []
        for path in sorted((OUT / "sample-products").glob("*.png")):
            product_images.append("data:image/png;base64," + base64.b64encode(path.read_bytes()).decode("ascii"))
        page.evaluate(
            """(images) => {
              const samples = [
                '실리콘 의자캡 소음방지 16개입',
                '빨래집게 세트 강력집게 50개',
                '핫팩 대형 12시간 지속 20매',
                '여행용 수납 파우치 세트 5종',
                '남성 양말 10족 세트 스포츠',
                '주방 수세미 거품망 세트 10개',
                '양말 발목형 쿠션 5족',
                '접이식 빨래건조대 미니',
                '캠핑 랜턴 USB 충전식',
                '욕실 코너선반 흡착식',
                '어린이 양말 5족 세트',
                '주방 행주 12매 세트',
              ];
              selectedCollectSupplierId = 'w3';
              renderCollectSupplierTree();
              showCollectPane('ownerclan');
              ownerclanProducts = samples.map((name, index) => ({
                code: 'SAMPLE' + String(2000 + index),
                name,
                supplier: '공급사' + String(10 + (index % 5)),
                price: 1200 + index * 350,
                shipping: index % 3 === 0 ? 0 : 3000,
                shipping_type: index % 3 === 0 ? 'F' : 'P',
                image: images[index] || '',
                url: 'https://domedome.example/item/SAMPLE' + String(2000 + index),
              }));
              ownerclanPage = 1;
              ownerclanPages = 3;
              ownerclanExcludedCount = 0;
              renderOwnerclanProducts();
              const list = document.querySelector('#ownerclanProductList');
              if (list) list.style.gridTemplateColumns = 'repeat(4, minmax(0, 1fr))';
              document.querySelectorAll('#ownerclanProductList a').forEach((node) => {
                node.style.aspectRatio = '5 / 2';
              });
              document.querySelectorAll('#ownerclanProductList img').forEach((node) => {
                node.style.objectFit = 'contain';
              });
              const total = document.querySelector('#ownerclanProductTotal');
              if (total) total.textContent = '총 128개';
              document.querySelectorAll('#ownerclanProductList a').forEach((link) => {
                link.removeAttribute('href');
                link.title = '상품 보기';
              });
            }""",
            product_images,
        )
        page.wait_for_timeout(300)
        shot(page, "04-ownerclan.png")

        page.locator("#appTabSettings").click()
        page.wait_for_timeout(300)
        with page.expect_response(lambda r: "/api/markets" in r.url, timeout=8000):
            page.locator("#settingsTabMarkets").click()
        page.wait_for_timeout(200)
        page.evaluate(
            """() => {
              markets.splice(0, markets.length, ...[
                { id: 'demo-ss-1', channel: 'smartstore', name: '블루마켓', login_id: 'seller-a', url: 'https://smartstore.naver.com/bluemarket', naver_account_id: 'ncp_sample_01', is_default: true, api_key_set: true, api_secret_set: true, login_password_set: true },
                { id: 'demo-ss-2', channel: 'smartstore', name: '그린스토어', login_id: 'seller-b', api_key_set: true, api_secret_set: true, login_password_set: true },
                { id: 'demo-cp-1', channel: 'coupang', name: '쿠팡홈샵', login_id: 'coupang01', vendor_code: 'A00012345', api_key_set: true, api_secret_set: true, login_password_set: true },
                { id: 'demo-11-1', channel: '11st', name: '일레븐샵', login_id: 'st11_01', login_password_set: true },
                { id: 'demo-au-1', channel: 'auction', name: '옥션리빙몰', login_id: 'auction01', esm_id: 'esm_sample_01', login_password_set: true },
              ]);
              if (typeof fillMarketTable === 'function') fillMarketTable();
              const form = document.querySelector('#marketForm');
              if (!form) return;
              const set = (name, value) => { const el = form.querySelector('[name="' + name + '"]'); if (el) el.value = value; };
              set('name', '블루마켓');
              set('url', 'https://smartstore.naver.com/bluemarket');
              set('naver_account_id', 'ncp_sample_01');
              set('login_id', 'seller-a');
              set('api_key', '********');
              set('api_secret', '********');
              set('login_password', 'sample-pass');
              set('vendor_code', 'A00012345');
              form.querySelectorAll('input[type="password"]').forEach((el) => { el.value = 'sample-pass'; });
              const message = document.querySelector('#marketMessage');
              if (message) message.textContent = '등록된 마켓 5개 · 위 목록에서 고르세요.';
              const wrap = document.querySelector('#viewSettings .delivery-table-wrap');
              if (wrap) wrap.scrollTop = 0;
            }"""
        )
        page.wait_for_timeout(200)
        shot(page, "05-settings.png")
        browser.close()

    for path in sorted(OUT.glob("0*.png")):
        print(path.name, path.stat().st_size)


if __name__ == "__main__":
    main()
