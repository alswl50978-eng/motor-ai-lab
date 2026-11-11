# LIGHT LAB · 손으로 가르치는 AI 스위치

고1 전기과 수준의 딥러닝 체험 수업. 손바닥·주먹·손이 없는 배경을 학습하여 **화면 속 가상 전등**을 제어한다. 기존 모터 실습을 대체한다. 기존 링크를 유지하기 위해 저장소 이름은 motor-ai-lab으로 유지한다.

- 실행: https://alswl50978-eng.github.io/motor-ai-lab/
- 소스: https://github.com/alswl50978-eng/motor-ai-lab
- 학생 학습지: `student-pack.pdf` (3쪽)
- 교사용 운영안: `teacher-guide.pdf` (2쪽)

## 수업 흐름

사진 모으기 → 실제 분류기 학습 → 새로운 사진 테스트 → 오류 조건 확인 → 사진 보완·재학습 → 또 다른 새 사진 테스트.

손바닥은 켜기, 주먹은 끄기, 손 없음은 대기·꺼짐. 최고 점수가 0.7 미만이면 판단을 보류하고 전등을 끈다. AI의 분류와 사람이 정한 제어 규칙을 구분하여 설명한다. 실제 전원·설비에 연결하지 않는다.

50분 수업 제안: 도입 5분, 원리 7분, 수집·학습 13분, 테스트·개선 15분, 활용·정리 10분. 시간·최소 사진 5장·최대 40장·30 epoch·보류 기준 0.7은 제작자의 실습 설정이며 공식 성능 또는 안전 기준이 아니다.

## 구현과 실행 조건

- TensorFlow.js 및 MobileNet 라이브러리는 `assets/`에 포함한다. **사전학습 모델 가중치는 첫 학습 때 인터넷으로 다운로드**한다. 완전 오프라인 앱이 아니다.
- MobileNet v2 alpha 0.5로 특징을 추출하고, 학생 사진으로 3출력 softmax Dense 분류기를 Adam(학습률 0.003), 범주형 교차 엔트로피로 학습한다. 클래스별 개수 차이는 classWeight로 보정한다.
- 큰 신경망 전체를 처음부터 학습하지 않는다. 사전학습된 특징 추출기와 새 분류기를 결합한 전이학습이다.
- 이미지 전체를 224×224 검정 여백 캔버스에 맞춘다. 수집·예측에 같은 전처리를 적용한다. 종류별 최대 40장, 파일당 최대 15MB.
- 사진 추가/삭제 후에는 다시 학습해야 예측할 수 있다. 학습 실패·예측 실패 때 전등을 끈다.
- 테스트 사진은 자동으로 학습에 들어가지 않는다. 사용자가 실제 종류를 선택한 결과만 모델 버전별로 기록한다. 보류를 포함한 전체 기록 중 맞힌 비율을 표시하며 일반 성능으로 해석하지 않는다.
- 카메라는 HTTPS 또는 localhost와 사용자 카메라 허용이 필요하다. 카메라 없는 기기는 이미지 파일을 사용한다. 예측은 버튼을 누를 때 한 번 수행한다.
- 외부 모델 다운로드 요청은 발생하지만 사진 업로드 요청은 구현하지 않는다. 사진·모델·테스트 기록은 메모리에만 저장하고 새로고침하면 사라진다. 답안은 `light-lab-answers-v1` 키로 브라우저에 저장한다. 삭제 시 다른 앱/기존 모터 실습 기록은 삭제하지 않는다.
- ‘내 활동지 인쇄/PDF 저장’은 입력 답안과 테스트 기록을 인쇄한다. 일반 브라우저 인쇄도 같은 인쇄용 내용을 생성한다.

## 교육과정

최신 사용자 요청에 따라 대상은 **2026학년도 고1 수준**, 연계 교육과정은 **2022 개정 인공지능 기초**다. 실제 과목 편성은 학교에서 확인한다.

- [12인기02-05] 인공신경망과 딥러닝의 특성에 대한 이해를 바탕으로 활용 분야를 탐색한다. → Q1·Q4
- [12인기02-06] 딥러닝을 활용하여 실생활 및 다양한 학문 분야의 문제를 해결하고, 성능을 평가한다. → 테스트 기록·Q2·Q3

MCP 공식 원문 필드로 확인했다. 관찰 평가와 피드백은 자체 수업 설계안이며 공식 수준별 성취수준으로 표시하지 않는다. `MCP-CHECK.md`는 이전 고3/2015 개정 조회의 이력이다.

## 검증·재생성

`node --check app.js` / `node test-dom.cjs`

테스트에는 `tmp/qa/node_modules/jsdom`이 필요하다. 없으면 `npm install --prefix tmp/qa jsdom --no-audit --no-fund`로 설치한다. Node 테스트는 모델 다운로드·실제 웹캠·브라우저 레이아웃을 검증하지 않는다. 검증 범위는 VALIDATION.md를 확인한다.

PDF: `python build_pdf.py`. Python reportlab, Windows 맑은 고딕 글꼴 필요. 선택적 의존성 경로는 `tmp/pdf-revision-deps`; 보통 Python 환경에 설치해도 된다. `tmp/`는 배포하지 않는다.

## 출처

- [교육부 2022 개정 교육과정 고시](https://www.moe.go.kr/boardCnts/viewRenew.do?boardID=141&boardSeq=93458&lev=0)
- [Google 전이학습 실습](https://codelabs.developers.google.com/tensorflowjs-transfer-learning-teachable-machine)
- [TensorFlow 이미지 분류 전이학습](https://www.tensorflow.org/js/tutorials/transfer/image_classification)
- [TensorFlow.js MobileNet 소스](https://github.com/tensorflow/tfjs-models/tree/master/mobilenet)

학교 공식 발행물이 아니다. 실습 결과는 학습 사진과 환경에 따라 달라지며 사전 성공률을 제시하지 않는다.
