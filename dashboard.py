"""
API Tehdit Tespit Sistemi — Streamlit Canlı Dashboard (Professional UI)
Öğrenci: Mohammad Juma Amiri | 20260819001
Çalıştır: streamlit run dashboard_pro.py
"""

import random
import requests
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

API_BASE = "http://127.0.0.1:8001"

st.set_page_config(
    page_title="API Tehdit Tespit Sistemi",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ────────────────────────────────────────────────────────────────────
# THEME / CSS
# ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    :root {
        --bg: #0b1020;
        --panel: rgba(18, 24, 38, 0.82);
        --panel-2: rgba(15, 21, 34, 0.92);
        --card-border: rgba(255,255,255,0.08);
        --text: #edf2f7;
        --muted: #97a3b6;
        --accent: #55c2ff;
        --green: #22c55e;
        --red: #ef4444;
        --amber: #f59e0b;
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(85,194,255,0.10), transparent 26%),
            radial-gradient(circle at top right, rgba(239,68,68,0.08), transparent 22%),
            linear-gradient(180deg, #08101d 0%, #0b1020 100%);
        color: var(--text);
    }

    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 1rem;
        max-width: 1450px;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(10,15,28,0.98), rgba(15,21,34,0.98));
        border-right: 1px solid rgba(255,255,255,0.06);
    }

    .top-banner {
        background: linear-gradient(135deg, rgba(22,33,56,0.95), rgba(13,20,35,0.95));
        border: 1px solid var(--card-border);
        border-radius: 22px;
        padding: 1.35rem 1.4rem;
        margin-bottom: 1rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.25);
    }

    .top-title {
        font-size: 1.8rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
        letter-spacing: 0.2px;
    }

    .top-subtitle {
        color: var(--muted);
        font-size: 0.97rem;
    }

    .status-chip {
        display: inline-block;
        padding: 0.35rem 0.75rem;
        border-radius: 999px;
        font-size: 0.82rem;
        font-weight: 700;
        border: 1px solid rgba(255,255,255,0.08);
        margin-top: 0.85rem;
        background: rgba(255,255,255,0.04);
    }

    .status-up { color: #86efac; background: rgba(34,197,94,0.12); }
    .status-down { color: #fca5a5; background: rgba(239,68,68,0.12); }

    .metric-card {
        background: linear-gradient(180deg, rgba(17,24,39,0.92), rgba(13,18,31,0.95));
        border: 1px solid var(--card-border);
        border-radius: 20px;
        padding: 1rem 1rem 0.9rem 1rem;
        min-height: 126px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.18);
    }

    .metric-label {
        color: var(--muted);
        font-size: 0.88rem;
        margin-bottom: 0.55rem;
        font-weight: 600;
    }

    .metric-value {
        font-size: 2rem;
        line-height: 1;
        font-weight: 800;
        margin-bottom: 0.55rem;
    }

    .metric-foot {
        display: inline-block;
        font-size: 0.82rem;
        color: #dbeafe;
        background: rgba(85,194,255,0.10);
        border: 1px solid rgba(85,194,255,0.15);
        border-radius: 999px;
        padding: 0.24rem 0.62rem;
    }

    .panel {
        background: linear-gradient(180deg, rgba(17,24,39,0.92), rgba(12,18,31,0.96));
        border: 1px solid var(--card-border);
        border-radius: 22px;
        padding: 1rem 1rem 0.75rem 1rem;
        box-shadow: 0 10px 28px rgba(0,0,0,0.18);
        height: 100%;
    }

    .section-title {
        font-size: 1.02rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }

    .section-subtitle {
        color: var(--muted);
        font-size: 0.84rem;
        margin-bottom: 0.65rem;
    }

    .alert-item {
        background: linear-gradient(90deg, rgba(127,29,29,0.36), rgba(69,10,10,0.18));
        border: 1px solid rgba(239,68,68,0.16);
        border-left: 4px solid rgba(239,68,68,0.95);
        border-radius: 14px;
        padding: 0.8rem 0.95rem;
        margin-bottom: 0.7rem;
    }

    .alert-top {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        margin-bottom: 0.35rem;
        font-weight: 700;
    }

    .alert-meta {
        color: var(--muted);
        font-size: 0.84rem;
        line-height: 1.55;
    }

    .pill-green, .pill-red, .pill-blue, .pill-amber {
        display:inline-block;
        padding: 0.24rem 0.62rem;
        border-radius:999px;
        font-size:0.78rem;
        font-weight:700;
        border:1px solid transparent;
    }

    .pill-green { background: rgba(34,197,94,0.14); color: #86efac; border-color: rgba(34,197,94,0.2); }
    .pill-red { background: rgba(239,68,68,0.14); color: #fca5a5; border-color: rgba(239,68,68,0.2); }
    .pill-blue { background: rgba(59,130,246,0.14); color: #bfdbfe; border-color: rgba(59,130,246,0.2); }
    .pill-amber { background: rgba(245,158,11,0.14); color: #fde68a; border-color: rgba(245,158,11,0.2); }

    div[data-testid="stMetric"] {
        background: transparent !important;
        border: none !important;
    }

    div[data-testid="stDataFrame"] {
        border-radius: 16px;
        overflow: hidden;
    }

    .stButton>button {
        border-radius: 12px;
        font-weight: 700;
        border: 1px solid rgba(255,255,255,0.08);
    }

    .stTextInput>div>div>input,
    .stTextArea textarea,
    .stNumberInput input,
    div[data-baseweb="select"] > div {
        border-radius: 12px !important;
    }
</style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────────────────────────
# DEMO PAYLOADS
# ────────────────────────────────────────────────────────────────────
NORMAL_REQUESTS = [
    {"ip_address": "192.168.1.10", "endpoint": "/api/products", "http_method": "GET",
     "status_code": 200, "user_agent": "Mozilla/5.0 Chrome/121", "response_time_ms": 145, "payload": None},
    {"ip_address": "10.0.0.5", "endpoint": "/api/cart", "http_method": "POST",
     "status_code": 201, "user_agent": "Mozilla/5.0 Safari/17", "response_time_ms": 230, "payload": '{"item_id":42}'},
    {"ip_address": "172.16.0.22", "endpoint": "/api/profile", "http_method": "GET",
     "status_code": 200, "user_agent": "Mozilla/5.0 Firefox/122", "response_time_ms": 98, "payload": None},
    {"ip_address": "192.168.1.55", "endpoint": "/api/search", "http_method": "GET",
     "status_code": 200, "user_agent": "Mozilla/5.0 Chrome/121", "response_time_ms": 312, "payload": None},
]

ATTACK_REQUESTS = [
    {"ip_address": "45.33.32.156", "endpoint": "/api/login", "http_method": "POST",
     "status_code": 401, "user_agent": "sqlmap/1.7",
     "response_time_ms": 52,
     "payload": "username=admin' OR 1=1 --&password=x"},
    {"ip_address": "198.51.100.5", "endpoint": "/api/admin", "http_method": "DELETE",
     "status_code": 403, "user_agent": "python-requests/2.31",
     "response_time_ms": 35,
     "payload": "DROP TABLE users; --"},
    {"ip_address": "203.0.113.88", "endpoint": "/api/payment", "http_method": "PUT",
     "status_code": 500, "user_agent": "nikto/2.1.6",
     "response_time_ms": 6200,
     "payload": "<script>alert('XSS')</script>"},
    {"ip_address": "45.33.32.200", "endpoint": "/api/token", "http_method": "POST",
     "status_code": 401, "user_agent": "go-http-client/1.1",
     "response_time_ms": 44,
     "payload": "reused_token=eyJhbGc..."},
]

# ────────────────────────────────────────────────────────────────────
# HELPERS
# ────────────────────────────────────────────────────────────────────
def send_request(payload: dict):
    try:
        r = requests.post(f"{API_BASE}/analyze", json=payload, timeout=5)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e)}

def fetch_log():
    try:
        r = requests.get(f"{API_BASE}/log", timeout=5)
        r.raise_for_status()
        return r.json()
    except Exception:
        return []

def fetch_stats():
    try:
        r = requests.get(f"{API_BASE}/stats", timeout=5)
        r.raise_for_status()
        return r.json()
    except Exception:
        return {}

def backend_ok():
    try:
        r = requests.get(f"{API_BASE}/health", timeout=3)
        return r.status_code == 200
    except Exception:
        return False

def reset_dashboard_data():
    endpoints = [
        ("POST", f"{API_BASE}/reset"),
        ("POST", f"{API_BASE}/clear"),
        ("DELETE", f"{API_BASE}/log"),
        ("POST", f"{API_BASE}/log/reset"),
    ]
    for method, url in endpoints:
        try:
            if method == "POST":
                r = requests.post(url, timeout=5)
            else:
                r = requests.delete(url, timeout=5)
            if r.status_code in (200, 204):
                return True, "Kayıtlar sıfırlandı."
        except Exception:
            pass
    return False, "Backend tarafında reset endpoint'i bulunamadı."

def metric_card(label, value, foot, accent="blue"):
    foot_class = {
        "blue": "pill-blue",
        "green": "pill-green",
        "red": "pill-red",
        "amber": "pill-amber",
    }.get(accent, "pill-blue")

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <span class="{foot_class}">{foot}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

def normalize_label_value(value):
    if isinstance(value, str):
        v = value.strip().lower()
        if v in ["tehdit", "threat", "attack", "malicious", "1"]:
            return 1
        return 0
    try:
        return int(value)
    except Exception:
        return 0

# ────────────────────────────────────────────────────────────────────
# SIDEBAR
# ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🛡️ Kontrol Merkezi")
    st.caption("Canlı trafik simülasyonu ve model testi")

    if backend_ok():
        st.markdown('<div class="status-chip status-up">● Backend aktif</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-chip status-down">● Backend pasif</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Demo Gönderimi")

    if st.button("✅ Normal İstek Gönder", use_container_width=True):
        req = random.choice(NORMAL_REQUESTS)
        result = send_request(req)
        if "error" in result:
            st.error(result.get("error", "İstek gönderilemedi"))
        else:
            label_bin = result.get("label_binary", normalize_label_value(result.get("label", 0)))
            if label_bin == 0:
                st.success(f"Normal trafik — Güven: {float(result.get('confidence', 0)):.0%}")
            else:
                st.error(f"Tehdit: {result.get('attack_type', 'Bilinmiyor')}")

    if st.button("🚨 Saldırı İsteği Gönder", use_container_width=True, type="primary"):
        req = random.choice(ATTACK_REQUESTS)
        result = send_request(req)
        if "error" in result:
            st.error(result.get("error", "İstek gönderilemedi"))
        else:
            label_bin = result.get("label_binary", normalize_label_value(result.get("label", 0)))
            if label_bin == 1:
                st.error(f"{result.get('attack_type', 'Tehdit')} — Güven: {float(result.get('confidence', 0)):.0%}")
            else:
                st.warning("Model bu saldırıyı normal olarak gördü.")

    if st.button("🧹 Verileri Sıfırla / Reset", use_container_width=True):
        ok, msg = reset_dashboard_data()
        if ok:
            st.success(msg)
            st.rerun()
        else:
            st.warning(msg)

    st.markdown("---")
    with st.expander("🧪 Manuel İstek Oluştur", expanded=False):
        custom_ip = st.text_input("IP Adresi", "192.168.1.1")
        custom_ep = st.selectbox("Endpoint", ["/api/login", "/api/admin", "/api/payment",
                                              "/api/products", "/api/search", "/api/users"])
        custom_method = st.selectbox("HTTP Method", ["GET", "POST", "PUT", "PATCH", "DELETE"])
        custom_status = st.number_input("Status Code", value=200, step=1)
        custom_ua = st.text_input("User Agent", "Mozilla/5.0")
        custom_rt = st.number_input("Response Time (ms)", value=200.0, step=10.0)
        custom_payload = st.text_area("Payload", "")
        if st.button("Gönder", use_container_width=True):
            result = send_request({
                "ip_address": custom_ip,
                "endpoint": custom_ep,
                "http_method": custom_method,
                "status_code": int(custom_status),
                "user_agent": custom_ua,
                "response_time_ms": float(custom_rt),
                "payload": custom_payload or None
            })
            st.json(result)

    st.markdown("---")
    auto_refresh = st.checkbox("Otomatik yenile (5 sn)", value=False)
    if auto_refresh:
        st_autorefresh(interval=5000, key="dashboard_refresh")

# ────────────────────────────────────────────────────────────────────
# DATA
# ────────────────────────────────────────────────────────────────────
stats = fetch_stats()
log = fetch_log()

df = pd.DataFrame(log) if log else pd.DataFrame()
if not df.empty:
    df["timestamp"] = pd.to_datetime(df.get("timestamp"), errors="coerce")
    df["idx"] = range(1, len(df) + 1)
    df["confidence"] = pd.to_numeric(df.get("confidence", 0), errors="coerce").fillna(0)
    df["latency_ms"] = pd.to_numeric(df.get("latency_ms", 0), errors="coerce").fillna(0)
    df["status"] = pd.to_numeric(df.get("status", 0), errors="coerce").fillna(0)

    if "label_binary" in df.columns:
        df["label_bin"] = pd.to_numeric(df["label_binary"], errors="coerce").fillna(0).astype(int)
    else:
        df["label_bin"] = df.get("label", 0).apply(normalize_label_value)

    if "label" not in df.columns:
        df["label"] = df["label_bin"].map({0: "Normal", 1: "Tehdit"})
    else:
        df["label"] = df["label"].astype(str)

# ────────────────────────────────────────────────────────────────────
# HEADER
# ────────────────────────────────────────────────────────────────────
backend_label = "Sistem aktif ve veri alıyor" if backend_ok() else "Backend bağlantısı bekleniyor"
status_html = "status-up" if backend_ok() else "status-down"

st.markdown(
    f"""
    <div class="top-banner">
        <div class="top-title">🛡️ API Tehdit Tespit Sistemi</div>
        <div class="top-subtitle">
            Makine Öğrenmesi ile gerçek zamanlı API / HTTP davranış analizi, tehdit sınıflandırma ve canlı izleme paneli
        </div>
        <div class="status-chip {status_html}">{backend_label}</div>
    </div>
    """,
    unsafe_allow_html=True
)

# ────────────────────────────────────────────────────────────────────
# KPIs
# ────────────────────────────────────────────────────────────────────
total = int(stats.get("total", len(df) if not df.empty else 0))
normal = int(stats.get("normal", int((df["label_bin"] == 0).sum()) if not df.empty else 0))
threats = int(stats.get("threats", int((df["label_bin"] == 1).sum()) if not df.empty else 0))
threat_rate = float(stats.get("threat_rate", (threats / total * 100) if total else 0))

avg_latency = float(df["latency_ms"].mean()) if not df.empty else 0.0

k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    metric_card("Toplam İstek", f"{total:,}".replace(",", "."), "Genel trafik", "blue")
with k2:
    metric_card("Normal Trafik", f"{normal:,}".replace(",", "."), "Temiz akış", "green")
with k3:
    metric_card("Tehdit Sayısı", f"{threats:,}".replace(",", "."), "Anomali kayıtları", "red")
with k4:
    metric_card("Tehdit Oranı", f"%{threat_rate:.1f}", "Risk seviyesi", "amber")
with k5:
    metric_card("Ort. Gecikme", f"{avg_latency:.0f} ms", "Servis yanıtı", "blue")

st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

# ────────────────────────────────────────────────────────────────────
# CHARTS ROW 1
# ────────────────────────────────────────────────────────────────────
left, mid, right = st.columns([2.1, 1.15, 1.15])

with left:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Trafik Akışı ve Güven Dağılımı</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Son isteklerin model güven skorları ve tehdit işaretleri</div>', unsafe_allow_html=True)

    if not df.empty:
        fig = go.Figure()

        normal_df = df[df["label_bin"] == 0]
        threat_df = df[df["label_bin"] == 1]

        fig.add_trace(go.Scatter(
            x=df["idx"], y=df["confidence"],
            mode="lines",
            name="Güven Skoru",
            line=dict(color="#55c2ff", width=2.5),
            fill="tozeroy",
            fillcolor="rgba(85,194,255,0.08)",
            hovertemplate="İstek #%{x}<br>Güven: %{y:.2f}<extra></extra>"
        ))

        if not normal_df.empty:
            fig.add_trace(go.Scatter(
                x=normal_df["idx"], y=normal_df["confidence"],
                mode="markers",
                name="Normal",
                marker=dict(color="#22c55e", size=8, line=dict(width=0)),
                hovertemplate="Normal<br>İstek #%{x}<br>Güven: %{y:.2f}<extra></extra>"
            ))

        if not threat_df.empty:
            fig.add_trace(go.Scatter(
                x=threat_df["idx"], y=threat_df["confidence"],
                mode="markers",
                name="Tehdit",
                marker=dict(color="#ef4444", size=11, symbol="diamond"),
                hovertemplate="Tehdit<br>İstek #%{x}<br>Güven: %{y:.2f}<extra></extra>"
            ))

        threshold_value = float(stats.get("threshold", 0.5))
        fig.add_hline(y=threshold_value, line_dash="dash", line_color="rgba(255,255,255,0.30)")

        fig.update_layout(
            height=350,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=10, b=10),
            font=dict(color="#edf2f7"),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor="rgba(0,0,0,0)"
            ),
            xaxis=dict(title="İstek Sırası", gridcolor="rgba(255,255,255,0.06)", zeroline=False),
            yaxis=dict(title="Güven Skoru", range=[0, 1], gridcolor="rgba(255,255,255,0.06)", zeroline=False),
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Grafik için henüz veri yok.")
    st.markdown('</div>', unsafe_allow_html=True)

with mid:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Trafik Kompozisyonu</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Normal ve tehdit oranlarının dağılımı</div>', unsafe_allow_html=True)

    fig_donut = go.Figure(go.Pie(
        labels=["Normal", "Tehdit"],
        values=[max(normal, 0), max(threats, 0)],
        hole=0.68,
        textinfo="label+percent",
        textfont=dict(color="#edf2f7", size=13),
        marker=dict(colors=["#22c55e", "#ef4444"], line=dict(color="rgba(255,255,255,0.06)", width=1))
    ))
    fig_donut.update_layout(
        height=350,
        margin=dict(l=10, r=10, t=15, b=10),
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        annotations=[dict(text=f"<b>{total}</b><br>Toplam", x=0.5, y=0.5, showarrow=False, font=dict(size=18, color="#edf2f7"))]
    )
    st.plotly_chart(fig_donut, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Model Risk Göstergesi</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Tehdit oranına göre canlı risk seviyesi</div>', unsafe_allow_html=True)

    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=threat_rate,
        number={'suffix': "%", 'font': {'size': 34, 'color': "#edf2f7"}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': "rgba(255,255,255,0.4)"},
            'bar': {'color': "#55c2ff"},
            'bgcolor': "rgba(255,255,255,0.03)",
            'borderwidth': 0,
            'steps': [
                {'range': [0, 25], 'color': "rgba(34,197,94,0.28)"},
                {'range': [25, 60], 'color': "rgba(245,158,11,0.24)"},
                {'range': [60, 100], 'color': "rgba(239,68,68,0.24)"},
            ],
        }
    ))
    gauge.update_layout(
        height=350,
        margin=dict(l=15, r=15, t=35, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#edf2f7")
    )
    st.plotly_chart(gauge, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

# ────────────────────────────────────────────────────────────────────
# CHARTS ROW 2
# ────────────────────────────────────────────────────────────────────
b1, b2 = st.columns([1.15, 1.85])

with b1:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">HTTP Method Dağılımı</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">İsteklerin metoda göre yoğunluğu</div>', unsafe_allow_html=True)

    if not df.empty and "method" in df.columns:
        method_counts = df["method"].fillna("N/A").value_counts().sort_values(ascending=True)
        fig_bar = go.Figure(go.Bar(
            x=method_counts.values,
            y=method_counts.index,
            orientation="h",
            text=method_counts.values,
            textposition="outside",
            marker=dict(
                color=method_counts.values,
                colorscale=[[0, "#274c77"], [1, "#55c2ff"]],
                line=dict(width=0)
            ),
            hovertemplate="%{y}: %{x}<extra></extra>"
        ))
        fig_bar.update_layout(
            height=320,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=5, b=10),
            font=dict(color="#edf2f7"),
            xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)", title="Adet"),
            yaxis=dict(showgrid=False, title="")
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("Method verisi yok.")
    st.markdown('</div>', unsafe_allow_html=True)

with b2:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">En Çok Hedeflenen Endpointler</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Son kayıtlarda en sık görülen API yolları</div>', unsafe_allow_html=True)

    if not df.empty and "endpoint" in df.columns:
        endpoint_counts = df["endpoint"].fillna("N/A").value_counts().head(8)
        fig_end = go.Figure(go.Bar(
            x=endpoint_counts.index,
            y=endpoint_counts.values,
            text=endpoint_counts.values,
            textposition="outside",
            marker=dict(color="#55c2ff"),
            hovertemplate="%{x}<br>Adet: %{y}<extra></extra>"
        ))
        fig_end.update_layout(
            height=320,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=5, b=10),
            font=dict(color="#edf2f7"),
            xaxis=dict(title="", tickangle=-25, showgrid=False),
            yaxis=dict(title="İstek Sayısı", gridcolor="rgba(255,255,255,0.06)")
        )
        st.plotly_chart(fig_end, use_container_width=True)
    else:
        st.info("Endpoint verisi yok.")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

# ────────────────────────────────────────────────────────────────────
# ALERTS + TABLE
# ────────────────────────────────────────────────────────────────────
a1, a2 = st.columns([1.1, 1.9])

with a1:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Son Tehdit Uyarıları</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">En güncel 8 saldırı kaydı</div>', unsafe_allow_html=True)

    if not df.empty:
        threats_only = df[df["label_bin"] == 1].tail(8).iloc[::-1]
        if threats_only.empty:
            st.success("Aktif tehdit görünmüyor.")
        else:
            for _, row in threats_only.iterrows():
                ts = row["timestamp"].strftime("%Y-%m-%d %H:%M:%S") if pd.notna(row["timestamp"]) else "-"
                attack = row.get("attack_type", "Tehdit")
                ip = row.get("ip", "-")
                endpoint = row.get("endpoint", "-")
                method = row.get("method", "-")
                conf = float(row.get("confidence", 0)) * 100

                st.markdown(
                    f"""
                    <div class="alert-item">
                        <div class="alert-top">
                            <span>🚨 {attack}</span>
                            <span class="pill-red">%{conf:.0f} güven</span>
                        </div>
                        <div class="alert-meta">
                            <b>IP:</b> {ip}<br>
                            <b>Endpoint:</b> {endpoint} &nbsp; <b>Method:</b> {method}<br>
                            <b>Zaman:</b> {ts}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    else:
        st.info("Henüz kayıt oluşmadı.")
    st.markdown('</div>', unsafe_allow_html=True)

with a2:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Detaylı Trafik Tablosu</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Tüm kayıtları filtrelenebilir tablo halinde inceleyin</div>', unsafe_allow_html=True)

    if not df.empty:
        display_cols = [
            "timestamp", "ip", "endpoint", "method", "status",
            "label", "confidence", "threat_probability", "attack_type",
            "latency_ms", "threshold"
        ]
        available_cols = [c for c in display_cols if c in df.columns]
        df_show = df[available_cols].copy().iloc[::-1]

        if "confidence" in df_show.columns:
            df_show["confidence"] = (
                pd.to_numeric(df_show["confidence"], errors="coerce").fillna(0) * 100
            ).round(1).astype(str) + "%"

        if "threat_probability" in df_show.columns:
            df_show["threat_probability"] = (
                pd.to_numeric(df_show["threat_probability"], errors="coerce").fillna(0) * 100
            ).round(1).astype(str) + "%"

        if "timestamp" in df_show.columns:
            df_show["timestamp"] = pd.to_datetime(df_show["timestamp"], errors="coerce").dt.strftime("%Y-%m-%d %H:%M:%S")

        st.dataframe(df_show, use_container_width=True, height=440)
    else:
        st.info("Log tablosu boş.")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
st.caption("Mohammad Juma Amiri · 20260819001 · Makine Öğrenimi 2025–2026 Bahar")