#!/usr/bin/env python3
"""봉다방 정식판 잠금: 게임 index.html 맨 앞에 관리자 코드 잠금 화면을 끼워 넣는다.

쓰는 법: python3 gate.py <게임 index.html> <출력 index.html>
- 관리자 코드의 SHA-256 해시는 게임 안 ADM_H를 그대로 읽어 쓴다(코드 평문은 어디에도 없음).
- 잠겨 있으면 document.write('<plaintext>')로 뒤의 게임 HTML·스크립트를 아예 실행하지 않는다.
- 한 번 열면 localStorage 'bcg-gate' = 해시로 기억(코드가 바뀌면 다시 잠김).
- 잠금을 풀려면(일반 공개) 이 스크립트를 거치지 말고 게임 index.html을 그대로 올리면 된다.
"""
import re, sys, json

src, out = sys.argv[1], sys.argv[2]
html = open(src, encoding='utf-8').read()
m = re.search(r"ADM_H='([0-9a-f]{64})'", html)
if not m:
    sys.exit('ADM_H를 못 찾음')
H = m.group(1)

LOCK = r'''<style>html,body{margin:0;height:100%;background:#141716}
#bcgL{position:fixed;inset:0;display:flex;align-items:center;justify-content:center;padding:16px;background:#141716;color:#e9edeb;font:15px/1.5 "Pretendard","Apple SD Gothic Neo","Malgun Gothic",system-ui,sans-serif;z-index:99999}
#bcgL .bx{width:100%;max-width:360px;background:#1b1f1e;border:1px solid #383d3b;padding:26px 22px;text-align:center;clip-path:polygon(0 0,calc(100% - 14px) 0,100% 14px,100% 100%,14px 100%,0 calc(100% - 14px))}
#bcgL h1{font-size:20px;margin:6px 0 4px}#bcgL p{color:#8d9692;margin:0 0 16px;font-size:14px}
#bcgL input{width:100%;box-sizing:border-box;padding:12px;background:#232726;border:1px solid #383d3b;color:#e9edeb;font:inherit;text-align:center;outline:none}
#bcgL input:focus{border-color:#3fd99a}
#bcgL button{width:100%;margin-top:10px;padding:12px;background:#3fd99a;color:#0c1411;border:0;font:inherit;font-weight:700;cursor:pointer}
#bcgL .er{color:#ff7b6b;font-size:13px;min-height:20px;margin-top:8px}
#bcgL a{color:#3fd99a;font-size:13px;text-decoration:none;display:inline-block;margin-top:6px}</style>
<div id="bcgL"><div class="bx"><div style="font-size:34px">🔒</div><h1>봉다방 타이쿤 정식판</h1><p>정식판은 아직 준비 중이에요.<br>지금은 데모로 즐겨 주세요.</p>
<form id="bcgF"><input id="bcgI" type="password" placeholder="관리자 코드" autocomplete="off"><button>들어가기</button></form><div class="er" id="bcgE"></div>
<a href="../bongcafe-demo/">데모 하러 가기 →</a><br><a href="../">봉다방게임즈 홈</a></div></div>
<script>document.getElementById('bcgF').onsubmit=async function(e){e.preventDefault();var v=document.getElementById('bcgI').value.trim(),h='';try{var b=await crypto.subtle.digest('SHA-256',new TextEncoder().encode(v));h=Array.from(new Uint8Array(b)).map(function(x){return x.toString(16).padStart(2,'0')}).join('')}catch(_){}
if(h===BCG_H){try{localStorage.setItem('bcg-gate',h)}catch(_){}location.reload()}else document.getElementById('bcgE').textContent='코드가 맞지 않아요'}</script>'''

GATE = ('<script>var BCG_H="%s";(function(){var ok=false;try{ok=localStorage.getItem("bcg-gate")===BCG_H}catch(e){}'
        'if(!ok){document.write(%s+"<plaintext style=\\"display:none\\">")}})();</script>') % (H, json.dumps(LOCK, ensure_ascii=False).replace('</', '<\\/'))

# <meta charset> 바로 뒤(다른 어떤 스크립트보다 먼저)에 넣는다
i = html.lower().find('<head>')
if i < 0:
    sys.exit('<head> 없음')
j = html.find('>', html.lower().find('<meta charset', i)) + 1 if '<meta charset' in html.lower() else i + 6
html = html[:j] + GATE + html[j:]
open(out, 'w', encoding='utf-8').write(html)
print('잠금 넣음', out)
