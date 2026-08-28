# -*- coding: utf-8 -*-
"""產生「多群組」示範頁：四個互不相連的群 + 未連結區"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "index.html"
OUT = ROOT / "demo-groups.html"
src = SRC.read_text(encoding="utf-8")
style = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
body = re.search(r"<body>(.*)</body>", src, re.S).group(1)

body = body.replace('const KEY = "renmai_data_v1";', 'const KEY = "renmai_groupdemo_v1";')
body = body.replace('''if ("serviceWorker" in navigator){
  window.addEventListener("load", () => navigator.serviceWorker.register("sw.js").catch(() => {}));
}''', '')
assert 'serviceWorker' not in body

_b_old = '<h1>織網</h1>'
_b_new = '<h1>織網</h1><span class="chip" style="background:#212121;color:#fff;flex:0 0 auto;">多群組示範</span>'
assert _b_old in body
body = body.replace(_b_old, _b_new, 1)

SEED = '''
function seedGroupDemo(){
  if (DB.customers.length) return;
  // 四個彼此不相連的群 + 兩位還沒連上任何人
  const G = [
    ["直銷組織", [["A1","陳志明","both","hot"],["A2","劉冠廷","both","hot"],["A3","吳俊傑","both","warm"],
                  ["A4","張家豪","customer","warm"],["A5","蔡佩珊","customer","cold"]],
      [["A1","A2","upline"],["A1","A3","upline"],["A2","A4","intro"],["A3","A5","intro"]]],
    ["瑜珈社團", [["B1","林美惠","both","hot"],["B2","王淑芬","customer","warm"],
                  ["B3","鄭曉玲","customer","cold"],["B4","黃雅婷","customer","warm"]],
      [["B1","B2","friend"],["B2","B3","club"],["B1","B4","intro"]]],
    ["前公司同事", [["C1","李建宏","customer","warm"],["C2","許明雄","customer","cold"],["C3","趙婉如","customer","warm"]],
      [["C1","C2","colleague"],["C2","C3","colleague"]]],
    ["家族", [["D1","陳淑貞","customer","hot"],["D2","陳世昌","customer","warm"]],
      [["D1","D2","family"]]],
  ];
  const cs = [], rs = [];
  let ri = 0;
  G.forEach(g => {
    g[1].forEach(m => cs.push({id:m[0], name:m[1], phone:"", company:g[0], source:"", lineId:"", birthday:"",
      tags:[g[0]], warmth:m[3], role:m[2], preference:"", note:"", pos:null,
      createdAt:Date.now(), updatedAt:Date.now()}));
    g[2].forEach(r => rs.push({id:"r" + (ri++), from:r[0], to:r[1], type:r[2], createdAt:Date.now()}));
  });
  [["E1","周文彬"],["E2","何雅琪"]].forEach(m => cs.push({id:m[0], name:m[1], phone:"", company:"還沒分群",
    source:"", lineId:"", birthday:"", tags:[], warmth:"cold", role:"customer", preference:"", note:"",
    pos:null, createdAt:Date.now(), updatedAt:Date.now()}));
  DB.customers = cs; DB.relations = rs;
  DB.interactions = []; DB.purchases = []; DB.tasks = [];
  save();
}
'''
body = body.replace('/* ---------- 啟動 ---------- */\nDB = loadDB();',
  '/* ---------- 啟動 ---------- */' + SEED + 'DB = loadDB();\nseedGroupDemo();')
assert 'seedGroupDemo();' in body

page = ('<!DOCTYPE html>\n<html lang="zh-Hant">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover, user-scalable=no">\n'
        '<title>織網 多群組示範</title>\n'
        '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lora:wght@400;500;600&family=Inter:wght@400;500;600&display=swap">\n'
        '<style>' + style + '</style>\n</head>\n<body>\n' + body + '\n</body>\n</html>\n')
OUT.write_text(page, encoding="utf-8")
print("demo-groups.html written, KB:", round(len(page.encode('utf-8'))/1024))
