#!/usr/bin/env python3
"""방문자 집계(GoatCounter) 태그를 html의 <head> 맨 앞(메타 charset 뒤)에 넣는다. 이미 있으면 그대로 둔다.
쓰는 법: python3 tools/stats.py <html> [<html> ...]
- 잠금(gate.py)보다 앞에 들어가야 잠긴 화면 방문도 셈. gate.py를 다시 돌린 뒤에 이걸 돌릴 것.
- 쿠키 없음, 개인정보 안 모음. 집계 사이트 코드는 아래 CODE.
"""
import sys
CODE = 'bongcafegames'
TAG = '<script data-goatcounter="https://%s.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>' % CODE
for f in sys.argv[1:]:
    s = open(f, encoding='utf-8').read()
    if 'gc.zgo.at/count.js' in s:
        print('이미 있음', f); continue
    lo = s.lower(); i = lo.find('<meta charset')
    j = s.find('>', i) + 1 if i >= 0 else lo.find('<head>') + 6
    s = s[:j] + TAG + s[j:]
    open(f, 'w', encoding='utf-8').write(s); print('넣음', f)
