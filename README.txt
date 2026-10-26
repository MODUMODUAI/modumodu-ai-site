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
- 짧은 사용 영상: website\shots\use-name, use-tags, use-attrs, use-image (상품명·태그·속성·이미지)
  python website\shots\_make_hero_slideshow.py
  익명화 PNG(01~06)로 만들어 실마켓 정보가 들어가지 않습니다.

결제 (카카오페이 / 네이버페이 / 토스페이)
1. https://admin.portone.io 에서 가맹점 식별코드(imp…)를 받습니다.
2. 결제 채널에서 카카오페이, 네이버페이, 토스페이를 켭니다.
3. website\config.js 의 portoneImpCode 에 코드를 넣습니다.
4. 결제창이 연결되면 결제가 끝난 뒤 가입 아이디의 시리얼키 사용기한을 결제한 기간만큼 늘리고, 새 키를 화면과 이메일로 보냅니다. 가맹 연결 전에는 문의 메일을 엽니다.

이용 범위
- PC 대수 제한 없음 (판매 페이지와 이용 키 기본값)
- 앱: app/license.py 의 MAX_DEVICES=0 이면 PC 대수 제한 없음. /api/license
- 키 발급 예: LICENSE_SIGNING_SECRET=비밀 .venv\Scripts\python.exe -c "from app.license import issue_key; print(issue_key(expires_at='2027-12-31', plan='m3'))"
- 여러 PC에 걸쳐 대수를 강제하려면 LICENSE_SERVER_URL(또는 license_url.txt) 필요

공개 주소 (GitHub Pages)
- https://modumoduai.github.io/modumodu-ai-site/
- 이용 방법·시험용: https://modumoduai.github.io/modumodu-ai-site/#how
- FAQ: https://modumoduai.github.io/modumodu-ai-site/#faq
- 저장소: https://github.com/MODUMODUAI/modumodu-ai-site
- siteUrl 은 website/config.js 에 넣어 두었습니다. 링크 공유 시 이 주소를 씁니다.
- 사이트 다시 올릴 때: website 폴더만 그 저장소 main 에 푸시하면 Pages가 갱신됩니다.

아직 없는 것
- 포트원 결제 확인 뒤에만 사용기한을 늘리는 잠금
- 고유 도메인(예: modumodu.ai) 연결

시험용 다운로드
- 이용 방법(#how)에서 회원가입한 뒤 받습니다.
- 파일은 최신 프로그램에서 주소 수집과 저장된 로그인 정보를 뺀 것입니다.
- 받는 주소: GitHub Releases `test-2026.10.22.8` 의 modumodu-trial.zip
- 가입 명단은 서버 프로그램의 고객 화면 「사이트 가입」에 나옵니다. 비밀번호는 저장하지 않습니다.

월 정가 200,000원. 실 결제액은 1개월 80,000원, 3개월 210,000원(월 7만원), 6개월 360,000원(월 6만원), 1년 600,000원(월 5만원). config.js · index.html.
