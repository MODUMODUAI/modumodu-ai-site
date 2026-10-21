모두모두AI 판매 홈페이지

안내 문구에는 오픈마켓 전체(스마트스토어, 쿠팡, 11번가, 지마켓, 옥션, 카카오, 토스, 테무, SSG 등)를 적습니다.
내부 용어(배포용, 마스터 등)는 고객 화면에 쓰지 않습니다.

열기
1. website\index.html 을 브라우저로 엽니다.
2. 또는 프로젝트 폴더에서:
   .venv\Scripts\python.exe -m http.server 5500 --directory website
   브라우저에서 http://127.0.0.1:5500 을 엽니다.

수정
- 이메일, 카카오, 계좌, 요금 문구: website\config.js
- 화면 글·구조: website\index.html
- 색·레이아웃: website\styles.css
- 히어로 15초 영상: website\shots\hero-demo.webm (슬라이드)
  python website\shots\_make_hero_slideshow.py
  익명화 PNG(01~06)로 만들어 실마켓 정보가 들어가지 않습니다.

결제 (카카오페이 / 네이버페이 / 토스페이)
1. https://admin.portone.io 에서 가맹점 식별코드(imp…)를 받습니다.
2. 결제 채널에서 카카오페이, 네이버페이, 토스페이를 켭니다.
3. website\config.js 의 portoneImpCode 에 코드를 넣습니다.
4. 결제 완료 후 서버 검증·키 자동 발급은 아직 없습니다. 지금은 완료 안내 + 메일로 주문 정보가 갑니다.

이용 범위
- Windows PC 5대까지 (판매 페이지 FAQ·앱 설정 > 이용 키와 동일)
- 앱: app/license.py 의 MAX_DEVICES=5, /api/license
- 키 발급 예: LICENSE_SIGNING_SECRET=비밀 .venv\Scripts\python.exe -c "from app.license import issue_key; print(issue_key(expires_at='2027-12-31', plan='m3'))"
- 여러 PC에 걸쳐 대수를 강제하려면 LICENSE_SERVER_URL(또는 license_url.txt) 필요

아직 없는 것
- 결제 완료 서버 검증(웹훅)
- 라이선스 키 자동 발급·라이선스 서버
- 도메인 연결

월 정가 100,000원. 전 요금 일시한정 할인(1개월 -30% ~ 1년 -60%). config.js · index.html.
