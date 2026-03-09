import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# ==========================================
# 0. KONFIGURASI HALAMAN & INJEKSI CSS
# ==========================================
st.set_page_config(
    page_title="Dufan Queue Simulator — Analytics",
    layout="wide",
    page_icon="🎢",
    initial_sidebar_state="expanded"
)

# ── DESIGN SYSTEM (from main.js) ──────────────────────────────────────────────
# Colors: deep navy bg, sky-blue primary, indigo/violet accent, green success,
#         red danger, amber warning — all on rgba glassmorphism surfaces.
# Fonts : Orbitron (display) · Share Tech Mono (mono/labels) · Exo 2 (body)

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&family=Share+Tech+Mono&family=Exo+2:wght@300;400;500;600&display=swap" rel="stylesheet">

<style>
/* ─── ROOT / TOKENS ──────────────────────────────────────────── */
:root {
    --bg-base:       #060e1e;
    --bg-surface:    rgba(10, 22, 46, 0.88);
    --bg-card:       rgba(14, 28, 56, 0.82);
    --border-glow:   rgba(56, 189, 248, 0.22);
    --border-subtle: rgba(56, 189, 248, 0.10);
    --cyan:          #38bdf8;
    --cyan-dim:      rgba(56, 189, 248, 0.55);
    --violet:        #818cf8;
    --violet-dim:    rgba(129, 140, 248, 0.55);
    --green:         #22c55e;
    --red:           #ef4444;
    --amber:         #facc15;
    --text-primary:  #e2e8f0;
    --text-muted:    #94a3b8;
    --text-faint:    #475569;
    --font-display:  'Orbitron', monospace;
    --font-mono:     'Share Tech Mono', monospace;
    --font-body:     'Exo 2', sans-serif;
}

/* ─── GLOBAL OVERRIDES ───────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: var(--font-body) !important;
    color: var(--text-primary) !important;
}
.stApp {
    background: var(--bg-base) !important;
    background-image:
        linear-gradient(rgba(30,80,160,0.045) 1px, transparent 1px),
        linear-gradient(90deg, rgba(30,80,160,0.045) 1px, transparent 1px),
        linear-gradient(rgba(20,55,120,0.022) 1px, transparent 1px),
        linear-gradient(90deg, rgba(20,55,120,0.022) 1px, transparent 1px) !important;
    background-size: 80px 80px, 80px 80px, 20px 20px, 20px 20px !important;
}

/* ─── TOPBAR ─────────────────────────────────────────────────── */
.sim-topbar {
    position: relative;
    width: 100%;
    padding: 18px 32px 18px 32px;
    margin-bottom: 28px;
    background: rgba(6, 14, 30, 0.96);
    backdrop-filter: blur(16px);
    border-bottom: 1px solid var(--border-glow);
    box-shadow: 0 2px 32px rgba(0,0,0,0.6), 0 0 80px rgba(56,189,248,0.04);
    display: flex;
    align-items: center;
    gap: 14px;
}
.sim-topbar-dot {
    width: 8px; height: 8px; border-radius: 50%;
    background: var(--green);
    box-shadow: 0 0 10px var(--green);
    animation: tbBlink 2s ease-in-out infinite;
    flex-shrink: 0;
}
@keyframes tbBlink { 0%,100%{opacity:1} 50%{opacity:0.15} }
.sim-topbar-title {
    font-family: var(--font-display) !important;
    font-size: 17px;
    font-weight: 700;
    letter-spacing: 2px;
    color: var(--text-primary) !important;
    white-space: nowrap;
}
.sim-topbar-title span {
    background: linear-gradient(90deg, var(--cyan), var(--violet));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.sim-topbar-badge {
    margin-left: auto;
    font-family: var(--font-mono) !important;
    font-size: 10px;
    letter-spacing: 2px;
    color: var(--cyan-dim);
    border: 1px solid var(--border-glow);
    padding: 4px 14px;
    border-radius: 20px;
    background: rgba(56,189,248,0.06);
}

/* ─── SECTION HEADERS ────────────────────────────────────────── */
.section-header {
    font-family: var(--font-display) !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 3px !important;
    color: var(--cyan) !important;
    text-transform: uppercase !important;
    margin: 36px 0 18px 0 !important;
    padding-bottom: 10px !important;
    border-bottom: 1px solid var(--border-glow) !important;
    display: flex;
    align-items: center;
    gap: 10px;
}
.section-header::before {
    content: '';
    display: inline-block;
    width: 3px; height: 14px;
    background: linear-gradient(180deg, var(--cyan), var(--violet));
    border-radius: 2px;
    flex-shrink: 0;
}

/* ─── KPI CARDS ──────────────────────────────────────────────── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 14px;
    margin-bottom: 28px;
}
.kpi-card {
    background: var(--bg-card);
    border: 1px solid var(--border-glow);
    border-radius: 12px;
    padding: 18px 16px 14px;
    backdrop-filter: blur(10px);
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s, box-shadow 0.2s;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--cyan), var(--violet));
    border-radius: 12px 12px 0 0;
}
.kpi-card:hover {
    border-color: var(--cyan-dim);
    box-shadow: 0 0 24px rgba(56,189,248,0.12);
}
.kpi-label {
    font-family: var(--font-mono) !important;
    font-size: 9px !important;
    letter-spacing: 2.5px !important;
    color: var(--text-muted) !important;
    text-transform: uppercase !important;
    margin-bottom: 10px;
}
.kpi-values {
    display: flex;
    align-items: flex-end;
    gap: 8px;
    flex-wrap: wrap;
}
.kpi-val-hier {
    font-family: var(--font-display) !important;
    font-size: 22px !important;
    font-weight: 700 !important;
    color: var(--cyan) !important;
    line-height: 1;
}
.kpi-val-base {
    font-family: var(--font-display) !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    color: var(--violet) !important;
    line-height: 1;
    opacity: 0.8;
}
.kpi-legend {
    display: flex;
    gap: 10px;
    margin-top: 8px;
    flex-wrap: wrap;
}
.kpi-dot {
    width: 6px; height: 6px; border-radius: 50%;
    display: inline-block; margin-right: 4px; flex-shrink: 0;
    position: relative; top: 1px;
}
.kpi-legend-item {
    font-family: var(--font-mono) !important;
    font-size: 8px !important;
    color: var(--text-faint) !important;
    letter-spacing: 1px;
    display: flex; align-items: center;
}
.kpi-delta-pos { color: var(--green) !important; font-size: 9px !important;
    font-family: var(--font-mono) !important; }
.kpi-delta-neg { color: var(--red) !important; font-size: 9px !important;
    font-family: var(--font-mono) !important; }

/* ─── CHART WRAPPERS ─────────────────────────────────────────── */
.chart-panel {
    background: var(--bg-card);
    border: 1px solid var(--border-glow);
    border-radius: 14px;
    padding: 20px 18px 16px;
    backdrop-filter: blur(10px);
    margin-bottom: 16px;
    position: relative;
    overflow: hidden;
}
.chart-panel::after {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 14px;
    background: radial-gradient(ellipse at 0% 0%, rgba(56,189,248,0.04), transparent 60%);
    pointer-events: none;
}
.chart-title {
    font-family: var(--font-mono) !important;
    font-size: 10px !important;
    letter-spacing: 2px !important;
    color: var(--text-muted) !important;
    text-transform: uppercase !important;
    margin-bottom: 14px !important;
    display: flex; align-items: center; gap: 8px;
}

/* ─── SIDEBAR ────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: rgba(6,14,30,0.97) !important;
    border-right: 1px solid var(--border-glow) !important;
}
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    font-family: var(--font-mono) !important;
    font-size: 10px !important;
    letter-spacing: 2px !important;
    color: var(--cyan) !important;
    text-transform: uppercase !important;
    border-bottom: 1px solid var(--border-subtle) !important;
    padding-bottom: 6px !important;
    margin-top: 20px !important;
}
[data-testid="stSidebar"] .stFileUploader {
    border: 1px solid var(--border-glow) !important;
    border-radius: 8px !important;
    background: rgba(56,189,248,0.04) !important;
}

/* ─── INFO / ALERT BOXES ─────────────────────────────────────── */
.stAlert, .stSuccess, .stWarning, .stInfo {
    border-radius: 10px !important;
    border: 1px solid var(--border-glow) !important;
    font-family: var(--font-body) !important;
}

/* ─── LEGEND BADGE ───────────────────────────────────────────── */
.legend-bar {
    display: flex;
    gap: 20px;
    align-items: center;
    margin-bottom: 20px;
    padding: 10px 16px;
    background: rgba(10,22,46,0.7);
    border: 1px solid var(--border-subtle);
    border-radius: 8px;
    width: fit-content;
}
.legend-item {
    display: flex; align-items: center; gap: 8px;
    font-family: var(--font-mono) !important;
    font-size: 10px !important;
    letter-spacing: 1.5px;
    color: var(--text-muted) !important;
}
.legend-swatch {
    width: 28px; height: 3px; border-radius: 2px;
}

/* ─── SPINNER ────────────────────────────────────────────────── */
.stSpinner > div {
    border-color: var(--cyan) transparent transparent transparent !important;
}

/* ─── DIVIDER ────────────────────────────────────────────────── */
hr {
    border: none !important;
    border-top: 1px solid var(--border-subtle) !important;
    margin: 32px 0 !important;
}
</style>
""", unsafe_allow_html=True)

# ─── TOPBAR ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="sim-topbar">
    <div class="sim-topbar-dot"></div>
    <div class="sim-topbar-title">🎢 DUFAN &nbsp;<span>ANALYTICS DASHBOARD</span></div>
    <div class="sim-topbar-badge">AGENT-BASED SIMULATION · M/M/1 · HIERARCHICAL + PWT</div>
</div>
""", unsafe_allow_html=True)

# ─── DESIGN TOKENS (for matplotlib — white/seaborn default) ──────────────────
CLR_CYAN   = "#38bdf8"
CLR_VIOLET = "#818cf8"
CLR_RED    = "#ef4444"

sns.set_theme(style="whitegrid")
plt.rcParams['font.family'] = 'sans-serif'

def apply_theme(ax, title="", xlabel="", ylabel=""):
    """Keep default seaborn whitegrid theme, just apply labels."""
    if title:
        ax.set_title(title, fontsize=12, fontweight='bold')
    if xlabel: ax.set_xlabel(xlabel, fontsize=10)
    if ylabel: ax.set_ylabel(ylabel, fontsize=10)

def styled_fig(w=10, h=5):
    fig, ax = plt.subplots(figsize=(w, h))
    return fig, ax

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
st.sidebar.markdown("## 📂 Upload Data Simulasi")
st.sidebar.markdown("### A · Skenario Dengan Strategi")
f_p_hier = st.sidebar.file_uploader("Data Pengunjung (Strategi)", type="csv", key="p_h")
f_w_hier = st.sidebar.file_uploader("Data Wahana (Strategi)", type="csv", key="w_h")
f_m_hier = st.sidebar.file_uploader("Data Meta (Strategi)", type="csv", key="m_h")

st.sidebar.markdown("### B · Skenario Tanpa Strategi")
f_p_base = st.sidebar.file_uploader("Data Pengunjung (Baseline)", type="csv", key="p_b")
f_w_base = st.sidebar.file_uploader("Data Wahana (Baseline)", type="csv", key="w_b")
f_m_base = st.sidebar.file_uploader("Data Meta (Baseline)", type="csv", key="m_b")

st.sidebar.markdown("---")
st.sidebar.markdown("## 📈 Analisis Sensitivitas")
st.sidebar.caption("Upload BANYAK file 'Data Meta' dari simulasi dengan jumlah N yang berbeda-beda.")
f_meta_multi_hier = st.sidebar.file_uploader("Kumpulan Meta (Strategi)", type="csv", accept_multiple_files=True, key="mm_h")
f_meta_multi_base = st.sidebar.file_uploader("Kumpulan Meta (Baseline)", type="csv", accept_multiple_files=True, key="mm_b")

# ─── LEGEND BAR ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="legend-bar">
  <div class="legend-item">
    <div class="legend-swatch" style="background:#38bdf8;"></div> HIERARCHICAL + PWT (Strategi)
  </div>
  <div class="legend-item">
    <div class="legend-swatch" style="background:#818cf8;"></div> NO HIERARCHICAL (Baseline)
  </div>
</div>
""", unsafe_allow_html=True)

# ─── HELPERS ─────────────────────────────────────────────────────────────────
def bar_pair(ax, categories, vals_hier, vals_base, title="", ylabel=""):
    """Render a grouped bar chart with default white seaborn style."""
    x = np.arange(len(categories))
    w = 0.35
    b1 = ax.bar(x - w/2, vals_hier, w, label='Hierarchical (Strategi)', color=CLR_CYAN)
    b2 = ax.bar(x + w/2, vals_base, w, label='No Hierarchical (Baseline)', color=CLR_VIOLET)
    apply_theme(ax, title=title, ylabel=ylabel)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation=45, ha='right', fontsize=8)
    ax.legend()
    return b1, b2

def create_wahana_plot(df_w_hier, df_w_base, col_name, title, ylabel):
    fig, ax = styled_fig(10, 4.5)
    names = df_w_hier['Nama Wahana'].values
    bar_pair(ax, names, df_w_hier[col_name].values, df_w_base[col_name].values, title=title, ylabel=ylabel)
    plt.tight_layout(pad=1.4)
    return fig

# ==========================================
# MAIN CONTENT — 1 RUN ANALYSIS
# ==========================================
if all([f_p_hier, f_w_hier, f_m_hier, f_p_base, f_w_base, f_m_base]):

    with st.spinner('Memproses data dan merender grafik...'):
        df_p_hier = pd.read_csv(f_p_hier)
        df_w_hier = pd.read_csv(f_w_hier)
        df_m_hier = pd.read_csv(f_m_hier)
        df_p_base = pd.read_csv(f_p_base)
        df_w_base = pd.read_csv(f_w_base)
        df_m_base = pd.read_csv(f_m_base)

        # ── SECTION 1: KPI CARDS ─────────────────────────────────────────────
        st.markdown('<div class="section-header">01 &nbsp; Ringkasan Performa — KPI Dashboard</div>', unsafe_allow_html=True)

        kpi_specs = [
            ('Total Pengunjung',      '👤', 'Orang'),
            ('Avg Rides',             '🎢', 'Wahana / Orang'),
            ('Avg Queue Global (m)',   '⏱', 'Menit'),
            ('Satisfaction Score (%)', '😊', '%'),
            ('Global Rho',            '📊', 'Utilisasi (ρ)'),
        ]

        cols = st.columns(5)
        for (col_name, icon, unit), c in zip(kpi_specs, cols):
            val_h = float(df_m_hier[col_name].values[0])
            val_b = float(df_m_base[col_name].values[0])
            delta_pct = ((val_h - val_b) / (val_b + 1e-9)) * 100
            delta_cls = "kpi-delta-pos" if delta_pct >= 0 else "kpi-delta-neg"
            delta_str = f"{'▲' if delta_pct >= 0 else '▼'} {abs(delta_pct):.1f}%"
            fmt = lambda v: f'{v:.2f}' if v % 1 != 0 else f'{int(v)}'

            c.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">{icon} &nbsp; {col_name}</div>
                <div class="kpi-values">
                    <div class="kpi-val-hier">{fmt(val_h)}</div>
                    <div class="kpi-val-base">{fmt(val_b)}</div>
                    <div class="{delta_cls}">{delta_str}</div>
                </div>
                <div class="kpi-legend">
                    <span class="kpi-legend-item"><span class="kpi-dot" style="background:#38bdf8;"></span>HIER</span>
                    <span class="kpi-legend-item"><span class="kpi-dot" style="background:#818cf8;"></span>BASE</span>
                </div>
                <div style="font-family:var(--font-mono);font-size:8px;color:var(--text-faint);margin-top:6px;letter-spacing:1px">{unit}</div>
            </div>
            """, unsafe_allow_html=True)

        # ── SECTION 2: WAHANA ANALYSIS ───────────────────────────────────────
        st.markdown('<div class="section-header">02 &nbsp; Analisis Antrean per Wahana</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="chart-panel"><div class="chart-title">▸ RATA-RATA WAKTU TUNGGU PER WAHANA</div>', unsafe_allow_html=True)
            fig = create_wahana_plot(df_w_hier, df_w_base, 'Avg Antre (m)', '', 'Waktu (Menit)')
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="chart-panel"><div class="chart-title">▸ TOTAL PENGUNJUNG PER WAHANA</div>', unsafe_allow_html=True)
            fig = create_wahana_plot(df_w_hier, df_w_base, 'Total Pengunjung Naik', '', 'Jumlah Orang')
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="chart-panel"><div class="chart-title">▸ UTILISASI WAHANA (ρ)</div>', unsafe_allow_html=True)
            fig = create_wahana_plot(df_w_hier, df_w_base, 'rho', '', 'ρ (0.0 – 1.5+)')
            # Overlay danger zone
            ax = fig.axes[0]
            ax.axhline(1.0, color=CLR_RED, linewidth=1, linestyle='--', alpha=0.6, zorder=5)
            ax.axhspan(1.0, ax.get_ylim()[1] if ax.get_ylim()[1] > 1 else 1.5,
                       color=CLR_RED, alpha=0.06, zorder=1)
            ax.text(0, 1.02, 'OVERLOAD ZONE', fontsize=7, color=CLR_RED,
                    fontfamily='monospace', va='bottom', alpha=0.7)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="chart-panel"><div class="chart-title">▸ PANJANG ANTREAN RATA-RATA (Lq)</div>', unsafe_allow_html=True)
            fig = create_wahana_plot(df_w_hier, df_w_base, 'Lq', '', 'Orang di Antrean')
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
            st.markdown('</div>', unsafe_allow_html=True)

        # ── SECTION 3: VISITOR BEHAVIOR ──────────────────────────────────────
        st.markdown('<div class="section-header">03 &nbsp; Perilaku &amp; Pola Kedatangan Pengunjung</div>', unsafe_allow_html=True)

        col3, col4 = st.columns(2)
        with col3:
            st.markdown('<div class="chart-panel"><div class="chart-title">▸ DISTRIBUSI JUMLAH WAHANA YANG DINAIKI</div>', unsafe_allow_html=True)
            bins   = [0, 2, 5, 9, 14, 20, 25]
            labels = ['1–2', '3–5', '6–9', '10–14', '15–20', '21+']
            out_h  = pd.cut(df_p_hier['Total Naik'], bins=bins, labels=labels, include_lowest=True).value_counts(sort=False)
            out_b  = pd.cut(df_p_base['Total Naik'], bins=bins, labels=labels, include_lowest=True).value_counts(sort=False)

            fig, ax = styled_fig(8, 4.5)
            bar_pair(ax, labels, out_h.values, out_b.values, title='Distribusi Jumlah Wahana yang Dinaiki', ylabel='Jumlah Pengunjung')
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
            st.markdown('</div>', unsafe_allow_html=True)

        with col4:
            st.markdown('<div class="chart-panel"><div class="chart-title">▸ POLA KEDATANGAN PENGUNJUNG PER JAM</div>', unsafe_allow_html=True)
            jam_h = df_p_hier['Jam Masuk'].str.split(':').str[0].astype(int).value_counts().sort_index()
            jam_b = df_p_base['Jam Masuk'].str.split(':').str[0].astype(int).value_counts().sort_index()

            fig, ax = styled_fig(8, 4.5)
            ax.plot(jam_h.index, jam_h.values, marker='o', color=CLR_CYAN, linewidth=2, label='Hierarchical')
            ax.plot(jam_b.index, jam_b.values, marker='o', color=CLR_VIOLET, linewidth=2, label='No Hierarchical')
            ax.fill_between(jam_h.index, jam_h.values, alpha=0.1, color=CLR_CYAN)
            ax.fill_between(jam_b.index, jam_b.values, alpha=0.1, color=CLR_VIOLET)
            apply_theme(ax, title='Pola Kedatangan Pengunjung per Jam', ylabel='Jumlah Kedatangan', xlabel='Jam')
            ax.set_xticks(np.arange(10, 21, 1))
            ax.legend()
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
            st.markdown('</div>', unsafe_allow_html=True)

        # ── SECTION 4: PERBANDINGAN DATA META ────────────────────────────────
        st.markdown('<div class="section-header">04 &nbsp; Perbandingan Data Meta: Strategi vs Baseline</div>', unsafe_allow_html=True)

        meta_cols = [
            ('Avg Rides',              'Wahana / Orang',          ''),
            ('Avg Queue Global (m)',   'Menit',                   ''),
            ('Satisfaction Score (%)', 'Persentase (%)',           ''),
            ('Global Rho',             'Utilisasi (0.0 – 1.5+)',  ''),
        ]

        val_hier_list = [float(df_m_hier[c].values[0]) for c, _, _ in meta_cols]
        val_base_list = [float(df_m_base[c].values[0]) for c, _, _ in meta_cols]
        col_names     = [c for c, _, _ in meta_cols]

        # ── Grafik 1: Grouped Bar semua KPI sekaligus ────────────────────────
        st.markdown('<div class="chart-panel"><div class="chart-title">▸ PERBANDINGAN SEMUA KPI — STRATEGI vs BASELINE</div>', unsafe_allow_html=True)
        fig, ax = styled_fig(12, 5)
        x = np.arange(len(col_names))
        w = 0.35
        b1 = ax.bar(x - w/2, val_hier_list, w, label='Hierarchical + PWT (Strategi)', color=CLR_CYAN)
        b2 = ax.bar(x + w/2, val_base_list, w, label='No Hierarchical (Baseline)',    color=CLR_VIOLET)
        for bar, val in zip(b1, val_hier_list):
            lbl = f'{val:.2f}' if val % 1 != 0 else f'{int(val)}'
            ax.text(bar.get_x() + bar.get_width()/2, val, lbl,
                    ha='center', va='bottom', fontsize=9, fontweight='bold', color=CLR_CYAN)
        for bar, val in zip(b2, val_base_list):
            lbl = f'{val:.2f}' if val % 1 != 0 else f'{int(val)}'
            ax.text(bar.get_x() + bar.get_width()/2, val, lbl,
                    ha='center', va='bottom', fontsize=9, fontweight='bold', color=CLR_VIOLET)
        apply_theme(ax, title='Perbandingan KPI Keseluruhan', ylabel='Nilai')
        ax.set_xticks(x)
        ax.set_xticklabels(col_names, fontsize=9)
        ax.legend()
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
        st.markdown('</div>', unsafe_allow_html=True)

        # ── Grafik 2: Bar chart per KPI individual (2 kolom x 3 baris) ───────
        st.markdown('<div class="chart-panel"><div class="chart-title">▸ DETAIL PER KPI</div>', unsafe_allow_html=True)
        fig, axes = plt.subplots(2, 3, figsize=(15, 8))
        axes = axes.flatten()
        labels_bar = ['Strategi (Hier)', 'Tanpa Strategi']
        colors_bar  = [CLR_CYAN, CLR_VIOLET]
        for i, (col, ylabel, icon) in enumerate(meta_cols):
            ax_i = axes[i]
            val_h = float(df_m_hier[col].values[0])
            val_b = float(df_m_base[col].values[0])
            bars = ax_i.bar(labels_bar, [val_h, val_b], color=colors_bar, width=0.5)
            apply_theme(ax_i, title=f'{icon}  {col.upper()}', ylabel=ylabel)
            for bar, val in zip(bars, [val_h, val_b]):
                lbl = f'{val:.2f}' if val % 1 != 0 else f'{int(val)}'
                ax_i.text(bar.get_x() + bar.get_width()/2, val, lbl,
                          ha='center', va='bottom', fontsize=11, fontweight='bold')
        axes[5].axis('off')
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
        st.markdown('</div>', unsafe_allow_html=True)

        # ── Grafik 3: Radar / Spider Chart ───────────────────────────────────
        st.markdown('<div class="chart-panel"><div class="chart-title">▸ RADAR CHART — PROFIL PERFORMA KESELURUHAN</div>', unsafe_allow_html=True)
        radar_cols   = ['Avg Rides', 'Avg Queue Global (m)', 'Satisfaction Score (%)', 'Global Rho']
        radar_labels = ['Avg Rides', 'Avg Queue\nGlobal (m)', 'Satisfaction\nScore (%)', 'Global Rho']
        vals_h_raw = np.array([float(df_m_hier[c].values[0]) for c in radar_cols])
        vals_b_raw = np.array([float(df_m_base[c].values[0]) for c in radar_cols])
        combined_max = np.maximum(vals_h_raw, vals_b_raw)
        combined_min = np.minimum(vals_h_raw, vals_b_raw)
        norm_range   = np.where(combined_max - combined_min == 0, 1, combined_max - combined_min)
        vals_h_norm  = (vals_h_raw - combined_min) / norm_range
        vals_b_norm  = (vals_b_raw - combined_min) / norm_range
        N_radar = len(radar_cols)
        angles  = np.linspace(0, 2 * np.pi, N_radar, endpoint=False).tolist()
        angles += angles[:1]
        vals_h_plot = vals_h_norm.tolist() + vals_h_norm[:1].tolist()
        vals_b_plot = vals_b_norm.tolist() + vals_b_norm[:1].tolist()
        fig_r, ax_r = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
        ax_r.set_facecolor('white')
        fig_r.patch.set_facecolor('white')
        ax_r.plot(angles, vals_h_plot, 'o-', linewidth=2, color=CLR_CYAN,   label='Hierarchical + PWT')
        ax_r.fill(angles, vals_h_plot, alpha=0.20, color=CLR_CYAN)
        ax_r.plot(angles, vals_b_plot, 'o-', linewidth=2, color=CLR_VIOLET, label='No Hierarchical', linestyle='--')
        ax_r.fill(angles, vals_b_plot, alpha=0.15, color=CLR_VIOLET)
        ax_r.set_thetagrids(np.degrees(angles[:-1]), radar_labels, fontsize=10)
        ax_r.set_ylim(0, 1.1)
        ax_r.set_yticks([0.25, 0.5, 0.75, 1.0])
        ax_r.set_yticklabels(['25%', '50%', '75%', '100%'], fontsize=7, color='grey')
        ax_r.grid(color='grey', linestyle=':', linewidth=0.6, alpha=0.5)
        ax_r.set_title('Radar Performa (Nilai Ternormalisasi)', fontsize=12, fontweight='bold', pad=20)
        ax_r.legend(loc='upper right', bbox_to_anchor=(1.35, 1.15), fontsize=9)
        col_r1, col_r2, col_r3 = st.columns([1, 2, 1])
        with col_r2:
            st.pyplot(fig_r, use_container_width=True)
        plt.close(fig_r)
        st.markdown('</div>', unsafe_allow_html=True)

        # ── Grafik 4: Delta / Selisih absolut & persen ───────────────────────
        st.markdown('<div class="chart-panel"><div class="chart-title">▸ DELTA IMPROVEMENT — STRATEGI vs BASELINE</div>', unsafe_allow_html=True)
        delta_abs  = [h - b for h, b in zip(val_hier_list, val_base_list)]
        delta_pct  = [((h - b) / (abs(b) + 1e-9)) * 100 for h, b in zip(val_hier_list, val_base_list)]
        bar_colors = [CLR_CYAN if d >= 0 else CLR_VIOLET for d in delta_pct]
        fig_d, (ax_da, ax_dp) = plt.subplots(1, 2, figsize=(14, 5))
        bars_a = ax_da.barh(col_names, delta_abs, color=bar_colors, height=0.5)
        ax_da.axvline(0, color='black', linewidth=0.8)
        apply_theme(ax_da, title='Selisih Absolut (Hier − Base)', xlabel='Δ Nilai')
        ax_da.tick_params(axis='y', labelsize=9)
        for bar, val in zip(bars_a, delta_abs):
            lbl = f'{val:+.2f}'
            x_pos = val + (max(abs(v) for v in delta_abs) * 0.02) * (1 if val >= 0 else -1)
            ax_da.text(x_pos, bar.get_y() + bar.get_height()/2, lbl,
                       va='center', ha='left' if val >= 0 else 'right',
                       fontsize=9, fontweight='bold',
                       color=CLR_CYAN if val >= 0 else CLR_VIOLET)
        bars_p = ax_dp.barh(col_names, delta_pct, color=bar_colors, height=0.5)
        ax_dp.axvline(0, color='black', linewidth=0.8)
        apply_theme(ax_dp, title='Selisih Persentase (Hier − Base)', xlabel='Δ (%)')
        ax_dp.tick_params(axis='y', labelsize=9)
        for bar, val in zip(bars_p, delta_pct):
            lbl = f'{val:+.1f}%'
            x_pos = val + (max(abs(v) for v in delta_pct) * 0.02) * (1 if val >= 0 else -1)
            ax_dp.text(x_pos, bar.get_y() + bar.get_height()/2, lbl,
                       va='center', ha='left' if val >= 0 else 'right',
                       fontsize=9, fontweight='bold',
                       color=CLR_CYAN if val >= 0 else CLR_VIOLET)
        plt.tight_layout()
        st.pyplot(fig_d, use_container_width=True)
        plt.close(fig_d)
        st.markdown('</div>', unsafe_allow_html=True)


    st.success('✔  Visualisasi 1 Run berhasil dimuat. Lanjut ke Analisis Sensitivitas di sidebar jika file multi-meta sudah siap.')

# ==========================================
# SECTION 4: SENSITIVITY ANALYSIS
# ==========================================
if f_meta_multi_hier and f_meta_multi_base:
    st.markdown('<div class="section-header">04 &nbsp; Analisis Sensitivitas Kapasitas Pengunjung (N)</div>', unsafe_allow_html=True)

    with st.spinner('Membangun Kurva Sensitivitas...'):
        def combine_meta(files):
            return pd.concat([pd.read_csv(f) for f in files], ignore_index=True).sort_values('Total Pengunjung').reset_index(drop=True)

        df_mh = combine_meta(f_meta_multi_hier)
        df_mb = combine_meta(f_meta_multi_base)

        sens_specs = [
            ('Avg Queue Global (m)',   'WAKTU TUNGGU vs N',         'Global Avg Queue (Menit)'),
            ('Global Rho',             'UTILISASI (ρ) vs N',        'Global ρ'),
            ('Avg Rides',              'WAHANA DIKUNJUNGI vs N',    'Rata-rata Wahana / Orang'),
            ('Satisfaction Score (%)', 'KEPUASAN vs N',             'Satisfaction Score (%)'),
        ]

        col5, col6 = st.columns(2)
        for i, (col_name, title, ylabel) in enumerate(sens_specs):
            c = col5 if i % 2 == 0 else col6

            st.markdown(f'<div class="chart-panel"><div class="chart-title">▸ {title}</div>', unsafe_allow_html=True)
            fig, ax = styled_fig(8, 4.2)
            ax.plot(df_mh['Total Pengunjung'], df_mh[col_name],
                    marker='o', color=CLR_CYAN, linewidth=2.5, label='Strategi (Hierarchical + PWT)')
            ax.plot(df_mb['Total Pengunjung'], df_mb[col_name],
                    marker='o', color=CLR_VIOLET, linewidth=2.5, linestyle='--', label='Tanpa Strategi')
            apply_theme(ax, title=title, ylabel=ylabel, xlabel='Total Pengunjung (N)')
            ax.legend()
            ax.grid(True, linestyle=':', alpha=0.6)
            plt.tight_layout()
            c.pyplot(fig, use_container_width=True)
            plt.close(fig)
            st.markdown('</div>', unsafe_allow_html=True)

elif (f_meta_multi_hier and not f_meta_multi_base) or (f_meta_multi_base and not f_meta_multi_hier):
    st.warning("⚠️ Upload Kumpulan Data Meta untuk **kedua** skenario agar Analisis Sensitivitas tampil.")

elif not all([f_p_hier, f_w_hier, f_m_hier, f_p_base, f_w_base, f_m_base]):
    # ── EMPTY STATE ──────────────────────────────────────────────────────────
    st.markdown("""
    <div style="
        text-align:center;
        padding: 80px 40px;
        background: rgba(10,22,46,0.6);
        border: 1px dashed rgba(56,189,248,0.2);
        border-radius: 16px;
        margin-top: 20px;
    ">
        <div style="font-size:56px;margin-bottom:20px">🎢</div>
        <div style="
            font-family:'Orbitron',monospace;
            font-size:14px;
            font-weight:700;
            letter-spacing:3px;
            color:#38bdf8;
            margin-bottom:10px;
        ">AWAITING SIMULATION DATA</div>
        <div style="
            font-family:'Share Tech Mono',monospace;
            font-size:11px;
            letter-spacing:1.5px;
            color:#475569;
            line-height:2;
        ">
            Upload file CSV di panel sidebar kiri untuk memulai visualisasi.<br>
            Aplikasi ini memproses log Agent-Based Simulation secara lokal.<br>
            Tidak ada data yang dikirim ke server eksternal.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─── FOOTER ──────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="
    display:flex; justify-content:space-between; align-items:center;
    padding: 10px 0;
    font-family:'Share Tech Mono',monospace;
    font-size:9px;
    letter-spacing:1.5px;
    color:#334155;
">
    <span>🎢 &nbsp; THEME PARK SIMULATOR · DUFAN QUEUE ANALYTICS</span>
    <span>TEKNIK INDUSTRI — SIMULASI SISTEM 2025 &nbsp; © 2025</span>
</div>
""", unsafe_allow_html=True)