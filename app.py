"""
======================================================
  Teachable Machine - Streamlit Frontend (app.py)
  Milestone 4: Premium Dark UX — Optimized & Clean
======================================================
"""

import os
import requests
import streamlit as st

# ─────────────────────────────────────────
#  Configuration
# ─────────────────────────────────────────
API_BASE = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(
    page_title="Teachable Machine",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────
#  Premium Dark UI CSS
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, .main, [data-testid="stAppViewContainer"] {
    background: #09090B !important;
    font-family: 'DM Sans', sans-serif;
    color: #E4E4E7;
}
.main .block-container {
    padding: 2rem 2.5rem 3rem 2.5rem;
    max-width: 1200px;
}
.tm-header {
    display: flex;
    align-items: flex-end;
    gap: 14px;
    margin-bottom: 6px;
}
.tm-logo {
    width: 44px; height: 44px;
    background: linear-gradient(135deg, #6366F1, #8B5CF6);
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 22px; flex-shrink: 0;
    box-shadow: 0 0 20px rgba(99,102,241,0.4);
}
.tm-title {
    font-family: 'Syne', sans-serif;
    font-size: 32px;
    font-weight: 800;
    color: #FAFAFA;
    letter-spacing: -0.03em;
    line-height: 1;
}
.tm-sub {
    font-size: 13px;
    color: #71717A;
    margin-top: 3px;
    font-weight: 300;
}
.badge-on  { background:#052E16; color:#4ADE80; border:1px solid #166534; padding:5px 12px; border-radius:20px; font-size:12px; font-weight:600; display:inline-flex; align-items:center; gap:6px; }
.badge-off { background:#1C0505; color:#F87171; border:1px solid #7F1D1D; padding:5px 12px; border-radius:20px; font-size:12px; font-weight:600; }
.dot-pulse { width:7px; height:7px; background:#4ADE80; border-radius:50%; display:inline-block; animation: pulse 2s infinite; }
@keyframes pulse { 0%,100%{opacity:1;} 50%{opacity:0.3;} }

.tm-div { height:1px; background:linear-gradient(90deg,#27272A,transparent); margin:1.5rem 0; }

.step-card {
    background: #18181B;
    border: 1px solid #27272A;
    border-radius: 16px;
    padding: 1.4rem 1.5rem;
    margin-bottom: 1rem;
}
.step-label {
    font-family: 'Syne', sans-serif;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.1em;
    color: #6366F1;
    text-transform: uppercase;
    margin-bottom: 4px;
}
.step-title {
    font-family: 'Syne', sans-serif;
    font-size: 18px;
    font-weight: 700;
    color: #FAFAFA;
}
.class-chip {
    background: #1C1C1F;
    border: 1px solid #2E2E32;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    text-align: center;
}
.class-name { font-family:'Syne',sans-serif; font-size:16px; font-weight:700; color:#FAFAFA; }
.class-count { font-size:12px; color:#6366F1; font-weight:500; margin-top:2px; }

.train-success {
    background: linear-gradient(135deg, #0C1A2E, #0F2A1E);
    border: 1px solid #1D4ED8;
    border-left: 4px solid #6366F1;
    border-radius: 12px;
    padding: 1.1rem 1.3rem;
    color: #93C5FD;
    font-size: 14px;
}
.locked-box {
    background: #111113;
    border: 1px dashed #27272A;
    border-radius: 14px;
    padding: 2.5rem;
    text-align: center;
    color: #52525B;
    font-size: 14px;
}
.pred-card {
    background: linear-gradient(135deg, #1E1B4B, #1C1C2E);
    border: 1px solid #4338CA;
    border-radius: 14px;
    padding: 1.3rem 1.5rem;
    margin-bottom: 1rem;
}
.pred-label { font-size:11px; font-weight:700; color:#818CF8; letter-spacing:0.08em; text-transform:uppercase; }
.pred-class { font-family:'Syne',sans-serif; font-size:26px; font-weight:800; color:#EEF2FF; margin:2px 0; }
.pred-conf  { font-size:14px; color:#A5B4FC; font-weight:500; }

.stProgress > div > div > div > div { background: linear-gradient(90deg, #6366F1, #8B5CF6) !important; border-radius: 4px !important; }
.stProgress > div > div > div { background: #27272A !important; border-radius: 4px !important; }

.stButton > button {
    background: linear-gradient(135deg, #6366F1, #8B5CF6) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    padding: 0.55rem 1.2rem !important;
    box-shadow: 0 4px 14px rgba(99,102,241,0.35) !important;
}
.stTextInput input, .stSelectbox select { background: #18181B !important; border: 1px solid #3F3F46 !important; border-radius: 8px !important; color: #E4E4E7 !important; }
div[data-testid="stExpander"] { background: #18181B !important; border: 1px solid #27272A !important; border-radius: 14px !important; }
[data-testid="stFileUploader"] { background: #111113 !important; border: 1px dashed #3F3F46 !important; border-radius: 10px !important; }
.stRadio label { color: #A1A1AA !important; font-size: 14px !important; }
.stRadio [data-testid="stWidgetLabel"] { color: #71717A !important; font-size:12px !important; }

.stSuccess { background:#052E16 !important; border:1px solid #166534 !important; color:#4ADE80 !important; border-radius:10px !important; }
.stWarning { background:#1C1200 !important; border:1px solid #854D0E !important; color:#FCD34D !important; border-radius:10px !important; }
.stError   { background:#1C0505 !important; border:1px solid #7F1D1D !important; color:#F87171 !important; border-radius:10px !important; }
.stInfo    { background:#0C1A2E !important; border:1px solid #1D4ED8 !important; color:#93C5FD !important; border-radius:10px !important; }

section[data-testid="stSidebar"] { background: #09090B !important; border-right: 1px solid #18181B !important; }
section[data-testid="stSidebar"] * { color: #A1A1AA !important; }
section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3, section[data-testid="stSidebar"] strong { color: #FAFAFA !important; }

[data-testid="stMetric"] { background:#18181B; border:1px solid #27272A; border-radius:12px; padding:0.8rem 1rem; }
[data-testid="stMetricLabel"] { color:#71717A !important; font-size:12px !important; }
[data-testid="stMetricValue"] { color:#FAFAFA !important; font-family:'Syne',sans-serif !important; }
[data-testid="stMetricDelta"] { color:#4ADE80 !important; }
[data-testid="stVegaLiteChart"] { background:transparent !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
#  API Service Helpers
# ─────────────────────────────────────────
def api_get_classes() -> dict:
    res = requests.get(f"{API_BASE}/classes", timeout=10)
    res.raise_for_status()
    return res.json()

def api_upload_images(cls_name: str, files: list) -> dict:
    file_tuples = [("files", (f.name, f.getvalue(), f.type or "image/jpeg")) for f in files]
    res = requests.post(f"{API_BASE}/upload-sample", data={"class_name": cls_name}, files=file_tuples, timeout=60)
    res.raise_for_status()
    return res.json()

def api_train() -> dict:
    res = requests.post(f"{API_BASE}/train", timeout=120)
    res.raise_for_status()
    return res.json()

def api_predict(img_bytes: bytes, fname: str = "image.jpg") -> dict:
    res = requests.post(f"{API_BASE}/predict", files={"file": (fname, img_bytes, "image/jpeg")}, timeout=30)
    res.raise_for_status()
    return res.json()


# ─────────────────────────────────────────
#  Header & System Status
# ─────────────────────────────────────────
hcol1, hcol2 = st.columns([5, 1])
with hcol1:
    st.markdown("""
    <div class="tm-header">
        <div class="tm-logo">🧠</div>
        <div>
            <div class="tm-title">Teachable Machine</div>
            <div class="tm-sub">Train your own image classifier instantly</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with hcol2:
    st.write("")
    try:
        health = requests.get(f"{API_BASE}/", timeout=3)
        if health.status_code == 200:
            st.markdown('<div class="badge-on"><span class="dot-pulse"></span> ONLINE</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="badge-off">⚠ ERROR</div>', unsafe_allow_html=True)
    except requests.exceptions.ConnectionError:
        if "localhost" not in API_BASE:
            try:
                health = requests.get("http://localhost:8000/", timeout=2)
                if health.status_code == 200:
                    st.markdown('<div class="badge-on"><span class="dot-pulse"></span> LOCAL</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="badge-off">❌ OFFLINE</div>', unsafe_allow_html=True)
                    st.stop()
            except Exception:
                st.markdown('<div class="badge-off">❌ OFFLINE</div>', unsafe_allow_html=True)
                st.stop()
        else:
            st.markdown('<div class="badge-off">❌ OFFLINE</div>', unsafe_allow_html=True)
            st.error("Backend Server is not running.")
            st.stop()

st.markdown('<div class="tm-div"></div>', unsafe_allow_html=True)


# ─────────────────────────────────────────
#  Session State Layer
# ─────────────────────────────────────────
is_trained = False
trained_classes = []
summary_data = {}

try:
    state = api_get_classes()
    is_trained = state.get("model_trained", False)
    trained_classes = list(state.get("classes", {}).keys())
    if is_trained:
        summary_data = {"classes": trained_classes, "total_samples": sum(state.get("classes", {}).values())}
except Exception:
    pass

if "model_trained"    not in st.session_state: st.session_state.model_trained = is_trained
if "trained_classes"  not in st.session_state: st.session_state.trained_classes = trained_classes
if "training_summary" not in st.session_state: st.session_state.training_summary = summary_data

if is_trained:
    st.session_state.model_trained = True
    st.session_state.trained_classes = trained_classes
    if not st.session_state.training_summary:
        st.session_state.training_summary = summary_data


# ═══════════════════════════════════════════════════════════════
#  STEP 1 — Dataset Collection
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div class="step-card">
    <div class="step-label">Step 01</div>
    <div class="step-title">📂 Add Training Images</div>
</div>
""", unsafe_allow_html=True)

try:
    current_classes = api_get_classes().get("classes", {})
except Exception:
    current_classes = {}

if current_classes:
    cols = st.columns(len(current_classes))
    for idx, (name, count) in enumerate(current_classes.items()):
        with cols[idx]:
            st.markdown(f"""
            <div class="class-chip">
                <div class="class-name">{name}</div>
                <div class="class-count">{'✅' if count > 0 else '⚠️'} {count} images</div>
            </div>
            """, unsafe_allow_html=True)
    st.write("")

with st.expander("➕ Collect Images", expanded=True):
    col1, col2 = st.columns([1, 2])

    with col1:
        cls_name = st.text_input("Class Label", placeholder="e.g., cat, dog")
        source_mode = st.radio("Source", ["📁 Upload Files", "📷 Use Webcam"])

    with col2:
        img_list = []
        if "Upload" in source_mode:
            uploaded = st.file_uploader("Choose files", type=["jpg", "jpeg", "png", "webp"], accept_multiple_files=True, label_visibility="collapsed")
            if uploaded:
                img_list = list(uploaded)
        else:
            shot = st.camera_input("Capture", label_visibility="collapsed")
            if shot:
                img_list.append(shot)

        if img_list:
            st.caption(f"Ready: {len(img_list)} image(s)")
            thumbs = st.columns(min(len(img_list), 6))
            for i, f in enumerate(img_list[:6]):
                with thumbs[i]:
                    st.image(f, use_container_width=True)

    if st.button("⬆️ Upload to Server", use_container_width=True):
        if not cls_name.strip():
            st.warning("⚠️ Enter a class name.")
        elif not img_list:
            st.warning("⚠️ Select or capture images first.")
        else:
            with st.spinner("Uploading..."):
                try:
                    res = api_upload_images(cls_name.strip(), img_list)
                    st.success(f"✅ Saved {res['saved']} images to '{res['class']}'")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Failed: {str(e)}")

st.markdown('<div class="tm-div"></div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  STEP 2 — Training
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div class="step-card">
    <div class="step-label">Step 02</div>
    <div class="step-title">🏋️ Train Model</div>
</div>
""", unsafe_allow_html=True)

st.info("Upload images for at least **2 classes**, then click Train.", icon="ℹ️")

t_col1, t_col2 = st.columns([1, 2])

with t_col1:
    if st.button("🚀 Train Model", use_container_width=True, type="primary"):
        with st.spinner("Training... Please wait ☕"):
            try:
                res = api_train()
                st.session_state.model_trained = True
                st.session_state.trained_classes = res.get("classes", [])
                st.session_state.training_summary = res
                st.rerun()
            except Exception as e:
                st.error(f"❌ Training failed: {str(e)}")
                st.session_state.model_trained = False

with t_col2:
    if st.session_state.model_trained and st.session_state.training_summary:
        summary = st.session_state.training_summary
        st.markdown(f"""
        <div class="train-success">
            🏆 <b>Model Ready!</b> Trained on <b>{summary.get('total_samples','?')} images</b> 
            across: <code>{', '.join(summary.get('classes', []))}</code>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<div class="tm-div"></div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  STEP 3 — Prediction
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div class="step-card">
    <div class="step-label">Step 03</div>
    <div class="step-title">🔍 Test Model</div>
</div>
""", unsafe_allow_html=True)

if not st.session_state.model_trained and not is_trained:
    st.markdown("""
    <div class="locked-box">
        🔒 Complete Step 2 (Train Model) to unlock classification tools.
    </div>
    """, unsafe_allow_html=True)
else:
    st.success(f"Active Model: **{', '.join(st.session_state.trained_classes)}**", icon="🎯")
    p_left, p_right = st.columns([1, 1])

    with p_left:
        test_mode = st.radio("Input Method", ["📁 Upload Image", "📷 Webcam Feed"], horizontal=True)
        img_bytes = None
        fname = "image.jpg"

        if "Upload" in test_mode:
            test_f = st.file_uploader("Test image", type=["jpg", "jpeg", "png", "webp"], key="pred_up", label_visibility="collapsed")
            if test_f:
                img_bytes = test_f.getvalue()
                fname = test_f.name
                st.image(test_f, caption="Test Target", width=250)
        else:
            test_cam = st.camera_input("Capture", key="pred_cam", label_visibility="collapsed")
            if test_cam:
                img_bytes = test_cam.getvalue()
                fname = "webcam_test.jpg"
                st.image(test_cam, caption="Captured Frame", width=250)

        run_predict = st.button("🔮 Predict", use_container_width=True, type="primary")

    with p_right:
        if run_predict:
            if img_bytes is None:
                st.warning("⚠️ Please input an image first.")
            else:
                with st.spinner("Analyzing..."):
                    try:
                        res = api_predict(img_bytes, fname)
                        pred = res["predicted_class"]
                        conf = res["confidence"]
                        scores = res["all_scores"]

                        st.markdown(f"""
                        <div class="pred-card">
                            <div class="pred-label">Prediction</div>
                            <div class="pred-class">🏷️ {pred.upper()}</div>
                            <div class="pred-conf">Confidence: {conf:.1f}%</div>
                        </div>
                        """, unsafe_allow_html=True)

                        st.markdown("**Confidence Scores:**")
                        for cls, val in sorted(scores.items(), key=lambda x: -x[1]):
                            c1, c2 = st.columns([3, 1])
                            with c1: st.progress(int(val) / 100, text=cls)
                            with c2: st.markdown(f"**{val:.1f}%**")

                        st.bar_chart(data=scores, height=180, color="#6366F1")
                    except Exception as e:
                        st.error(f"❌ Prediction failed: {str(e)}")
        else:
            st.markdown("""
            <div style="border:1px dashed #27272A; border-radius:14px; min-height:240px; 
                        display:flex; align-items:center; justify-content:center; padding:2rem; text-align:center;">
                <p style="color:#3F3F46; font-size:14px;">
                    📊 Prediction analysis outputs will render here.
                </p>
            </div>
            """, unsafe_allow_html=True)


# ─────────────────────────────────────────
#  Sidebar Layout
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📋 Guidelines")
    st.markdown("""
    **1. Ingest Data**
    - Name your class label.
    - Add at least **2 separate classes**.
    
    **2. Training**
    - Compile with **Train Model**.
    
    **3. Inference**
    - Upload/Capture test images to evaluate.
    """)
    st.divider()
    st.markdown("### 🔧 Server Status")
    try:
        diag = api_get_classes()
        cls_map = diag.get("classes", {})
        st.markdown(f"**Total Classes:** {len(cls_map)}")
        for k, v in cls_map.items():
            st.markdown(f"- `{k}`: {v} samples")
        st.markdown(f"**Status:** {'Ready' if diag.get('model_trained', False) else 'Untrained'}")
    except Exception:
        st.caption("Unable to fetch server metrics.")
    st.divider()
    st.caption("Streamlit + FastAPI + MobileNetV3")