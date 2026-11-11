"""Build the illustrated four-page Korean student mission book (ReportLab)."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent

from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor,white
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
pdfmetrics.registerFont(TTFont('KR',r'C:\Windows\Fonts\malgun.ttf'))
pdfmetrics.registerFont(TTFont('KB',r'C:\Windows\Fonts\malgunbd.ttf'))
pdfmetrics.registerFontFamily('KR',normal='KR',bold='KB')
W,H=A4; M=38; CW=W-2*M
NAVY='#24364D'; BLUE='#397BBD'; SKY='#EDF5FD'; GOLD='#FFC95D'; INK='#283A50'; MUTED='#61758B'; LINE='#D7E2ED'; ORANGE='#EA945D'
c=canvas.Canvas(str(ROOT/'student-pack.pdf'),pagesize=A4)
c.setTitle('LIGHT LAB | AI 전등 실험 미션북');c.setAuthor('LIGHT LAB')
def box(x,y,w,h,fill=white,stroke=None,r=12):
 c.setFillColor(HexColor(fill) if isinstance(fill,str) else fill)
 c.setStrokeColor(HexColor(stroke or fill) if isinstance(stroke or fill,str) else stroke or fill)
 c.roundRect(x,H-y-h,w,h,r,stroke=bool(stroke),fill=1)
def txt(x,y,s,size=10,color=INK,bold=False):
 c.setFillColor(HexColor(color));c.setFont('KB' if bold else 'KR',size);c.drawString(x,H-y-size,s)
def para(x,y,w,s,size=9.5,color=INK,leading=16,bold=False):
 st=ParagraphStyle('p',fontName='KB' if bold else 'KR',fontSize=size,leading=leading,textColor=HexColor(color),wordWrap='CJK')
 p=Paragraph(s,st);_,h=p.wrap(w,1000);p.drawOn(c,x,H-y-h);return h
def line(x,y,w,color=LINE):
 c.setStrokeColor(HexColor(color));c.setLineWidth(.6);c.line(x,H-y,x+w,H-y)
def bulb(x,y,scale=1):
 c.saveState();c.translate(x,H-y);c.scale(scale,scale)
 c.setFillColor(HexColor('#FFF0BF'));c.circle(0,0,43,fill=1,stroke=0)
 c.setFillColor(HexColor(GOLD));c.setStrokeColor(HexColor('#B88025'));c.setLineWidth(1.2);c.circle(0,5,25,fill=1,stroke=1)
 c.setFillColor(HexColor(NAVY));c.roundRect(-13,-30,26,17,4,fill=1,stroke=0)
 c.setStrokeColor(HexColor('#C2D1DF'));c.line(-10,-19,10,-19);c.line(-10,-24,10,-24)
 c.setFillColor(HexColor(NAVY));c.circle(-8,6,1.6,fill=1,stroke=0);c.circle(8,6,1.6,fill=1,stroke=0)
 p=c.beginPath();p.moveTo(-5,0);p.curveTo(-2,-4,2,-4,5,0);c.drawPath(p)
 for a,b,d,e in [(-35,5,-42,5),(35,5,42,5),(-27,34,-32,40),(27,34,32,40),(0,41,0,49)]:
  c.setStrokeColor(HexColor('#DCAC43'));c.line(a,b,d,e)
 c.restoreState()
def page(n,kicker,title,sub):
 c.setFillColor(HexColor('#FAFCFE'));c.rect(0,0,W,H,fill=1,stroke=0)
 box(M,24,79,22,NAVY,r=7);txt(M+10,28,'LIGHT LAB',9,'#FFFFFF',True)
 txt(M+91,29,'AI SWITCH / STUDENT MISSION BOOK',7,MUTED)
 for i in range(4):box(W-M-56+i*15,31,8,8,BLUE if i<n else '#E0E8F0',r=4)
 txt(M,66,kicker,9,BLUE,True);txt(M,87,title,25,NAVY,True);para(M,128,CW-80,sub,9.5,MUTED)
 line(M,782,CW);txt(M,794,'고1 전기과 · 교육용 가상 전등 실습',7.2,MUTED)
 txt(W-M-75,794,f'MISSION {n:02d} / 04',7.2,BLUE,True)
def section(y,num,title,sub=None):
 box(M,y,26,26,BLUE,r=8);txt(M+6,y+5,num,10,'#FFFFFF',True)
 txt(M+37,y+1,title,14,NAVY,True)
 if sub:para(M+37,y+26,CW-40,sub,9,MUTED)
def answer(y,h,prompt=None):
 box(M,y,CW,h,'#FFFFFF',LINE,r=12)
 if prompt:txt(M+15,y+12,prompt,8.5,BLUE,True)
 start=y+(46 if prompt else 25)
 for yy in range(int(start),int(y+h-9),25):line(M+15,yy,CW-30)
def note(y,label,s,h=62):
 box(M,y,CW,h,'#FFF7E6',r=12);txt(M+14,y+10,label,9,'#8F6424',True)
 para(M+14,y+29,CW-28,s,8.5,'#796B54',14)
def check(x,y,s):
 c.setStrokeColor(HexColor('#8297AE'));c.setLineWidth(.8);c.roundRect(x,H-y-9,9,9,2,fill=0,stroke=1);txt(x+16,y-1,s,9)
page(1,'MISSION 01 / DISCOVER','내 손이 스위치가 된다면?','사진을 가르치고, 새로운 손동작을 테스트하며 AI의 판단을 살펴보자.')
bulb(W-92,109,.75)
box(M,173,CW,39,'#FFFFFF',LINE,8);txt(M+14,185,'학년 / 반 ________   번호 ________   이름 ______________   모둠 ______________',9)
box(M,229,CW,102,NAVY,r=17)
txt(M+18,244,'오늘의 미션',10,'#FFCE6B',True)
para(M+18,269,CW-36,'손바닥 · 주먹 · 손 없음 사진을 학습시켜<br/><b>화면 속 전등을 켜고 끄는 AI 스위치</b>를 완성하자.',13,'#FFFFFF',23)
for i,(label,desc,col) in enumerate([('손바닥','전등 켜기','#FFF1CD'),('주먹','전등 끄기','#E8F1FC'),('손 없음','대기 · 꺼짐','#EDF0F5')]):
 x=M+i*(CW+12)/3;w=(CW-24)/3;box(x,346,w,73,col,r=12);txt(x+13,358,'0'+str(i+1),9,BLUE,True);txt(x+13,377,label,14,NAVY,True);txt(x+13,399,desc,8.5,MUTED)
section(443,'01','AI가 배우는 것, 사람이 정하는 것')
items=[('사진 입력','픽셀을 숫자로'),('특징 추출','사전학습 신경망'),('종류 분류','우리 사진으로 학습'),('전등 제어','사람이 정한 규칙')]
for i,(a,b) in enumerate(items):
 x=M+i*(CW/4);box(x,487,CW/4-8,70,'#FFFFFF',LINE,10);txt(x+11,500,a,11,NAVY,True);para(x+11,524,CW/4-28,b,8,MUTED,12)
para(M,574,CW,'<b>전이학습</b>은 이미 학습된 MobileNet으로 사진의 특징을 뽑고, 우리가 모은 사진으로 마지막 분류기를 새로 학습하는 방법이다. 큰 신경망 전체를 처음부터 학습하지 않는다.',9.5,INK,17)
note(642,'생각해 보기','“손바닥이면 켜기”는 AI가 스스로 정한 걸까? AI의 분류와 사람이 정한 제어 규칙을 구분해 보자.',70)
txt(M,736,'준비물  카메라 또는 손동작 사진 파일 · 인터넷 · 관찰하는 눈!',8.5,MUTED)
c.showPage()
page(2,'MISSION 02 / COLLECT & TRAIN','AI에게 사진을 가르치자','한 가지 모습만 보여 주지 말고, 거리와 각도를 조금씩 바꾸어 보자.')
section(177,'02','사진 수집 체크인','얼굴 대신 손과 배경을 담자. 세 종류를 각각 5장 이상, 최대 40장까지 모은다.')
for i,(title,col) in enumerate([('손바닥','#FFF1CD'),('주먹','#E8F1FC'),('손 없음','#EDF0F5')]):
 x=M+i*(CW+12)/3;w=(CW-24)/3;box(x,240,w,116,'#FFFFFF',LINE,12);box(x+10,250,w-20,27,col,r=7);txt(x+20,255,title,11,NAVY,True);txt(x+14,292,'모은 사진   ______ 장',9);txt(x+14,319,'다양한 각도 / 거리',8,MUTED)
check(M,377,'세 종류를 모두 모았다');check(M+245,377,'거리와 각도를 바꾸었다')
section(415,'03','사진 모으기 → 학습 → 새 사진 테스트')
steps=[('1','모으기','손동작 이름에 맞게 사진을 모은다.'),('2','학습하기','분류기 학습 버튼을 누르고 진행을 살핀다.'),('3','테스트하기','학습에 쓰지 않은 새 사진으로 확인한다.'),('4','개선하기','틀린 조건을 보완하고 또 다른 새 사진으로 확인한다.')]
for i,(num,a,b) in enumerate(steps):
 yy=460+i*48;box(M,yy,CW,40,'#FFFFFF',LINE,9);txt(M+13,yy+10,num,11,BLUE,True);txt(M+40,yy+10,a,10,NAVY,True);para(M+124,yy+10,CW-138,b,9,MUTED,14)
note(668,'실험 전에 기억하기','사진을 추가하거나 지우면 다시 학습해야 한다. 첫 학습에는 모델 다운로드를 위한 인터넷이 필요하다. 카메라는 HTTPS 또는 localhost에서 사용한다.',73)
para(M,750,CW,'사진·모델·테스트 기록은 새로고침하면 사라지고 답안만 브라우저에 저장된다. 학습 손실이 작아져도 새 사진에서 확인해야 한다. 테스트 조건이 다르면 모델 간 비교도 신중히 하자.',7.5,MUTED,12)
c.showPage()
page(3,'MISSION 03 / TEST & OBSERVE','처음 보는 손도 알아볼까?','학습 사진을 다시 맞히는 것과, 새로운 사진을 알아보는 것은 다르다.')
section(178,'Q1','AI와 스위치 규칙은 어떻게 다를까?','사진 → 특징 → 분류 → 전등 흐름을 써 보자. 학습하는 부분과 사람이 정한 부분을 구분하자.')
answer(241,105,'AI가 하는 일 / 사람이 정한 규칙')
section(369,'Q2','새 사진 실험 로그','거리 · 각도 · 조명 중 하나를 바꿔 보자. 실제 종류와 AI 예측을 비교하자.')
widths=[46,94,143,100,CW-383];heads=['모델','실제 손동작','바꾼 조건','AI 예측','결과']
x=M
for w,head in zip(widths,heads):box(x,433,w,30,NAVY,r=0);txt(x+7,442,head,8,'#FFFFFF',True);x+=w
for i in range(4):
 x=M;yy=463+i*35
 for j,w in enumerate(widths):
  box(x,yy,w,35,'#FFFFFF',LINE,r=0)
  if j==0:txt(x+9,yy+10,'v1' if i<2 else 'v2',8,MUTED)
  x+=w
txt(M,614,'결과에는 맞음 / 틀림 / 보류를 적자. 보류는 맞힌 것으로 세지 않는다.',8,MUTED)
answer(640,73,'맞힌 사례와 틀림·보류 사례는? 모두 맞았다면 더 확인할 조건은?')
note(726,'70% 규칙','최고 점수가 70% 미만이면 판단 보류 후 꺼짐. 손 없음도 꺼짐이다. 이 점수는 실제 정답 확률이나 안전 보증이 아니다.',48)
c.showPage()
page(4,'MISSION 04 / IMPROVE & INVENT','한 번 더 가르치고, 다르게 쓰자','잘 안 맞아도 괜찮다. 어떤 조건에서 달라졌는지 설명하는 것이 실험이다.')
section(177,'Q3','무엇을 더 가르쳤고, 달라졌을까?','추가한 사진의 조건, 모델 버전, 새 테스트 결과를 비교하자. 좋아지지 않아도 관찰한 그대로 쓰자.')
answer(239,133,'추가한 조건 → 다시 학습한 모델 → 또 다른 새 사진의 결과')
section(394,'Q4','다른 전기 장치에 활용한다면?','환풍기나 표시등을 골라 설계하자. 잘못 판단했을 때의 문제와 사람이 확인할 점도 쓰자.')
for i,label in enumerate(['입력','AI 분류','제어 규칙','출력']):
 x=M+i*CW/4;box(x,455,CW/4-7,43,SKY,r=8);txt(x+10,466,label+'  ______',9,BLUE,True)
answer(511,110,'나의 활용 아이디어 / 오작동 때의 문제 / 사람이 확인할 점')
box(M,642,CW,96,'#EEF5FC',r=12);txt(M+15,654,'MISSION COMPLETE?  나의 배움 체크',10,BLUE,True)
check(M+15,681,'분류와 제어 규칙을 구분했다');check(M+269,681,'새 사진으로 테스트했다')
check(M+15,708,'오류 조건과 개선 결과를 적었다');check(M+269,708,'활용 방법과 한계를 설명했다')
para(M,749,CW,'실제 설비 연결이 아닌 설계 제안이다. 사진 수·학습 횟수·70%는 수업용 설정이다.<br/>2022 개정 인공지능 기초 연계: [12인기02-05] 개념·활용 / [12인기02-06] 문제 해결·평가',7.1,MUTED,11)
c.save()
