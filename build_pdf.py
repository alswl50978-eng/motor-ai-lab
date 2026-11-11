"""Build Korean classroom PDFs with embedded Malgun Gothic fonts.
Install reportlab, pymupdf and pypdf in your Python environment first.
"""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tmp/pdf-revision-deps'))
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
pdfmetrics.registerFont(TTFont('KR','C:/Windows/Fonts/malgun.ttf'))
pdfmetrics.registerFont(TTFont('KRB','C:/Windows/Fonts/malgunbd.ttf'))
pdfmetrics.registerFontFamily('KR',normal='KR',bold='KRB')
W,H=A4; M=43; CW=W-M*2
GREEN=colors.HexColor('#116854'); INK=colors.HexColor('#172f2b'); MUTED=colors.HexColor('#52685f'); PALE=colors.HexColor('#eaf3eb'); LINE=colors.HexColor('#ccdcd1')
styles={
 'body':ParagraphStyle('body',fontName='KR',fontSize=9.3,leading=16,textColor=INK,wordWrap='CJK',spaceAfter=0),
 'small':ParagraphStyle('small',fontName='KR',fontSize=8,leading=13,textColor=MUTED,wordWrap='CJK'),
 'h2':ParagraphStyle('h2',fontName='KRB',fontSize=13,leading=20,textColor=GREEN,wordWrap='CJK'),
 'title':ParagraphStyle('title',fontName='KRB',fontSize=25,leading=35,textColor=INK,wordWrap='CJK')}
class PDF:
 def __init__(self,name,title):
  self.c=canvas.Canvas(str(ROOT/name),pagesize=A4); self.c.setTitle(title);self.c.setAuthor('MOTOR / AI LAB');self.n=0;self.y=0
 def page(self,label,title):
  if self.n:self.finish_page();self.c.showPage()
  self.n+=1;self.c.setFillColor(GREEN);self.c.rect(0,H-9,W,9,fill=1,stroke=0)
  self.c.setFont('KRB',9);self.c.drawString(M,H-39,'MOTOR / AI LAB');self.c.setFont('KR',8);self.c.drawRightString(W-M,H-39,label)
  self.y=H-68;self.p(title,'title',after=19)
 def finish_page(self):
  assert self.y>49, f'Page overflow: {self.n}, y={self.y}'
  self.c.setStrokeColor(LINE);self.c.line(M,40,W-M,40);self.c.setFillColor(MUTED);self.c.setFont('KR',7)
  self.c.drawString(M,27,'청주공업고등학교 전기제어과 맞춤 수업 | 교육용 합성 데이터 | 학교 공식 발행물 아님')
  self.c.drawRightString(W-M,27,str(self.n))
 def p(self,text,kind='body',after=9):
  p=Paragraph(text,styles[kind]);w,h=p.wrap(CW,1000);p.drawOn(self.c,M,self.y-h);self.y-=h+after
 def note(self,text):
  p=Paragraph(text,styles['body']);w,h=p.wrap(CW-24,1000);self.c.setFillColor(PALE);self.c.roundRect(M,self.y-h-22,CW,h+22,6,fill=1,stroke=0);p.drawOn(self.c,M+12,self.y-h-11);self.y-=h+34
 def lines(self,n=3):
  self.c.setStrokeColor(LINE)
  for _ in range(n): self.y-=23;self.c.line(M,self.y,W-M,self.y)
  self.y-=16
 def table(self,rows,widths=None):
  data=[[Paragraph(str(v),styles['small']) for v in row] for row in rows]
  t=Table(data,colWidths=widths or [CW/len(rows[0])]*len(rows[0]));t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),PALE),('GRID',(0,0),(-1,-1),.5,LINE),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)]));w,h=t.wrap(CW,1000);t.drawOn(self.c,M,self.y-h);self.y-=h+16
 def close(self):self.finish_page();self.c.save()

s=PDF('student-pack.pdf','모터 이상을 찾는 AI - 학생 학습자료와 학습지')
s.page('STUDENT PACK / 01 · 개념','모터 이상을 찾는 AI,<br/>바로 믿어도 될까?')
s.p('2026학년도 고3 · 2015 개정 인공지능 기초 · 60분 · 3인 모둠','small')
s.note('<b>오늘의 임무</b>  온도·전류·진동으로 모터의 점검 필요 상태를 분류하고, 모델의 오류를 근거로 개선안을 제시한다. 실제 기기를 연결하지 않는다.')
s.p('01  오늘의 도착점','h2')
s.p('① 딥러닝의 개념을 설명하고 PLC 규칙과 비교한다.<br/>② 같은 조건에서 학습 데이터의 다양성에 따른 성능을 비교한다.<br/>③ 다른 활용 분야의 입력·출력과 적용 이유를 탐색한다.')
s.p('02  신경망의 판단 흐름','h2')
s.table([['입력층: 센서 3개','은닉층: 6개 → 4개 뉴런','출력층: 이상 점수 1개'],['온도·전류·진동의 수치 범위를 조정해 입력한다.','정답과 예측의 오차가 줄어들도록 연결 강도인 가중치를 조정한다.','0~1 점수가 임계값 이상이면 이상, 미만이면 정상으로 분류한다.']])
s.p('<b>학습</b>은 가중치를 조정하는 과정이다. <b>추론</b>은 학습한 가중치로 새로운 입력을 판단하는 과정이다. 여러 은닉층을 사용하는 신경망 학습은 딥러닝의 한 형태이다.')
s.p('PLC의 비교 규칙은 사람이 조건을 정한다. 신경망은 데이터로 가중치를 학습한다. 두 방법은 함께 사용할 수 있으며, 간단한 문제는 규칙만으로도 해결될 수 있다.')
s.note('<b>주의</b>  이 자료의 센서값과 정답은 수업용으로 만든 합성 데이터이다. 실제 모터의 정상 범위나 안전 기준이 아니다. 출력 0.9는 보정되지 않은 점수이며, 실제 고장 확률 90%를 뜻한다고 단정할 수 없다.')
s.p('03  한 시간의 흐름','h2')
s.table([['0–8분','8–18분','18–38분','38–52분','52–60분'],['문제 발견<br/>역할 나누기','원리 연결<br/>개념 설명','A/B 학습<br/>오류 비교','임계값 토론<br/>개선 계획','활용 탐색<br/>개인 설명']])

s.page('STUDENT PACK / 02 · 실험','학습 버튼 다음에는<br/>무엇을 확인해야 할까?')
s.p('조작자: 실행·조건 변경 / 검증자: 오분류·수치 확인 / 기록자: 근거 기록·발표. B 학습에서는 조작자를 교대한다. 2인 모둠은 검증과 기록을 함께 맡는다.')
s.p('01  공정한 비교 실험','h2')
s.table([['순서','할 일','관찰할 것'],['1','A 선택 → 학습 → 임계값 0.50 → 결과 기록','학습 정확도와 새 조건 평가 정확도가 같은가?'],['2','평가 데이터 펼치기 → 오분류 ID 찾기','어떤 운전 조건에서 오류가 생기는가?'],['3','B 선택 → 학습 → 임계값 0.50 → 결과 기록','A와 비교할 때 오경보·이상 누락은 어떻게 변했는가?'],['4','A로 다시 학습 → 임계값 0.30, 0.70 비교','경보가 쉬워지거나 어려워지면 어떤 오류가 늘어나는가?']],[30,240,CW-270])
s.p('<b>같게 두는 것:</b> 학습 80개(정상 40, 이상 40), 모델 구조 3→6→4→1, 초기값, 700회 학습, 새 조건 평가 40개(정상 20, 이상 20). <b>바꾸는 것:</b> 운전 조건의 다양성. A에는 낮은 온도 정상·높은 온도 이상만, B에는 높은 온도 정상·낮은 온도 이상도 포함된다. 모든 개수는 수업 설계값이다.')
s.p('02  숫자를 해석하는 방법','h2')
s.table([['','AI 정상','AI 이상'],['정답 정상','TN: 정상 확인','FP: 오경보'],['정답 이상','FN: 이상 누락','TP: 이상 탐지']])
s.p('<b>정확도</b> = (TP + TN) / 전체 × 100<br/><b>이상 재현율</b> = TP / (TP + FN) × 100<br/>같은 평가 데이터에서 임계값을 낮추면 이상으로 분류되는 수는 줄지 않는다. 오경보와 이상 누락을 함께 확인하자.')
s.note('<b>인터넷·기기 문제가 있을 때</b><br/>제공된 대체 결과를 계산하고 토론한다. 임계값 0.50에서 A: TN 15, FP 5, FN 1, TP 19. B: TN 20, FP 0, FN 0, TP 20. 둘 다 학습 정확도 100%. 이는 model.js의 고정 시드 실습 결과이며 실측 통계가 아니다.')
s.p('평가 데이터를 보며 계속 조건을 조정하면 개발용 검증 데이터가 된다. 최종 성능은 아직 보지 않은 별도 시험 데이터로 확인해야 한다. B의 좋은 결과가 현장 성능을 보장하지는 않는다.','small')

s.page('STUDENT PACK / 03 · 기록','우리 모둠의<br/>실험 노트')
s.p('모둠 별칭: __________________  역할: 조작 ______ 검증 ______ 기록 ______','small')
s.p('01  예측 · 뜨거운 모터는 모두 이상일까?','h2')
s.p('내 예상과 이유, 추가로 확인할 센서값을 쓰세요.');s.lines(2)
s.p('02  연결 · 센서에서 경보까지','h2')
s.p('여러 은닉층과 가중치 학습을 연결해 딥러닝을 설명하고, 사람이 조건을 정하는 PLC 규칙과 비교하세요.');s.lines(2)
s.p('03  실험 비교표','h2')
s.table([['조건','임계값','학습 정확도','평가 정확도','FP','FN','재현율'],['A','0.50','','','','',''],['B','0.50','','','','',''],['A','0.30','','','','',''],['A','0.70','','','','','']],[45,48,82,82,40,40,CW-337])
s.p('같은 임계값에서 A와 B는 어떻게 달랐나요? 오분류 데이터 ID와 실제 수치를 근거로 설명하세요.');s.lines(3)

s.page('STUDENT PACK / 04 · 성찰','오류를 찾는 사람이<br/>모델을 개선한다.')
s.p('04  판단 · 오경보와 이상 누락, 무엇을 줄일까?','h2')
s.p('생산팀과 정비팀의 입장을 각각 적고, 임계값 변경 결과를 근거로 우리 모둠의 제안을 쓰세요.');s.lines(3)
s.p('05  개선 · “딸깍”으로 해결되지 않은 문제','h2')
s.p('데이터 다양성·정답 오류·새 환경 중 하나를 고르세요. 문제 → 증거 → 개선 → 재검증 계획을 쓰세요.');s.lines(3)
s.p('06  활용 탐색 · 다른 분야에 적용한다면?','h2')
s.p('모터 진단 외에 이미지 분류 또는 소리 분류를 선택하세요. 입력 데이터 → 해결할 문제 → 출력, 딥러닝을 적용할 이유와 한계를 쓰세요. 제안과 실제 적용 사례를 구분하고, 실제 사례라면 출처를 적으세요.');s.lines(2)
s.note('<b>스스로 점검</b>  □ 딥러닝의 개념과 활용 분야를 내 말로 설명했다. □ 같은 조건에서 A/B를 비교했다. □ 정확도뿐 아니라 오류 유형을 확인했다. □ 수치에 근거해 개선과 재검증을 제안했다.')
s.p('출처·온라인 자료','h2')
s.p('교육과정: 2015 개정, 교육부 고시 제2020-236호 별책 10. 핵심 [12인기02-09]: 딥러닝의 개념 이해·활용 분야 탐색. 연계 [12인기03-07], [12인기03-08]: 훈련·테스트 데이터 및 학습·성능 평가. 공식 성취수준 및 학교 평가계획은 미확인. 확인일 2026-11-11.','small')
s.p('<link href="https://alswl50978-eng.github.io/motor-ai-lab/" color="#116854">수업 페이지·전체 출처 링크: https://alswl50978-eng.github.io/motor-ai-lab/</link>','small')
s.close()

t=PDF('teacher-guide.pdf','모터 이상을 찾는 AI - 교사용 운영안')
t.page('TEACHER GUIDE / 01 · 설계','학생의 클릭을<br/>근거 있는 판단으로.')
t.p('고3 · 인공지능 기초 · 60분 · 전기제어과 맞춤형 참여 수업','small')
t.p('교육과정 연결','h2')
t.p('<b>[12인기02-09] 딥러닝의 개념을 이해하고, 활용 분야를 탐색한다.</b><br/>연계 [12인기03-07]: 훈련 데이터와 테스트 데이터의 역할 비교. [12인기03-08]: 훈련 데이터로 분류 모델 학습 및 테스트 데이터로 성능 평가.')
t.p('2026학년도 고3 · 2015 개정 인공지능 기초. 교육부 고시 제2020-236호 별책 10에 근거한다. 공식 성취수준 및 학교 평가계획은 미확인. 별도 수록한 수준별 피드백은 수업용 설계안이다.','small')
t.note('<b>준비</b>  모둠별 브라우저 기기 1대, 학생 PDF 1부, 화면 공유 장치. 비율 계산과 센서·PLC 기초 개념을 먼저 확인한다. 계정·외부 라이브러리·실물 설비 연결은 필요 없다. 답안은 로컬 저장되므로 공용 기기에서는 PDF 저장 후 삭제하도록 안내한다.')
t.table([['시간','학생의 활동','교사의 발문·지원'],['0–8분','상황 읽기, 개별 예측, 역할 배정','“온도가 높다는 사실만으로 이상이라고 할 수 있을까?” 먼저 개인 의견을 적게 한다.'],['8–18분','딥러닝 개념과 PLC 규칙 비교','가중치 조정이 학습임을 짚는다. 수식 유도보다 학습과 추론의 차이에 집중한다.'],['18–28분','A 학습, 0.50 기록, 오분류 탐색','“학습 정확도와 새 조건 정확도가 왜 다를까?” 실제 오분류 ID를 찾게 한다.'],['28–38분','역할 교대, B 학습, 같은 임계값 비교','데이터 수·초기값·학습 횟수가 같은지 확인한다. 조건 다양성의 효과를 토론한다.'],['38–46분','A 임계값 0.30/0.70 비교, 입장 토론','생산팀·정비팀 관점에서 FP/FN 비용을 비교한다. 특정 임계값을 정답으로 제시하지 않는다.'],['46–52분','문제·증거·개선·재검증 작성','관측되지 않은 조건과 정답 품질을 어떻게 확인할지 묻는다.'],['52–60분','다른 활용 분야 탐색, 발표','이미지·소리 분류의 입력·출력과 적용 이유를 제안한다. Q2·Q6은 각자 설명하게 한다.']],[50,165,CW-215])
t.p('학급 규모가 크면 모든 모둠을 순차 발표시키지 말고 이웃 모둠끼리 동시에 공유한 뒤 대표 발표를 진행한다.','small')

t.page('TEACHER GUIDE / 02 · 피드백','정답 숫자보다<br/>설명의 근거를 봅니다.')
t.p('실행 확인용 기준 결과','h2')
t.table([['조건 / 임계값','학습 정확도','평가 정확도','TN / FP / FN / TP','이상 재현율'],['A / 0.50','100%','85%','15 / 5 / 1 / 19','95%'],['B / 0.50','100%','100%','20 / 0 / 0 / 20','100%']],[85,75,75,155,CW-390])
t.p('출처: model.js를 test.cjs로 검증한 고정 시드 합성 데이터 결과. 학습 80개, 평가 40개. B의 높은 점수는 실제 설비 성능을 뜻하지 않는다.','small',after=5)
t.p('예시 답안과 예상 반론','h2')
t.p('<b>Q1–2.</b> 높은 온도만으로 상태를 단정하지 않는다. 정답과 입력의 오차가 줄어들도록 가중치를 학습하고, 추론 점수를 임계값과 비교한다.<br/><b>Q3.</b> A는 학습 정확도가 높지만 보지 못한 운전 조건에서 FP 5건·FN 1건이 발생했다. B는 다양한 조건을 포함하여 이 평가 세트의 오류가 줄었다. 단순히 학습을 더 반복하는 것과 구분한다.<br/><b>Q4.</b> 생산팀은 불필요한 점검·정지, 정비팀은 이상 누락의 위험을 고려할 수 있다. 임계값은 실제 오류 비용과 검증 결과를 함께 보고 정해야 한다.<br/><b>Q5.</b> 부족한 운전 조건의 데이터를 수집하고 정답 품질을 확인한다. 조정에 사용하지 않은 별도 데이터로 재검증하며 실제 적용 전 기존 보호·점검 체계와의 역할을 검토한다.')
t.p('“규칙으로도 가능한데 왜 딥러닝인가?” → 이 단순한 합성 데이터는 규칙으로도 분류 가능하다. 딥러닝이 언제나 우수하다는 수업이 아니다. 신경망의 학습과 검증을 경험하고, 도입 시 규칙 방식과 비교하도록 한다.<br/>“A가 틀렸으니 과적합인가?” → 학습 조건과 새 조건의 차이에 따른 일반화 실패를 관찰한 것이다. 이 결과만으로 과적합 원인을 단정하지 않는다.')
t.p('관찰 평가 · 수업용 제안, 공식 성취수준 아님','h2')
t.table([['관찰 요소','도달 증거','보완이 필요한 경우'],['개념 설명','입력·가중치·출력의 관계를 자기 말로 설명','학습과 추론을 분리해 그림으로 다시 설명'],['비교 실험','같은 임계값에서 A/B 결과와 오류 ID 제시','한 번에 하나의 조건만 변경하도록 안내'],['의사결정','FP/FN 수치와 입장을 연결하고 재검증 제안','“문제→증거→개선→재검증” 문장 틀 제공']],[75,215,CW-290])
t.p('기기·연결 장애: 학생 PDF 2쪽의 대체 결과로 정확도·재현율을 계산하고 토론한다. 오프라인 대체는 실제 모델 학습 경험을 대신하지 않으므로 추후 기기 실습을 보완한다.','small')
t.p('<link href="https://alswl50978-eng.github.io/motor-ai-lab/" color="#116854">수업 및 전체 공식 출처 링크: https://alswl50978-eng.github.io/motor-ai-lab/</link><br/><link href="https://github.com/alswl50978-eng/motor-ai-lab" color="#116854">구현·검증 기록: https://github.com/alswl50978-eng/motor-ai-lab</link>','small')
t.page('TEACHER GUIDE / 03 · 기준과 평가','성취기준에서<br/>학생의 설명까지.')
t.p('2026학년도 고3 · 2015 개정 교육과정','small')
t.note('<b>핵심 [12인기02-09]</b> 딥러닝의 개념을 이해하고, 활용 분야를 탐색한다. Q2는 개념 이해, Q6은 활용 탐색의 증거이다. 실험 정확도가 높다는 이유만으로 이 기준에 도달했다고 판단하지 않는다.')
t.p('수준별 피드백 · 수업용 설계안','h2')
t.p('국가 공통 또는 학교 승인 성취수준을 인용한 표가 아니다. 공식 성취수준 및 학교의 평가계획 원문은 미확인 상태이다. 아래 단계는 형성평가를 위한 설계안이며 A·B·C 성적에 직접 대응하지 않는다.','small')
t.table([['평가 요소', '심화 도달', '기본 도달', '보완 지도'], ('개념 설명 · Q2', '여러 은닉층과 가중치 학습을 연결하여 딥러닝을 설명하고 PLC 규칙과 비교한다.', '신경망이 데이터로 학습한다는 개념을 설명한다.', '입력·은닉층·출력 그림과 문장 틀로 개념 설명을 다시 작성한다.'), ('활용 탐색 · Q6', '입력 데이터·해결할 문제·출력·딥러닝 적용 이유와 한계를 연결한다.', '활용 분야와 입력·출력을 연결하여 설명한다.', '제시된 분야를 골라 입력과 출력을 짝짓고 이유를 보완한다.'), ('학습·평가 · Q3', '훈련·평가 데이터의 역할을 구분하고 A/B 수치와 오류 사례를 해석한다.', '훈련·평가 결과를 기록하고 정확도를 비교한다.', '도움을 받아 학습·평가를 실행하고 결과표를 완성한다.')],[75,145,135,CW-355])
t.p('활용 탐색 예시 · 실제 도입 사례가 아닌 설계 제안','h2')
t.p('소리 분류를 선택했다면 입력은 녹음된 소리, 출력은 구분할 소리의 종류로 정한다. 왜 데이터 기반 학습을 고려하는지 설명하고, 배경 소음이나 새로운 녹음 환경에서도 확인해야 한다는 한계를 제시하도록 지도한다. 실제 사례를 조사했다면 기관·논문 출처를 추가한다.')
t.p('피드백 운영','h2')
t.p('Q2: 용어 나열에 그치면 “무엇이 학습 중 바뀌는가?”를 묻는다. Q6: 분야명만 적었다면 입력과 출력을 연결하게 한다. Q3: 결과만 옮겼다면 훈련·평가 데이터의 역할과 오류 사례를 설명하게 한다. 모둠 보고서와 별도로 개인 설명을 확인한다.')
t.p('<link href="https://www.moe.go.kr/boardCnts/viewRenew.do?boardID=141&amp;boardSeq=81884&amp;lev=0" color="#116854">공식 근거: 교육부 고시 제2020-236호, 별책 10</link>','small')
t.close()
print('Created student-pack.pdf (4 pages), teacher-guide.pdf (3 pages)')
