# -*- coding: utf-8 -*-
"""판매 페이지용 짧은 사용 영상. 샘플 상품만 쓰고, 실제 화면 버튼을 누릅니다."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import time
from copy import deepcopy
from pathlib import Path

import imageio_ffmpeg
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
SAMPLES = OUT / "sample-products"
PORT = 8795
BASE = f"http://127.0.0.1:{PORT}"
PID = "sample-01"
NEW_NAME = "USB 충전 탁상 미니 선풍기 3단 풍속 사무실용 BM-210"
TAGS = ["선풍기", "탁상용", "USB", "사무실", "미니", "충전식", "휴대용", "여름", "책상", "저소음"]
SCHEMA = [
    {"attributeSeq": 1, "attributeName": "용도", "values": [{"attributeValueSeq": 11, "minAttributeValue": "탁상용", "label": "탁상용"}]},
    {"attributeSeq": 2, "attributeName": "전원", "values": [{"attributeValueSeq": 21, "minAttributeValue": "USB", "label": "USB"}]},
    {"attributeSeq": 3, "attributeName": "풍속", "values": [{"attributeValueSeq": 31, "minAttributeValue": "3단", "label": "3단"}]},
]
NAVER = [
    {"attributeSeq": 1, "attributeValueSeq": 11, "attributeRealValue": "탁상용"},
    {"attributeSeq": 2, "attributeValueSeq": 21, "attributeRealValue": "USB"},
    {"attributeSeq": 3, "attributeValueSeq": 31, "attributeRealValue": "3단"},
]
ATTRS = [
    {"name": "용도", "value": "탁상용"},
    {"name": "전원", "value": "USB"},
    {"name": "풍속", "value": "3단"},
]


def product() -> dict:
    return {
        "id": PID,
        "name": "미니 선풍기",
        "model": "BM-210",
        "brand": "라이트홈",
        "manufacturer": "캠프라이프",
        "origin": "중국",
        "price": 18900,
        "cost": 7900,
        "stock": 50,
        "seller_code": "SAMPLE-1001",
        "category_id": "50002633",
        "category_name": "선풍기",
        "wholesale_name": "도매플러스",
        "market_name": "블루마켓",
        "market_id": "demo-ss-1",
        "master_id": "master-sample",
        "channel": "smartstore",
        "status": "collected",
        "tags": [],
        "attributes": [],
        "naver_attributes": [],
        "attribute_schema": SCHEMA,
        "options": [],
        "images": [
            {"kind": "gallery", "file": "01.png", "representative": True, "included": True, "width": 500, "height": 500},
            {"kind": "gallery", "file": "02.png", "representative": False, "included": True, "width": 500, "height": 500},
        ],
        "detail_html": '<p>USB로 충전하는 탁상용 미니 선풍기입니다. 풍속은 3단입니다.</p><p><img src="/media/sample-01/03.png" alt="상세"></p>',
        "created_at": "2026-10-20T09:00:00",
        "updated_at": "2026-10-20T09:00:00",
    }


STATE = product()
PRODUCTS: list[dict] = []
COLLECT_ITEMS = [
    ("S1001", "USB 충전 탁상 미니 선풍기", 7900, "01.png"),
    ("S1002", "접이식 캠핑 테이블 휴대용", 12900, "02.png"),
    ("S1003", "규조토 발매트 욕실 대형", 8900, "03.png"),
    ("S1004", "LED 데스크램프 밝기조절", 15900, "04.png"),
    ("S1005", "실리콘 주방장갑 내열 2개입", 6900, "05.png"),
    ("S1006", "무선 미니 가습기 USB", 9900, "06.png"),
    ("S1007", "접이식 캠핑 의자 경량", 14900, "07.png"),
    ("S1008", "여행용 수납 파우치 5종", 11900, "08.png"),
]


def reset_state(with_store: bool = True) -> None:
    STATE.clear()
    STATE.update(product())
    PRODUCTS.clear()
    if with_store:
        PRODUCTS.append(STATE)


def collect_payload(keyword: str = "") -> dict:
    rows = [
        {
            "code": code,
            "name": name,
            "price": price,
            "supplier": "샘플도매",
            "shipping_type": "F",
            "shipping": 0,
            "image": f"/media/sample-01/{image}",
        }
        for code, name, price, image in COLLECT_ITEMS
        if not keyword or keyword in name or keyword in "선풍기생활"
    ]
    return {"products": rows or collect_payload("")["products"], "page": 1, "pages": 1, "excluded_count": 0}


def dump(payload) -> str:
    return json.dumps(payload, ensure_ascii=False)


def fulfill(route, payload, delay: float = 0) -> None:
    if delay:
        time.sleep(delay)
    route.fulfill(status=200, content_type="application/json; charset=utf-8", body=dump(payload))


def on_api(route) -> None:
    request = route.request
    path = request.url.split("?", 1)[0]
    method = request.method.upper()
    if path.endswith("/api/settings") and method == "GET":
        fulfill(route, {"ai_provider": "gemini", "gemini_api_key_set": True, "gemini_api_key": ""})
        return
    if path.endswith("/api/markets") and method == "GET":
        fulfill(route, [{
            "id": "demo-ss-1",
            "channel": "smartstore",
            "channel_name": "스마트스토어",
            "name": "블루마켓",
            "login_id": "seller-a",
            "api_key_set": True,
            "api_secret_set": True,
        }])
        return
    if path.endswith("/api/products") and method == "GET":
        fulfill(route, deepcopy(PRODUCTS))
        return
    if path.endswith("/api/wholesalers") and method == "GET":
        fulfill(route, [{
            "id": "demo-oc",
            "name": "오너클랜",
            "type": "ownerclan",
            "type_label": "오너클랜",
            "enabled": True,
        }])
        return
    if path.endswith("/api/ownerclan") and method == "GET":
        fulfill(route, {"excluded_suppliers": [], "categories": [], "search_filters": {}})
        return
    if path.endswith("/api/ownerclan/categories") and method == "GET":
        fulfill(route, {"groups": [{"code": "life", "name": "생활용품"}]}, 0.4)
        return
    if "/api/ownerclan/category/" in path and method == "GET":
        code = path.rstrip("/").rsplit("/", 1)[-1]
        if code == "fan":
            fulfill(route, {
                "title": [{"code": "life", "name": "생활용품"}, {"code": "fan", "name": "선풍기"}],
                "children": [],
            })
        else:
            fulfill(route, {
                "title": [{"code": "life", "name": "생활용품"}],
                "children": [
                    {"code": "fan", "name": "선풍기", "count": 1280},
                    {"code": "lamp", "name": "조명", "count": 860},
                ],
            }, 0.3)
        return
    if "/api/ownerclan/products/import" in path and method == "POST":
        picked = json.loads(request.post_data or "{}").get("items") or []
        for item in picked:
            PRODUCTS.append({
                "id": f"picked-{item.get('code')}",
                "name": item.get("name") or "샘플 상품",
                "price": item.get("price") or 0,
                "cost": item.get("price") or 0,
                "stock": 50,
                "status": "collected",
                "wholesale_name": "오너클랜",
                "wholesale_id": "demo-oc",
                "seller_code": item.get("code") or "",
                "images": [],
                "tags": [],
                "attributes": [],
                "created_at": "2026-10-26T10:00:00",
            })
        fulfill(route, {"added": len(picked), "kept": 0}, 0.6)
        return
    if "/api/ownerclan/products" in path and method == "GET":
        keyword = ""
        if "keyword=" in request.url:
            keyword = request.url.split("keyword=", 1)[1].split("&", 1)[0]
            keyword = keyword.replace("+", " ")
        fulfill(route, collect_payload(keyword), 0.6)
        return
    if "/search-keywords" in path and method == "GET":
        if "basis=tag" in request.url:
            words = [{"keyword": tag, "monthly": 12000 - index * 700} for index, tag in enumerate(TAGS)]
        else:
            words = [
                {"keyword": "미니선풍기", "monthly": 42000},
                {"keyword": "탁상선풍기", "monthly": 31000},
                {"keyword": "usb선풍기", "monthly": 18000},
            ]
        fulfill(route, {"keywords": words, "category": "선풍기", "detail": ""})
        return
    if path.endswith("/name/suggest") and method == "POST":
        fulfill(route, {
            "name": NEW_NAME,
            "keywords": [
                {"keyword": "미니선풍기", "monthly": 42000},
                {"keyword": "탁상선풍기", "monthly": 31000},
            ],
        }, 0.7)
        return
    if path.endswith("/tags/ai") and method == "POST":
        STATE["tags"] = list(TAGS)
        fulfill(route, deepcopy(STATE), 0.7)
        return
    if path.endswith("/attributes/ai") and method == "POST":
        STATE["attributes"] = list(ATTRS)
        STATE["naver_attributes"] = list(NAVER)
        fulfill(route, deepcopy(STATE), 0.7)
        return
    if path.endswith("/attributes/fetch") and method == "POST":
        fulfill(route, deepcopy(STATE), 0.3)
        return
    if path.endswith("/images/refit") and method == "POST":
        fulfill(route, deepcopy(STATE))
        return
    if path.endswith("/images/ai-edit") and method == "POST":
        STATE["images"][0]["file"] = "05.png"
        STATE["updated_at"] = "2026-10-26T10:00:01"
        fulfill(route, deepcopy(STATE), 0.8)
        return
    if path.endswith(f"/api/products/{PID}") and method == "PUT":
        patch = json.loads(request.post_data or "{}")
        if isinstance(patch, dict):
            STATE.update(patch)
        fulfill(route, deepcopy(STATE))
        return
    route.continue_()


def on_media(route) -> None:
    name = route.request.url.split("?", 1)[0].rsplit("/", 1)[-1]
    path = SAMPLES / name
    if not path.is_file():
        path = SAMPLES / "01.png"
    route.fulfill(status=200, content_type="image/png", body=path.read_bytes())


def scroll_to(page, selector: str) -> None:
    page.evaluate(
        """(selector) => {
          const node = document.querySelector(selector);
          if (node) node.scrollIntoView({inline: 'center', block: 'center'});
        }""",
        selector,
    )


def record_clip(browser, name: str, play, prepare: str = "store") -> Path:
    reset_state(with_store=prepare == "store")
    folder = OUT / f"_usage_{name}"
    if folder.exists():
        shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True, exist_ok=True)
    context = browser.new_context(
        viewport={"width": 1440, "height": 900},
        device_scale_factor=1,
        record_video_dir=str(folder),
        record_video_size={"width": 1440, "height": 900},
    )
    page = context.new_page()
    page.route("**/api/**", on_api)
    page.route("**/media/**", on_media)
    page.goto(BASE + "/", wait_until="domcontentloaded", timeout=90000)
    page.add_style_tag(content="#appEdition,#appQuit,.titlebar-theme,#arrivalNotice{display:none!important}")
    if prepare == "store":
        page.wait_for_selector('#marketTree button[data-filter="smartstore"] .market-item-label', timeout=30000)
        page.locator('#marketTree button[data-filter="smartstore"] .market-item-label').click()
        page.wait_for_selector("#productTable tr", timeout=15000)
        page.locator("#productTable tr .check-cell input").first.click()
        page.wait_for_timeout(400)
    else:
        page.wait_for_selector("#appTabCollect", timeout=30000)
        page.wait_for_timeout(400)
    play(page)
    page.wait_for_timeout(400)
    video = page.video
    context.close()
    raw = Path(video.path())
    target = OUT / f"_raw_{name}.webm"
    if target.exists():
        target.unlink()
    raw.replace(target)
    shutil.rmtree(folder, ignore_errors=True)
    return target


def play_name(page) -> None:
    scroll_to(page, '#productTable [data-field="name"]')
    page.wait_for_timeout(400)
    page.locator("#changeNameButton").click()
    page.wait_for_selector("#nameDialog[open]")
    page.wait_for_timeout(1800)
    page.locator('[data-name-mode="category"]').click()
    page.wait_for_function(
        """(name) => (document.querySelector('#nameInput') || {}).value === name""",
        arg=NEW_NAME,
        timeout=10000,
    )
    page.wait_for_timeout(900)
    page.locator("#nameForm button[type='submit']").click()
    page.wait_for_function(
        """(name) => (document.querySelector('#previewText') || {}).textContent.includes(name)""",
        arg="USB 충전",
        timeout=10000,
    )
    scroll_to(page, '#productTable [data-field="name"]')
    page.wait_for_timeout(1800)


def play_tags(page) -> None:
    page.locator("#aiTagButton").click()
    page.wait_for_function(
        """() => (document.querySelector('#productTable [title*="태그"]') || {}).textContent.includes('선풍기')""",
        timeout=10000,
    )
    scroll_to(page, '#productTable [title*="태그"]')
    page.wait_for_timeout(700)
    page.locator("#changeTagButton").click()
    page.wait_for_selector("#tagDialog[open] #tagChips span")
    page.wait_for_timeout(1400)


def play_attrs(page) -> None:
    page.locator("#aiAttrButton").click()
    page.wait_for_function(
        """() => (document.querySelector('#productTable [title*="속성"]') || {}).textContent.includes('탁상용')""",
        timeout=10000,
    )
    scroll_to(page, '#productTable [title*="속성"]')
    page.wait_for_timeout(700)
    page.locator("#changeAttributeButton").click()
    page.wait_for_selector("#attributeDialog[open]")
    page.wait_for_timeout(1400)


def play_collect(page) -> None:
    page.locator("#appTabCollect").click()
    page.wait_for_selector(".ownerclan-child", timeout=20000)
    page.wait_for_timeout(2200)
    page.locator(".ownerclan-child", has_text="선풍기").click()
    page.wait_for_selector(".ownerclan-product img", timeout=20000)
    page.wait_for_timeout(2800)
    page.locator("#ownerclanSearchKeyword").fill("선풍기")
    page.wait_for_timeout(900)
    page.locator("#ownerclanProductSearch").click()
    page.wait_for_timeout(2600)
    page.locator("#ownerclanSelectAll").click()
    page.wait_for_timeout(800)
    page.locator(".ownerclan-product input").nth(0).click()
    page.locator(".ownerclan-product input").nth(1).click()
    page.wait_for_timeout(1400)
    page.locator("#ownerclanSend").click()
    page.wait_for_timeout(1600)
    page.locator("#appTabProducts").click()
    page.wait_for_selector("#viewProducts #productTable tr", timeout=20000)
    page.wait_for_timeout(2800)


def play_process(page) -> None:
    play_name(page)
    page.wait_for_timeout(400)
    page.locator("#aiTagButton").click()
    page.wait_for_function(
        """() => (document.querySelector('#productTable [title*="태그"]') || {}).textContent.includes('선풍기')""",
        timeout=10000,
    )
    page.locator("#changeTagButton").click()
    page.wait_for_selector("#tagDialog[open] #tagChips span")
    page.wait_for_timeout(2800)
    page.locator("#closeTag").click()
    page.wait_for_timeout(700)
    page.locator("#aiAttrButton").click()
    page.wait_for_function(
        """() => (document.querySelector('#productTable [title*="속성"]') || {}).textContent.includes('탁상용')""",
        timeout=10000,
    )
    page.locator("#changeAttributeButton").click()
    page.wait_for_selector("#attributeDialog[open]")
    page.wait_for_timeout(2800)
    page.locator("#closeAttribute").click()
    page.wait_for_timeout(700)
    play_image(page)


def play_image(page) -> None:
    page.locator("#changeImageButton").click()
    page.wait_for_selector("#imageDialog[open] #imageThumbs img")
    page.wait_for_timeout(600)
    page.locator("#imageThumbs .image-slot").first.click(position={"x": 36, "y": 78})
    page.locator("#imageAiCommand").fill("글씨를 지워 줘")
    page.wait_for_timeout(400)
    page.locator("#imageAiRun").click()
    page.wait_for_function(
        """() => [...document.querySelectorAll('#imageThumbs img')].some((img) => img.src.includes('05.png'))""",
        timeout=10000,
    )
    page.locator("#imageForm button[type='submit']").click()
    page.wait_for_function(
        """() => !document.querySelector('#imageDialog[open]')
          && (document.querySelector('#previewImage') || {}).src.includes('05.png')
          && (document.querySelector('#previewText') || {}).textContent.includes('USB')""",
        timeout=15000,
    )
    scroll_to(page, '#productTable [data-field="name"]')
    page.wait_for_timeout(2800)


def duration_seconds(ff: str, src: Path) -> float:
    probe = subprocess.run([ff, "-i", str(src)], capture_output=True, text=True)
    text = (probe.stderr or "") + (probe.stdout or "")
    for line in text.splitlines():
        if "Duration:" in line:
            stamp = line.split("Duration:", 1)[1].split(",", 1)[0].strip()
            hours, minutes, seconds = stamp.split(":")
            return int(hours) * 3600 + int(minutes) * 60 + float(seconds)
    return 0


def publish(ff: str, raw: Path, stem: str, tail: float = 9) -> None:
    length = duration_seconds(ff, raw)
    start = max(0, length - tail)
    webm = OUT / f"{stem}.webm"
    mp4 = OUT / f"{stem}.mp4"
    poster = OUT / f"{stem}.jpg"
    subprocess.run(
        [ff, "-y", "-ss", f"{start:.2f}", "-i", str(raw), "-t", str(tail), "-an", "-c:v", "libvpx-vp9", "-b:v", "1.2M", str(webm)],
        capture_output=True,
        check=False,
    )
    subprocess.run(
        [ff, "-y", "-ss", f"{start:.2f}", "-i", str(raw), "-t", str(tail), "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(mp4)],
        capture_output=True,
        check=False,
    )
    subprocess.run(
        [ff, "-y", "-sseof", "-0.4", "-i", str(mp4 if mp4.exists() else raw), "-frames:v", "1", str(poster)],
        capture_output=True,
        check=False,
    )
    raw.unlink(missing_ok=True)
    print(stem, "sec", round(length, 1), "tail", tail, "mp4", mp4.stat().st_size if mp4.exists() else 0)


def main() -> None:
    data = Path(os.environ.get("TEMP", ".")) / "modumodu-usage-video"
    if data.exists():
        shutil.rmtree(data, ignore_errors=True)
    data.mkdir(parents=True, exist_ok=True)
    version = ROOT / "version.txt"
    if version.exists():
        shutil.copyfile(version, data / "version.txt")
    env = os.environ.copy()
    env["MODUMODU_ROOT"] = str(data)
    env["MODUMODU_KIND"] = "master"
    server = subprocess.Popen(
        [str(ROOT / ".venv" / "Scripts" / "python.exe"), "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", str(PORT)],
        cwd=str(ROOT),
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        deadline = time.time() + 30
        while time.time() < deadline:
            try:
                import urllib.request
                with urllib.request.urlopen(BASE + "/api/health", timeout=2) as response:
                    if response.status == 200:
                        break
            except Exception:
                time.sleep(0.4)
        else:
            raise SystemExit("local app did not start")
        ff = imageio_ffmpeg.get_ffmpeg_exe()
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(channel="msedge", headless=True)
            clips = [
                ("use-collect", play_collect, "collect", 28),
                ("use-process", play_process, "store", 36),
            ]
            for stem, play, prepare, tail in clips:
                raw = record_clip(browser, stem, play, prepare)
                publish(ff, raw, stem, tail)
            browser.close()
    finally:
        server.terminate()
        try:
            server.wait(timeout=8)
        except subprocess.TimeoutExpired:
            server.kill()


if __name__ == "__main__":
    main()
