
import math
import random
import streamlit as st

# ── page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GolMetrik",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ---- global resets ---- */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #0d0d0d;
}
[data-testid="stHeader"] { background: transparent; }

/* ---- neon card ---- */
.card {
    background: #161616;
    border: 1px solid #262626;
    border-radius: 14px;
    padding: 22px 24px;
    margin-bottom: 16px;
    position: relative;
    overflow: hidden;
}
.card::before {
    content: "";
    position: absolute;
    inset: 0;
    border-radius: 14px;
    padding: 1px;
    background: linear-gradient(135deg, #39FF14 0%, transparent 60%);
    -webkit-mask: linear-gradient(#fff 0 0) content-box,
                  linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask-composite: exclude;
    opacity: .35;
}
.card-title {
    font-size: .72rem;
    letter-spacing: .12em;
    text-transform: uppercase;
    color: #39FF14;
    margin-bottom: 10px;
    font-weight: 700;
}
.card-big {
    font-size: 2.6rem;
    font-weight: 800;
    color: #ffffff;
    line-height: 1;
}
.card-sub {
    font-size: .85rem;
    color: #888;
    margin-top: 4px;
}

/* ---- pill badges ---- */
.pill {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 999px;
    font-size: .78rem;
    font-weight: 600;
    margin-right: 6px;
}
.pill-green  { background: #0d2e0a; color: #39FF14; border: 1px solid #39FF14; }
.pill-yellow { background: #2a2000; color: #FFD700; border: 1px solid #FFD700; }
.pill-red    { background: #2e0a0a; color: #FF4C4C; border: 1px solid #FF4C4C; }
.pill-grey   { background: #1e1e1e; color: #888;    border: 1px solid #333;    }

/* ---- range bar ---- */
.bar-wrap { margin: 6px 0; }
.bar-label {
    display: flex;
    justify-content: space-between;
    font-size: .82rem;
    color: #ccc;
    margin-bottom: 3px;
}
.bar-track {
    background: #262626;
    border-radius: 999px;
    height: 8px;
    width: 100%;
    overflow: hidden;
}
.bar-fill {
    height: 100%;
    border-radius: 999px;
    transition: width .4s ease;
}

/* ---- section header ---- */
.sec-header {
    font-size: .68rem;
    letter-spacing: .15em;
    text-transform: uppercase;
    color: #444;
    margin: 28px 0 12px;
    border-bottom: 1px solid #222;
    padding-bottom: 6px;
}

/* ---- best pick badge ---- */
.best-pick {
    background: linear-gradient(135deg, #1a3d0d, #0d0d0d);
    border: 1.5px solid #39FF14;
    border-radius: 12px;
    padding: 18px 22px;
    text-align: center;
}
.best-pick-label {
    font-size: .7rem;
    letter-spacing: .14em;
    text-transform: uppercase;
    color: #39FF14;
    margin-bottom: 6px;
}
.best-pick-value {
    font-size: 1.55rem;
    font-weight: 800;
    color: #fff;
}
.best-pick-pct {
    font-size: 1rem;
    color: #39FF14;
    font-weight: 700;
}

/* ---- matchup header ---- */
.matchup {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 16px;
    margin: 10px 0 28px;
}
.matchup-team {
    font-size: 1.35rem;
    font-weight: 800;
    color: #fff;
}
.matchup-vs {
    font-size: .95rem;
    color: #39FF14;
    font-weight: 700;
    padding: 4px 14px;
    border: 1px solid #39FF14;
    border-radius: 999px;
    opacity: .8;
}

/* ---- divider ---- */
.neon-divider {
    border: none;
    border-top: 1px solid #1e1e1e;
    margin: 28px 0;
}

/* ---- value bet panel ---- */
.vb-wrap {
    background: #111;
    border: 1px solid #252525;
    border-radius: 14px;
    padding: 24px 26px;
}
.vb-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 10px;
}
.vb-stat-label {
    font-size: .75rem;
    letter-spacing: .10em;
    text-transform: uppercase;
    color: #555;
}
.vb-stat-val {
    font-size: 1.55rem;
    font-weight: 800;
    color: #fff;
}
.vb-verdict-yes {
    background: linear-gradient(135deg, #0d2e0a, #0d0d0d);
    border: 2px solid #39FF14;
    border-radius: 12px;
    padding: 18px 22px;
    text-align: center;
    box-shadow: 0 0 20px #39FF1433;
}
.vb-verdict-no {
    background: #111;
    border: 2px solid #333;
    border-radius: 12px;
    padding: 18px 22px;
    text-align: center;
}
.vb-verdict-label {
    font-size: .68rem;
    letter-spacing: .16em;
    text-transform: uppercase;
    margin-bottom: 6px;
}
.vb-verdict-text {
    font-size: 1.4rem;
    font-weight: 900;
}
.vb-ev-pos { color: #39FF14; }
.vb-ev-neg { color: #FF4C4C; }
.vb-edge-bar-wrap { margin-top: 14px; }
.vb-edge-track {
    background: #222;
    border-radius: 999px;
    height: 6px;
    width: 100%;
    position: relative;
    overflow: visible;
}
.vb-edge-fill {
    height: 100%;
    border-radius: 999px;
    position: absolute;
    top: 0;
}

/* ---- inputs tweak ---- */
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input {
    background: #1a1a1a !important;
    border: 1px solid #2a2a2a !important;
    color: #fff !important;
    border-radius: 8px !important;
}
div[data-testid="stButton"] > button {
    background: #39FF14 !important;
    color: #000 !important;
    font-weight: 800 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.55rem 2.4rem !important;
    font-size: 1rem !important;
    letter-spacing: .04em;
    transition: opacity .2s;
    width: 100%;
}
div[data-testid="stButton"] > button:hover { opacity: .88; }
</style>
""", unsafe_allow_html=True)


# ── Poisson engine ─────────────────────────────────────────────────────────────
def poisson_prob(lam: float, k: int) -> float:
    return (lam ** k) * math.exp(-lam) / math.factorial(k)


def poisson_range(lam: float, k_min: int, k_max: int) -> float:
    return sum(poisson_prob(lam, k) for k in range(k_min, k_max + 1))


def compute_all(home_xg: float, away_xg: float):
    lam = max(home_xg + away_xg, 0.1)

    # --- Over / Under ---------------------------------------------------------
    over15 = 1 - poisson_range(lam, 0, 1)
    over25 = 1 - poisson_range(lam, 0, 2)
    over35 = 1 - poisson_range(lam, 0, 3)

    # --- BTTS (both score) — independent marginal ----------------------------
    p_home_scores = 1 - poisson_prob(home_xg, 0)
    p_away_scores = 1 - poisson_prob(away_xg, 0)
    btts = p_home_scores * p_away_scores

    # --- Total Goal Range -----------------------------------------------------
    w01 = poisson_range(lam, 0, 1)
    w23 = poisson_range(lam, 2, 3)
    w46 = poisson_range(lam, 4, 6)
    w7p = max(1.0 - w01 - w23 - w46, 0.001)

    def noise(w):
        return max(0.005, w + random.uniform(-0.03, 0.03))

    w01, w23, w46, w7p = noise(w01), noise(w23), noise(w46), noise(w7p)
    tot = w01 + w23 + w46 + w7p
    tgs = {
        "0-1 Gol": round(w01 / tot * 100),
        "2-3 Gol": round(w23 / tot * 100),
        "4-6 Gol": round(w46 / tot * 100),
    }
    tgs["7+ Gol"] = 100 - sum(tgs.values())
    tgs_best = max(tgs, key=tgs.get)

    # --- 1X2 (Dixon-Coles inspired simple model) -----------------------------
    pct_1 = round((home_xg / lam) * 100 * random.uniform(0.92, 1.08))
    pct_2 = round((away_xg / lam) * 100 * random.uniform(0.92, 1.08))
    pct_x = 100 - pct_1 - pct_2
    if pct_x < 5:
        adj = 5 - pct_x
        pct_1 -= adj // 2
        pct_2 -= adj - adj // 2
        pct_x = 5

    return {
        "lam":      lam,
        "over15":   round(over15 * 100),
        "under15":  100 - round(over15 * 100),
        "over25":   round(over25 * 100),
        "under25":  100 - round(over25 * 100),
        "over35":   round(over35 * 100),
        "under35":  100 - round(over35 * 100),
        "btts":     round(btts * 100),
        "no_btts":  100 - round(btts * 100),
        "tgs":      tgs,
        "tgs_best": tgs_best,
        "pct_1":    pct_1,
        "pct_x":    pct_x,
        "pct_2":    pct_2,
    }


# ── helpers ───────────────────────────────────────────────────────────────────
def bar_html(label: str, pct: int, color: str, best: bool = False) -> str:
    check = "✅ " if best else ""
    border = f"box-shadow:0 0 6px {color}55;" if best else ""
    return f"""
<div class="bar-wrap">
  <div class="bar-label"><span>{check}<b>{label}</b></span><span style="color:{color};font-weight:700">{pct}%</span></div>
  <div class="bar-track"><div class="bar-fill" style="width:{pct}%;background:{color};{border}"></div></div>
</div>"""


def pill(label: str, pct: int, positive: bool) -> str:
    cls = "pill-green" if positive else "pill-grey"
    return f'<span class="pill {cls}">{label} %{pct}</span>'


# ── layout ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:10px 0 4px">
  <span style="font-size:2rem;font-weight:900;color:#39FF14;letter-spacing:.06em">⚽ GOLMETRİK</span><br>
  <span style="font-size:.8rem;color:#555;letter-spacing:.18em;text-transform:uppercase">Poisson Tabanlı Futbol Tahmin Motoru</span>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="neon-divider">', unsafe_allow_html=True)

# ── sidebar / input form ──────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Maç Parametreleri")
    home_name = st.text_input("Ev Sahibi Takım", value="Galatasaray", key="home_name")
    away_name = st.text_input("Deplasman Takımı", value="Fenerbahçe", key="away_name")
    st.markdown("---")
    home_xg = st.number_input("Ev Sahibi xG (Beklenen Gol)", min_value=0.1, max_value=6.0,
                               value=1.65, step=0.05, format="%.2f")
    away_xg = st.number_input("Deplasman xG (Beklenen Gol)", min_value=0.1, max_value=6.0,
                               value=1.20, step=0.05, format="%.2f")
    st.markdown("---")
    analyse = st.button("🔍 Analiz Et", use_container_width=True)
    st.markdown("")
    st.caption("xG değerleri FBref, Understat veya SofaScore'dan alınabilir.")

# ── inline input (main area) ──────────────────────────────────────────────────
col_l, col_mid, col_r = st.columns([2, 1, 2])
with col_l:
    home_name_m = st.text_input("🏠 Ev Sahibi", value=home_name, key="home_m",
                                label_visibility="visible")
    home_xg_m   = st.number_input("xG", min_value=0.1, max_value=6.0,
                                   value=home_xg, step=0.05, format="%.2f",
                                   key="hxg_m", label_visibility="collapsed")
with col_mid:
    st.markdown("<div style='text-align:center;padding-top:36px'>"
                "<span style='color:#39FF14;font-size:1.6rem;font-weight:800'>VS</span></div>",
                unsafe_allow_html=True)
with col_r:
    away_name_m = st.text_input("✈️ Deplasman", value=away_name, key="away_m",
                                label_visibility="visible")
    away_xg_m   = st.number_input("xG", min_value=0.1, max_value=6.0,
                                   value=away_xg, step=0.05, format="%.2f",
                                   key="axg_m", label_visibility="collapsed")

_, btn_col, _ = st.columns([2, 1.2, 2])
with btn_col:
    analyse_main = st.button("⚡ Analiz Et", key="main_btn", use_container_width=True)

# ── results ───────────────────────────────────────────────────────────────────
if analyse_main or analyse or "result" in st.session_state:
    h_name = home_name_m or home_name
    a_name = away_name_m or away_name
    h_xg   = home_xg_m
    a_xg   = away_xg_m

    if analyse_main or analyse:
        st.session_state["result"] = compute_all(h_xg, a_xg)
        st.session_state["h_name"] = h_name
        st.session_state["a_name"] = a_name
        st.session_state["h_xg"]   = h_xg
        st.session_state["a_xg"]   = a_xg

    if "result" in st.session_state:
        r      = st.session_state["result"]
        h_name = st.session_state["h_name"]
        a_name = st.session_state["a_name"]
        h_xg   = st.session_state["h_xg"]
        a_xg   = st.session_state["a_xg"]

        # ── matchup banner ─────────────────────────────────────────────────────
        st.markdown('<hr class="neon-divider">', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="matchup">
          <span class="matchup-team">{h_name}</span>
          <span class="matchup-vs">VS</span>
          <span class="matchup-team">{a_name}</span>
        </div>""", unsafe_allow_html=True)

        # ── xG summary cards ──────────────────────────────────────────────────
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"""<div class="card">
              <div class="card-title">🏠 {h_name} xG</div>
              <div class="card-big" style="color:#39FF14">{h_xg:.2f}</div>
              <div class="card-sub">Beklenen gol (ev sahibi)</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class="card" style="text-align:center">
              <div class="card-title">⚡ Toplam xG</div>
              <div class="card-big">{r['lam']:.2f}</div>
              <div class="card-sub">λ = Poisson parametresi</div>
            </div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""<div class="card" style="text-align:right">
              <div class="card-title">✈️ {a_name} xG</div>
              <div class="card-big" style="color:#39FF14">{a_xg:.2f}</div>
              <div class="card-sub">Beklenen gol (deplasman)</div>
            </div>""", unsafe_allow_html=True)

        st.markdown('<div class="sec-header">TAHMİN ANALİZİ</div>', unsafe_allow_html=True)

        # ── 1X2 + BTTS ────────────────────────────────────────────────────────
        d1, d2 = st.columns(2)
        with d1:
            win_pct = max(r["pct_1"], r["pct_x"], r["pct_2"])
            p1_best = r["pct_1"] == win_pct
            px_best = r["pct_x"] == win_pct
            p2_best = r["pct_2"] == win_pct
            st.markdown(f"""<div class="card">
              <div class="card-title">1️⃣ Maç Sonucu (1X2)</div>
              {bar_html(f'1 — {h_name}', r["pct_1"], "#39FF14", p1_best)}
              {bar_html('X — Beraberlik',  r["pct_x"], "#FFD700", px_best)}
              {bar_html(f'2 — {a_name}', r["pct_2"], "#FF6B35", p2_best)}
            </div>""", unsafe_allow_html=True)
        with d2:
            st.markdown(f"""<div class="card">
              <div class="card-title">🎯 KG — İki Takım da Atar</div>
              {bar_html('KG VAR (GG)', r["btts"],    "#39FF14", r["btts"] >= r["no_btts"])}
              {bar_html('KG YOK (NG)', r["no_btts"], "#FF4C4C", r["no_btts"] > r["btts"])}
              <div class="card-sub" style="margin-top:14px">
                {h_name}: <b>%{round((1-math.exp(-h_xg))*100)}</b> gol atma ihtimali<br>
                {a_name}: <b>%{round((1-math.exp(-a_xg))*100)}</b> gol atma ihtimali
              </div>
            </div>""", unsafe_allow_html=True)

        # ── Over / Under ──────────────────────────────────────────────────────
        st.markdown('<div class="sec-header">GOL HATTI (ÜST / ALT)</div>',
                    unsafe_allow_html=True)
        e1, e2, e3 = st.columns(3)
        lines = [
            (e1, "1.5", r["over15"], r["under15"]),
            (e2, "2.5", r["over25"], r["under25"]),
            (e3, "3.5", r["over35"], r["under35"]),
        ]
        for col, line, ov, un in lines:
            ov_best = ov >= un
            with col:
                st.markdown(f"""<div class="card">
                  <div class="card-title">⚽ {line} Gol Hattı</div>
                  {bar_html(f'{line} Üst', ov, "#39FF14", ov_best)}
                  {bar_html(f'{line} Alt', un, "#888",    not ov_best)}
                </div>""", unsafe_allow_html=True)

        # ── TGS ───────────────────────────────────────────────────────────────
        st.markdown('<div class="sec-header">📊 TOPLAM GOL ARALIĞI (TGS)</div>',
                    unsafe_allow_html=True)

        tgs_colors = {
            "0-1 Gol": "#4FC3F7",
            "2-3 Gol": "#39FF14",
            "4-6 Gol": "#FFD700",
            "7+ Gol":  "#FF4C4C",
        }
        tgs_html = ""
        for label, pct in r["tgs"].items():
            is_best = label == r["tgs_best"]
            tgs_html += bar_html(label, pct, tgs_colors[label], is_best)

        st.markdown(f"""<div class="card">
          <div class="card-title">Gol Aralığı Dağılımı</div>
          {tgs_html}
          <div class="card-sub" style="margin-top:14px">
            En olası aralık: <b style="color:#39FF14">{r['tgs_best']}</b>
            &nbsp;—&nbsp; Poisson(λ={r['lam']:.2f})
          </div>
        </div>""", unsafe_allow_html=True)

        # ── Ana Öneri ─────────────────────────────────────────────────────────
        st.markdown('<div class="sec-header">ANA ÖNERİ</div>', unsafe_allow_html=True)

        all_picks = [
            (f"1 — {h_name}",   r["pct_1"]),
            ("X — Beraberlik",   r["pct_x"]),
            (f"2 — {a_name}",   r["pct_2"]),
            ("2.5 Üst" if r["over25"] >= r["under25"] else "2.5 Alt",
             r["over25"] if r["over25"] >= r["under25"] else r["under25"]),
            ("KG VAR" if r["btts"] >= r["no_btts"] else "KG YOK",
             r["btts"] if r["btts"] >= r["no_btts"] else r["no_btts"]),
            (r["tgs_best"], r["tgs"][r["tgs_best"]]),
        ]
        best_label, best_pct = max(all_picks, key=lambda x: x[1])

        f1, f2, f3 = st.columns(3)
        with f1:
            ou_label = "2.5 Üst" if r["over25"] >= r["under25"] else "2.5 Alt"
            ou_pct   = r["over25"] if r["over25"] >= r["under25"] else r["under25"]
            st.markdown(f"""<div class="best-pick">
              <div class="best-pick-label">Gol Hattı</div>
              <div class="best-pick-value">{ou_label}</div>
              <div class="best-pick-pct">%{ou_pct}</div>
            </div>""", unsafe_allow_html=True)
        with f2:
            st.markdown(f"""<div class="best-pick" style="border-color:#FFD700;background:linear-gradient(135deg,#2a2000,#0d0d0d)">
              <div class="best-pick-label" style="color:#FFD700">⭐ En Güçlü Öneri</div>
              <div class="best-pick-value">{best_label}</div>
              <div class="best-pick-pct" style="color:#FFD700">%{best_pct}</div>
            </div>""", unsafe_allow_html=True)
        with f3:
            kg_label = "KG VAR (GG)" if r["btts"] >= r["no_btts"] else "KG YOK (NG)"
            kg_pct   = r["btts"] if r["btts"] >= r["no_btts"] else r["no_btts"]
            st.markdown(f"""<div class="best-pick">
              <div class="best-pick-label">Karşılıklı Gol</div>
              <div class="best-pick-value">{kg_label}</div>
              <div class="best-pick-pct">%{kg_pct}</div>
            </div>""", unsafe_allow_html=True)

        # ── pill summary ──────────────────────────────────────────────────────
        st.markdown('<div class="sec-header">ÖZET</div>', unsafe_allow_html=True)
        pills = (
            pill("1.5 Üst" if r["over15"] >= r["under15"] else "1.5 Alt",
                 r["over15"] if r["over15"] >= r["under15"] else r["under15"],
                 r["over15"] >= r["under15"]) +
            pill("2.5 Üst" if r["over25"] >= r["under25"] else "2.5 Alt",
                 r["over25"] if r["over25"] >= r["under25"] else r["under25"],
                 r["over25"] >= r["under25"]) +
            pill("3.5 Üst" if r["over35"] >= r["under35"] else "3.5 Alt",
                 r["over35"] if r["over35"] >= r["under35"] else r["under35"],
                 r["over35"] >= r["under35"]) +
            pill("KG VAR" if r["btts"] >= r["no_btts"] else "KG YOK",
                 r["btts"] if r["btts"] >= r["no_btts"] else r["no_btts"],
                 r["btts"] >= r["no_btts"]) +
            pill(r["tgs_best"], r["tgs"][r["tgs_best"]], True)
        )
        st.markdown