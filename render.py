from pathlib import Path
import json, html

ROOT = Path(__file__).resolve().parent
cfg = json.loads((ROOT/"config.json").read_text(encoding="utf-8"))
data = json.loads((ROOT/"data/latest.json").read_text(encoding="utf-8"))
BASE = cfg["site"].get("base_path","").rstrip("/")

def e(x): return html.escape(str(x or ""))

def card(item):
    title_zh = item.get('title_zh') or item.get('title') or ""
    title_en = item.get('title') if item.get('title_zh') and item.get('title_zh') != item.get('title') else ""
    summary = item.get('summary_zh') or item.get('summary') or ""
    why = item.get('why_it_matters_zh') or item.get('why_it_matters') or ""
    excerpt = item.get('original_excerpt') or ""
    meta_parts = []
    if item.get('source'): meta_parts.append(item['source'])
    if item.get('published_at'): meta_parts.append(item['published_at'])
    if item.get('badge'): meta_parts.append(item['badge'])
    meta_line = " · ".join(meta_parts)
    # soften: no hard label box, just an em dash lead-in
    why_html = f'<p class="card-why">— {e(why)}</p>' if why else ''
    excerpt_html = f'<p class="card-excerpt">{e(excerpt)}</p>' if excerpt else ''
    return f"""
    <article class="card">
      <div class="card-meta">{e(meta_line)}</div>
      <h3 class="card-title"><a href="{e(item.get('url'))}" target="_blank" rel="noopener noreferrer">{e(title_zh)}</a></h3>
      {f'<div class="card-en">{e(title_en)}</div>' if title_en else ''}
      <p class="card-summary">{e(summary)}</p>
      {why_html}
      {excerpt_html}
      <a class="card-link" href="{e(item.get('url'))}" target="_blank" rel="noopener noreferrer">阅读原文 →</a>
    </article>"""

archive_dir = ROOT/"archive"
archive_links = []
for f in sorted(archive_dir.glob("*.html"), reverse=True)[:24]:
    archive_links.append(f'<a href="{BASE}/archive/{e(f.name)}">{e(f.stem)}</a>')

section_html = []
for s in cfg["sections"]:
    items = data["sections"].get(s["id"], [])
    if not items:
        if s["id"] in ("top","for_you"):
            body = '<p class="muted">今日暂无高信号内容。</p>'
        else:
            continue
        grid = f'<div class="cards">{body}</div>'
    else:
        # All sections use grid; top's first item spans
        cards = "".join(card(it) for it in items)
        grid = f'<div class="cards">{cards}</div>'
    section_html.append(f'<section id="{e(s["id"])}"><h2 class="section-title"><span class="section-num" aria-hidden="true">—</span> {e(s["title"])}</h2>{grid}</section>')

signal = ""
if data.get("signal"):
    signal = f'<section class="signal"><div class="signal-label">The Signal</div><p>{e(data["signal"])}</p></section>'

style = """
:root{--bg:#fdfbf7;--card:#fff;--ink:#1e1c18;--muted:#9a9590;--line:#ebe6dd;--accent:#d48a1a;--accent-soft:#fdf2d8;--radius:16px}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.7 ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Helvetica Neue",sans-serif;-webkit-font-smoothing:antialiased}
a{color:inherit}
.wrap{max-width:1120px;margin:0 auto;padding:28px 20px 72px}
.masthead{display:flex;flex-wrap:wrap;align-items:end;justify-content:space-between;gap:16px;padding:10px 0 18px;border-bottom:1px solid var(--line);margin-bottom:20px}
.masthead-left h1{margin:0;font-size:28px;font-weight:800;letter-spacing:-.025em}
.masthead-left h1 span{color:var(--accent)}
.masthead-meta{font-size:12px;color:var(--muted);margin-top:6px}
.nav{display:flex;flex-wrap:wrap;gap:8px}
.nav a{font-size:12px;padding:7px 12px;border-radius:999px;background:var(--card);border:1px solid var(--line);text-decoration:none;color:var(--muted)}
.nav a:hover{border-color:var(--accent);color:var(--ink)}
.archive-bar{margin:18px 0 6px;font-size:12px;color:var(--muted);display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.archive-bar a{color:var(--muted);text-decoration:none;border-bottom:1px solid var(--line)}
.archive-bar a:hover{color:var(--ink)}
.section{margin-top:28px}
.section-title{font-size:14px;font-weight:700;letter-spacing:-.01em;margin:0 0 14px;padding-bottom:8px;border-bottom:1px solid var(--line)}
.section-num{color:var(--accent);margin-right:4px}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px}
.card{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);padding:16px 18px;display:flex;flex-direction:column;gap:0;transition:box-shadow .15s,border-color .15s}
.card:hover{border-color:#ddd5c6;box-shadow:0 8px 28px rgba(0,0,0,.06)}
.card-meta{font-size:11px;color:var(--muted);letter-spacing:.02em;margin-bottom:8px}
.card-title{margin:0 0 6px;font-size:15px;line-height:1.45;font-weight:700}
.card-title a{text-decoration:none}
.card-title a:hover{color:var(--accent)}
.card-en{font-size:11px;color:var(--muted);margin-bottom:8px;line-height:1.5}
.card-summary{margin:0;font-size:13.5px;line-height:1.7;color:#2c2c2a}
.card-why{margin:10px 0 0;font-size:12.5px;line-height:1.6;color:#5a554f;font-style:italic}
.card-excerpt{margin:8px 0 0;font-size:11.5px;line-height:1.6;color:var(--muted);border-left:2px solid var(--line);padding-left:10px}
.card-link{margin-top:12px;font-size:12px;font-weight:600;color:var(--accent);text-decoration:none}
.card-link:hover{text-decoration:underline}
.signal{margin:24px 0;background:#1e1c18;color:#fdfbf7;border-radius:var(--radius);padding:18px 20px}
.signal-label{font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--accent);font-weight:700;margin-bottom:6px}
.signal p{margin:0;font-size:13.5px;line-height:1.65;color:#e8e2d8}
.muted{color:var(--muted);font-size:13px;grid-column:1/-1}
footer{margin-top:36px;padding-top:14px;border-top:1px solid var(--line);font-size:11px;color:var(--muted)}
@media(max-width:640px){.wrap{padding:18px 14px 56px}.masthead{flex-direction:column;align-items:stretch}.cards{grid-template-columns:1fr}}
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
  <div class="masthead-left">
    <h1><span>pika</span> — daily</h1>
    <div class="masthead-meta">{e(data["date"])} · {e(cfg["site"]["subtitle"])} · America/Los_Angeles · 每日 08:00 PT</div>
    <div class="archive-bar"><span>归档</span>{''.join(archive_links) if archive_links else '<span class="muted">首期</span>'}</div>
  </div>
  <nav class="nav">{''.join(f'<a href="#{e(s["id"])}">{e(s["title"])}</a>' for s in cfg["sections"])}</nav>
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
print(f"Rendered {data['date']} — polished grid, soft why")
