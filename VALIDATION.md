## Curriculum revision: 2026-11-11

- Confirmed audience: grade 12 in school year 2026; corrected to 2015 curriculum.
- Main standard: 12AI02-09 (Korean code in index.html). Linked training/evaluation standards: 03-07 and 03-08.
- Q2 concept/PLC comparison and Q6 application exploration updated.
- Official achievement levels and school assessment plan remain unverified; rubric is a lesson proposal.
- DOM regression passed; student PDF 4 pages and teacher PDF 3 pages rendered and reviewed.
- Local revision only; GitHub/Pages not updated. Historical validation follows.

# 검증 기록

확인일: 2026-11-11. 아래는 실제 수행한 검사와 한계를 구분한 기록입니다.

## 통과한 검사

- `node --check app.js`: JavaScript 구문 검사.
- `node test.cjs`: 학습·평가 데이터 중복 없음, 데이터 개수·클래스 균형, 손실 감소, 출력 점수 범위, 혼동 행렬 합계, 임계값에 따른 FP/FN 단조성, A/B 성능 차이.
- `node test-dom.cjs`: jsdom 환경에서 초기 데이터 표, 중복 ID 없음, 내부 앵커·자산 경로, A/B 학습 버튼, 임계값, 결과 기록, 답변 로컬 저장, 인쇄용 답변 생성·HTML 이스케이프, 퀴즈 피드백, CSV 다운로드 호출, 초기화 동작.
- `build_pdf.py`: 페이지 하단 여백 검사 통과. 학생용 4쪽·교사용 2쪽 PDF 생성.
- PDF를 PyMuPDF로 6쪽 모두 PNG 렌더링하여 한글, 표, 본문, 답안 작성 공간, 페이지 끝 배치를 육안 확인.
- 배포 대상 파일 목록 확인: 임시 패키지와 렌더링 파일은 `tmp/`에 두고 `.gitignore`로 제외. 학생 개인정보·실제 답안·자격증명 없음.

## 제한

- Microsoft Edge 제어 요청이 승인되지 않아 실제 브라우저의 화면 조작·반응형 레이아웃·인쇄 대화상자 검증은 완료하지 못했습니다. jsdom 테스트는 이 검증을 대신하지 않습니다.
- 작성 학습지 PDF 저장은 브라우저 인쇄 기능을 사용합니다. 직접 다운로드 PDF 2종은 별도 생성·렌더링 검증했습니다.
- 이 합성 데이터의 성능은 실제 전기설비 성능이 아닙니다.
- 공식 성취수준 문구는 확인하지 못했습니다. 수업의 관찰 평가 항목은 제작한 제안입니다.
- 오류가 전혀 없음을 보증하지 않습니다. 담당 교사는 실제 수업 기기에서 A/B 학습과 PDF 저장을 사전 확인할 수 있습니다.

## 공개 배포 확인

- GitHub API에서 저장소 visibility가 `PUBLIC`임을 확인했습니다.
- GitHub Pages API에서 배포 상태 `built`, 오류 메시지 없음, 게시 경로 `main` 브랜치 `/`를 확인했습니다.
- `https://alswl50978-eng.github.io/motor-ai-lab/` 및 `style.css`, `app.js`, `model.js`, `student-pack.pdf`, `teacher-guide.pdf`의 HTTP 200 응답을 확인했습니다.
- 위 6개 배포 파일을 다운로드한 바이트와 로컬 원본이 모두 일치했습니다. PDF의 응답 MIME 타입은 `application/pdf`입니다.

## 재현

```sh
node test.cjs
npm install --prefix tmp/qa jsdom --no-audit --no-fund
node test-dom.cjs
```

PDF 재생성에는 Python, reportlab, Windows 맑은 고딕 글꼴이 필요합니다.
