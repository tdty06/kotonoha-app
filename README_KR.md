# 코토노하 (Kotonoha) 모바일 앱 패키지

이 패키지에는 **스마트폰에 바로 설치해 쓰는 PWA 앱(`www/`)**과 **안드로이드(APK)·아이폰(IPA) 네이티브 앱 빌드용 Capacitor 프로젝트 설정**이 모두 포함되어 있습니다.

---

## 방법 1 · 가장 빠른 스마트폰 앱 설치 (1분, 스토어 심사 불필요)

1. 이 폴더 안의 `www/` 폴더를 **Vercel**, **Netlify**, 또는 **GitHub Pages**에 드래그 앤 드롭으로 무료 배포합니다.
2. 스마트폰 브라우저에서 배포된 HTTPS 주소로 접속합니다.
   - **iPhone (Safari):** 하단 공유 버튼 → **「홈 화면에 추가」**
   - **Android (Chrome):** 우측 상단 메뉴(⋮) → **「앱 설치」** 또는 **「홈 화면에 추가」**
3. 홈 화면에 앱 아이콘이 생성되며, 전체 화면(주소창 없음)과 오프라인 캐시로 일반 상용 앱처럼 바로 사용할 수 있습니다.

---

## 방법 2 · 실제 Android APK / iOS 앱으로 빌드하기 (Capacitor)

PC에 Node.js(v18 이상)가 설치되어 있다면 아래 명령어로 바로 네이티브 프로젝트가 생성됩니다.

```bash
# 1. 패키지 설치
npm install

# 2-A. 안드로이드(APK) 프로젝트 생성 및 열기 (Android Studio 필요)
npx cap add android
npx cap sync android
npx cap open android

# 2-B. 아이폰(iOS) 프로젝트 생성 및 열기 (macOS + Xcode 필요)
npx cap add ios
npx cap sync ios
npx cap open ios
```

Android Studio가 열리면 상단 메뉴 **`Build > Build Bundle(s) / APK(s) > Build APK(s)`**를 눌러 설치용 `.apk` 파일을 바로 생성할 수 있습니다.

---

## 포함된 주요 기능
- **PBKDF2-SHA256 + 랜덤 솔트 암호화 잠금**, 5회 오입력 30초 잠금, 미사용 자동 잠금
- **12일 단계별 실전 커리큘럼 (N5 → N2)**, **132개 핵심 어휘 + 도쿄 악센트 시각화 + 4지선다 퀴즈**
- **24개 실전 문법 블록 조립**, **72문장 리얼 듣기 (×3 반복 듣기, 북마크 ☆, 쉐도잉)**
- **12종 AI 실시간 프리토킹** (존댓말/반말 전환, 한국어 힌트 구조대, 지하철 무음 모드, 교정 리포트)
- **오픈 사전 검색 + CSV/JSON 단어장 무한 확장 + 안전한 JSON 백업**
