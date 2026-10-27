# -*- coding: utf-8 -*-
"""판매 페이지 히어로용 약 15초 샘플 화면 녹화. 실마켓·실데이터 제거."""
from pathlib import Path
import importlib.util
import json
import shutil
import subprocess

from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent
BASE = "http://127.0.0.1:8787"
TMP = OUT / "_hero_record_tmp"
FINAL = OUT / "hero-demo.webm"

spec = importlib.util.spec_from_file_location("cap", OUT / "_capture_anon.py")
cap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cap)

FAKE_MARKETS = [
    {"id": "demo-ss-1", "channel": "smartstore", "channel_name": "스마트스토어", "name": "블루마켓", "login_id": "seller-a", "url": "https://smartstore.naver.com/bluemarket", "naver_account_id": "ncp_sample_01", "is_default": True, "api_key_set": True, "api_secret_set": True, "login_password_set": True},
    {"id": "demo-ss-2", "channel": "smartstore", "channel_name": "스마트스토어", "name": "그린스토어", "login_id": "seller-b", "url": "https://smartstore.naver.com/greenstore", "api_key_set": True, "api_secret_set": True, "login_password_set": True},
    {"id": "demo-ss-3", "channel": "smartstore", "channel_name": "스마트스토어", "name": "스카이홈", "login_id": "seller-c", "url": "https://smartstore.naver.com/skyhome", "api_key_set": True, "api_secret_set": True, "login_password_set": True},
    {"id": "demo-ss-4", "channel": "smartstore", "channel_name": "스마트스토어", "name": "라이트샵", "login_id": "seller-d", "url": "https://smartstore.naver.com/lightshop", "api_key_set": True, "api_secret_set": True, "login_password_set": True},
    {"id": "demo-cp-1", "channel": "coupang", "channel_name": "쿠팡", "name": "쿠팡홈샵", "login_id": "coupang01", "vendor_code": "A00012345", "api_key_set": True, "api_secret_set": True, "login_password_set": True},
    {"id": "demo-cp-2", "channel": "coupang", "channel_name": "쿠팡", "name": "로켓리빙", "login_id": "coupang02", "vendor_code": "A00067890", "api_key_set": True, "api_secret_set": True, "login_password_set": True},
    {"id": "demo-au-1", "channel": "auction", "channel_name": "옥션", "name": "옥션리빙몰", "login_id": "auction01", "login_password_set": True},
    {"id": "demo-gm-1", "channel": "gmarket", "channel_name": "G마켓", "name": "지마켓하우스", "login_id": "gmarket01", "login_password_set": True},
    {"id": "demo-11-1", "channel": "11st", "channel_name": "11번가", "name": "일레븐샵", "login_id": "st11_01", "login_password_set": True},
    {"id": "demo-11-2", "channel": "11st", "channel_name": "11번가", "name": "엘레븐몰", "login_id": "st11_02", "login_password_set": True},
    {"id": "demo-ts-1", "channel": "toss", "channel_name": "토스쇼핑", "name": "토스홈", "login_id": "toss01", "login_password_set": True},
    {"id": "demo-lo-1", "channel": "lotteon", "channel_name": "롯데ON", "name": "롯데리빙", "login_id": "lotte01", "login_password_set": True},
    {"id": "demo-kk-1", "channel": "kakao", "channel_name": "카카오톡스토어", "name": "카카오홈샵", "login_id": "kakao01", "login_password_set": True},
    {"id": "demo-ssg-1", "channel": "ssg", "channel_name": "SSG.COM", "name": "쓱리빙", "login_id": "ssg01", "login_password_set": True},
    {"id": "demo-tm-1", "channel": "temu", "channel_name": "테무", "name": "테무리빙", "login_id": "temu01", "login_password_set": True},
]


FORCE_JS = r"""
() => {
  const bad = /헤마스|위시웨이|바람집|사무실|가성비|신일|openning|오픈닝|hemas|wishway|baramjip|kpage|케이페이지|sellpie|셀파이|셀피아|wjmorning|오너클랜|ownerclan|SAFE-|UM2/i;
  const fakeStores = {
    smartstore: ['블루마켓','그린스토어','스카이홈','라이트샵'],
    coupang: ['쿠팡홈샵','로켓리빙'],
    auction: ['옥션리빙몰'],
    gmarket: ['지마켓하우스'],
    '11st': ['일레븐샵','엘레븐몰'],
    toss: ['토스홈'],
    lotteon: ['롯데리빙'],
    kakao: ['카카오홈샵'],
    ssg: ['쓱리빙'],
    temu: ['테무리빙'],
  };
  const fakeProducts = [
    '대용량 스텐 보온병 1L 텀블러 세트 캠핑용',
    '접이식 캠핑 테이블 휴대용 야외 탁자',
    '무선 미니 선풍기 USB 충전식 탁상형',
    '규조토 발매트 욕실 흡수 발판 대형',
    '실리콘 주방장갑 내열 오븐장갑 2개입',
    'LED 데스크램프 스탠드 조명 밝기조절',
  ];
  const fakeSuppliers = ['도매플러스', '공급마트', '도매도매'];
  const malls = ['블루마켓','그린스토어','스카이홈','라이트샵','쿠팡홈샵','로켓리빙','일레븐샵'];

  const byChannel = {};
  document.querySelectorAll('#marketTree button.market-item, #orderMarketTree button.market-item').forEach((btn) => {
    const kind = btn.dataset.kind || '';
    const ch = btn.dataset.channel || '';
    const label = btn.querySelector('.market-item-label');
    if (!label) return;
    const text = label.textContent || '';
    if (kind === 'store' || kind === 'empty' || /마켓을 등록하세요/.test(text) || bad.test(text)) {
      if (kind === 'channel' || kind === 'source' || kind === 'master') return;
      const list = fakeStores[ch] || ['샘플스토어'];
      const n = byChannel[ch] || 0;
      byChannel[ch] = n + 1;
      const name = list[Math.min(n, list.length - 1)] || '샘플스토어';
      label.textContent = name;
      btn.title = name;
      if (kind === 'empty') btn.dataset.kind = 'store';
    }
  });

  // depth-2 스토어 라벨은 채널별 가짜 이름으로 전부 재배치
  const channelOrder = ['smartstore','coupang','auction','gmarket','11st','toss','lotteon','kakao','ssg','temu'];
  channelOrder.forEach((ch) => {
    const stores = [...document.querySelectorAll('#marketTree button.market-item[data-channel=\"' + ch + '\"]')]
      .filter((b) => (b.dataset.kind === 'store' || b.dataset.kind === 'empty' || (b.querySelector('.market-item-label') && !['스마트스토어','쿠팡','옥션','G마켓','11번가','토스쇼핑','롯데ON','카카오톡스토어','SSG.COM','테무','원본상품','마스터상품'].includes((b.querySelector('.market-item-label').textContent||'').trim()))));
    const names = fakeStores[ch] || [];
    stores.forEach((btn, idx) => {
      const label = btn.querySelector('.market-item-label');
      if (!label || !names.length) return;
      // skip channel header buttons (depth-1 usually has kind=channel)
      if (btn.dataset.kind === 'channel') return;
      if (btn.classList.contains('depth-1')) return;
      label.textContent = names[idx % names.length];
      btn.title = names[idx % names.length];
    });
  });

  const tab = document.querySelector('#appTabOwnerclan');
  if (tab) tab.textContent = '도매도매';

  document.querySelectorAll('#productTable tr').forEach((tr, row) => {
    const setField = (field, value) => {
      const input = tr.querySelector('[data-field=\"' + field + '\"]');
      if (!input) return;
      if ('value' in input) input.value = value;
      const view = input.closest('td')?.querySelector('.cell-view');
      if (view) { view.textContent = value; view.dataset.value = value; }
    };
    const name = fakeProducts[row % fakeProducts.length];
    setField('name', name);
    setField('seller_code', 'SAMPLE-' + String(1000 + row));
    setField('model', 'BM-' + String(100 + row));
    setField('brand', '라이트홈');
    setField('manufacturer', '캠프라이프');
    setField('summary', name);
    const tds = tr.querySelectorAll('td');
    if (tds[5]) tds[5].textContent = fakeSuppliers[row % fakeSuppliers.length];
    if (tds[6]) tds[6].textContent = malls[row % malls.length];
  });

  const previewText = document.querySelector('#previewText');
  if (previewText) previewText.textContent = fakeProducts[0] + ' · SAMPLE-1000';
  const previewImg = document.querySelector('#previewImage');
  if (previewImg) { previewImg.removeAttribute('src'); previewImg.alt = 'sample'; }

  // 본문 텍스트에 남은 실명 제거
  const walk = (node) => {
    if (!node) return;
    if (node.nodeType === Node.TEXT_NODE) {
      if (bad.test(node.nodeValue || '')) {
        node.nodeValue = (node.nodeValue || '')
          .replace(/헤마스/g,'그린스토어').replace(/위시웨이|신일N?위시웨이/g,'블루마켓')
          .replace(/바람집/g,'스카이홈').replace(/사무실[^\\s]*/g,'라이트샵')
          .replace(/케이페이지|셀파이|셀피아/g,'도매플러스').replace(/오너클랜/g,'도매도매');
      }
      return;
    }
    if (node.nodeType === Node.ELEMENT_NODE && node.tagName !== 'SCRIPT' && node.tagName !== 'STYLE') {
      for (const child of Array.from(node.childNodes)) walk(child);
    }
  };
  walk(document.body);

  ['#arrivalNotice','#appEdition','#appQuit','.titlebar-theme'].forEach((sel) => {
    document.querySelectorAll(sel).forEach((el) => { el.style.display = 'none'; });
  });
}
"""


def install_routes(page) -> None:
    def markets(route):
        route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps(FAKE_MARKETS, ensure_ascii=False),
        )

    page.route("**/api/markets", markets)
    page.route("**/api/markets?**", markets)


def scrub(page) -> None:
    cap.prep(page)
    page.evaluate(FORCE_JS)


def scrub_inquiries(page) -> None:
    page.evaluate(
        """() => {
      const malls = ['04.스마트스토어','05.쿠팡','03.11번가','01.옥션','02.G마켓'];
      const stores = ['bluemarket','coupang01','st11_01','auction01','gmarket01'];
      const names = ['블루마켓','쿠팡홈샵','일레븐샵','옥션리빙몰','지마켓하우스'];
      const products = ['대용량 스텐 보온병 1L 텀블러','충전식 미니 가습기 USB','접이식 캠핑 의자 경량','규조토 발매트 욕실 대형'];
      document.querySelectorAll('#viewInquiries table tbody tr').forEach((tr, idx) => {
        const tds = tr.querySelectorAll('td');
        tds.forEach((td, i) => {
          if (i === 1) td.textContent = malls[idx % malls.length];
          else if (i === 2) td.textContent = stores[idx % stores.length];
          else if (i === 3 || i === 4) td.textContent = names[idx % names.length];
          else if (i === 8) td.textContent = products[idx % products.length];
        });
      });
    }"""
    )


def scrub_wholesalers(page) -> None:
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
    }"""
    )


def start_guard(page) -> None:
    page.evaluate(
        """(fn) => {
      if (window.__heroAnonGuard) clearInterval(window.__heroAnonGuard);
      const run = new Function('return (' + fn + ')')();
      run();
      window.__heroAnonGuard = setInterval(run, 200);
    }""",
        FORCE_JS,
    )


def trim_to_15s(src: Path) -> None:
    try:
        import imageio_ffmpeg
        import cv2

        ff = imageio_ffmpeg.get_ffmpeg_exe()
        tmp = OUT / "_hero_trim.webm"
        # 숨김 해제 이후만 사용
        subprocess.run(
            [ff, "-y", "-ss", "3", "-t", "15", "-i", str(src), "-c:v", "libvpx", "-b:v", "1.5M", "-an", str(tmp)],
            capture_output=True,
            check=False,
        )
        if tmp.exists() and tmp.stat().st_size > 20000:
            src.unlink(missing_ok=True)
            tmp.replace(src)
        cap_v = cv2.VideoCapture(str(src))
        fps = cap_v.get(cv2.CAP_PROP_FPS) or 25
        n = cap_v.get(cv2.CAP_PROP_FRAME_COUNT)
        cap_v.release()
        print("trimmed_sec", round(n / fps, 1), "size", src.stat().st_size)
    except Exception as exc:
        print("trim_skip", exc)


def main() -> None:
    if TMP.exists():
        shutil.rmtree(TMP, ignore_errors=True)
    TMP.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=True)
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            device_scale_factor=1.2,
            record_video_dir=str(TMP),
            record_video_size={"width": 1440, "height": 900},
        )
        page = context.new_page()
        install_routes(page)
        page.add_init_script("document.documentElement.style.visibility='hidden';")
        page.goto(BASE + "/", wait_until="networkidle", timeout=90000)
        page.add_style_tag(
            content="#appEdition,.app-edition,#appQuit,.app-quit,.titlebar-theme,#arrivalNotice{display:none!important;}"
        )
        page.wait_for_timeout(500)
        scrub(page)
        start_guard(page)
        page.evaluate("document.documentElement.style.visibility='visible';")
        page.wait_for_timeout(800)

        page.locator("#appTabOrders").click()
        page.wait_for_timeout(120)
        cap.fill_orders(page)
        scrub(page)
        page.wait_for_timeout(900)

        page.locator("#appTabInquiries").click()
        page.wait_for_timeout(150)
        scrub_inquiries(page)
        scrub(page)
        page.wait_for_timeout(700)

        page.locator("#appTabWholesalers").click()
        page.wait_for_timeout(120)
        scrub_wholesalers(page)
        scrub(page)
        page.wait_for_timeout(700)

        page.locator("#appTabOwnerclan").click()
        page.wait_for_timeout(150)
        scrub(page)
        try:
            page.locator("#ownerclanSearchKeyword").fill("양말", timeout=1500)
            page.locator("#ownerclanProductSearch").click(timeout=1500)
            for _ in range(18):
                loaded = page.evaluate(
                    """() => [...document.querySelectorAll('#viewOwnerclan img')].filter((img) => img.complete && img.naturalWidth > 8).length"""
                )
                if loaded >= 6:
                    break
                page.wait_for_timeout(250)
        except Exception:
            page.wait_for_timeout(400)
        page.evaluate(
            """() => {
          const samples = ['실리콘 의자캡 소음방지 16개입','빨래집게 세트 강력집게 50개','핫팩 대형 12시간 지속 20매','여행용 수납 파우치 세트 5종','남성 양말 10족 세트 스포츠','주방 수세미 거품망 세트 10개'];
          document.querySelectorAll('#viewOwnerclan *').forEach((el, idx) => {
            if (el.children.length || el.tagName === 'IMG') return;
            let t = (el.textContent || '').trim();
            if (/오너클랜|헤마스|위시웨이|바람집|사무실/i.test(t)) {
              el.textContent = '도매도매';
              return;
            }
            if (t.length > 14 && !/원$|배송|검색|과세|면세|국내|해외|페이지|선택|제외|정렬|가격|전체|도매도매|인기순/.test(t)) {
              el.textContent = samples[idx % samples.length];
            }
            if (/^[A-Z]{2,}[A-Z0-9]{4,}$/.test(t)) el.textContent = 'SAMPLE' + String(1000 + (idx % 800));
          });
        }"""
        )
        scrub(page)
        page.wait_for_timeout(700)

        page.locator("#appTabSettings").click()
        page.wait_for_timeout(120)
        try:
            page.locator("#settingsTabMarkets").click(timeout=1500)
        except Exception:
            pass
        page.wait_for_timeout(150)
        scrub(page)
        page.wait_for_timeout(800)

        page.locator("#appTabProducts").click()
        page.wait_for_timeout(120)
        scrub(page)
        page.wait_for_timeout(700)

        page.evaluate("if (window.__heroAnonGuard) clearInterval(window.__heroAnonGuard);")
        page.close()
        context.close()
        browser.close()

    videos = list(TMP.glob("*.webm"))
    if not videos:
        raise SystemExit("녹화 파일을 찾지 못했습니다.")
    src = max(videos, key=lambda p: p.stat().st_size)
    if FINAL.exists():
        FINAL.unlink()
    shutil.move(str(src), str(FINAL))
    shutil.rmtree(TMP, ignore_errors=True)
    trim_to_15s(FINAL)
    print(FINAL.name, FINAL.stat().st_size)


if __name__ == "__main__":
    main()
