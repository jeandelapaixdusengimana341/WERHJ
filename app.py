import streamlit as st
import pandas as pd
import os
import base64
import json
from PIL import Image
from datetime import datetime

# ============================================================
# FUTURE TECHNOLOGY RWANDA — Redesigned Interface (Streamlit)
# A cleaner, more modern UI with refined typography, spacing,
# stronger visual hierarchy, accessible cards, and polished
# admin tooling. Logic is preserved from the original app.
# ============================================================

st.set_page_config(
    page_title="Future Technology Rwanda",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

IMAGE_DIR = "uploaded_images"
INVENTORY_FILE = "company_inventory.json"
ORDERS_FILE = "company_orders.json"
ADMIN_PASSWORD = "admin123"

os.makedirs(IMAGE_DIR, exist_ok=True)

# ---------- Session bootstrap ----------
st.session_state.setdefault("app_mode", "Portal")
st.session_state.setdefault("shopping_cart", {})
st.session_state.setdefault("theme", "Dark")
st.session_state.setdefault("admin_authed", False)


# ---------- Persistence ----------
def _read_json(path, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Read error ({path}): {e}")
        return default


def _write_json(path, data):
    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        st.error(f"Write error ({path}): {e}")
        return False


def load_inventory():
    return _read_json(INVENTORY_FILE, [])


def save_inventory():
    _write_json(INVENTORY_FILE, st.session_state.company_inventory)


def load_orders():
    return _read_json(ORDERS_FILE, [])


def save_order(new_order):
    orders = load_orders()
    orders.append(new_order)
    return _write_json(ORDERS_FILE, orders)


def save_all_orders(orders_list):
    return _write_json(ORDERS_FILE, orders_list)


st.session_state.setdefault("company_inventory", load_inventory())


def get_base64_image(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""


# ---------- Theme tokens ----------
def theme_tokens(mode: str):
    if mode == "Dark":
        return dict(
            bg="#0B1020",
            surface="#121933",
            surface_2="#1A2347",
            text="#F4F6FB",
            muted="#9AA4C2",
            border="rgba(255,255,255,0.08)",
            accent="#FF6B00",
            accent_2="#FFB347",
            success="#22C55E",
            danger="#EF4444",
            warn="#F59E0B",
            grad="linear-gradient(135deg,#FF6B00 0%,#FF3D81 100%)",
            shadow="0 10px 30px rgba(0,0,0,0.35)",
        )
    return dict(
        bg="#F6F7FB",
        surface="#FFFFFF",
        surface_2="#F0F2F8",
        text="#0B1020",
        muted="#5B6479",
        border="rgba(11,16,32,0.08)",
        accent="#FF6B00",
        accent_2="#E25C00",
        success="#16A34A",
        danger="#DC2626",
        warn="#D97706",
        grad="linear-gradient(135deg,#FF6B00 0%,#FF3D81 100%)",
        shadow="0 10px 24px rgba(15,23,42,0.08)",
    )


# Sidebar theme switch only when inside app
if st.session_state.app_mode != "Portal":
    with st.sidebar:
        st.markdown("### 🇷🇼 FTR Control Room")
        st.session_state.theme = st.radio(
            "Appearance", ["Dark", "Light"],
            horizontal=True,
            index=0 if st.session_state.theme == "Dark" else 1,
        )

T = theme_tokens(st.session_state.theme if st.session_state.app_mode != "Portal" else "Dark")

# ---------- Global CSS ----------
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Space+Grotesk:wght@500;600;700&display=swap');

html, body, [class*="css"], .stApp {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
    background: {T['bg']} !important;
    color: {T['text']} !important;
}}
.block-container {{ padding-top: 1.2rem; padding-bottom: 2rem; max-width: 1280px; }}

/* Top utility ribbon */
.ribbon {{
    display:flex; justify-content:space-between; align-items:center;
    padding: 10px 22px; font-size: .8rem; color:#E5E7F0;
    background: linear-gradient(90deg,#0B1020 0%,#1A2347 100%);
    border-radius: 12px; margin-bottom: 14px; border:1px solid {T['border']};
}}
.ribbon .dot {{ width:6px;height:6px;border-radius:50%;background:#22C55E;display:inline-block;margin-right:6px;box-shadow:0 0 10px #22C55E;}}

/* Navbar */
.navbar {{
    display:flex; justify-content:space-between; align-items:center;
    padding: 16px 22px; background: {T['surface']};
    border:1px solid {T['border']}; border-radius: 16px;
    box-shadow: {T['shadow']}; margin-bottom: 22px;
}}
.brand {{ display:flex; align-items:center; gap:12px; }}
.brand-mark {{
    width:42px;height:42px;border-radius:12px;
    background: {T['grad']}; display:flex;align-items:center;justify-content:center;
    color:white;font-weight:900;font-size:1.2rem;box-shadow:0 6px 18px rgba(255,107,0,.35);
}}
.brand-text .t1 {{ font-family:'Space Grotesk',sans-serif; font-weight:800; font-size:1.05rem; letter-spacing:.4px; color:{T['text']}; }}
.brand-text .t2 {{ font-size:.75rem; color:{T['muted']}; letter-spacing:1.5px; text-transform:uppercase;}}

/* Hero */
.hero {{
    background: {T['surface']};
    border:1px solid {T['border']};
    border-radius: 24px; padding: 42px 38px;
    box-shadow: {T['shadow']}; position:relative; overflow:hidden;
}}
.hero::before {{
    content:""; position:absolute; right:-80px; top:-80px; width:320px; height:320px;
    background: {T['grad']}; filter: blur(80px); opacity:.35; border-radius:50%;
}}
.hero-eyebrow {{
    display:inline-block; padding:6px 12px; border-radius:999px;
    background: rgba(255,107,0,.12); color:{T['accent']};
    font-size:.75rem; font-weight:700; letter-spacing:1.5px; text-transform:uppercase;
    margin-bottom:14px; border:1px solid rgba(255,107,0,.25);
}}
.hero h1 {{
    font-family:'Space Grotesk',sans-serif; font-weight:800;
    font-size: clamp(2rem, 4.5vw, 3.4rem); line-height:1.05;
    margin:0 0 12px 0; color:{T['text']};
}}
.hero h1 .accent {{ background:{T['grad']}; -webkit-background-clip:text; background-clip:text; color:transparent; }}
.hero p {{ color:{T['muted']}; font-size:1.05rem; max-width:680px; margin:0; }}

/* Stat strip */
.stats {{ display:grid; grid-template-columns:repeat(4,1fr); gap:14px; margin-top:22px; }}
.stat {{
    background:{T['surface_2']}; border:1px solid {T['border']}; border-radius:14px;
    padding:14px 16px;
}}
.stat .v {{ font-family:'Space Grotesk',sans-serif; font-weight:700; font-size:1.4rem; color:{T['text']}; }}
.stat .l {{ font-size:.75rem; color:{T['muted']}; text-transform:uppercase; letter-spacing:1.2px; }}

/* Product card */
.card {{
    background: {T['surface']}; border:1px solid {T['border']};
    border-radius:18px; padding:14px; transition: all .25s ease;
    box-shadow: {T['shadow']}; height:100%;
}}
.card:hover {{ transform: translateY(-3px); border-color: rgba(255,107,0,.5); }}
.card .img-wrap {{
    background: {T['surface_2']}; border-radius:12px; overflow:hidden;
    aspect-ratio: 4/3; display:flex; align-items:center; justify-content:center;
    border:1px solid {T['border']};
}}
.card .img-wrap .ph {{ color:{T['muted']}; text-align:center; padding:14px; }}
.card .meta-row {{ display:flex; justify-content:space-between; align-items:center; margin-top:12px; font-size:.72rem; }}
.pill {{ padding:4px 10px; border-radius:999px; font-weight:700; letter-spacing:.4px; }}
.pill.in {{ background: rgba(34,197,94,.12); color:{T['success']}; border:1px solid rgba(34,197,94,.25); }}
.pill.out {{ background: rgba(239,68,68,.12); color:{T['danger']}; border:1px solid rgba(239,68,68,.25); }}
.pill.cat {{ background:{T['surface_2']}; color:{T['muted']}; border:1px solid {T['border']}; }}
.card h3 {{ font-family:'Space Grotesk',sans-serif; font-size:1.1rem; font-weight:700; margin:10px 0 6px; color:{T['text']}; }}
.card .price {{ font-family:'Space Grotesk',sans-serif; font-weight:800; font-size:1.3rem; color:{T['accent']}; }}
.card .desc {{ color:{T['muted']}; font-size:.85rem; min-height:42px; margin: 8px 0; }}
.card .specs {{
    background:{T['surface_2']}; border:1px solid {T['border']};
    border-radius:10px; padding:8px 10px; font-family:'JetBrains Mono',monospace;
    font-size:.75rem; color:{T['text']}; margin-bottom:10px;
}}

/* Empty */
.empty {{
    background:{T['surface']}; border:1.5px dashed {T['border']}; border-radius:18px;
    padding:48px 24px; text-align:center;
}}

/* Order card */
.order {{
    background:{T['surface']}; border:1px solid {T['border']};
    border-left:4px solid {T['accent']}; border-radius:14px;
    padding:18px; margin-bottom:14px; box-shadow:{T['shadow']};
}}
.order .hd {{ display:flex; justify-content:space-between; align-items:center; padding-bottom:10px; border-bottom:1px solid {T['border']}; margin-bottom:12px; }}
.order .id {{ font-family:'Space Grotesk',sans-serif; font-weight:700; color:{T['accent']}; font-size:1.05rem; }}
.order .ts {{ color:{T['muted']}; font-size:.78rem; font-family:'JetBrains Mono',monospace; }}

/* Footer */
.footer {{
    text-align:center; padding:24px; color:{T['muted']}; font-size:.82rem;
    border-top:1px solid {T['border']}; margin-top:42px;
}}

/* Buttons */
.stButton>button {{
    border-radius: 12px !important; font-weight:600 !important;
    transition: all .2s ease !important; border:1px solid {T['border']} !important;
}}
.stButton>button[kind="primary"] {{
    background: {T['grad']} !important; color:white !important;
    border:none !important; box-shadow: 0 8px 20px rgba(255,107,0,.3) !important;
}}
.stButton>button[kind="primary"]:hover {{ transform: translateY(-1px); filter:brightness(1.05); }}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {{ gap: 6px; background:{T['surface']}; padding:6px; border-radius:14px; border:1px solid {T['border']}; }}
.stTabs [data-baseweb="tab"] {{ border-radius:10px; padding:8px 16px; font-weight:600; color:{T['muted']}; }}
.stTabs [aria-selected="true"] {{ background: {T['grad']} !important; color:white !important; }}

/* Inputs */
.stTextInput input, .stTextArea textarea, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {{
    border-radius: 10px !important;
}}

/* Sidebar */
[data-testid="stSidebar"] {{ background:{T['surface']} !important; border-right:1px solid {T['border']}; }}
[data-testid="stSidebar"] * {{ color:{T['text']}; }}

/* Hide default header padding */
header[data-testid="stHeader"] {{ background: transparent; }}
</style>
""", unsafe_allow_html=True)


# ============================================================
# PORTAL VIEW
# ============================================================
if st.session_state.app_mode == "Portal":
    portal_b64 = get_base64_image("Gemini_Generated_Image_515e3d515e3d515e.png")
    bg_layer = (
        f'background-image: linear-gradient(135deg, rgba(11,16,32,.85), rgba(26,35,71,.92)), url("data:image/png;base64,{portal_b64}");'
        if portal_b64 else
        'background: radial-gradient(1200px 600px at 20% 10%, rgba(255,107,0,.25), transparent 60%), radial-gradient(1000px 600px at 80% 90%, rgba(255,61,129,.25), transparent 60%), #0B1020;'
    )
    st.markdown(f"""
    <style>
        .stApp {{ {bg_layer} background-size: cover; background-position: center; background-attachment: fixed; }}
        [data-testid="stSidebar"] {{ display:none !important; }}
        .block-container {{ max-width: 1100px; }}
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center; margin-top: 4rem;">
        <div style="display:inline-flex; align-items:center; gap:10px; padding:8px 16px; background:rgba(255,255,255,.08); border:1px solid rgba(255,255,255,.15); border-radius:999px; color:#fff; font-size:.78rem; letter-spacing:1.5px; text-transform:uppercase; backdrop-filter: blur(10px);">
            <span style="width:8px;height:8px;border-radius:50%;background:#22C55E;box-shadow:0 0 12px #22C55E;"></span>
            System Online · Kigali, Rwanda
        </div>
        <h1 style="font-family:'Space Grotesk',sans-serif; font-weight:800; font-size: clamp(2.8rem,6vw,5rem); color:white; margin: 22px 0 12px; line-height:1.02;">
            Future Technology<br>
            <span style="background:linear-gradient(135deg,#FF6B00,#FF3D81); -webkit-background-clip:text; background-clip:text; color:transparent;">Rwanda Hub</span>
        </h1>
        <p style="font-size:1.15rem; color:#CBD2E0; max-width:680px; margin:0 auto; line-height:1.6;">
            Enter our enterprise ecosystem. Choose your access tier to interface with production lifecycles and product deployment channels.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    c1, c2 = st.columns(2, gap="large")
    cards = [
        (c1, "🏬", "Customer Marketplace",
         "Browse engineering blueprints, filter portfolios, and provision components directly to your operations team.",
         "Launch Marketplace", "primary", "🏬 Consumer View", "#FF6B00"),
        (c2, "🔒", "Admin Terminal",
         "Authenticate, ingest fresh inventory, edit pricing, and control the global data state live.",
         "Launch Terminal", "secondary", "🔒 Admin Dashboard", "rgba(255,255,255,.2)"),
    ]
    for col, icon, title, desc, btn, kind, target, border in cards:
        with col:
            st.markdown(f"""
            <div style="background:rgba(18,25,51,.75); backdrop-filter:blur(14px);
                        padding:38px 32px; border-radius:22px; border:1.5px solid {border};
                        min-height:240px; box-shadow:0 20px 50px rgba(0,0,0,.4);">
                <div style="font-size:2.8rem; margin-bottom:10px;">{icon}</div>
                <h2 style="color:white; font-family:'Space Grotesk',sans-serif; font-weight:700; margin:0 0 10px;">{title}</h2>
                <p style="color:#9AA4C2; font-size:.95rem; line-height:1.55; margin:0 0 18px;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(btn, type=kind, use_container_width=True, key=f"portal_{target}"):
                st.session_state.app_mode = target
                st.rerun()

    st.markdown(f"""
    <div class="footer" style="color:#9AA4C2; border-color:rgba(255,255,255,.1); margin-top:60px;">
        © {datetime.now().year} <b style="color:white;">Future Technology Rwanda Ltd.</b> — Kigali, Rwanda
    </div>
    """, unsafe_allow_html=True)
    st.stop()


# ============================================================
# APP SHELL (Ribbon + Navbar)
# ============================================================
st.markdown(f"""
<div class="ribbon">
    <span><span class="dot"></span>All systems operational</span>
    <span style="opacity:.8;">Support · Warranty · Kigali Core Delivery</span>
</div>
<div class="navbar">
    <div class="brand">
        <div class="brand-mark">⚡</div>
        <div class="brand-text">
            <div class="t1">FUTURE TECHNOLOGY RWANDA</div>
            <div class="t2">Enterprise Hardware · Telecom · Software</div>
        </div>
    </div>
    <div style="font-size:.78rem; color:{T['muted']}; letter-spacing:1.2px; text-transform:uppercase;">
        Mode · {'Consumer' if st.session_state.app_mode == '🏬 Consumer View' else 'Admin'}
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# CONSUMER VIEW
# ============================================================
if st.session_state.app_mode == "🏬 Consumer View":
    tabs = st.tabs(["🏬 Marketplace", "ℹ️ About", "⚙️ How It Works", "👨‍💻 Developer"])

    with tabs[0]:
        inv = st.session_state.company_inventory
        total_units = sum(i["stock"] for i in inv)
        in_stock = sum(1 for i in inv if i["stock"] > 0)

        st.markdown(f"""
        <div class="hero">
            <div class="hero-eyebrow">⚡ Live Catalog</div>
            <h1>Engineering-grade <span class="accent">systems</span><br>for Rwanda & beyond.</h1>
            <p>Elite components across electronics, telecommunications, and electrical infrastructure — sourced and assembled for production deployments.</p>
            <div class="stats">
                <div class="stat"><div class="v">{len(inv)}</div><div class="l">Active SKUs</div></div>
                <div class="stat"><div class="v">{in_stock}</div><div class="l">In Stock</div></div>
                <div class="stat"><div class="v">{total_units}</div><div class="l">Total Units</div></div>
                <div class="stat"><div class="v">24/7</div><div class="l">Support</div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.write("")

        if not inv:
            st.markdown(f"""
            <div class="empty">
                <div style="font-size:3rem;">📦</div>
                <h3 style="margin:8px 0; color:{T['text']};">No Systems Cataloged Yet</h3>
                <p style="color:{T['muted']};">Switch to the Admin Terminal to ingest network stock units.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            f1, f2 = st.columns([3, 1])
            with f1:
                division = st.radio(
                    "Filter Portfolio",
                    ["All Portfolios", "Electronics & Telecom", "Electrical Technology", "Software Development"],
                    horizontal=True, label_visibility="collapsed",
                )
            with f2:
                sort_by = st.selectbox("Sort", ["Featured", "Price: Low → High", "Price: High → Low", "Stock"], label_visibility="collapsed")

            items = inv if division == "All Portfolios" else [i for i in inv if i["category"] == division]
            if sort_by == "Price: Low → High": items = sorted(items, key=lambda x: x["price"])
            elif sort_by == "Price: High → Low": items = sorted(items, key=lambda x: -x["price"])
            elif sort_by == "Stock": items = sorted(items, key=lambda x: -x["stock"])

            if not items:
                st.info("No items in this category.")
            else:
                cols = st.columns(3, gap="medium")
                for idx, item in enumerate(items):
                    with cols[idx % 3]:
                        oos = item["stock"] <= 0
                        st.markdown('<div class="card">', unsafe_allow_html=True)
                        if item.get("img_path") and os.path.exists(item["img_path"]):
                            st.markdown('<div class="img-wrap">', unsafe_allow_html=True)
                            st.image(item["img_path"], use_container_width=True)
                            st.markdown('</div>', unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div class="img-wrap">
                                <div class="ph">
                                    <div style="font-size:2.2rem;">🔧</div>
                                    <div style="font-weight:700; margin-top:6px;">{item['id']}</div>
                                    <div style="font-size:.72rem; opacity:.7;">No image</div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

                        st.markdown(f"""
                        <div class="meta-row">
                            <span class="pill {'out' if oos else 'in'}">{'● OUT OF STOCK' if oos else f'● IN STOCK · {item["stock"]}'}</span>
                            <span class="pill cat">{item['category']}</span>
                        </div>
                        <h3>{item['title']}</h3>
                        <div class="price">${item['price']:,.2f}</div>
                        <div class="desc">{item['desc']}</div>
                        <div class="specs">⚙ {item['specs']}</div>
                        """, unsafe_allow_html=True)

                        if oos:
                            st.button("Unavailable", key=f"buy_{item['id']}", disabled=True, use_container_width=True)
                        else:
                            if st.button("＋ Add to Cart", key=f"buy_{item['id']}", type="primary", use_container_width=True):
                                cur = st.session_state.shopping_cart.get(item["id"], 0)
                                if cur < item["stock"]:
                                    st.session_state.shopping_cart[item["id"]] = cur + 1
                                    st.toast(f"Added {item['title']}")
                                    st.rerun()
                        st.markdown('</div>', unsafe_allow_html=True)

        # ----- Sidebar cart -----
        with st.sidebar:
            st.markdown("---")
            st.markdown("### 🛒 Cart")
            cart = st.session_state.shopping_cart
            if not cart:
                st.info("Your cart is empty.")
            else:
                subtotal = 0.0
                items_summary = []
                for iid, qty in list(cart.items()):
                    it = next((x for x in st.session_state.company_inventory if x["id"] == iid), None)
                    if it:
                        line = it["price"] * qty
                        subtotal += line
                        st.markdown(f"**{it['title']}**  \n`x{qty}` · ${line:,.2f}")
                        items_summary.append({"title": it["title"], "qty": qty, "unit_price": it["price"]})

                st.markdown(f"### Total: ${subtotal:,.2f}")
                st.markdown("#### 👤 Shipping Details")
                with st.form("checkout"):
                    name = st.text_input("Full name / Company*")
                    phone = st.text_input("Phone*")
                    addr = st.text_input("Sector / Province*")
                    pay = st.selectbox("Payment*", [
                        "Mobile Money (MTN / Airtel)",
                        "Bank Transfer (BK / I&M / Equity)",
                        "Cash on Delivery",
                        "Credit / Debit Card",
                    ])
                    if st.form_submit_button("🚀 Place Order", type="primary", use_container_width=True):
                        if name and phone and addr:
                            order = {
                                "order_id": f"FTR-ORD-{datetime.now().strftime('%m%d%H%M%S')}",
                                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "customer_name": name, "customer_phone": phone,
                                "customer_address": addr, "payment_method": pay,
                                "items": items_summary, "total_amount": subtotal,
                            }
                            for cid, cq in cart.items():
                                for inv_i in st.session_state.company_inventory:
                                    if inv_i["id"] == cid:
                                        inv_i["stock"] = max(0, inv_i["stock"] - cq)
                            save_inventory()
                            if save_order(order):
                                st.session_state.shopping_cart = {}
                                st.success("Order placed!")
                                st.balloons()
                                st.rerun()
                        else:
                            st.error("Please fill all required fields.")
                if st.button("Clear Cart", use_container_width=True):
                    st.session_state.shopping_cart = {}
                    st.rerun()

    with tabs[1]:
        st.markdown(f"""
        <div class="hero">
            <div class="hero-eyebrow">About</div>
            <h1>Bridging engineering gaps across <span class="accent">Sub-Saharan Africa.</span></h1>
            <p>Future Technology Rwanda (FTR) is a premier technology manufacturer and enterprise distributor headquartered in Kigali. We fabricate industrial electrical infrastructure, advanced telecom telemetry, and production-grade software frameworks.</p>
        </div>
        """, unsafe_allow_html=True)

    with tabs[2]:
        st.markdown(f"""
        <div class="hero">
            <div class="hero-eyebrow">Workflow</div>
            <h1>From catalog to <span class="accent">delivery</span> in three steps.</h1>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        steps = [
            ("01", "Catalog Ingestion", "Engineers log into the admin terminal to provision fresh devices into the registry."),
            ("02", "Procurement", "Clients browse the storefront, filter by portfolio, and add components to the cart."),
            ("03", "Finalization", "Orders are confirmed against live warehouse stock and dispatched from Kigali."),
        ]
        cs = st.columns(3)
        for col, (n, t, d) in zip(cs, steps):
            with col:
                st.markdown(f"""
                <div class="card">
                    <div style="font-family:'Space Grotesk',sans-serif; font-weight:800; font-size:2.4rem; background:{T['grad']}; -webkit-background-clip:text; color:transparent;">{n}</div>
                    <h3>{t}</h3>
                    <div class="desc">{d}</div>
                </div>
                """, unsafe_allow_html=True)

    with tabs[3]:
        st.markdown(f"""
        <div class="hero">
            <div class="hero-eyebrow">Developer</div>
            <h1>Built with <span class="accent">Streamlit + Python.</span></h1>
            <p>Engineered and maintained by Ineza Sangwa Remy Cedrick.</p>
        </div>
        """, unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""
            <div class="card"><h3>Stack</h3>
            <div class="desc">Streamlit · Python 3.13 · Pandas · Pillow · JSON persistence.</div></div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class="card"><h3>Contact</h3>
            <div class="desc">📞 0796 286 768<br>👤 Ineza Sangwa Remy Cedrick</div></div>
            """, unsafe_allow_html=True)


# ============================================================
# ADMIN VIEW
# ============================================================
elif st.session_state.app_mode == "🔒 Admin Dashboard":
    if not st.session_state.admin_authed:
        st.markdown(f"""
        <div class="hero" style="max-width:520px; margin: 40px auto;">
            <div class="hero-eyebrow">🔒 Restricted</div>
            <h1>Admin <span class="accent">authentication</span></h1>
            <p>Enter your engineer authorization key to access the terminal.</p>
        </div>
        """, unsafe_allow_html=True)
        c = st.columns([1, 2, 1])[1]
        with c:
            pw = st.text_input("Authorization key", type="password", label_visibility="collapsed", placeholder="Authorization key")
            if st.button("Unlock Terminal", type="primary", use_container_width=True):
                if pw == ADMIN_PASSWORD:
                    st.session_state.admin_authed = True
                    st.rerun()
                else:
                    st.error("Invalid key.")
    else:
        inv = st.session_state.company_inventory
        orders = load_orders()
        revenue = sum(o["total_amount"] for o in orders)
        low_stock = sum(1 for i in inv if 0 < i["stock"] <= 3)

        st.markdown(f"""
        <div class="hero">
            <div class="hero-eyebrow">⚙️ Admin</div>
            <h1>Operations <span class="accent">terminal.</span></h1>
            <p>Manage inventory, pricing, stock, and order manifests in one place.</p>
            <div class="stats">
                <div class="stat"><div class="v">{len(inv)}</div><div class="l">SKUs</div></div>
                <div class="stat"><div class="v">{len(orders)}</div><div class="l">Orders</div></div>
                <div class="stat"><div class="v">${revenue:,.0f}</div><div class="l">Revenue</div></div>
                <div class="stat"><div class="v">{low_stock}</div><div class="l">Low Stock</div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.write("")

        t_add, t_edit, t_stock, t_orders = st.tabs(["➕ New Product", "📝 Edit Product", "📊 Stock", "📦 Orders"])

        with t_add:
            with st.form("add_form", clear_on_submit=True):
                c1, c2 = st.columns(2)
                with c1:
                    t = st.text_input("Product name*", placeholder="Fiber Optic Splicer")
                    cat = st.selectbox("Category*", ["Electronics & Telecom", "Electrical Technology", "Software Development"])
                    price = st.number_input("Price ($)", min_value=0.0, value=150.0)
                with c2:
                    stock = st.number_input("Initial stock", min_value=0, value=10)
                    specs = st.text_input("Specifications*", placeholder="220V · 0.02dB splice loss")
                    img = st.file_uploader("Image", type=["jpg", "jpeg", "png"])
                desc = st.text_area("Description*", height=100)
                if st.form_submit_button("Publish Product", type="primary", use_container_width=True):
                    if t and specs and desc:
                        new_id = f"PROD-{len(inv) + 1:03d}"
                        img_path = ""
                        if img is not None:
                            try:
                                im = Image.open(img)
                                img_path = os.path.join(IMAGE_DIR, f"{new_id}_{img.name.replace(' ', '_')}")
                                im.save(img_path)
                            except Exception as e:
                                st.error(f"Image error: {e}")
                        st.session_state.company_inventory.append({
                            "id": new_id, "title": t, "category": cat, "price": price,
                            "specs": specs, "desc": desc, "stock": stock, "img_path": img_path,
                        })
                        save_inventory()
                        st.success(f"Published · {new_id}")
                        st.rerun()
                    else:
                        st.error("Fill all required fields.")

        with t_edit:
            if not inv:
                st.info("No products yet.")
            else:
                labels = [f"{i['id']} — {i['title']}" for i in inv]
                sel = st.selectbox("Select product", labels)
                tid = sel.split(" — ")[0]
                idx = next((k for k, i in enumerate(inv) if i["id"] == tid), None)
                if idx is not None:
                    cur = inv[idx]
                    with st.form("edit_form"):
                        c1, c2 = st.columns(2)
                        with c1:
                            t = st.text_input("Name", value=cur["title"])
                            cats = ["Electronics & Telecom", "Electrical Technology", "Software Development"]
                            cat = st.selectbox("Category", cats, index=cats.index(cur["category"]))
                            price = st.number_input("Price ($)", min_value=0.0, value=float(cur["price"]))
                        with c2:
                            stock = st.number_input("Stock", min_value=0, value=int(cur["stock"]))
                            specs = st.text_input("Specs", value=cur["specs"])
                            new_img = st.file_uploader("Replace image", type=["jpg", "jpeg", "png"], key="edit_img")
                        desc = st.text_area("Description", value=cur["desc"], height=100)
                        if st.form_submit_button("Save Changes", type="primary", use_container_width=True):
                            inv[idx].update({"title": t, "category": cat, "price": price,
                                             "stock": stock, "specs": specs, "desc": desc})
                            if new_img is not None:
                                if cur["img_path"] and os.path.exists(cur["img_path"]):
                                    try: os.remove(cur["img_path"])
                                    except: pass
                                try:
                                    im = Image.open(new_img)
                                    p = os.path.join(IMAGE_DIR, f"{cur['id']}_{new_img.name.replace(' ', '_')}")
                                    im.save(p)
                                    inv[idx]["img_path"] = p
                                except: pass
                            save_inventory()
                            st.success("Saved.")
                            st.rerun()

        with t_stock:
            if not inv:
                st.info("No products yet.")
            else:
                rows = []
                for i in inv:
                    if i["stock"] == 0: s = "🔴 Out of stock"
                    elif i["stock"] <= 3: s = "⚠️ Low"
                    else: s = "🟢 Normal"
                    rows.append({"SKU": i["id"], "Product": i["title"], "Category": i["category"],
                                 "Units": i["stock"], "Status": s})
                st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
                st.markdown("#### ⚡ Quick Restock")
                labels = [f"{i['id']} — {i['title']} (qty {i['stock']})" for i in inv]
                sel = st.selectbox("Component", labels, key="restock_sel")
                tid = sel.split(" — ")[0]
                idx = next((k for k, i in enumerate(inv) if i["id"] == tid), None)
                if idx is not None:
                    c1, c2 = st.columns([2, 1])
                    with c1:
                        new_q = st.number_input("New stock level", min_value=0, value=int(inv[idx]["stock"]))
                    with c2:
                        st.write("")
                        if st.button("Update Stock", type="primary", use_container_width=True):
                            inv[idx]["stock"] = new_q
                            save_inventory()
                            st.success(f"{inv[idx]['title']} → {new_q}")
                            st.rerun()

        with t_orders:
            if not orders:
                st.info("No orders logged yet.")
            else:
                c1, _ = st.columns([1, 3])
                with c1:
                    if st.button("🗑️ Clear all", use_container_width=True):
                        if save_all_orders([]):
                            st.success("Cleared.")
                            st.rerun()
                for order in reversed(orders):
                    st.markdown(f"""
                    <div class="order">
                        <div class="hd">
                            <span class="id">📄 {order['order_id']}</span>
                            <span class="ts">⏱ {order['timestamp']}</span>
                        </div>
                        <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-bottom:12px; font-size:.9rem;">
                            <div><b style="color:{T['muted']};">Customer</b><br>{order['customer_name']}</div>
                            <div><b style="color:{T['muted']};">Phone</b><br>{order['customer_phone']}</div>
                            <div><b style="color:{T['muted']};">Address</b><br>{order['customer_address']}</div>
                            <div><b style="color:{T['muted']};">Payment</b><br><span style="color:{T['accent']}; font-weight:700;">{order.get('payment_method','—')}</span></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    df = pd.DataFrame(order["items"])
                    df.columns = ["Product", "Qty", "Unit ($)"]
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    st.markdown(f"""
                    <div style="text-align:right; font-weight:700; font-size:1.05rem; color:{T['success']}; margin: -6px 0 16px;">
                        Total: ${order['total_amount']:,.2f}
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"Delete {order['order_id']}", key=f"d_{order['order_id']}"):
                        save_all_orders([o for o in orders if o["order_id"] != order["order_id"]])
                        st.rerun()


# ============================================================
# Bottom nav + footer
# ============================================================
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"<h4 style='text-align:center; color:{T['muted']}; font-weight:600; letter-spacing:1px; text-transform:uppercase; font-size:.8rem;'>🧭 Platform Navigation</h4>", unsafe_allow_html=True)

n1, n2 = st.columns(2)
with n1:
    if st.session_state.app_mode == "🏬 Consumer View":
        if st.button("🔒 Switch to Admin Terminal", use_container_width=True, type="primary"):
            st.session_state.app_mode = "🔒 Admin Dashboard"
            st.rerun()
    else:
        if st.button("🏬 Switch to Marketplace", use_container_width=True, type="primary"):
            st.session_state.app_mode = "🏬 Consumer View"
            st.rerun()
with n2:
    if st.button("❌ Exit to Portal", use_container_width=True):
        st.session_state.app_mode = "Portal"
        st.session_state.admin_authed = False
        st.rerun()

st.markdown(f"""
<div class="footer">
    © {datetime.now().year} <b style="color:{T['text']};">Future Technology Rwanda Ltd.</b> · All Rights Reserved<br>
    <span style="opacity:.7; font-size:.74rem;">Elite Hardware · Telecommunications · Enterprise Software · Kigali, Rwanda</span>
</div>
""", unsafe_allow_html=True)
