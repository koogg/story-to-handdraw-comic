#!/usr/bin/env python3
"""Build the offline theme colors gallery from canonical colors index."""
from __future__ import annotations

import html
import json
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
COLORS_JSON = SKILL / "references" / "colors.json"
GALLERY = SKILL / "gallery" / "colors.html"

CATEGORIES = (
    ("all", "全部", "All"),
    ("blue", "经典蓝系", "Classic Blue"),
    ("green", "清新绿系", "Fresh Green"),
    ("red", "古典红绿", "Classic Red & Vintage"),
    ("purple", "浪漫粉紫", "Romantic Pink & Purple"),
    ("warm", "暖阳大地", "Warm Sun & Earth"),
)


def gallery_html(colors: list[dict[str, object]]) -> str:
    counts = {"all": len(colors)}
    for cat_id, _, _ in CATEGORIES[1:]:
        counts[cat_id] = sum(c["category"] == cat_id for c in colors)

    controls = "".join(
        f'<button class="filter{" is-active" if cat_id == "all" else ""}" type="button" '
        f'data-category="{cat_id}" data-label-zh="{label_zh}" data-label-en="{label_en}">'
        f'{label_zh} <span>{counts[cat_id]}</span></button>'
        for cat_id, label_zh, label_en in CATEGORIES
    )

    cards = []
    for c in colors:
        card_html = (
            f'<article class="color-card" data-id="{c["id"]}" data-category="{c["category"]}" '
            f'data-name-zh="{html.escape(str(c["name_zh"]))}" data-name-en="{html.escape(str(c["name_en"]))}" '
            f'data-quote-zh="{html.escape(str(c["quote_zh"]))}" data-quote-en="{html.escape(str(c["quote_en"]))}" '
            f'data-prompt-zh="{html.escape(str(c["prompt_zh"]))}" data-prompt-en="{html.escape(str(c["prompt_en"]))}" '
            f'data-image="{html.escape(str(c["image"]))}">'
            f'<button class="card-thumb-btn" type="button" aria-label="放大查看 {c["id"]} {html.escape(str(c["name_zh"]))}">'
            f'<img src="{html.escape(str(c["image"]))}" alt="{c["id"]} {html.escape(str(c["name_zh"]))}">'
            f'</button>'
            f'<div class="color-info">'
            f'<div class="color-header">'
            f'<span class="color-id">{c["id"]}</span>'
            f'<h3 class="color-name" data-zh="{html.escape(str(c["name_zh"]))}" data-en="{html.escape(str(c["name_en"]))}">{html.escape(str(c["name_zh"]))}</h3>'
            f'</div>'
            f'<p class="color-quote" data-zh="{html.escape(str(c["quote_zh"]))}" data-en="{html.escape(str(c["quote_en"]))}">{html.escape(str(c["quote_zh"]))}</p>'
            f'<button class="copy-btn" type="button" data-i18n="copyBtn">复制提示词</button>'
            f'</div>'
            f'</article>'
        )
        cards.append(card_html)
    cards_str = "\n".join(cards)

    return f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>经典单色主题色画廊</title><style>
:root{{color:#24211e;background:#f7f5f0;font:16px/1.5 system-ui,"Microsoft YaHei",sans-serif}} body{{margin:0}} main{{max-width:1440px;margin:auto;padding:18px 30px 30px}} .sticky-header{{position:sticky;top:0;z-index:100}} .site-nav{{display:flex;align-items:center;gap:10px;margin:0;padding:12px 30px;border-bottom:1px solid #ded8cf;background:#fffdf9}} .site-nav a{{border:1px solid #9e9185;border-radius:8px;background:#fff;color:#403a34;padding:7px 13px;text-decoration:none;font-weight:800;line-height:1.2;transition:background .15s,color .15s,border-color .15s}} .site-nav a:hover{{border-color:#b74227;background:#fff0eb;color:#9f351f}} .site-nav a[aria-current="page"]{{border-color:#b74227;background:#b74227;color:#fff;box-shadow:0 1px 3px #b7422744}} .nav-right{{margin-left:auto;display:flex;align-items:center;gap:8px}} .nav-ext{{display:inline-flex;align-items:center;font-weight:700}} .nav-btn{{border:1px solid #9e9185;border-radius:8px;background:#fff;color:#403a34;padding:7px 13px;font:inherit;font-weight:700;line-height:1.2;cursor:pointer;transition:background .15s,color .15s,border-color .15s}} .nav-btn:hover{{border-color:#b74227;background:#fff0eb;color:#9f351f}} .nav-btn:focus-visible,.site-nav a:focus-visible{{outline:3px solid #d67d4d;outline-offset:3px}} .sub-nav{{display:flex;gap:10px;align-items:center;padding:9px 30px;background:#faf7f2;border-bottom:1px solid #ded8cf;box-shadow:0 2px 6px rgba(0,0,0,0.03)}} .filter{{display:inline-flex;align-items:center;gap:6px;border:1px solid #c9c1b6;border-radius:6px;background:#fff;color:#514a43;padding:6px 14px;font:inherit;font-size:14px;font-weight:600;line-height:1.4;cursor:pointer;transition:background .15s,color .15s,border-color .15s,box-shadow .15s}} .filter:hover{{border-color:#b74227;color:#b74227;background:#fff8f5}} .filter span{{display:inline-block;padding:1px 6px;border-radius:999px;background:#eee8df;color:#6b6257;font-size:12px;font-weight:700;font-variant-numeric:tabular-nums;line-height:1.2;transition:all .15s}} .filter.is-active{{border-color:#b74227;background:#b74227;color:#fff;box-shadow:0 1px 3px rgba(183,66,39,0.3)}} .filter.is-active span{{background:rgba(255,255,255,0.25);color:#fff}} h1{{margin:0}} .lead{{margin:8px 0 16px;color:#665f57}} .prompt-examples{{display:flex;align-items:center;flex-wrap:wrap;gap:10px 18px;margin:0 0 22px;padding:12px 16px;border:1px solid #ded8cf;border-radius:10px;background:#fffdf9}} .prompt-examples h2{{margin:0;color:#665f57;font-size:14px;font-weight:600}} .prompt-example{{display:flex;align-items:center;gap:8px;min-width:0}} .prompt-label{{color:#71685e;font-size:13px;white-space:nowrap}} .prompt-value{{padding:4px 8px;border:1px solid #d9d2c8;border-radius:6px;background:#f7f5f0;color:#24211e;font:13px/1.4 ui-monospace,SFMono-Regular,Consolas,"Liberation Mono",monospace;white-space:nowrap}} .gallery{{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:20px;align-items:stretch}} .color-card{{display:flex;flex-direction:column;box-sizing:border-box;border-radius:12px;background:#fff;box-shadow:0 2px 8px rgba(0,0,0,0.06);overflow:hidden;transition:transform .15s,box-shadow .15s}} .color-card:hover{{transform:translateY(-2px);box-shadow:0 6px 16px rgba(0,0,0,0.1)}} .card-thumb-btn{{display:block;width:100%;margin:0;padding:0;border:0;background:#ede8e1;cursor:zoom-in;overflow:hidden}} .card-thumb-btn img{{display:block;width:100%;height:auto;object-fit:cover;transition:transform .2s}} .card-thumb-btn:hover img{{transform:scale(1.02)}} .color-info{{display:flex;flex-direction:column;flex-grow:1;padding:12px 14px;background:#fffdf9}} .color-header{{display:flex;align-items:baseline;gap:8px;margin-bottom:4px}} .color-id{{color:#b74227;font-weight:850;font-size:14px;font-variant-numeric:tabular-nums}} .color-name{{margin:0;font-size:15px;font-weight:750;color:#24211e}} .color-quote{{margin:0 0 12px;font-size:12.5px;color:#7a7268;line-height:1.4;flex-grow:1}} .copy-btn{{width:100%;padding:7px 0;border:1px solid #d0c8be;border-radius:7px;background:#fcfaf7;color:#453e37;font:inherit;font-size:13px;font-weight:650;cursor:pointer;transition:all .15s;text-align:center}} .copy-btn:hover{{border-color:#b74227;background:#b74227;color:#fff}} .copy-btn.copied{{border-color:#2a854a;background:#2a854a;color:#fff}} dialog{{width:min(94vw,900px);padding:16px;border:0;border-radius:14px;background:#171513;color:#fff;box-shadow:0 20px 70px #0008}} dialog::backdrop{{background:#000b}} dialog img{{display:block;max-width:100%;max-height:75vh;margin:0 auto 12px;object-fit:contain;border-radius:8px}} .dialog-actions{{display:flex;align-items:center;gap:12px}} .dialog-title{{margin:0;font-size:17px;font-weight:700}} .dialog-quote{{margin:4px 0 0;font-size:13px;color:#bbb}} .dialog-copy{{border:0;border-radius:7px;padding:8px 14px;background:#b74227;color:#fff;font:inherit;font-weight:700;cursor:pointer;margin-left:auto}} .dialog-copy:hover{{background:#d64a27}} .dialog-close{{border:0;border-radius:7px;padding:8px 12px;background:#444;color:#fff;font:inherit;cursor:pointer}} [hidden]{{display:none!important}} @media(max-width:760px){{main{{padding:14px 16px}} .site-nav{{padding:10px 16px;flex-wrap:wrap;gap:8px}} .nav-right{{width:100%;justify-content:flex-start;gap:6px;margin-left:0}} .site-nav a,.nav-btn{{padding:6px 10px;font-size:13px}} .sub-nav{{padding:8px 16px;gap:8px;overflow-x:auto;-webkit-overflow-scrolling:touch}} .filter{{padding:5px 10px;font-size:13px;white-space:nowrap}} .prompt-examples{{flex-direction:column;align-items:flex-start;gap:8px}} .prompt-example{{flex-wrap:wrap}} .prompt-value{{white-space:normal}} .gallery{{grid-template-columns:repeat(2,1fr);gap:12px}}}} @media(max-width:420px){{.gallery{{grid-template-columns:1fr}}}}
</style></head><body>
<header class="sticky-header">
<nav class="site-nav" aria-label="画廊导航"><a href="index.html" data-i18n="stylesNav">风格画廊</a><a href="layouts.html" data-i18n="layoutsNav">图型画廊</a><a href="colors.html" aria-current="page" data-i18n="colorsNav">色彩画廊</a><div class="nav-right"><a class="nav-ext" href="https://github.com/yang0/handraw-style" target="_blank" rel="noopener noreferrer" title="GitHub 仓库"><svg width="14" height="14" viewBox="0 0 16 16" fill="currentColor" style="vertical-align:-2px;margin-right:4px" aria-hidden="true"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>GitHub</a><a class="nav-ext" href="https://x.com/yang02010" target="_blank" rel="noopener noreferrer" title="X (Twitter) @yang02010"><svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor" style="vertical-align:-2px;margin-right:4px" aria-hidden="true"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>X (@yang02010)</a><button class="nav-btn" id="wechat-btn" type="button" data-i18n="wechatBtn">💬 交流群 / 作者微信</button><button class="nav-btn" id="lang-btn" type="button" aria-label="Switch Language">🌐 EN / 中</button></div></nav>
<nav class="sub-nav filters" aria-label="色彩分类">{controls}</nav>
</header>
<main>
<h1 data-i18n="title">经典单色主题色画廊</h1>
<p class="lead" data-i18n="lead">精选 30 款经典单色主题色。点击卡片放大查看，或点击卡片下方的【复制提示词】直接用于 AI 生图。</p>
<section class="prompt-examples" aria-labelledby="prompt-examples-title">
<h2 id="prompt-examples-title" data-i18n="promptTitle">提示词案例</h2>
<div class="prompt-example"><span class="prompt-label" data-i18n="ex1Label">1 · 组合出图</span><code class="prompt-value" data-i18n="ex1Code">风格：276，图型：SC-001，主题色：C-01 克莱因蓝，主题：海边漫步</code></div>
<div class="prompt-example"><span class="prompt-label" data-i18n="ex2Label">2 · 单色调用</span><code class="prompt-value" data-i18n="ex2Code">主题色：C-10 鼠尾草绿，主题：室内盆栽与书桌</code></div>
</section>
<section id="gallery" class="gallery">{cards_str}</section>
</main>
<dialog id="preview" aria-labelledby="dialog-title">
<img id="preview-image" alt="">
<div class="dialog-actions">
<div><h3 class="dialog-title" id="dialog-title"></h3><p class="dialog-quote" id="dialog-quote"></p></div>
<button class="dialog-copy" id="dialog-copy-btn" type="button" data-i18n="copyBtn">复制提示词</button>
<button class="dialog-close" type="button" data-i18n="closeBtn">关闭 ×</button>
</div>
</dialog>
<dialog id="wechat-modal" aria-labelledby="wechat-title" style="width:min(90vw,360px);padding:20px;border:0;border-radius:14px;background:#1e1b18;color:#fff;box-shadow:0 20px 70px #000a;text-align:center"><button class="close" type="button" aria-label="关闭" style="position:absolute;top:12px;right:12px;border:0;border-radius:7px;padding:5px 9px;background:#fff;color:#24211e;cursor:pointer;font:inherit">关闭 ×</button><h3 id="wechat-title" style="margin:4px 0 14px;font-size:17px;color:#fff" data-i18n="wechatTitle">💬 交流群 / 作者微信</h3><img id="wechat-img" src="https://raw.githubusercontent.com/yang0/handraw-style/master/images/wechat_community.jpg" onerror="this.onerror=null;this.src='../../../images/wechat_personal_fallback.jpg';const s=document.getElementById('wechat-status');if(s)s.textContent='（已切换为本地备用二维码）';" alt="微信二维码" style="display:block;width:100%;max-width:260px;margin:0 auto;border-radius:10px;box-shadow:0 2px 8px rgba(0,0,0,0.3)"><p style="margin:14px 0 4px;font-size:14px;color:#eee" data-i18n="wechatSub">微信扫一扫加我为朋友</p><p style="margin:0 0 4px;font-size:13px;color:#d67d4d;font-weight:600" data-i18n="wechatNote">备注【手绘】拉你进群</p><p id="wechat-status" style="margin:4px 0 0;font-size:12px;color:#999"></p><div style="margin-top:14px;padding-top:12px;border-top:1px solid #332f2b;display:flex;justify-content:center;gap:16px;font-size:13px"><a href="https://github.com/yang0/handraw-style" target="_blank" rel="noopener noreferrer" style="color:#d67d4d;text-decoration:none;font-weight:600">GitHub 仓库 ↗</a><a href="https://x.com/yang02010" target="_blank" rel="noopener noreferrer" style="color:#d67d4d;text-decoration:none;font-weight:600">X @yang02010 ↗</a></div></dialog>
<script>
const cards=[...document.querySelectorAll('.color-card')],filters=[...document.querySelectorAll('.filter')],dialog=document.querySelector('#preview'),preview=document.querySelector('#preview-image'),dialogTitle=document.querySelector('#dialog-title'),dialogQuote=document.querySelector('#dialog-quote'),dialogCopyBtn=document.querySelector('#dialog-copy-btn'),dialogCloseBtn=dialog.querySelector('.dialog-close'),wechatBtn=document.querySelector('#wechat-btn'),wechatModal=document.querySelector('#wechat-modal'),langBtn=document.querySelector('#lang-btn');
let activeCard=null;
const I18N = {{
  zh: {{
    pageTitle: "经典单色主题色画廊",
    stylesNav: "风格画廊",
    layoutsNav: "图型画廊",
    colorsNav: "色彩画廊",
    wechatBtn: "💬 交流群 / 作者微信",
    wechatTitle: "💬 交流群 / 作者微信",
    wechatSub: "微信扫一扫加我为朋友",
    wechatNote: "备注【手绘】拉你进群",
    title: "经典单色主题色画廊",
    lead: "精选 30 款经典单色主题色。点击卡片放大查看，或点击卡片下方的【复制提示词】直接用于 AI 生图。",
    promptTitle: "提示词案例",
    ex1Label: "1 · 组合出图",
    ex1Code: "风格：276，图型：SC-001，主题色：C-01 克莱因蓝，主题：海边漫步",
    ex2Label: "2 · 单色调用",
    ex2Code: "主题色：C-10 鼠尾草绿，主题：室内盆栽与书桌",
    copyBtn: "复制提示词",
    copiedBtn: "已复制! ✓",
    closeBtn: "关闭 ×"
  }},
  en: {{
    pageTitle: "Classic Monochrome Colors Gallery",
    stylesNav: "Styles",
    layoutsNav: "Layouts",
    colorsNav: "Colors",
    wechatBtn: "💬 Community / WeChat",
    wechatTitle: "💬 Community / WeChat",
    wechatSub: "Scan QR code to add WeChat",
    wechatNote: "Note 'handdraw' to join group",
    title: "Classic Monochrome Colors Gallery",
    lead: "30 curated classic monochrome theme colors. Click cards to enlarge, or click 'Copy Prompt' to use directly.",
    promptTitle: "Prompt Examples",
    ex1Label: "1 · Combined Prompt",
    ex1Code: "Style: 276, Layout: SC-001, Theme color: C-01 Klein Blue, Theme: Seaside stroll",
    ex2Label: "2 · Color-Only",
    ex2Code: "Theme color: C-10 Sage Green, Theme: Indoor potted plant on desk",
    copyBtn: "Copy Prompt",
    copiedBtn: "Copied! ✓",
    closeBtn: "Close ×"
  }}
}};

let currentLang = localStorage.getItem('handdraw_lang') || 'zh';

function setCategory(cat) {{
  filters.forEach(btn => btn.classList.toggle('is-active', btn.dataset.category === cat));
  cards.forEach(card => {{
    const match = cat === 'all' || card.dataset.category === cat;
    card.hidden = !match;
  }});
}}

filters.forEach(btn => btn.addEventListener('click', () => setCategory(btn.dataset.category)));

function copyText(text, btn) {{
  navigator.clipboard.writeText(text).then(() => {{
    const orig = btn.textContent;
    btn.textContent = I18N[currentLang].copiedBtn;
    btn.classList.add('copied');
    setTimeout(() => {{
      btn.textContent = orig;
      btn.classList.remove('copied');
    }}, 1500);
  }}).catch(() => prompt('请复制提示词：', text));
}}

cards.forEach(card => {{
  const thumbBtn = card.querySelector('.card-thumb-btn');
  const copyBtn = card.querySelector('.copy-btn');
  thumbBtn.addEventListener('click', () => {{
    activeCard = card;
    preview.src = card.dataset.image;
    updateDialogContent();
    dialog.showModal();
  }});
  copyBtn.addEventListener('click', (e) => {{
    e.stopPropagation();
    const prompt = currentLang === 'zh' ? card.dataset.promptZh : card.dataset.promptEn;
    copyText(prompt, copyBtn);
  }});
}});

function updateDialogContent() {{
  if (!activeCard) return;
  const name = currentLang === 'zh' ? activeCard.dataset.nameZh : activeCard.dataset.nameEn;
  const quote = currentLang === 'zh' ? activeCard.dataset.quoteZh : activeCard.dataset.quoteEn;
  dialogTitle.textContent = `${{activeCard.dataset.id}} · ${{name}}`;
  dialogQuote.textContent = quote;
}}

dialogCopyBtn.addEventListener('click', () => {{
  if (!activeCard) return;
  const prompt = currentLang === 'zh' ? activeCard.dataset.promptZh : activeCard.dataset.promptEn;
  copyText(prompt, dialogCopyBtn);
}});

dialogCloseBtn.addEventListener('click', () => dialog.close());
dialog.addEventListener('click', (e) => {{ if (e.target === dialog) dialog.close(); }});

if (wechatBtn && wechatModal) {{
  wechatBtn.addEventListener('click', () => wechatModal.showModal());
  wechatModal.querySelector('.close')?.addEventListener('click', () => wechatModal.close());
  wechatModal.addEventListener('click', (e) => {{ if (e.target === wechatModal) wechatModal.close(); }});
}}

function applyLanguage(lang) {{
  currentLang = lang;
  localStorage.setItem('handdraw_lang', lang);
  document.documentElement.lang = lang === 'zh' ? 'zh-CN' : 'en';
  document.title = I18N[lang].pageTitle;
  document.querySelectorAll('[data-i18n]').forEach(el => {{
    const key = el.dataset.i18n;
    if (I18N[lang][key]) el.textContent = I18N[lang][key];
  }});
  filters.forEach(btn => {{
    const label = lang === 'zh' ? btn.dataset.labelZh : btn.dataset.labelEn;
    const count = btn.querySelector('span')?.textContent || '';
    btn.innerHTML = `${{label}} <span>${{count}}</span>`;
  }});
  cards.forEach(card => {{
    const nameEl = card.querySelector('.color-name');
    const quoteEl = card.querySelector('.color-quote');
    if (nameEl) nameEl.textContent = lang === 'zh' ? nameEl.dataset.zh : nameEl.dataset.en;
    if (quoteEl) quoteEl.textContent = lang === 'zh' ? quoteEl.dataset.zh : quoteEl.dataset.en;
  }});
  updateDialogContent();
  if (langBtn) langBtn.textContent = lang === 'zh' ? '🌐 EN / 中' : '🌐 中 / EN';
}}

if (langBtn) {{
  langBtn.addEventListener('click', () => {{
    applyLanguage(currentLang === 'zh' ? 'en' : 'zh');
  }});
}}

applyLanguage(currentLang);
</script>
</body></html>'''


def main() -> None:
    if not COLORS_JSON.exists():
        raise SystemExit(f"Missing {COLORS_JSON}")
    colors = json.loads(COLORS_JSON.read_text(encoding="utf-8"))
    html_content = gallery_html(colors)
    GALLERY.parent.mkdir(parents=True, exist_ok=True)
    GALLERY.write_text(html_content, encoding="utf-8")
    print(f"Built {len(colors)} colors into {GALLERY.relative_to(SKILL.parent.parent)}")


if __name__ == "__main__":
    main()
