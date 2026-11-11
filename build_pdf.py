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
  self.c=canvas.Canvas(str(ROOT/name),pagesize=A4); self.c.setTitle(title);self.c.setAuthor('LIGHT LAB');self.n=0;self.y=0
 def page(self,label,title):
  if self.n:self.finish_page();self.c.showPage()
  self.n+=1;self.c.setFillColor(GREEN);self.c.rect(0,H-9,W,9,fill=1,stroke=0)
  self.c.setFont('KRB',9);self.c.drawString(M,H-39,'LIGHT LAB');self.c.setFont('KR',8);self.c.drawRightString(W-M,H-39,label)
  self.y=H-68;self.p(title,'title',after=19)
 def finish_page(self):
  assert self.y>49, f'Page overflow: {self.n}, y={self.y}'
  self.c.setStrokeColor(LINE);self.c.line(M,40,W-M,40);self.c.setFillColor(MUTED);self.c.setFont('KR',7)
  self.c.drawString(M,27,'고1 전기과 | 손동작으로 가상 전등 제어 | 학교 공식 발행물 아님')
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

s=PDF('student-pack.pdf','LIGHT LAB - 학생 학습지')
s.page('STUDENT / 01 · 개념','내 손으로 가르치는<br/>AI 스위치')
s.p('고1 전기과 · 2022 개정 인공지능 기초 연계 · 50분 수업 제안','small')
s.note('손바닥은 켜기, 주먹은 끄기, 손이 없는 배경은 대기. 사진을 학습시켜 화면 속 전등을 제어한다. 실제 전기 배선이나 설비를 연결하지 않는다.')
s.p('01  알아보는 일과 켜는 일','h2')
s.table([['사진 입력','신경망 특징 추출','새 분류기','전등 규칙'],['픽셀을 숫자로 입력','여러 층의 신경망으로 특징 계산','손바닥·주먹·손 없음 분류','손바닥이면 켜기']])
s.p('이 실습은 사전학습된 MobileNet의 특징 추출 부분을 활용하고, 우리가 모은 사진으로 마지막 분류기를 학습하는 전이학습이다. 큰 신경망 전체를 처음부터 학습하지 않는다. 손동작 분류는 AI가 수행하고, 분류 결과를 전등에 연결하는 규칙은 사람이 정한다.')
s.p('02  실습 순서','h2')
s.table([['단계','할 일'],['모으기','손바닥·주먹·손 없음 사진을 각각 5장 이상 모은다. 거리와 각도를 바꾸고 얼굴은 담지 않는다. 종류별 최대 40장.'],['학습하기','분류기 학습 버튼을 누른다. 진행과 손실을 관찰한다.'],['테스트하기','학습에 쓰지 않은 새 사진으로 예측한다. 실제 종류를 선택하고 결과를 기록한다.'],['개선하기','틀린 조건의 사진을 추가하고 다시 학습한다. 또 다른 새 사진으로 확인한다.']],[80,CW-80])
s.note('학습 사진을 추가하면 기존 모델로 예측할 수 없고 다시 학습해야 한다. 가장 높은 점수가 70% 미만이면 판단 보류, 전등은 꺼진다. 손 없음도 대기·꺼짐이다. 사진 개수·학습 횟수·70%는 수업용 설정이며 성능 보장 기준이 아니다.')
s.p('준비: 웹캠 또는 손동작 사진 파일, 인터넷. 카메라는 HTTPS/localhost에서 사용한다. 처음 학습할 때 모델 다운로드가 필요하다. 사진은 페이지 메모리에서 처리하고, 답안만 브라우저에 저장한다.','small')
s.page('STUDENT / 02 · 실험 기록','처음 보는 사진도<br/>알아볼 수 있을까?')
s.p('모둠 별칭: _______________________','small')
s.p('1. AI와 스위치 규칙은 무엇이 다른가?','h2')
s.p('사진 → 특징 → 분류 → 전등 흐름으로 설명하자. 학습하는 부분과 사람이 정한 규칙을 구분하자.');s.lines(3)
s.p('2. 새 사진에서 어떤 일이 생겼는가?','h2')
s.table([['모델','실제 손동작','바꾼 조건','AI 예측','맞음/틀림/보류'],['v1','','','',''],['v1','','','',''],['v2','','','',''],['v2','','','','']],[45,95,145,100,CW-385])
s.p('맞힌 사례와 틀리거나 보류한 사례를 설명하자. 모두 맞았다면 더 확인할 조건을 제안하자.');s.lines(3)
s.note('손실이 작아지거나 학습 사진을 잘 맞혀도 새 사진에서 확인해야 한다. 보류는 맞힌 것으로 세지 않는다. 모델별 기록의 맞힌 비율을 비교하되 테스트 조건과 사진이 다르면 공정한 비교인지 함께 검토한다.')
s.page('STUDENT / 03 · 개선과 활용','더 가르치고,<br/>다르게 써 보기')
s.p('3. 무엇을 더 가르쳤고, 달라졌는가?','h2')
s.p('추가한 사진의 조건, 다시 학습한 모델 버전, 새 테스트 결과를 비교하자. 좋아지지 않아도 관찰한 그대로 적자.');s.lines(4)
s.p('4. 다른 전기 장치에 활용한다면?','h2')
s.p('환풍기나 표시등을 골라 입력 → AI 분류 → 제어 규칙 → 출력을 제안하자. 잘못 판단했을 때의 문제와 사람이 확인할 점도 적자. 실제 설치 사례가 아닌 설계 제안이다.');s.lines(4)
s.note('자기 점검: □ 딥러닝 분류와 제어 규칙을 구분했다. □ 학습과 테스트 사진을 구분했다. □ 틀린 조건과 개선 결과를 기록했다. □ 다른 장치의 활용 방법과 한계를 설명했다.')
s.p('연계: [12인기02-05] 개념·활용 탐색 / [12인기02-06] 문제 해결·성능 평가. 평가 질문은 수업용 설계안이며 공식 수준별 성취수준이 아니다.','small')
s.p('<link href="https://www.tensorflow.org/js/tutorials/transfer/image_classification">참고: TensorFlow 이미지 분류 전이학습</link>','small')
s.close()
t=PDF('teacher-guide.pdf','LIGHT LAB - 교사용 운영안')
t.page('TEACHER / 01 · 수업 설계','딥러닝을 체험하는<br/>첫 번째 스위치')
t.p('2026학년도 고1 전기과 수준 · 50분 제안 · 2022 개정 인공지능 기초 연계','small')
t.p('핵심 성취기준','h2')
t.p('[12인기02-05] 인공신경망과 딥러닝의 특성에 대한 이해를 바탕으로 활용 분야를 탐색한다.<br/>[12인기02-06] 딥러닝을 활용하여 실생활 및 다양한 학문 분야의 문제를 해결하고, 성능을 평가한다.')
t.p('교육과정 MCP의 officialText와 대조했다. 실제 학교 과목 편성은 확인한다. 공식 수준별 성취수준은 인용하지 않으며 아래 평가는 수업용 설계안이다.','small')
t.table([['시간','학생 활동','교사의 확인'],['0–5분','손동작 스위치 상황 예측','사진을 알아보는 것과 스위치 규칙의 차이'],['5–12분','사진→특징→분류→전등 설명','사전학습 신경망과 새 분류기의 역할'],['12–25분','세 종류 사진 수집·학습','배경 다양성, 정답 이름, 사진 수 균형'],['25–40분','새 사진 테스트·오류 기록·재학습','독립 테스트, 오류 조건, 모델 버전 비교'],['40–50분','다른 장치 활용 제안·개인 설명','Q1·Q4 개념과 활용, Q2·Q3 평가와 개선']],[55,195,CW-250])
t.note('준비: 카메라 있는 기기 또는 사진 파일, 인터넷. HTTPS/localhost로 연다. 첫 학습 전에 모델 다운로드 가능 여부를 확인한다. 카메라는 버튼을 눌러 요청하며 얼굴 대신 손과 배경을 담는다. 실제 전원·설비에 연결하지 않는다.')
t.p('카메라가 없으면 이미지 파일로 같은 과정을 수행한다. 모델 다운로드가 막히면 실제 학습은 불가능하다. 준비된 사진·결과로 분류와 규칙을 토의하고 실제 학습은 연결 가능한 환경에서 보완한다.','small')
t.page('TEACHER / 02 · 평가와 피드백','성공한 전등보다<br/>설명의 근거를 봅니다.')
t.p('성취기준과 수행 증거','h2')
t.table([['연계','도달 증거','보완 지도'],['02-05 / Q1·Q4','특징 추출·분류·규칙 구분, 다른 장치의 입력·출력·한계 설명','개념 흐름에 각 단계의 담당을 표시'],['02-06 / 기록·Q2·Q3','새 사진의 실제/예측 비교, 오류 조건 기록, 재학습 후 새 테스트','한 조건씩 바꾸고 오류 사례를 말로 설명']],[90,215,CW-305])
t.p('예시 답안','h2')
t.p('<b>Q1.</b> 기존 신경망은 사진의 특징을 추출하고, 새 분류기는 학생 사진으로 학습한다. 손바닥이면 전등을 켜는 연결은 사람이 정한 규칙이다.<br/><b>Q2.</b> 같은 손동작이라도 배경·거리·조명 변화에 따라 예측이 달라질 수 있다. 실제 관찰한 결과로 설명하고 오류를 강제로 만들어 쓰지 않는다.<br/><b>Q3.</b> 오류 조건을 포함한 사진을 추가한 뒤 새 사진으로 확인한다. 개선되지 않았다면 정답·사진 조건·테스트 범위를 점검한다.<br/><b>Q4.</b> 손동작으로 환풍기 운전을 요청하는 설계를 제안할 수 있다. 오인식 때 불필요한 동작이 생길 수 있으므로 사람이 확인하는 절차를 제안한다. 실제 도입 사례나 안전 설계로 주장하지 않는다.')
t.p('예상 반론과 설명','h2')
t.p('“버튼을 누르면 끝 아닌가?” → 모델이 맞혔는지 정답과 비교하고, 학습·테스트 구분 및 오류 조건을 설명하게 한다.<br/>“70%면 안전한가?” → 수업용 보류 기준이며 실제 정답 확률·안전 기준이 아니다.<br/>“신경망을 전부 학습했나?” → 아니다. 사전학습 MobileNet은 고정하고 마지막 분류기만 학습한다.')
t.p('사진은 페이지 메모리에만 유지한다. 답안은 브라우저 저장소에 남는다. 공용 기기는 인쇄/PDF 저장 후 이 실습 답안 지우기를 사용한다. 페이지를 닫으면 사진·모델·테스트 기록은 사라진다.','small')
t.p('<link href="https://www.moe.go.kr/boardCnts/viewRenew.do?boardID=141&amp;boardSeq=93458&amp;lev=0">교육부 2022 개정 교육과정 고시</link><br/><link href="https://codelabs.developers.google.com/tensorflowjs-transfer-learning-teachable-machine">Google TensorFlow.js 전이학습 실습</link>','small')
t.close()
print('Created LIGHT LAB PDFs: student 3 pages, teacher 2 pages')
