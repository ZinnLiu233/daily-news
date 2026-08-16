from pathlib import Path
import json, html
from datetime import datetime

ROOT = Path(__file__).resolve().parent
cfg = json.loads((ROOT/"config.json").read_text(encoding="utf-8"))
data = json.loads((ROOT/"data/latest.json").read_text(encoding="utf-8"))
BASE = cfg["site"].get("base_path","").rstrip("/")

def e(x): return html.escape(str(x or ""))

# --- pika design tokens ---
def card(item):
    title_zh = item.get('title_zh') or item.get('title') or ""
    title_en = item.get('title') if item.get('title_zh') and item.get('title_zh') != item.get('title') else ""
    summary = item.get('summary_zh') or item.get('summary') or ""
    why = item.get('why_it_matters_zh') or item.get('why_it_matters') or ""
    excerpt = item.get('original_excerpt') or ""
    # meta line: source · date · badge
    meta_parts = []
    if item.get('source'): meta_parts.append(item['source'])
    if item.get('published_at'): meta_parts.append(item['published_at'])
    if item.get('badge'): meta_parts.append(item['badge'])
    meta_line = " · ".join(meta_parts)

    return f"""
    <article class="card">
      <div class="card-meta">{e(meta_line)}</div>
      <h3 class="card-title"><a href="{e(item.get('url'))}" target="_blank" rel="noopener noreferrer">{e(title_zh)}</a></h3>
      {f'<div class="card-en">{e(title_en)}</div>' if title_en else ''}
      <p class="card-summary">{e(summary)}</p>
      {f'<div class="card-why"><span>为什么重要</span>{e(why)}</div>' if why else ''}
      {f'<blockquote class="card-excerpt"><span>原文</span>{e(excerpt)}</blockquote>' if excerpt else ''}
      <a class="card-link" href="{e(item.get('url'))}" target="_blank" rel="noopener noreferrer">阅读原文 →</a>
    </article>"""

archive_dir = ROOT/"archive"
archive_links = []
for p in sorted(archive_dir.glob("*.html"), reverse=True)[:28]:
    archive_links.append(f'<a href="{BASE}/archive/{e(p.name)}">{e(p.stem)}</a>')

# Section rendering - top gets hero treatment (first item large)
section_html = []
for idx, s in enumerate(cfg["sections"]):
    items = data["sections"].get(s["id"], [])
    if not items and s["id"] not in ("top","for_you"):
        continue
    if not items:
        body = '<p class="muted">今日暂无高信号内容。</p>'
    elif s["id"] == "top" and len(items) >= 1:
        # Hero: first item larger, rest normal
        hero = card(items[0]).replace('class="card"', 'class="card card-hero"', 1)
        rest = "".join(card(i) for i in items[1:])
        body = hero + rest
    else:
        body = "".join(card(i) for i in items)
    section_html.append(f'<section id="{e(s["id"])}"><h2 class="section-title">{e(s["title"])}</h2><div class="section-grid">{body}</div></section>')

signal = ""
if data.get("signal"):
    signal = f'<section class="signal"><div class="signal-label">The Signal</div><p>{e(data["signal"])}</p></section>'

# --- pika styles: warm stone + ink + amber accent, own type (no clawpage copy) ---
style = """
:root{--bg:#fdfbf7;--surface:#ffffff;--surface-soft:#f7f3ee;--ink:#1a1a18;--muted:#8a857e;--line:#ece6dc;--amber:#d48806;--amber-soft:#fef3c7;--sage:#6b7c3f;--slate:#6b7280;--radius:16px}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.7 'Inter',ui-sans-serif,system-ui,-apple-system,sans-serif;-webkit-font-smoothing:antialiased}
a{color:inherit}
.wrap{max-width:760px;margin:0 auto;padding:28px 20px 80px}
.masthead{padding:32px 0 24px;text-align:left;border-bottom:1px solid var(--line);margin-bottom:28px}
.masthead h1{margin:0;font-size:30px;font-weight:800;letter-spacing:-0.03em}
.masthead h1 span{color:var(--amber);font-weight:800}
.masthead .sub{margin-top:6px;font-size:13px;color:var(--muted);letter-spacing:0.02em}
.masthead .sub b{color:var(--ink);font-weight:600}
.nav{margin-top:14px;display:flex;flex-wrap:wrap;gap:8px}
.nav a{font-size:12px;padding:6px 12px;border-radius:999px;background:var(--surface);border:1px solid var(--line);text-decoration:none;color:var(--muted)}
.nav a:hover{border-color:var(--amber);color:var(--ink)}
.archive-bar{margin-top:14px;font-size:12px;color:var(--muted);display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.archive-bar a{color:var(--muted);text-decoration:none;border-bottom:1px solid var(--line);padding-bottom:1px}
.archive-bar a:hover{color:var(--ink)}
.section{margin-top:36px}
.section-title{font-size:15px;font-weight:700;letter-spacing:-0.01em;margin:0 0 14px;padding-bottom:8px;border-bottom:1px solid var(--line)}
.section-grid{display:flex;flex-direction:column;gap:12px}
.card{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:18px 20px;transition:border-color .15s,box-shadow .15s}
.card:hover{border-color:#e0d8cc;box-shadow:0 4px 20px rgba(0,0,0,.04)}
.card-hero{border-color:var(--amber);background:linear-gradient(180deg,#fffef9 0%,#ffffff 100%);box-shadow:0 4px 24px rgba(212,136,6,.08)}
.card-meta{font-size:11px;color:var(--muted);letter-spacing:.04em;margin-bottom:8px}
.card-title{margin:0 0 8px;font-size:16px;line-height:1.45;font-weight:700;letter-spacing:-.01em}
.card-title a{text-decoration:none}
.card-title a:hover{color:var(--amber)}
.card-en{font-size:12px;color:var(--muted);margin:-4px 0 8px;line-height:1.5}
.card-summary{margin:0;font-size:14px;line-height:1.75;color:#2b2b2b}
.card-why{margin-top:12px;padding:10px 12px;background:var(--amber-soft);border-radius:10px;font-size:13px;line-height:1.6}
.card-why span{font-weight:700;color:var(--amber);margin-right:6px}
.card-excerpt{margin:12px 0 0;padding:10px 12px;border-left:3px solid var(--line);background:var(--surface-soft);border-radius:0 10px 10px 0;font-size:12px;line-height:1.65;color:var(--muted)}
.card-excerpt span{font-weight:700;color:var(--ink);margin-right:6px}
.card-link{display:inline-block;margin-top:12px;font-size:12px;font-weight:600;color:var(--amber);text-decoration:none}
.card-link:hover{text-decoration:underline}
.signal{margin-top:36px;background:var(--ink);color:#fdfbf7;border-radius:var(--radius);padding:20px 22px}
.signal-label{font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--amber);font-weight:700;margin-bottom:8px}
.signal p{margin:0;font-size:14px;line-height:1.7;color:#e8e4de}
.muted{color:var(--muted);font-size:13px}
footer{margin-top:48px;padding-top:16px;border-top:1px solid var(--line);font-size:11px;color:var(--muted)}
@media(max-width:640px){.wrap{padding:20px 14px 64px}.masthead h1{font-size:24px}.card{padding:16px}}
"""

doc = f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(cfg["site"]["title"])} — {e(data["date"])}</title>
<style>{style}</style>
</head>
<body>
<main class="wrap">
<header class="masthead">
<h1><span>pika</span> — daily</h1>
<div class="sub"><b>{e(data["date"])}</b> · {e(cfg["site"]["subtitle"])} · America/Los_Angeles · 每日 08:00 PT 更新</div>
<nav class="nav">{''.join(f'<a href="#{e(s["id"])}">{e(s["title"])}</a>' for s in cfg["sections"])}</nav>
<div class="archive-bar"><span>归档</span>{''.join(archive_links) if archive_links else '<span class="muted">首期</span>'}</div>
</header>
{signal}
{''.join(section_html)}
<footer>由 Hermes 生成 · {e(data.get("generated_at",""))} · <a href="{e(BASE)}/archive/{e(data["date"])}.html">本期归档</a></footer>
</main>
</body>
</html>"""

(ROOT/"index.html").write_text(doc, encoding="utf-8")
(ROOT/"archive"/f'{data["date"]}.html').write_text(doc, encoding="utf-8")
(ROOT/"data/archive"/f'{data["date"]}.json').write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Rendered {data['date']} — pika style")
