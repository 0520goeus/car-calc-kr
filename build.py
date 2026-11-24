#!/usr/bin/env python3
"""Build 2026 Korean Car Tax, Used Car Registration Tax, EV/HEV 5-Year TCO, Fuel Cost & Car Loan Calculator (car-calc-kr)."""
from __future__ import annotations

import html
import json
from datetime import datetime
from pathlib import Path

BASE_URL = "https://0520goeus.github.io/car-calc-kr"
INDEXNOW_KEY = "d92f7b14e6a84c35b019e7c24a8f103d"
ADSENSE_CLIENT = "ca-pub-8749404731911210"
GSC_FILE = "google873809343766a3b6.html"
GSC_CONTENT = "google-site-verification: google873809343766a3b6.html"
TODAY = datetime.now().strftime("%Y-%m-%d")

DIST = Path(__file__).resolve().parent / "dist"

ECOSYSTEM_LINKS = [
    ("자동차세·유지비·취등록세", "https://0520goeus.github.io/car-calc-kr/"),
    ("부동산·대출·복비 계산기", "https://0520goeus.github.io/house-calc-kr/"),
    ("실수령액·금융 계산기", "https://0520goeus.github.io/money-calc-kr/"),
    ("2026 지원금·근로장려금", "https://0520goeus.github.io/benefit-calc-kr/"),
    ("평수별 가전·직구관세", "https://0520goeus.github.io/life-fee-calc/"),
    ("전기세 얼마 계산기", "https://0520goeus.github.io/elec-calc/"),
    ("가성비 VS 비교(124종)", "https://0520goeus.github.io/vs-pick/"),
    ("해뎐 가격노트(588품목)", "https://0520goeus.github.io/price-note/"),
    ("셀러 마진·엑셀 템플릿", "https://0520goeus.github.io/seller-margin-calc/"),
    ("실시간 트렌드 브리핑", "https://0520goeus.github.io/kr-trend-brief/"),
    ("생활비 물가 연구소", "https://0520goeus.github.io/life-money-lab/"),
]

COUPANG_HTML = """<div style="margin:24px 0;padding:14px;background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;text-align:center;">
<div style="font-size:12px;color:#64748b;margin-bottom:8px;">이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.</div>
<script src="https://ads-partners.coupang.com/g.js"></script>
<script>new PartnersCoupang.G({"id":1049499,"template":"carousel","trackingCode":"AF9170267","width":"100%","height":"140","tsource":""});</script>
</div>"""

CSS = """
:root{--bg:#f8fafc;--card:#fff;--ink:#0f172a;--muted:#475569;--brand:#0f766e;--accent:#1d4ed8;--line:#e2e8f0;}
*{box-sizing:border-box}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,'Apple SD Gothic Neo','Malgun Gothic',sans-serif;background:var(--bg);color:var(--ink);line-height:1.7}
header{background:linear-gradient(135deg,#0f172a,#0f766e);color:#fff;padding:28px 18px}
.wrap{max-width:980px;margin:0 auto;padding:0 16px}
header h1{margin:0 0 8px;font-size:26px}
header p{margin:0;opacity:.92;font-size:15px}
nav.top{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}
nav.top a{color:#fff;text-decoration:none;background:rgba(255,255,255,.15);padding:6px 12px;border-radius:999px;font-size:13px}
nav.top a:hover{background:rgba(255,255,255,.28)}
main{padding:22px 0 44px}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:20px;margin-bottom:18px;box-shadow:0 2px 10px rgba(15,23,42,.04)}
.grid2{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px}
label{display:block;font-size:13px;font-weight:700;color:var(--muted);margin-bottom:8px}
input,select{width:100%;padding:10px 12px;border:1px solid #cbd5e1;border-radius:10px;font-size:15px;margin-top:4px}
button.btn{background:var(--brand);color:#fff;border:none;border-radius:10px;padding:11px 16px;font-size:15px;font-weight:700;cursor:pointer;width:100%}
button.btn:hover{filter:brightness(1.06)}
.res{background:#f0fdfa;border-left:4px solid var(--brand);padding:14px 16px;border-radius:10px;margin-top:14px;font-size:15px}
.res strong{color:#115e59;font-size:18px}
table{width:100%;border-collapse:collapse;margin:14px 0;font-size:14px}
th,td{padding:10px;border:1px solid var(--line);text-align:left}
th{background:#f1f5f9;font-weight:700}
.pill{display:inline-block;background:#ccfbf1;color:#115e59;padding:2px 9px;border-radius:999px;font-size:12px;font-weight:700}
.linklist{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:8px}
.linklist a{display:block;padding:10px 12px;border:1px solid var(--line);border-radius:10px;text-decoration:none;color:var(--ink);font-size:14px;background:#fff}
.linklist a:hover{border-color:var(--brand);background:#f0fdfa}
footer{background:#0f172a;color:#cbd5e1;padding:28px 16px;font-size:13px}
footer a{color:#5eead4;text-decoration:none}
.eco{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0 16px}
.eco a{background:#1e293b;padding:5px 10px;border-radius:8px;font-size:12px;color:#e2e8f0}
"""


def _car_tax_won(cc: int, age_years: int = 1, is_ev: bool = False) -> tuple[int, int]:
    """2026 Korean non-commercial passenger car tax (incl. 30% local edu tax) & Jan annual prepay (4.58% off)."""
    if is_ev:
        full = 130_000
    else:
        rate = 80 if cc <= 1000 else (140 if cc <= 1600 else 200)
        base = cc * rate
        # Age reduction: 3yr 5%, 4yr 10%, ..., 12yr+ 50%
        disc_pct = min(50, max(0, (age_years - 2) * 5))
        full = round(base * (1 - disc_pct / 100.0) * 1.3)
    prepay = round(full * (1 - 0.0458))
    return full, prepay


def _monthly_pmt(principal: int, rate_pct: float, months: int) -> int:
    r = (rate_pct / 100.0) / 12.0
    if r == 0:
        return round(principal / months)
    return round(principal * (r * (1 + r) ** months) / ((1 + r) ** months - 1))


def _render_page(title: str, desc: str, canonical_path: str, body: str, faq: list[tuple[str, str]]) -> str:
    canonical = f"{BASE_URL}/{canonical_path.lstrip('/')}" if canonical_path else f"{BASE_URL}/"
    ld_blocks = [
        {
            "@context": "https://schema.org",
            "@type": "WebApplication",
            "name": title,
            "url": canonical,
            "applicationCategory": "FinanceApplication",
            "operatingSystem": "All",
            "inLanguage": "ko",
            "description": desc,
        }
    ]
    if faq:
        ld_blocks.append(
            {
                "@context": "https://schema.org",
                "@type": "FAQPage",
                "mainEntity": [
                    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                    for q, a in faq
                ],
            }
        )
    ld_html = "".join(f'<script type="application/ld+json">{json.dumps(b, ensure_ascii=False)}</script>' for b in ld_blocks)
    eco_html = "".join(f'<a href="{u}" target="_blank" rel="noopener">{html.escape(n)}</a>' for n, u in ECOSYSTEM_LINKS)
    faq_html = ""
    if faq:
        items = "".join(f"<p><strong>Q. {html.escape(q)}</strong><br>A. {html.escape(a)}</p>" for q, a in faq)
        faq_html = f'<section class="card"><h2>자주 묻는 질문 (FAQ)</h2>{items}</section>'

    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canonical}">
<meta name="google-site-verification" content="E0MKLI_9g0wTNR9pjNKmxb_QGiA51AIK93dV9qBKumg">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT}" crossorigin="anonymous"></script>
{ld_html}
<style>{CSS}</style>
</head>
<body>
<header>
  <div class="wrap">
    <h1><a href="{BASE_URL}/" style="color:#fff;text-decoration:none">2026 자동차세·중고차 취등록세·유지비 계산기</a></h1>
    <p>배기량별 자동차세·연납 할인·중고차 이전비(7%)·가솔린 vs 하이브리드 5년 유지비·할부금 즉시 계산 ({TODAY})</p>
    <nav class="top">
      <a href="{BASE_URL}/#tax">자동차세·연납</a>
      <a href="{BASE_URL}/#reg">중고차 취등록세</a>
      <a href="{BASE_URL}/#fuel">기름값·유류비</a>
      <a href="{BASE_URL}/#loan">차량 할부금</a>
      <a href="{BASE_URL}/#directory">차종·가격표 38종</a>
    </nav>
  </div>
</header>
<main class="wrap">
{body}
{faq_html}
{COUPANG_HTML}
<div style="margin:20px auto;max-width:960px;padding:16px 20px;border-radius:14px;background:linear-gradient(135deg,#0f172a,#0f766e);color:#fff;display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:12px;"><div><div style="font-weight:800;font-size:16px;">2026 직장인·1인셀러 무매크로 자동계산 엑셀 3종 올인원 번들</div><div style="font-size:13px;opacity:.9;margin-top:2px;">1인셀러 마진·ROAS + 내집마련 매물10개 비교 + 월급 가계부·순자산 대시보드 (즉시 다운로드)</div></div><a href="https://scopekit-studio.lemonsqueezy.com/checkout/buy/ba4f11c6-8609-49c0-a947-39bead163d74" target="_blank" rel="noopener" style="background:#facc15;color:#0f172a;padding:10px 18px;border-radius:10px;font-weight:800;font-size:14px;text-decoration:none;white-space:nowrap;">3종 번들 즉시 다운로드 →</a></div>
</main>
<footer>
  <div class="wrap">
    <strong>해뎐 무료 생활금융·절약 계산기 네트워크 (11개 사이트)</strong>
    <div class="eco">{eco_html}</div>
    <div>2026년 지방세법 비영업용 승용차 기준 참고용 계산기입니다. 실제 납부 전 위택스·이택스 및 지자체 차량등록사업소 확인을 권장합니다. · Updated {TODAY}</div>
  </div>
</footer>
</body>
</html>"""


def main() -> None:
    DIST.mkdir(parents=True, exist_ok=True)
    (DIST / "p").mkdir(exist_ok=True)
    urls: list[str] = [f"{BASE_URL}/"]
    tax_links, reg_links, vs_links, loan_links = [], [], [], []

    # 1. Displacement Car Tax Pages (10)
    cc_specs = [
        ("1000cc", 998, False, "모닝·레이·캐스퍼 (경차)"),
        ("1200cc", 1197, False, "소형 가솔린"),
        ("1500cc", 1498, False, "코나·셀토스·트레일블레이저"),
        ("1600cc", 1598, False, "아반떼·투싼 HEV·쏘렌토 HEV·스포티지 HEV"),
        ("2000cc", 1999, False, "쏘나타·K5·스포티지·투싼 2.0"),
        ("2500cc", 2497, False, "그랜저·K8·쏘렌토·싼타페·G80 2.5T"),
        ("3000cc", 2998, False, "팰리세이드·GV80·모하비"),
        ("3500cc", 3470, False, "카니발·그랜저·G80·G90 3.5"),
        ("ev-tax", 0, True, "아이오닉5·EV6·테슬라 모델Y·모델3 (전기차)"),
    ]
    for slug, cc, is_ev, models in cc_specs:
        rows = []
        for yr in (1, 3, 5, 7, 10, 12):
            full, pre = _car_tax_won(cc, yr, is_ev)
            rows.append(f"<tr><td>{yr}년차{' (신차)' if yr==1 else ''}</td><td><strong>{full:,}원</strong></td><td>{pre:,}원 (연납)</td><td>{full - pre:,}원 절약</td></tr>")
        full1, pre1 = _car_tax_won(cc, 1, is_ev)
        label = "전기차 정액" if is_ev else f"{cc:,}cc"
        title = f"2026 {label} 자동차세 계산표 ({models}) — 차령별·1월 연납 할인액"
        desc = f"{models}({label})의 2026년 1년 자동차세({full1:,}원)와 1월 연납 할인({pre1:,}원), 3년~12년 차령 경감표입니다."
        body = f"""<section class="card"><span class="pill">자동차세 실측표</span><h2>{html.escape(title)}</h2>
<p>대표 차종: <strong>{html.escape(models)}</strong> · 신차 1년 세액(지방교육세 30% 포함)은 <strong>{full1:,}원</strong>이며, 1월 연납 신청 시 <strong>{pre1:,}원</strong>으로 할인됩니다.</p>
<table><thead><tr><th>차령(연식)</th><th>연간 자동차세</th><th>1월 연납 납부액</th><th>연납 절약액</th></tr></thead><tbody>{''.join(rows)}</tbody></table>
<p>👉 <a href="{BASE_URL}/#tax"><strong>내 차량 정확한 배기량·연식 입력하기 →</strong></a></p></section>"""
        faq = [(f"{label} 자동차세 1월 연납 시 얼마 할인되나요?", f"신차 기준 연간 {full1:,}원에서 1월 연납 약 4.58% 공제가 적용되어 {pre1:,}원({full1-pre1:,}원 절약)을 납부합니다.")]
        (DIST / "p" / f"tax-{slug}.html").write_text(_render_page(title, desc, f"p/tax-{slug}.html", body, faq), encoding="utf-8")
        urls.append(f"{BASE_URL}/p/tax-{slug}.html")
        tax_links.append((f"{label} 자동차세 ({models.split('·')[0]})", f"p/tax-{slug}.html"))

    # 2. Used Car Registration Tax Pages (10)
    for price_man in [500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 5000, 6000]:
        won = price_man * 10000
        normal_tax = round(won * 0.07)
        light_tax = max(0, round(won * 0.04) - 750_000)
        bond_est = round(won * 0.012)
        title = f"중고차 {price_man:,}만원 취등록세·이전비 총정리 (2026 승용 7%·경차 감면)"
        desc = f"{price_man:,}만원 중고차 구매 시 승용차 취등록세(7% · {normal_tax:,}원), 경차 감면({light_tax:,}원), 공채할인·매도비 포함 총 이전비 계산표입니다."
        body = f"""<section class="card"><span class="pill">중고차 이전비표</span><h2>{html.escape(title)}</h2>
<table><thead><tr><th>차량 구분</th><th>취등록세율</th><th>예상 취등록세</th><th>공채·인지대 포함 총 이전비(추정)</th></tr></thead><tbody>
<tr><td>일반 승용차 (비영업용)</td><td>7%</td><td><strong>{normal_tax:,}원</strong></td><td>약 {normal_tax + bond_est + 50000:,}원</td></tr>
<tr><td>경차 (1000cc 미만)</td><td>4% (75만원 한도 면제)</td><td><strong>{light_tax:,}원</strong></td><td>약 {light_tax + 30000:,}원</td></tr>
<tr><td>다자녀(3자녀↑) / 전기차 감면</td><td>법정 감면 적용</td><td>최대 140만~200만원 절감</td><td>차종·지자체별 상이</td></tr>
</tbody></table>
<p>👉 <a href="{BASE_URL}/#reg"><strong>중고차 가격 직접 입력해 이전비 계산하기 →</strong></a></p></section>"""
        faq = [(f"{price_man:,}만원 중고차 취등록세는 얼마인가요?", f"일반 비영업용 승용차 7% 기준 {normal_tax:,}원이며, 공채 매입 할인과 증지·번호판 비용을 합치면 약 {normal_tax + bond_est + 50000:,}원 수준입니다.")]
        (DIST / "p" / f"used-{price_man}.html").write_text(_render_page(title, desc, f"p/used-{price_man}.html", body, faq), encoding="utf-8")
        urls.append(f"{BASE_URL}/p/used-{price_man}.html")
        reg_links.append((f"중고차 {price_man:,}만원 취등록세", f"p/used-{price_man}.html"))

    # 3. Popular Gas vs HEV / EV 5-Year TCO Comparisons (8)
    comparisons = [
        ("avante-gas-vs-hev", "아반떼 가솔린 vs 아반떼 하이브리드", 2200, 2650, 15.0, 21.1, 1598, 1580, False),
        ("sorento-gas-vs-hev", "쏘렌토 2.5T 가솔린 vs 쏘렌토 1.6T 하이브리드", 3600, 4050, 10.5, 15.7, 2497, 1598, False),
        ("sportage-gas-vs-hev", "스포티지 1.6T 가솔린 vs 스포티지 하이브리드", 2850, 3400, 12.0, 16.3, 1598, 1598, False),
        ("grandeur-gas-vs-hev", "그랜저 2.5 가솔린 vs 그랜저 하이브리드", 3800, 4350, 11.5, 18.0, 2497, 1598, False),
        ("santafe-gas-vs-hev", "싼타페 2.5T 가솔린 vs 싼타페 하이브리드", 3600, 4080, 10.7, 15.5, 2497, 1598, False),
        ("carnival-gas-vs-hev", "카니발 3.5 가솔린 vs 카니발 하이브리드", 3550, 4000, 9.0, 14.0, 3470, 1598, False),
        ("modely-vs-ioniq5", "테슬라 모델Y vs 아이오닉5 5년 전기충전비·유지비", 5300, 4900, 5.1, 5.2, 0, 0, True),
        ("casper-vs-ray", "캐스퍼 vs 레이 경차 5년 총유지비 비교", 1650, 1550, 14.3, 12.7, 998, 998, False),
    ]
    for slug, name, pA, pB, effA, effB, ccA, ccB, is_ev in comparisons:
        km = 15000
        if is_ev:
            # kWh/km with 330 won/kWh
            fA5 = round((km / effA) * 330 * 5)
            fB5 = round((km / effB) * 330 * 5)
            tA5 = 130_000 * 5
            tB5 = 130_000 * 5
            unit = "km/kWh"
        else:
            gas_p = 1650
            fA5 = round((km / effA) * gas_p * 5)
            fB5 = round((km / effB) * gas_p * 5)
            tA5 = _car_tax_won(ccA, 1)[0] * 5
            tB5 = _car_tax_won(ccB, 1)[0] * 5
            unit = "km/L"
        totA = pA * 10000 + fA5 + tA5
        totB = pB * 10000 + fB5 + tB5
        save_5y = (fA5 + tA5) - (fB5 + tB5)
        diff_price = (pB - pA) * 10000
        breakeven_yr = round(diff_price / max(1, save_5y / 5), 1) if save_5y > 0 and diff_price > 0 else 0
        title = f"2026 {name} 5년 총유지비(TCO) 실측 비교 — 연 1.5만km 손익분기점은?"
        desc = f"{name}의 차량가격 차이, 5년 연료비, 5년 자동차세를 합산해 연 15,000km 주행 시 어느 차가 유리한지 계산했습니다."
        body = f"""<section class="card"><span class="pill">5년 총유지비 비교</span><h2>{html.escape(title)}</h2>
<p>연간 15,000km 주행(휘발유 1,650원/L 또는 전기차 충전 330원/kWh) 기준 5년 누적 비용을 비교했습니다.</p>
<table><thead><tr><th>항목</th><th>모델 A ({name.split(' vs ')[0]})</th><th>모델 B ({name.split(' vs ')[1]})</th></tr></thead><tbody>
<tr><td>기준 차량가(추정)</td><td>{pA:,}만원</td><td>{pB:,}만원</td></tr>
<tr><td>복합 연비/전비</td><td>{effA} {unit}</td><td>{effB} {unit}</td></tr>
<tr><td>5년 누적 연료/충전비</td><td>{fA5:,}원</td><td><strong>{fB5:,}원</strong></td></tr>
<tr><td>5년 누적 자동차세(신차 기준)</td><td>{tA5:,}원</td><td><strong>{tB5:,}원</strong></td></tr>
<tr><td>5년 총비용(차량가+연료+세금)</td><td><strong>{totA:,}원</strong></td><td><strong>{totB:,}원</strong></td></tr>
</tbody></table>
<p>{f'유지비 절감액(연간 약 {round(save_5y/5):,}원)으로 차량가 차이를 회수하는 손익분기점은 약 <strong>{breakeven_yr}년</strong>입니다.' if breakeven_yr else '주행거리와 세금 감면 혜택에 따라 실구매 총비용 차이가 크게 달라집니다.'}</p>
<p>👉 <a href="{BASE_URL}/#fuel"><strong>내 연간 주행거리로 기름값 직접 계산하기 →</strong></a></p></section>"""
        faq = [(f"{name} 중 연 1.5만km 주행 시 무엇이 유리한가요?", f"5년 연료비와 자동차세 합산 시 모델 B가 약 {abs(save_5y):,}원 유지비 차이가 발생합니다. 주행거리가 연 2만km 이상이면 하이브리드·전기차 회수 속도가 훨씬 빨라집니다.")]
        (DIST / "p" / f"{slug}.html").write_text(_render_page(title, desc, f"p/{slug}.html", body, faq), encoding="utf-8")
        urls.append(f"{BASE_URL}/p/{slug}.html")
        vs_links.append((name, f"p/{slug}.html"))

    # 4. Car Installment Pages (4) & Fuel Distance Pages (6)
    for amt in [2000, 3000, 4000, 5000]:
        P = amt * 10000
        rows = []
        for rate in (4.5, 5.5, 6.5):
            rows.append(f"<tr><td>연 {rate:.1f}%</td><td>월 {_monthly_pmt(P, rate, 36):,}원</td><td>월 {_monthly_pmt(P, rate, 48):,}원</td><td><strong>월 {_monthly_pmt(P, rate, 60):,}원</strong></td></tr>")
        title = f"자동차 할부 {amt:,}만원 월 납입금 계산표 (36·48·60개월 금리별)"
        desc = f"신차·중고차 할부원금 {amt:,}만원을 연 4.5%~6.5% 금리로 36·48·60개월 분납 시 월 납입금 비교표입니다."
        body = f"""<section class="card"><span class="pill">차량 할부 계산표</span><h2>{html.escape(title)}</h2>
<table><thead><tr><th>할부 금리</th><th>36개월(3년)</th><th>48개월(4년)</th><th>60개월(5년)</th></tr></thead><tbody>{''.join(rows)}</tbody></table>
<p>👉 <a href="{BASE_URL}/#loan"><strong>원하는 할부원금·금리 직접 입력하기 →</strong></a></p></section>"""
        (DIST / "p" / f"loan-{amt}.html").write_text(_render_page(title, desc, f"p/loan-{amt}.html", body, []), encoding="utf-8")
        urls.append(f"{BASE_URL}/p/loan-{amt}.html")
        loan_links.append((f"차량 할부 {amt:,}만원 월납입금", f"p/loan-{amt}.html"))

    # 5. Home Page
    home_body = f"""
<div class="grid2">
  <section class="card" id="tax">
    <span class="pill">1. 자동차세 & 연납</span>
    <h2>2026 자동차세 계산기</h2>
    <label>차량 종류
      <select id="tEv"><option value="ice">내연기관·하이브리드 (배기량 기준)</option><option value="ev">전기차 (정액 13만원)</option></select>
    </label>
    <label>배기량 (cc)<input id="tCc" type="number" value="1598"></label>
    <label>차령 (최초등록 후 경과년수, 1~15년)<input id="tAge" type="number" value="1" min="1" max="15"></label>
    <button class="btn" onclick="calcTax()">자동차세 즉시 계산</button>
    <div class="res" id="tOut"></div>
  </section>

  <section class="card" id="reg">
    <span class="pill">2. 중고차·신차 이전비</span>
    <h2>취등록세 계산기</h2>
    <label>차량 매매가 (만원)<input id="rPrice" type="number" value="2500"></label>
    <label>차종 구분
      <select id="rKind"><option value="normal">일반 승용차 (7%)</option><option value="light">경차 1000cc 미만 (4% · 75만 감면)</option><option value="van">승합·화물 (5%)</option></select>
    </label>
    <button class="btn" onclick="calcReg()">취등록세·총 이전비 계산</button>
    <div class="res" id="rOut"></div>
  </section>
</div>

<div class="grid2">
  <section class="card" id="fuel">
    <span class="pill">3. 기름값·유류비</span>
    <h2>월간·연간 유류비 계산기</h2>
    <label>연간 주행거리 (km)<input id="fKm" type="number" value="15000"></label>
    <label>차량 복합연비 (km/L)<input id="fEff" type="number" step="0.1" value="12.5"></label>
    <label>리터당 유가 (원)<input id="fP" type="number" value="1650"></label>
    <button class="btn" onclick="calcFuel()">기름값 즉시 계산</button>
    <div class="res" id="fOut"></div>
  </section>

  <section class="card" id="loan">
    <span class="pill">4. 차량 할부금</span>
    <h2>자동차 할부 월납입금 계산기</h2>
    <label>할부 원금 (만원)<input id="cAmt" type="number" value="3000"></label>
    <label>할부 금리 (연 %)<input id="cRate" type="number" step="0.1" value="5.5"></label>
    <label>할부 개월수
      <select id="cMon"><option value="36">36개월 (3년)</option><option value="48">48개월 (4년)</option><option value="60" selected>60개월 (5년)</option></select>
    </label>
    <button class="btn" onclick="calcCarLoan()">월 할부금 계산</button>
    <div class="res" id="cOut"></div>
  </section>
</div>

<section class="card" id="directory">
  <h2>차종·가격대별 상세 계산표 ({len(urls)-1}페이지)</h2>
  <h3>배기량별 2026 자동차세표</h3>
  <div class="linklist">{''.join(f'<a href="{u}">{html.escape(t)}</a>' for t, u in tax_links)}</div>
  <h3>중고차 가격대별 취등록세표</h3>
  <div class="linklist">{''.join(f'<a href="{u}">{html.escape(t)}</a>' for t, u in reg_links)}</div>
  <h3>인기 차종 가솔린 vs 하이브리드·전기차 5년 유지비</h3>
  <div class="linklist">{''.join(f'<a href="{u}">{html.escape(t)}</a>' for t, u in vs_links)}</div>
  <h3>차량 할부 금액별 월납입금표</h3>
  <div class="linklist">{''.join(f'<a href="{u}">{html.escape(t)}</a>' for t, u in loan_links)}</div>
</section>
""" + """
<script>
function fmt(n){return Math.round(n).toLocaleString('ko-KR');}
function calcTax(){
  const ev=document.getElementById('tEv').value==='ev';
  const cc=+document.getElementById('tCc').value||0;
  const age=Math.max(1, +document.getElementById('tAge').value||1);
  let full=130000;
  if(!ev){
    const rate=cc<=1000?80:(cc<=1600?140:200);
    const disc=Math.min(50, Math.max(0, (age-2)*5));
    full=cc*rate*(1-disc/100)*1.3;
  }
  const pre=full*(1-0.0458);
  document.getElementById('tOut').innerHTML=`연간 자동차세(교육세 포함): <strong>${fmt(full)}원</strong><br>1월 연납 할인 적용 시: <strong>${fmt(pre)}원</strong> (${fmt(full-pre)}원 절약)`;
}
function calcReg(){
  const won=(+document.getElementById('rPrice').value||0)*10000;
  const k=document.getElementById('rKind').value;
  let tax=won*0.07;
  if(k==='light') tax=Math.max(0, won*0.04-750000);
  else if(k==='van') tax=won*0.05;
  const est=tax + won*0.012 + 50000;
  document.getElementById('rOut').innerHTML=`예상 취등록세: <strong>${fmt(tax)}원</strong><br>공채할인·증지 포함 총 이전비 추정: 약 ${fmt(est)}원`;
}
function calcFuel(){
  const km=+document.getElementById('fKm').value||0;
  const eff=Math.max(1, +document.getElementById('fEff').value||1);
  const p=+document.getElementById('fP').value||0;
  const yr=(km/eff)*p;
  document.getElementById('fOut').innerHTML=`월 평균 기름값: <strong>${fmt(yr/12)}원</strong><br>연간 유류비: ${fmt(yr)}원 · 5년 누적: ${fmt(yr*5)}원`;
}
function calcCarLoan(){
  const P=(+document.getElementById('cAmt').value||0)*10000;
  const r=(+document.getElementById('cRate').value||0)/100/12;
  const n=+document.getElementById('cMon').value||60;
  const m=r===0?P/n:P*(r*Math.pow(1+r,n))/(Math.pow(1+r,n)-1);
  document.getElementById('cOut').innerHTML=`월 할부 납입금: <strong>${fmt(m)}원</strong><br>총 이자: ${fmt(m*n-P)}원 · 총 납입액: ${fmt(m*n)}원`;
}
calcTax();calcReg();calcFuel();calcCarLoan();
</script>
"""
    home_faq = [
        ("2026년 1600cc 하이브리드(쏘렌토·그랜저·아반떼) 자동차세는 얼마인가요?", "배기량 1,598cc 기준 신차 1년 세액은 지방교육세 30% 포함 약 290,836원이며, 1월 연납 시 약 277,516원입니다."),
        ("중고차 취등록세는 몇 퍼센트인가요?", "일반 비영업용 승용차는 7%, 승합·화물차는 5%, 경차(1000cc 미만)는 4%에서 최대 75만원까지 감면됩니다."),
    ]
    (DIST / "index.html").write_text(
        _render_page(
            "2026 자동차세·중고차 취등록세·가솔린 vs 하이브리드 5년 유지비 무료 계산기",
            "배기량별 자동차세와 1월 연납 할인, 중고차 취등록세(7%), 아반떼·쏘렌토·그랜저 가솔린 vs 하이브리드 5년 유지비, 차량 할부금을 한 번에 계산하세요.",
            "",
            home_body,
            home_faq,
        ),
        encoding="utf-8",
    )

    (DIST / "ads.txt").write_text(f"google.com, {ADSENSE_CLIENT.replace('ca-', '')}, DIRECT, f08c47fec0942fa0\n", encoding="utf-8")
    (DIST / GSC_FILE).write_text(GSC_CONTENT, encoding="utf-8")
    (DIST / f"{INDEXNOW_KEY}.txt").write_text(INDEXNOW_KEY, encoding="utf-8")
    (DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}/sitemap.xml\n", encoding="utf-8")
    sm = (
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>" for u in urls)
        + "\n</urlset>\n"
    )
    (DIST / "sitemap.xml").write_text(sm, encoding="utf-8")
    print(f"Built car-calc-kr: {len(urls)} pages -> {DIST}")


if __name__ == "__main__":
    main()
