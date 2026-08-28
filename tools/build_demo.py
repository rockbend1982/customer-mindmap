# -*- coding: utf-8 -*-
"""從 style/nuskin 分支的 index.html 產生 demo 版與 artifact 模擬版"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "index.html"
OUT = ROOT

src = SRC.read_text(encoding="utf-8")
style = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
body = re.search(r"<body>(.*)</body>", src, re.S).group(1)

body = body.replace('const KEY = "renmai_data_v1";', 'const KEY = "renmai_nuskin_demo_v12";')
body = body.replace('''if ("serviceWorker" in navigator){
  window.addEventListener("load", () => navigator.serviceWorker.register("sw.js").catch(() => {}));
}''', '')
assert 'serviceWorker' not in body
_badge_old = '<h1>織網</h1>'
_badge_new = '<h1>織網</h1><span class="chip" style="background:#212121;color:#fff;flex:0 0 auto;">DEMO 假資料</span>'
assert _badge_old in body, "DEMO badge anchor not found（App 是不是又改名了？）"
body = body.replace(_badge_old, _badge_new, 1)
assert 'DEMO 假資料' in body

seed = '''
function seedDemo(){
  if (DB.customers.length) return;
  const P = [
    ["c01","陳志明","0912-000-001","明泰保險 業務經理","老客戶",["保險","台北"],"hot","很挺我，轉介紹主力","保守型，只考慮有保本的；決策前一定問太太","03-15","chihming_tw"],
    ["c02","林美惠","0912-000-002","美惠美容工作室","社團認識",["美容","高潛力"],"hot","人脈廣，社團核心人物","喜歡天然無香精；預算彈性但要看到成分表","","meihui.beauty"],
    ["c03","張家豪","0912-000-003","豪運車業","陳志明介紹",["汽車"],"warm","太太對儲蓄險有興趣","重視 CP 值，會多方比價；只在週日有空"],
    ["c04","王淑芬","0912-000-004","芬芳花坊","市集擺攤認識",["台中"],"warm",""],
    ["c05","李建宏","0912-000-005","宏達會計事務所","大學同學",["財務"],"warm","每年報稅季後聚一次"],
    ["c06","黃雅婷","0912-000-006","婷婷甜點","網路社群",["餐飲"],"cold",""],
    ["c07","吳俊傑","0912-000-007","傑克健身房 教練","林美惠介紹",["健身","高潛力"],"warm","想擴點，可能有資金需求","偏好一次付清拿折扣；訊息用 LINE 比較快"],
    ["c08","蔡佩珊","0912-000-008","珊瑚旅行社","展覽交換名片",["旅遊"],"cold",""],
    ["c09","劉冠廷","0912-000-009","廷威室內設計","老同事",["設計","台北"],"hot","案場多，常互相介紹客戶"],
    ["c10","鄭曉玲","0912-000-010","玲瓏服飾","王淑芬介紹",["服飾","台中"],"cold",""],
    ["c11","周文彬","0912-000-011","彬彬水電行","網路詢問",["工程"],"cold","只來問過一次價，還沒建立任何關係"],
  ];
  DB.customers = P.map(p => ({id:p[0], name:p[1], phone:p[2], company:p[3], source:p[4],
    tags:p[5], warmth:p[6], note:p[7], preference:p[8] || "", birthday:p[9] || "", lineId:p[10] || "", role:(["c01","c02","c07","c09"].includes(p[0]) ? "both" : "customer"), pos:null, createdAt:Date.now(), updatedAt:Date.now()}));
  const R = [
    ["c01","c03","intro"],["c02","c07","intro"],["c04","c10","intro"],["c09","c02","intro"],
    ["c04","c06","family"],
    ["c01","c09","friend"],["c05","c01","friend"],
    ["c05","c08","colleague"],["c01","c09","colleague"],
    ["c01","c09","upline"],["c02","c07","upline"],
    ["c02","c04","club"],["c07","c03","club"],
  ];
  DB.relations = R.map((r,i) => ({id:"r"+i, from:r[0], to:r[1], type:r[2], createdAt:Date.now()}));
  const I = [
    ["c09","2026-08-26","介紹新案場，聊下半年合作方式"],
    ["c01","2026-08-25","聊了新保單方案，下週約見面細談"],
    ["c02","2026-08-24","生日聚會碰到，聊近況，氣氛很好"],
    ["c03","2026-08-20","車子保養順便聊，太太想了解儲蓄險"],
    ["c07","2026-08-18","上完課聊到健身房想擴點"],
    ["c04","2026-08-10","母親節檔期後回訪，生意不錯"],
    ["c05","2026-08-05","報稅季結束，約了咖啡敘舊"],
    ["c06","2026-07-15","甜點店開幕去捧場"],
  ];
  DB.interactions = I.map((x,i) => ({id:"i"+i, customerId:x[0], date:x[1], text:x[2], createdAt:Date.now()+i}));
  const B = [
    ["c01","2026-03-12","終身壽險 20 年期",120000,"分 12 期"],
    ["c01","2025-11-02","醫療附約",18000,""],
    ["c03","2026-06-08","儲蓄險三年期",36000,"太太的名義投保"],
    ["c05","2026-01-20","report 顧問年約",24000,""],
    ["c04","2026-05-06","母親節花禮專案",4800,"公司團購"],
    ["c02","2026-08-05","保健食品三入組",5400,"",30],
    ["c09","2026-07-30","辦公室設計監工費",85000,"分兩期"],
    ["c06","2025-12-24","聖誕蛋糕預購",1200,""],
  ];
  DB.purchases = B.map((x,i) => ({id:"p"+i, customerId:x[0], date:x[1], item:x[2], qty:1, unit:x[3],
    amount:x[3], svUnit:null, sv:null, orderId:null, note:x[4], cycle:x[5] || null, createdAt:Date.now()+i}));
  // 體驗紀錄：試用過但還沒成交（蔡佩珊）、以及試用後成交的（張家豪）
  DB.purchases.push(
    {id:"pt1", customerId:"c08", date:"2026-08-22", orderId:"o_trial1", kind:"trial",
     reaction:"膚觸有感，想再試一次", item:"ageLOC LumiSpa 潔膚儀", qty:1,
     unit:null, amount:null, svUnit:null, sv:null, cycle:null, note:"在她家客廳體驗", createdAt:Date.now()+80},
    {id:"pt2", customerId:"c03", date:"2026-05-30", orderId:"o_trial2", kind:"trial",
     reaction:"太太覺得不錯", item:"活顏深層抗皺精華", qty:2,
     unit:null, amount:null, svUnit:null, sv:null, cycle:null, note:"", createdAt:Date.now()+81},
  );
  // 一張單多品項、且其中一項買了 3 組
  const ORDER = "o_demo1";
  DB.purchases.push(
    {id:"pm1", customerId:"c02", date:"2026-08-26", orderId:ORDER, item:"ageLOC LumiSpa 潔膚儀",
     qty:1, unit:8900, amount:8900, svUnit:120, sv:120, cycle:null, note:"母親節檔期", createdAt:Date.now()+90},
    {id:"pm2", customerId:"c02", date:"2026-08-26", orderId:ORDER, item:"活顏深層抗皺精華",
     qty:3, unit:1780, amount:5340, svUnit:35, sv:105, cycle:null, note:"母親節檔期", createdAt:Date.now()+91},
  );
  DB.tasks = [
    {id:"t0", customerId:"c01", due:todayStr(), text:"約見面談新保單方案", done:false, createdAt:Date.now()},
    {id:"t1", customerId:"c03", due:"2026-08-20", text:"回覆太太的儲蓄險試算", done:false, createdAt:Date.now()},
    {id:"t2", customerId:"c07", due:"2026-09-15", text:"追蹤擴點資金需求", done:false, createdAt:Date.now()},
  ];
  save();
}
'''
body = body.replace('/* ---------- 啟動 ---------- */\nDB = loadDB();',
  '/* ---------- 啟動 ---------- */' + seed + 'DB = loadDB();\nseedDemo();')
assert 'seedDemo();' in body

demo = ('<meta charset="utf-8">\n<title>織網 Nu Skin 試裝</title>\n'
  '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
  '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
  '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lora:wght@400;500;600&family=Inter:wght@400;500;600&display=swap">\n'
  '<style>' + style + '</style>\n' + body)
(OUT / "renmai-nuskin-demo.html").write_text(demo, encoding="utf-8")

sim = ('<!doctype html><html><head><base href="http://localhost:9999/_f/fake/">'
       '<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
       '<style>:root{color-scheme:light}body{margin:0;padding:0;font:14px -apple-system,BlinkMacSystemFont,sans-serif;'
       'background:#faf9f5;color:#141413}img{max-width:100%}</style></head><body>\n'
       + demo + '\n</body></html>')
(OUT / "artifact-sim.html").write_text(sim, encoding="utf-8")
print("regenerated ok")


_demo = (OUT / "renmai-nuskin-demo.html")
if _demo.exists():
    _s = _demo.read_text(encoding="utf-8")
    _s = ('<!DOCTYPE html>\n<html lang="zh-Hant">\n<head>\n'
          '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover, user-scalable=no">\n'
          + _s + '\n</body>\n</html>\n')
    _s = _s.replace('<title>織網 Nu Skin 試裝</title>', '<title>織網 DEMO（假資料）</title>', 1)
    _i = _s.find('<div id="app">')
    assert _i > 0, "找不到 app 錨點"
    _s = _s[:_i] + '</head>\n<body>\n' + _s[_i:]
    assert 'DEMO 假資料' in _s, "DEMO 標籤不見了"
    (ROOT / "demo.html").write_text(_s, encoding="utf-8")
    _demo.unlink()
    print("demo.html written")
