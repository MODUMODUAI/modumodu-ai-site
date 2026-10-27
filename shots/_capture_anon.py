# -*- coding: utf-8 -*-
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent
BASE = "http://127.0.0.1:8787"

HIDE = """
#arrivalNotice, #appEdition, .titlebar-theme, #appQuit { display: none !important; }
#globalStatusLog, .status-log-global { display: none !important; }
.loading-overlay, .spinner, .busy-overlay, #globalBusy, .app-busy { display: none !important; }
#viewSettings .delivery-table-wrap { max-height: 360px !important; height: auto !important; }
"""

ANON_JS = r"""
() => {
  const storeMap = [
    [/신일N위시웨이/g, '블루마켓'],
    [/신일\s*N\s*위시웨이/g, '블루마켓'],
    [/신일전자/g, '라이트홈'],
    [/신일/g, '라이트홈'],
    [/위시웨이/g, '블루마켓'],
    [/wishway/gi, 'bluemarket'],
    [/shinil/gi, 'lighthome'],
    [/헤마스\s*사무실업소용가정용[^\s]*/g, '그린스토어'],
    [/헤마스/g, '그린스토어'],
    [/hemas/gi, 'greenstore'],
    [/사무실업소용가정용가성비선물/g, '라이트샵'],
    [/사무실업소용가정용[^\s]*/g, '라이트샵'],
    [/사무실업소용[^\s]*/g, '라이트샵'],
    [/사무실\/집 가성비 햇빛가리개/g, '라이트샵'],
    [/가성비선물/g, '라이트샵'],
    [/가성비[^\s]{0,20}/g, '라이트샵'],
    [/바람집/g, '스카이홈'],
    [/baramjip/gi, 'skyhome'],
    [/openning/gi, 'mintshop'],
    [/오픈닝/g, '민트샵'],
    [/케이페이지/g, '도매플러스'],
    [/kpage\.co\.kr/gi, 'domeplus.example'],
    [/kpage/gi, 'domeplus'],
    [/셀파이|셀피아/g, '공급마트'],
    [/sellpie\.co\.kr/gi, 'supplymart.example'],
    [/sellpie/gi, 'supplymart'],
    [/오너클랜랭킹순/g, '인기순'],
    [/오너클랜/g, '도매도매'],
    [/ownerclan\.com/gi, 'domedome.example'],
    [/ownerclan/gi, 'domedome'],
    [/wjmorning@naver\.com/gi, 'seller01@example.com'],
    [/wjmorning/gi, 'seller01'],
    [/newfeeld7/gi, 'seller02'],
    [/ibccomae1/gi, 'owner01'],
    [/ibccomae/gi, 'owner'],
    [/ncp_[a-z0-9_]+/gi, 'ncp_sample_01'],
    [/smartstore\.naver\.com\/[A-Za-z0-9_-]+/gi, 'smartstore.naver.com/bluemarket'],
  ];

  const scrub = (text) => {
    let t = String(text ?? '');
    for (const [re, to] of storeMap) t = t.replace(re, to);
    t = t.replace(/[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}/gi, 'user@example.com');
    return t;
  };

  const walk = (node) => {
    if (!node) return;
    if (node.nodeType === Node.TEXT_NODE) {
      const next = scrub(node.nodeValue);
      if (next !== node.nodeValue) node.nodeValue = next;
      return;
    }
    if (node.nodeType !== Node.ELEMENT_NODE) return;
    if (node.tagName === 'SCRIPT' || node.tagName === 'STYLE') return;
    for (const attr of ['title', 'placeholder', 'aria-label', 'alt', 'value']) {
      if (node.hasAttribute?.(attr)) {
        const cur = node.getAttribute(attr);
        const next = scrub(cur);
        if (next !== cur) node.setAttribute(attr, next);
      }
    }
    if ((node.tagName === 'INPUT' || node.tagName === 'TEXTAREA') && typeof node.value === 'string') {
      const next = scrub(node.value);
      if (next !== node.value) node.value = next;
    }
    for (const child of Array.from(node.childNodes)) walk(child);
  };
  walk(document.body);

  // 모든 채널에 가짜 마켓 계정 주입 (쿠팡·11번가 등 포함)
  const fakeByChannel = {
    smartstore: [
      { id: 'demo-ss-1', channel: 'smartstore', name: '블루마켓', login_id: 'seller-a', url: 'https://smartstore.naver.com/bluemarket', naver_account_id: 'ncp_sample_01', is_default: true },
      { id: 'demo-ss-2', channel: 'smartstore', name: '그린스토어', login_id: 'seller-b', url: 'https://smartstore.naver.com/greenstore', naver_account_id: 'ncp_sample_02' },
      { id: 'demo-ss-3', channel: 'smartstore', name: '스카이홈', login_id: 'seller-c', url: 'https://smartstore.naver.com/skyhome', naver_account_id: 'ncp_sample_03' },
      { id: 'demo-ss-4', channel: 'smartstore', name: '라이트샵', login_id: 'seller-d', url: 'https://smartstore.naver.com/lightshop', naver_account_id: 'ncp_sample_04' },
    ],
    coupang: [
      { id: 'demo-cp-1', channel: 'coupang', name: '쿠팡홈샵', login_id: 'coupang01', vendor_code: 'A00012345', api_key: '••••••••', api_secret: '••••••••' },
      { id: 'demo-cp-2', channel: 'coupang', name: '로켓리빙', login_id: 'coupang02', vendor_code: 'A00067890', api_key: '••••••••', api_secret: '••••••••' },
    ],
    auction: [
      { id: 'demo-au-1', channel: 'auction', name: '옥션리빙몰', login_id: 'auction01', esm_id: 'esm_sample_01' },
    ],
    gmarket: [
      { id: 'demo-gm-1', channel: 'gmarket', name: '지마켓하우스', login_id: 'gmarket01', esm_id: 'esm_sample_02' },
    ],
    '11st': [
      { id: 'demo-11-1', channel: '11st', name: '일레븐샵', login_id: 'st11_01' },
      { id: 'demo-11-2', channel: '11st', name: '엘레븐몰', login_id: 'st11_02' },
    ],
    toss: [
      { id: 'demo-ts-1', channel: 'toss', name: '토스홈', login_id: 'toss01' },
    ],
    lotteon: [
      { id: 'demo-lo-1', channel: 'lotteon', name: '롯데리빙', login_id: 'lotte01' },
    ],
    kakao: [
      { id: 'demo-kk-1', channel: 'kakao', name: '카카오홈샵', login_id: 'kakao01' },
    ],
    ssg: [
      { id: 'demo-ssg-1', channel: 'ssg', name: '쓱리빙', login_id: 'ssg01' },
    ],
    temu: [
      { id: 'demo-tm-1', channel: 'temu', name: '테무리빙', login_id: 'temu01' },
    ],
  };
  if (typeof markets !== 'undefined' && Array.isArray(markets)) {
    const channelName = {
      smartstore: '스마트스토어', coupang: '쿠팡', auction: '옥션', gmarket: 'G마켓',
      '11st': '11번가', toss: '토스쇼핑', lotteon: '롯데ON', kakao: '카카오톡스토어',
      ssg: 'SSG.COM', temu: '테무',
    };
    const next = [];
    Object.entries(fakeByChannel).forEach(([ch, rows]) => {
      if (typeof channelExpanded !== 'undefined') channelExpanded[ch] = true;
      rows.forEach((row) => next.push({
        ...row,
        channel_name: channelName[ch] || ch,
        api_key_set: true,
        api_secret_set: true,
        login_password_set: true,
      }));
    });
    markets.splice(0, markets.length, ...next);
    if (typeof sourceExpanded !== 'undefined') sourceExpanded = true;
    if (typeof fillMarketTree === 'function') fillMarketTree();
    if (typeof fillOrderMarketTree === 'function') fillOrderMarketTree();
    if (typeof fillMarketTable === 'function') fillMarketTable();
    if (typeof fillInquiryMallSelects === 'function') fillInquiryMallSelects();
  }
  // 트리에 남은 실명·빈칸 라벨 강제 교체
  document.querySelectorAll('#marketTree button.market-item, #orderMarketTree button.market-item').forEach((btn) => {
    const label = btn.querySelector('.market-item-label') || btn;
    const t = (label.textContent || '').trim();
    if (/헤마스|위시웨이|바람집|사무실|가성비|openning|오픈닝/i.test(t)) {
      label.textContent = '블루마켓';
      btn.title = '블루마켓';
    }
    if (t === '마켓을 등록하세요') {
      const ch = btn.dataset.channel || '';
      const fallback = {
        coupang: '쿠팡홈샵', auction: '옥션리빙몰', gmarket: '지마켓하우스',
        '11st': '일레븐샵', toss: '토스홈', lotteon: '롯데리빙',
        kakao: '카카오홈샵', ssg: '쓱리빙', temu: '테무리빙', smartstore: '블루마켓',
      };
      const name = fallback[ch] || '샘플스토어';
      label.textContent = name;
      btn.title = name;
      btn.dataset.kind = 'store';
    }
  });

  const fakeProducts = [
    '대용량 스텐 보온병 1L 텀블러 세트 캠핑용',
    '접이식 캠핑 테이블 휴대용 야외 탁자',
    '무선 미니 선풍기 USB 충전식 탁상형',
    '규조토 발매트 욕실 흡수 발판 대형',
    '실리콘 주방장갑 내열 오븐장갑 2개입',
    'LED 데스크램프 스탠드 조명 밝기조절',
    '진공 압축백 이불 옷 수납팩 10매',
    '원목 트레이 홈카페 티테이블 쟁반',
    '세라믹 머그컵 세트 선물용 350ml',
    '휴대용 넥밴드 선풍기 여름 캠핑',
    '다용도 수납 정리함 서랍형 3단',
    '주방 가위 세트 야채칼 포함 4종',
    '충전식 미니 가습기 USB 무드등',
    '접이식 세탁바구니 대용량 빨래통',
    '논슬립 욕실 발판 매트 미끄럼방지',
    '스테인리스 수저세트 가족용 10인',
    '차량용 무선 충전기 거치대 고속',
    '방수 피크닉 매트 대형 돗자리',
    '유리 밀폐용기 세트 냉장고 보관',
    '블루투스 이어폰 노이즈캔슬링',
    '메모리폼 목베개 여행용 쿠션',
    '주방 칼도마 세트 항균 도마포함',
    'LED 센서등 현관 무선 무드등',
    '접이식 옷걸이 세탁용 30개입',
    '캠핑 의자 접이식 경량 낚시의자',
    '실리콘 수저통 주방 정리 홀더',
    '원터치 텀블러 보온보냉 500ml',
    '차량용 쓰레기통 미니 휴지통',
  ];
  const fakeModels = [
    'BM-TUM100', 'CP-TBL200', 'FN-MINI30', 'JM-MAT40',
    'SL-GLV02', 'LD-DESK50', 'VC-BAG10', 'WD-TRY01',
    'CR-MUG03', 'NB-FAN20', 'ST-BOX3', 'KT-SC04',
  ];
  const fakeBrands = ['라이트홈', '캠프라이프', '홈디포', '리빙픽'];
  const fakeSuppliers = ['도매플러스', '공급마트', '도매도매'];
  const fakeCategories = [
    '생활/건강 > 주방용품 > 텀블러',
    '스포츠/레저 > 캠핑 > 테이블',
    '가전디지털 > 계절가전 > 선풍기',
    '생활/건강 > 욕실용품 > 발매트',
    '생활/건강 > 주방용품 > 조리도구',
    '가구/인테리어 > 조명 > 스탠드',
    '생활/건강 > 수납/정리 > 압축팩',
    '가구/인테리어 > 주방가구 > 트레이',
  ];
  const malls = [
    '블루마켓', '그린스토어', '스카이홈', '라이트샵',
    '쿠팡홈샵', '로켓리빙', '일레븐샵', '엘레븐몰',
    '옥션리빙몰', '지마켓하우스', '토스홈', '롯데리빙',
    '카카오홈샵', '쓱리빙', '테무리빙',
  ];

  const setField = (root, field, value) => {
    const input = root.querySelector(`[data-field="${field}"]`);
    if (input) {
      if ('value' in input) input.value = value;
      const view = input.closest('td')?.querySelector('.cell-view');
      if (view) {
        view.textContent = value;
        view.dataset.value = value;
      }
    }
  };

  const headRow = document.querySelector('#viewProducts table.grid thead tr, table.grid thead tr');
  const headers = headRow
    ? [...headRow.querySelectorAll('th')].map((th) => (th.textContent || '').trim())
    : [];
  const col = (label) => headers.findIndex((h) => h === label);

  document.querySelectorAll('#productTable tr').forEach((tr, row) => {
    const name = fakeProducts[row % fakeProducts.length];
    const model = fakeModels[row % fakeModels.length];
    const brand = fakeBrands[row % fakeBrands.length];
    const maker = fakeBrands[(row + 1) % fakeBrands.length];
    const code = 'SAMPLE-' + String(1000 + row);
    const cost = String(8900 + (row % 12) * 700);
    const price = String(19800 + (row % 12) * 1500);
    const stock = String(50 + (row % 9) * 10);
    const cat = fakeCategories[row % fakeCategories.length];
    const url = 'https://example.com/p/' + code.toLowerCase();

    setField(tr, 'name', name);
    setField(tr, 'seller_code', code);
    setField(tr, 'model', model);
    setField(tr, 'brand', brand);
    setField(tr, 'manufacturer', maker);
    setField(tr, 'tags', '생활용품,홈인테리어,선물추천');
    setField(tr, 'summary', name);
    setField(tr, 'origin', '상세설명참조');
    setField(tr, 'stock', stock);
    setField(tr, 'cost', cost);
    setField(tr, 'price', price);
    setField(tr, 'as_phone', '1588-0000');
    setField(tr, 'as_guide', '평일 10-17시 고객센터');
    setField(tr, 'options', '색상:실버,블랙');
    setField(tr, 'attributes', '소재:스테인리스');
    setField(tr, 'source_url', url);
    setField(tr, 'detail_html', '샘플 상세설명입니다.');
    setField(tr, 'extra_components', '');
    setField(tr, 'certification', '');
    setField(tr, 'certification_date', '');
    setField(tr, 'main_ingredient', '');
    setField(tr, 'manufacture_date', '');
    setField(tr, 'expire_date', '');
    setField(tr, 'unit_price', '');
    setField(tr, 'memo', '샘플 상품');

    const tds = tr.querySelectorAll('td');
    const paint = (idx, value) => {
      if (idx < 0 || !tds[idx]) return;
      const btn = tds[idx].querySelector('button.category-pick');
      if (btn) {
        btn.textContent = value;
        btn.title = value;
        return;
      }
      const view = tds[idx].querySelector('.cell-view');
      const input = tds[idx].querySelector('input, textarea');
      const select = tds[idx].querySelector('select');
      if (input) input.value = value;
      if (select) {
        // keep sale/display selects as-is if value matches option
        const opt = [...select.options].find((o) => o.textContent === value || o.value === value);
        if (opt) select.value = opt.value;
      }
      if (view) {
        view.textContent = value;
        view.dataset.value = value;
      } else if (!input && !select && !btn) {
        tds[idx].textContent = value;
      }
    };
    paint(col('수집일'), '2026-10-0' + String(1 + (row % 9)));
    paint(col('등록상태'), row % 3 === 0 ? '등록완료' : '대기');
    paint(col('품절'), '정상');
    paint(col('공급처'), fakeSuppliers[row % fakeSuppliers.length]);
    paint(col('마켓'), malls[row % malls.length]);
    paint(col('카테고리'), cat);
    paint(col('판매자코드'), code);
    paint(col('모델명'), model);
    paint(col('상품명'), name);
    paint(col('재고'), stock);
    paint(col('원가'), cost);
    paint(col('판매가'), price);
    paint(col('브랜드'), brand);
    paint(col('제조사'), maker);
    paint(col('원산지'), '상세설명참조');
    paint(col('A/S번호'), '1588-0000');
    paint(col('A/S안내'), '평일 10-17시 고객센터');
    paint(col('상품태그'), '생활용품,홈인테리어,선물추천');
    paint(col('옵션'), '색상:실버,블랙');
    paint(col('속성'), '소재:스테인리스');
    paint(col('URL'), url);
    paint(col('상세설명'), '샘플 상세설명입니다.');
    paint(col('상품요약'), name);
    paint(col('원상품번호'), 'ORG' + String(10000 + row));
    paint(col('채널상품번호'), 'CH' + String(20000 + row));
    paint(col('비고'), '샘플 상품');
  });

  // 마켓 트리 숫자·상태 문구도 샘플로
  document.querySelectorAll('#marketTree .market-count, #orderMarketTree .market-count').forEach((el, idx) => {
    const n = [1280, 860, 42, 18, 12, 9, 7, 5, 4, 3, 2, 1][idx % 12];
    el.textContent = '(' + n.toLocaleString('ko-KR') + ')';
  });
  document.querySelectorAll('#productFilterCount, #orderFilterCount, #inquiryFilterCount').forEach((el) => {
    if (el) el.textContent = (el.id === 'orderFilterCount' ? '28건' : el.id === 'inquiryFilterCount' ? '4건' : '25개');
  });
  document.querySelectorAll('#workStatus, #jobStatus, .work-status, #statusText, #globalStatus').forEach((el) => {
    if (el && 'textContent' in el) el.textContent = '대기';
  });
  document.querySelectorAll('#statusLog li, #workLog li, .status-log li').forEach((el, idx) => {
    el.textContent = idx === 0 ? '샘플 데이터로 표시 중입니다.' : '저장 완료 (샘플)';
  });

  // bottom preview
  const previewText = document.querySelector('#previewText');
  if (previewText) previewText.textContent = fakeProducts[0] + ' · SAMPLE-1000';
  document.querySelectorAll('.preview-name, #previewName, .product-preview, .bottom .name, .thumb-name').forEach((el) => {
    el.textContent = fakeProducts[0];
  });
  const previewImg = document.querySelector('#previewImage');
  if (previewImg) {
    previewImg.alt = fakeProducts[0];
    previewImg.removeAttribute('src');
    previewImg.src = '';
  }
  // 내 상품/미리보기 이미지만 제거. 도매처(도매도매) 카탈로그 이미지는 유지
  document.querySelectorAll('#productTable img, .preview img, #previewImage').forEach((img) => {
    img.removeAttribute('src');
    img.src = '';
    img.alt = 'sample';
    img.style.background = '#e8eef5';
  });
  document.querySelectorAll('#viewOwnerclan img').forEach((img, idx) => {
    img.alt = fakeProducts[idx % fakeProducts.length];
  });

  // inquiry detail
  const detail = document.querySelector('#inquiryDetail');
  if (detail) {
    detail.querySelectorAll('input, textarea').forEach((el) => {
      el.value = '배송 일정 문의 샘플입니다.';
    });
  }
  return true;
}
"""


def prep(page):
    page.add_style_tag(content=HIDE)
    page.evaluate(ANON_JS)
    page.evaluate(
        """() => {
      const tab = document.querySelector('#appTabOwnerclan');
      if (tab) tab.textContent = '도매도매';
      document.querySelectorAll('option').forEach((opt) => {
        if ((opt.textContent || '').trim() === '오너클랜') opt.textContent = '도매도매';
      });
    }"""
    )


def fill_orders(page):
    page.evaluate(
        """() => {
      const body = document.querySelector('#orderTable');
      if (!body) return 0;
      const names = ['김민수','이서연','박지훈','최유진','정하늘','한도윤'];
      const statuses = ['신규주문','배송중','구매확정','취소','반품'];
      const stores = [
        '블루마켓','쿠팡홈샵','일레븐샵','그린스토어','로켓리빙',
        '스카이홈','엘레븐몰','옥션리빙몰','지마켓하우스','토스홈',
        '롯데리빙','카카오홈샵','쓱리빙','테무리빙','라이트샵',
      ];
      const products = [
        '대용량 스텐 보온병 1L 텀블러 세트',
        '무선 미니 선풍기 USB 충전식',
        '접이식 캠핑 의자 경량 낚시의자',
        '실리콘 수저통 주방 정리 홀더',
        '충전식 미니 가습기 USB 무드등',
        '규조토 발매트 욕실 흡수 발판',
        '원터치 텀블러 보온보냉 500ml',
      ];
      body.innerHTML = '';
      for (let idx = 0; idx < 28; idx++) {
        const tr = document.createElement('tr');
        const vals = [
          idx + 1,
          statuses[idx % statuses.length],
          stores[idx % stores.length],
          names[idx % names.length],
          names[(idx + 2) % names.length],
          '202610' + String(10000 + idx),
          products[idx % products.length],
          (idx % 3) + 1,
          (19800 + (idx * 500)).toLocaleString('ko-KR')
        ];
        vals.forEach((v) => {
          const td = document.createElement('td');
          td.textContent = String(v);
          td.style.padding = '6px 8px';
          td.style.borderBottom = '1px solid #e5e5e5';
          td.style.whiteSpace = 'nowrap';
          tr.appendChild(td);
        });
        body.appendChild(tr);
      }
      const count = document.querySelector('#orderFilterCount');
      if (count) count.textContent = '28건';
      return 28;
    }"""
    )


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1.35)
        page.goto(BASE + "/", wait_until="networkidle", timeout=90000)
        page.wait_for_timeout(1000)
        prep(page)
        page.evaluate(
            """() => {
          const wrap = document.querySelector('#viewProducts .grid-wrap, .grid-wrap');
          const nameTh = document.querySelector('#viewProducts th[data-sort="name"], th.sortable[title*="상품명"]');
          if (wrap && nameTh) {
            // 카테고리~브랜드가 같이 보이도록
            const left = Math.max(0, nameTh.offsetLeft - 420);
            wrap.scrollLeft = left;
          }
        }"""
        )
        page.screenshot(path=str(OUT / "01-products.png"), full_page=False)

        page.locator("#appTabOrders").click()
        page.wait_for_timeout(800)
        page.locator("#orderDateFrom").fill("2026-08-01")
        page.locator("#orderDateTo").fill("2026-10-21")
        fill_orders(page)
        prep(page)
        page.screenshot(path=str(OUT / "02-orders.png"), full_page=False)

        page.locator("#appTabInquiries").click()
        page.wait_for_timeout(900)
        page.locator("#inquiryDateFrom").fill("2026-08-01")
        page.locator("#inquiryDateTo").fill("2026-10-21")
        ic = page.locator("#viewInquiries button.inquiry-collect")
        if ic.count():
            try:
                ic.first.click(timeout=2000)
                page.wait_for_timeout(1800)
            except Exception:
                pass
        page.evaluate(
            """() => {
          const malls = ['04.스마트스토어','05.쿠팡','03.11번가','01.옥션','02.G마켓'];
          const stores = ['bluemarket','coupang01','st11_01','auction01','gmarket01'];
          const names = ['블루마켓','쿠팡홈샵','일레븐샵','옥션리빙몰','지마켓하우스'];
          const products = [
            '대용량 스텐 보온병 1L 텀블러',
            '충전식 미니 가습기 USB',
            '접이식 캠핑 의자 경량',
            '규조토 발매트 욕실 대형',
          ];
          document.querySelectorAll('#viewInquiries table tbody tr').forEach((tr, idx) => {
            const tds = tr.querySelectorAll('td');
            tds.forEach((td, i) => {
              if (i === 1) td.textContent = malls[idx % malls.length];
              else if (i === 2) td.textContent = stores[idx % stores.length];
              else if (i === 3) td.textContent = names[idx % names.length];
              else if (i === 4) td.textContent = names[idx % names.length];
              else if (i === 5) td.textContent = '';
              else if (i === 6) td.textContent = 'ORD' + String(100000 + idx);
              else if (i === 7) td.textContent = String(10000000001 + idx);
              else if (i === 8) td.textContent = products[idx % products.length];
            });
          });
        }"""
        )
        rows = page.locator("#viewInquiries table tbody tr")
        if rows.count():
            try:
                rows.first.click(timeout=2000)
                page.wait_for_timeout(400)
            except Exception:
                pass
        page.evaluate(
            """() => {
          const detail = document.querySelector('#inquiryDetail');
          if (!detail) return;
          detail.hidden = false;
          const setText = (id, text) => { const el = document.getElementById(id); if (el) el.textContent = text; };
          const setVal = (id, text) => { const el = document.getElementById(id); if (el) el.value = text; };
          setText('inquiryMall', '04.스마트스토어');
          setText('inquiryMallId', 'bluemarket');
          setText('inquiryState', '미답변');
          setText('inquiryWhen', '2026-10-06 10:04:41');
          setText('inquiryWriter', '김**');
          setText('inquiryProductNo', '10000000001');
          setText('inquiryProductName', '대용량 스텐 보온병 1L 텀블러 세트');
          setText('inquiryTitle', '[상품문의] 배송 일정 문의');
          setVal('inquiryContent', '배송 일정 문의 샘플입니다. 언제쯤 받을 수 있을까요?');
          setVal('inquiryAnswerView', '');
          setVal('inquiryAnswerAt', '');
          setVal('inquiryAnswerTitle', '');
          setVal('inquiryAnswerDraft', '');
        }"""
        )
        prep(page)
        page.screenshot(path=str(OUT / "03-inquiries.png"), full_page=False)

        page.locator("#appTabWholesalers").click()
        page.wait_for_timeout(800)
        page.evaluate(
            """() => {
          const fake = [
            ['도매플러스','https://domeplus.example/','카페24','seller01@example.com','1280'],
            ['공급마트','https://supplymart.example/','카페24','seller02','540'],
            ['도매도매','https://domedome.example/','도매도매','hub01','120'],
          ];
          document.querySelectorAll('#viewWholesalers tbody tr').forEach((tr, idx) => {
            const tds = tr.querySelectorAll('td');
            const f = fake[idx];
            if (!f) return;
            f.forEach((v, i) => { if (tds[i]) tds[i].textContent = v; });
          });
          document.querySelectorAll('#viewWholesalers input, #viewWholesalers textarea').forEach((el) => {
            const name = (el.name || el.id || '').toLowerCase();
            if (name.includes('name') || name.includes('title')) el.value = '도매플러스';
            else if (name.includes('url') || name.includes('site')) el.value = 'https://domeplus.example/';
            else if (name.includes('id') || name.includes('user') || name.includes('login')) el.value = 'seller01@example.com';
            else if (name.includes('pass')) el.value = '저장되어 있습니다';
            else if (name.includes('memo') || el.tagName === 'TEXTAREA') el.value = '생활용품 도매 샘플 공급처입니다.';
          });
          document.querySelectorAll('#viewWholesalers select, #viewWholesalers option').forEach((el) => {
            if ('textContent' in el && /오너클랜/i.test(el.textContent || '')) el.textContent = '도매도매';
            if ('value' in el && String(el.value || '').toLowerCase() === 'ownerclan') {
              /* keep value for app logic; label already scrubbed above */
            }
          });
        }"""
        )
        prep(page)
        page.screenshot(path=str(OUT / "06-wholesalers.png"), full_page=False)

        page.locator("#appTabOwnerclan").click()
        page.wait_for_timeout(2000)
        page.locator("#ownerclanSearchKeyword").fill("양말")
        page.locator("#ownerclanProductSearch").click()
        for _ in range(50):
            imgs = page.locator("#viewOwnerclan img")
            if imgs.count() >= 12:
                # 실제 썸네일 로딩 대기
                loaded = page.evaluate(
                    """() => [...document.querySelectorAll('#viewOwnerclan img')].filter((img) => img.complete && img.naturalWidth > 8).length"""
                )
                if loaded >= 8:
                    break
            page.wait_for_timeout(400)
        page.wait_for_timeout(800)
        page.evaluate(
            """() => {
          const samples = [
            '실리콘 의자캡 소음방지 16개입',
            '빨래집게 세트 강력집게 50개',
            '핫팩 대형 12시간 지속 20매',
            '여행용 수납 파우치 세트 5종',
            '남성 양말 10족 세트 스포츠',
            '주방 수세미 거품망 세트 10개',
            '양말 발목형 쿠션 5족',
            '접이식 빨래건조대 미니',
          ];
          const tab = document.querySelector('#appTabOwnerclan');
          if (tab) tab.textContent = '도매도매';
          document.querySelectorAll('#viewOwnerclan img').forEach((img, idx) => {
            img.alt = samples[idx % samples.length];
          });
          document.querySelectorAll('#viewOwnerclan *').forEach((el, idx) => {
            if (el.children.length) return;
            if (el.tagName === 'IMG') return;
            let t = (el.textContent || '').trim();
            if (/오너클랜/.test(t)) {
              el.textContent = t.replace(/오너클랜/g, '도매도매').replace(/랭킹순/, '인기순');
              t = el.textContent.trim();
            }
            if (t.length > 12 && !/원$|배송|검색|과세|면세|국내|해외|페이지|선택|제외|정렬|가격|전체|도매도매|인기순/.test(t)) {
              el.textContent = samples[idx % samples.length];
            }
            if (/^[A-Z]{2,}[A-Z0-9]{4,}$/.test(t)) el.textContent = 'SAMPLE' + String(1000 + (idx % 800));
            if (/^[0-9]{1,3}(,[0-9]{3})*원$/.test(t)) el.textContent = String(1000 + (idx % 40) * 100) + '원';
          });
        }"""
        )
        prep(page)
        page.evaluate(
            """() => {
          const tab = document.querySelector('#appTabOwnerclan');
          if (tab) tab.textContent = '도매도매';
        }"""
        )
        page.screenshot(path=str(OUT / "04-ownerclan.png"), full_page=False)

        page.locator("#appTabSettings").click()
        page.wait_for_timeout(400)
        page.locator("#settingsTabMarkets").click()
        page.wait_for_timeout(700)
        prep(page)
        page.evaluate(
            """() => {
          if (typeof fillMarketTable === 'function') fillMarketTable();
          const wrap = document.querySelector('#viewSettings .delivery-table-wrap');
          if (wrap) wrap.scrollTop = 0;
          // 쿠팡·11번가가 보이도록 중간쯤 스크롤
          if (wrap) wrap.scrollTop = 90;
          const form = document.querySelector('#marketForm');
          if (!form) return;
          const byName = (n) => form.querySelector('[name=\"' + n + '\"]');
          if (byName('name')) byName('name').value = '블루마켓';
          if (byName('url')) byName('url').value = 'https://smartstore.naver.com/bluemarket';
          if (byName('naver_account_id')) byName('naver_account_id').value = 'ncp_sample_01';
          if (byName('login_id')) byName('login_id').value = 'seller-a';
          if (byName('api_key')) byName('api_key').value = '••••••••';
          if (byName('api_secret')) byName('api_secret').value = '••••••••';
          if (byName('login_password')) byName('login_password').value = '••••••••';
          if (byName('vendor_code')) byName('vendor_code').value = 'A00012345';
          form.querySelectorAll('input[type=\"password\"]').forEach((el) => { el.value = '••••••••'; });
        }"""
        )
        page.screenshot(path=str(OUT / "05-settings.png"), full_page=False)
        browser.close()

    for path in sorted(OUT.glob("*.png")):
        print(path.name, path.stat().st_size)


if __name__ == "__main__":
    main()
