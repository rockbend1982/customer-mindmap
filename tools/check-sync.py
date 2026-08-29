# -*- coding: utf-8 -*-
"""五檔同步檢查

這個專案有五個 HTML，程式主體共用、關係圖畫法不同：

  四檔（正式）  index.html / demo.html / demo-groups.html / artifact-sim.html
                關係圖畫法完全一樣，整段必須逐字相同
  第五檔（demo） demo-mindmap.html
                心智圖風格，關係圖畫法是另一套，只有「共通功能」要跟上

改東西時：
  改到關係圖畫法      → 只套四檔（第五檔自己一套）
  改到其他任何地方    → 五檔都要套（設定、名單、業績、詳情、CSS、資料處理）

用法：python3 tools/check-sync.py
"""
import hashlib
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
CORE = ["index.html", "demo.html", "demo-groups.html", "artifact-sim.html"]
ALL = CORE + ["demo-mindmap.html"]

# 五檔都必須具備的共通功能特徵（漏掉任何一個就是有檔案沒跟上）
SHARED = [
    ("節點形狀設定", "const NODE_SHAPES = {patch:"),
    ("形狀同步到名單", "body.shape-patch .person .dot,"),
    ("形狀同步到膠囊", "body.shape-patch .ppill .av,"),
    ("形狀同步到圖例", "body.shape-patch #graph-legend .swdot{"),
    ("套外觀時一起套形狀", 'classList.toggle("shape-patch", currentShape() === "patch")'),
    ("換形狀時重套外觀", "save(); applySkin(); renderSettings();"),
    ("匯入備份保住形狀", "if (NODE_SHAPES[st.nodeShape])"),
    ("舊裝置設定升級", "function upgradeLegacyColors("),
    ("六套配色主題", "const THEMES = {"),
    ("關係針法編碼", "const RELTYPE_STITCH = {"),
    ("首頁快捷鈕視覺重心", ".qa button.lead .ic{"),
]

# 四檔的關係圖畫法必須逐字相同（起訖以這兩個函式為界）
SEG_START = "function convexHull(pts){"
SEG_END = "function applyGraphTransformOnly(){"

fail = []
src = {}
for name in ALL:
    p = BASE / name
    if not p.exists():
        fail.append("缺檔案：" + name)
        continue
    src[name] = p.read_text(encoding="utf-8")

print("=== 共通功能（五檔都要有）===")
for label, needle in SHARED:
    miss = [n for n in ALL if n in src and needle not in src[n]]
    print(("  OK   " if not miss else "  MISS ") + label + ("" if not miss else "  ← " + ", ".join(miss)))
    if miss:
        fail.append("%s 沒跟上：%s" % (", ".join(miss), label))

print("\n=== 關係圖畫法（四檔要逐字相同）===")
seg = {}
for name in CORE:
    s = src.get(name, "")
    i, j = s.find(SEG_START), s.find(SEG_END)
    if i < 0 or j < 0 or j <= i:
        fail.append("%s 找不到關係圖區段" % name)
        print("  ERR  %s 找不到區段" % name)
        continue
    seg[name] = hashlib.md5(s[i:j].encode("utf-8")).hexdigest()
    print("  %-20s %s" % (name, seg[name][:12]))
if len(set(seg.values())) > 1:
    fail.append("四檔的關係圖畫法不一致")
    print("  → 不一致")
elif seg:
    print("  → 一致")

print("\n=== 結果 ===")
if fail:
    for f in fail:
        print("  FAIL " + f)
    sys.exit(1)
print("  五檔同步，沒有落後的檔案")
