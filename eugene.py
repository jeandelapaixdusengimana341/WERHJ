import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# ============================================================
# EUGENE SMART TECHNOLOGY — CORPORATE ENTERPRISE OS
# Optimized configuration featuring global theme toggles
# ============================================================

st.set_page_config(
    page_title="Eugene Smart Technology",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# File Storage Configuration Pointers
INVENTORY_FILE = "store_inventory.json"
ORDERS_FILE = "store_orders.json"

# Corporate Specific Variable Anchors
COMPANY_NAME = "Eugene Smart Technology"
ADMIN_PASSWORD = "eugene2006"
COMPANY_PHONE = "0798769799"
COMPANY_LOCATION = "Bugesera District, Juru Sector, Rwinume Cell"

def init_db():
    if not os.path.exists(INVENTORY_FILE):
        mock_data = [
            {"id": "SKU-001", "title": "Quantum Wash Pro", "category": "Home Appliances", "price": 899.99, "stock": 5, "desc": "Next-gen smart inverter washing machine with AI cycle matching.", "img": "https://images.unsplash.com/photo-1626806787461-102c1bfaaea1?w=500"},
            {"id": "SKU-002", "title": "AeroWatch Series Alpha", "category": "Wearables", "price": 249.50, "stock": 12, "desc": "AMOLED always-on display with cellular connectivity and biometric telemetry.", "img": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500"},
            {"id": "SKU-003", "title": "SoundArch Studio Buds", "category": "Audio", "price": 129.99, "stock": 0, "desc": "Active Hybrid Noise Cancelling true wireless monitors with spatial audio mapping.", "img": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500"},
            {"id": "SKU-004", "title": "Horizon OLED 55", "category": "Home Entertainment", "price": 1199.00, "stock": 7, "desc": "True-black pixel emissive display featuring variable refresh rate gaming profiles.", "img": "https://images.unsplash.com/photo-1593305841991-05c297ba4575?w=500"},
            {"id": "SKU-005", "title": "Apex Smartphone X1", "category": "Mobile Systems", "price": 999.00, "stock": 3, "desc": "200MP sensor array system featuring ultra-bandwidth processing chips.", "img": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=500"}
        ]
        with open(INVENTORY_FILE, "w") as f:
            json.dump(mock_data, f, indent=4)

init_db()

# --- Session Bootstrap State Control ---
st.session_state.setdefault("app_mode", "Portal")
st.session_state.setdefault("shopping_cart", {})
st.session_state.setdefault("theme", "Dark")

def load_json(path):
    if not os.path.exists(path): return []
    with open(path, "r") as f: return json.load(f)

def save_json(path, data):
    with open(path, "w") as f: json.dump(data, f, indent=4)

inventory = load_json(INVENTORY_FILE)

# --- Dynamic Style Tokens Matrix ---
def get_theme_tokens(mode):
    if mode == "Dark":
        return dict(
            bg="#0B1020", surface="#121933", surface_2="#1A2347",
            text="#F4F6FB", muted="#9AA4C2", border="rgba(255,255,255,0.08)",
            accent="#2563EB", accent_grad="linear-gradient(135deg, #2563EB 0%, #3B82F6 100%)",
            shadow="0 10px 30px rgba(0,0,0,0.35)", card_bg="#121933"
        )
    return dict(
        bg="#F8FAFC", surface="#FFFFFF", surface_2="#F1F5F9",
        text="#0F172A", muted="#64748B", border="#E2E8F0",
        accent="#2563EB", accent_grad="linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%)",
        shadow="0 10px 25px rgba(15,23,42,0.04)", card_bg="#FFFFFF"
    )

# Sidebar Configuration Controls (Only active outside the Portal page)
if st.session_state.app_mode != "Portal":
    with st.sidebar:
        st.markdown(f"### 🎛️ Operational Controls")
        st.session_state.theme = st.radio(
            "Appearance Mode", ["Dark", "Light"],
            horizontal=True,
            index=0 if st.session_state.theme == "Dark" else 1
        )
        st.markdown("<hr style='opacity:0.15;'>", unsafe_allow_html=True)
        st.markdown(f"""
        **📍 Logistics Node Hub:** <br><small style='color:#9AA4C2;'>{COMPANY_LOCATION}</small><br><br>
        **📞 Support Hotline Line:** <br><small style='color:#9AA4C2;'>{COMPANY_PHONE}</small>
        """, unsafe_allow_html=True)

# Fetch active theme variables
T = get_theme_tokens(st.session_state.theme if st.session_state.app_mode != "Portal" else "Dark")

# ==========================================
# CUSTOM GLOBAL UI CSS INJECTION
# ==========================================
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@600;700&display=swap');

html, body, [class*="css"], .stApp {{
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    background-color: {T['bg']} !important;
    color: {T['text']} !important;
}}

/* Header Navbar Styling */
.navbar {{
    display: flex; justify-content: space-between; align-items: center;
    padding: 16px 24px; background: {T['surface']}; border-radius: 16px;
    box-shadow: {T['shadow']}; border: 1px solid {T['border']};
    margin-bottom: 24px;
}}
.brand {{ display: flex; align-items: center; gap: 10px; }}
.brand-icon {{
    background: {T['accent_grad']};
    color: white; width: 40px; height: 40px; border-radius: 10px;
    display: flex; align-items: center; justify-content: center; font-weight: 800;
}}
.brand-name {{ font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 1.3rem; color: {T['text']}; }}

/* Promotional Banner Hero */
.promo-banner {{
    background: {T['accent_grad']}; color: white;
    padding: 40px; border-radius: 20px; margin-bottom: 30px; position: relative; overflow: hidden;
}}
.promo-banner h1 {{ font-family: 'Space Grotesk', sans-serif; font-size: 2.5rem; margin: 0 0 10px 0; color: white !important; }}
.promo-tag {{ background: rgba(255,255,255,0.15); padding: 4px 12px; border-radius: 999px; font-size: 0.8rem; font-weight: 600; }}

/* Product Display Grid Cards */
.product-card {{
    background: {T['card_bg']}; border-radius: 16px; padding: 16px; border: 1px solid {T['border']};
    box-shadow: {T['shadow']}; height: 100%; display: flex; flex-direction: column;
    transition: transform 0.2s ease, border-color 0.2s ease;
}}
.product-card:hover {{ transform: translateY(-4px); border-color: {T['accent']}; }}
.img-container {{
    width: 100%; aspect-ratio: 1.1; background-size: cover; background-position: center;
    border-radius: 12px; margin-bottom: 12px; border: 1px solid {T['border']};
}}
.status-pill {{
    font-size: 0.72rem; font-weight: 700; padding: 4px 10px; border-radius: 999px; width: fit-content;
}}
.instock {{ background: rgba(34, 197, 94, 0.15); color: #22C55E; border: 1px solid rgba(34,197,94,0.3); }}
.outstock {{ background: rgba(239, 68, 68, 0.15); color: #EF4444; border: 1px solid rgba(239,68,68,0.3); }}
.prod-title {{ font-size: 1.1rem; font-weight: 700; margin: 8px 0 4px 0; color: {T['text']}; }}
.prod-desc {{ color: {T['muted']}; font-size: 0.85rem; line-height: 1.4; flex-grow: 1; margin-bottom: 12px; }}
.prod-price {{ font-size: 1.3rem; font-weight: 800; color: {T['accent']}; font-family: 'Space Grotesk', sans-serif; }}

/* Custom Form and Management Layout Styling */
.admin-order-box {{
    background: {T['surface']}; border: 1px solid {T['border']}; border-radius: 14px;
    padding: 20px; margin-bottom: 16px; box-shadow: {T['shadow']};
}}

/* Sidebar & Inputs */
[data-testid="stSidebar"] {{ background: {T['surface']} !important; border-right: 1px solid {T['border']}; }}
[data-testid="stSidebar"] * {{ color: {T['text']}; }}
div.stButton > button:first-child {{ border-radius: 10px !important; font-weight: 600 !important; }}
div.stButton > button[kind="primary"]:first-child {{
    background: {T['accent_grad']} !important; color: white !important; border: none !important;
}}

.stTabs [data-baseweb="tab-list"] {{ gap: 8px; background: {T['surface']}; padding: 6px; border-radius: 12px; border: 1px solid {T['border']}; }}
.stTabs [data-baseweb="tab"] {{ border-radius: 8px; padding: 8px 16px; font-weight: 600; }}
</style>
""", unsafe_allow_html=True)

# ==========================================
# GATEWAY ENTRY PORTAL VIEW
# ==========================================
if st.session_state.app_mode == "Portal":
    st.markdown(f"""
    <div style="text-align:center; margin-top: 4rem;">
        <div style="display:inline-flex; align-items:center; gap:8px; padding:6px 14px; background:rgba(255,255,255,.05); border:1px solid rgba(255,255,255,.1); border-radius:999px; color:#9AA4C2; font-size:.8rem; letter-spacing:1px; text-transform:uppercase;">
            <span style="width:8px;height:8px;border-radius:50%;background:#22C55E;display:inline-block;"></span>
            Sovereign Technology Core Hub Active
        </div>
        <h1 style="font-family:'Space Grotesk',sans-serif; font-weight:800; font-size: clamp(2.5rem, 5vw, 4.2rem); color:white; margin: 20px 0 10px; line-height:1.1;">
            {COMPANY_NAME}
        </h1>
        <p style="font-size:1.1rem; color:#9AA4C2; max-width:650px; margin:0 auto 3rem; line-height:1.6;">
            Next-generation automated commercial marketplace pipeline layers and telemetry ledger nodes.<br>
            <span style="color:#3B82F6; font-size:0.95rem;">📍 {COMPANY_LOCATION}</span>
        </p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="large")
    
    with c1:
        st.markdown(f"""
        <div style="background:#121933; padding:36px; border-radius:20px; border:1.5px solid #2563EB; min-height:220px; box-shadow:0 20px 40px rgba(0,0,0,0.4);">
            <div style="font-size:2.5rem; margin-bottom:8px;">🏬</div>
            <h3 style="color:white; font-family:'Space Grotesk',sans-serif; margin:0 0 8px;">Customer Portal</h3>
            <p style="color:#9AA4C2; font-size:0.9rem; line-height:1.5; margin-bottom:0;">Browse smart asset portfolios, manage delivery queues, and execute transactions securely.</p>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("Launch Storefront Pipeline", type="primary", use_container_width=True):
            st.session_state.app_mode = "Storefront"
            st.rerun()

    with c2:
        st.markdown(f"""
        <div style="background:#121933; padding:36px; border-radius:20px; border:1.5px solid rgba(255,255,255,0.15); min-height:220px; box-shadow:0 20px 40px rgba(0,0,0,0.4);">
            <div style="font-size:2.5rem; margin-bottom:8px;">🔒</div>
            <h3 style="color:white; font-family:'Space Grotesk',sans-serif; margin:0 0 8px;">Admin Control Console</h3>
            <p style="color:#9AA4C2; font-size:0.9rem; line-height:1.5; margin-bottom:0;">Log securely into management matrix databases, adjust pricing profiles, and check logistics streams.</p>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        
        # Admin Lock Verification Area
        with st.popover("Unlock Admin Console Terminal", use_container_width=True):
            input_pass = st.text_input("Enter Private Access Key", type="password")
            if st.button("Verify Verification Phrase", use_container_width=True, type="primary"):
                if input_pass == ADMIN_PASSWORD:
                    st.session_state.app_mode = "Backend Admin"
                    st.rerun()
                else:
                    st.error("Authentication Denied: Access key incorrect.")
            
    st.stop()


# ==========================================
# STANDARD PLATFORM SHELL NAVBAR
# ==========================================
st.markdown(f"""
<div class="navbar">
    <div class="brand">
        <div class="brand-icon">⚡</div>
        <div class="brand-name">{COMPANY_NAME}</div>
    </div>
    <div style="font-weight: 600; font-size: 0.8rem; color: {T['text']}; letter-spacing: 1.2px; text-transform: uppercase; background:rgba(37,99,235,0.15); padding:6px 14px; border-radius:8px;">
        {'Consumer Space' if st.session_state.app_mode == 'Storefront' else 'Operator Matrix'}
    </div>
</div>
""", unsafe_allow_html=True)


# ==========================================
# APPLICATION ROUTE: CONSUMER STOREFRONT
# ==========================================
if st.session_state.app_mode == "Storefront":
    
    st.markdown(f"""
    <div class="promo-banner">
        <span class="promo-tag">{COMPANY_NAME} • EXCLUSIVE OFFERS</span>
        <h1>Smart Technology Foundations</h1>
        <p>Reliable devices, appliances, and automated infrastructure lines deployed straight to your destination network.</p>
    </div>
    """, unsafe_allow_html=True)
    
    cats = ["All Matrix Profiles", "Home Appliances", "Wearables", "Audio", "Home Entertainment", "Mobile Systems"]
    sel_cat = st.radio("Display Filter Layer", cats, horizontal=True, label_visibility="collapsed")
    st.write("")
    
    filtered_items = inventory if sel_cat == "All Matrix Profiles" else [i for i in inventory if i["category"] == sel_cat]
    
    if not filtered_items:
        st.info("No assets match this category filter index.")
    else:
        cols = st.columns(3, gap="large")
        for idx, item in enumerate(filtered_items):
            with cols[idx % 3]:
                is_oos = item["stock"] <= 0
                status_class = "outstock" if is_oos else "instock"
                status_text = "OUT OF STOCK" if is_oos else f"IN STOCK ({item['stock']})"
                
                st.markdown(f"""
                <div class="product-card">
                    <div class="img-container" style="background-image: url('{item['img']}');"></div>
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span class="status-pill {status_class}">● {status_text}</span>
                        <span style="font-size:0.75rem; color:{T['muted']}; font-weight:600;">{item['category']}</span>
                    </div>
                    <div class="prod-title">{item['title']}</div>
                    <div class="prod-desc">{item['desc']}</div>
                    <div style="display:flex; justify-content:space-between; align-items:center; padding-top:10px; border-top:1px solid {T['border']};">
                        <div class="prod-price">${item['price']:,.2f}</div>
                        <div style="font-size:0.7rem; color:{T['muted']};">{item['id']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if is_oos:
                    st.button("Unavailable", key=f"btn_{item['id']}", disabled=True, use_container_width=True)
                else:
                    if st.button("🛒 Add to Cart Pipeline", key=f"btn_{item['id']}", type="primary", use_container_width=True):
                        current_cart_qty = st.session_state.shopping_cart.get(item["id"], 0)
                        if current_cart_qty < item["stock"]:
                            st.session_state.shopping_cart[item["id"]] = current_cart_qty + 1
                            st.toast(f"Allocated {item['title']} into tracking cart stream.")
                            st.rerun()
                        else:
                            st.error("Insufficient inventory depth allocation available.")
            st.markdown("<br>", unsafe_allow_html=True)

    # --- SIDEBAR LOGISTICS CART TRACKER PANEL ---
    with st.sidebar:
        st.markdown("### 🛒 Active Logistics Manifest")
        cart = st.session_state.shopping_cart
        
        if not cart:
            st.info("The checkout allocation manifest is currently empty.")
        else:
            net_total = 0.0
            manifest_items = []
            
            for item_sku, quantity in list(cart.items()):
                matched_item = next((x for x in inventory if x["id"] == item_sku), None)
                if matched_item:
                    line_valuation = matched_item["price"] * quantity
                    net_total += line_valuation
                    manifest_items.append({"title": matched_item["title"], "qty": quantity, "price": matched_item["price"]})
                    
                    st.markdown(f"""
                    <div style="background:{T['surface_2']}; padding:12px; border-radius:10px; margin-bottom:8px; border:1px solid {T['border']};">
                        <div style="font-weight:700; font-size:0.9rem; color:{T['text']};">{matched_item['title']}</div>
                        <div style="display:flex; justify-content:space-between; color:{T['muted']}; font-size:0.8rem; margin-top:4px;">
                            <span>Units: <b>x{quantity}</b></span>
                            <span style="color:{T['accent']}; font-weight:600;">${line_valuation:,.2f}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown(f"### Pay Total: <span style='color:{T['accent']};'>${net_total:,.2f}</span>", unsafe_allow_html=True)
            
            with st.form("checkout_form"):
                st.markdown(f"<small style='color:{T['muted']};'>Logistics Delivery Coordinates</small>", unsafe_allow_html=True)
                cust_name = st.text_input("Customer/Company Name*")
                cust_addr = st.text_input("Destination Target Address*", placeholder="e.g., Kigali, Gasabo")
                cust_phone_input = st.text_input("Active Phone Line*")
                payment_vector = st.selectbox("Payment Gateway Protocol", ["Mobile Money Transfer", "Direct Banking Wire Switch", "Cash Verification on Delivery"])
                
                if st.form_submit_button("🚀 Finalize Core Order", type="primary", use_container_width=True):
                    if cust_name.strip() and cust_addr.strip() and cust_phone_input.strip():
                        for sku_id, count in cart.items():
                            for inv_node in inventory:
                                if inv_node["id"] == sku_id:
                                    inv_node["stock"] = max(0, inv_node["stock"] - count)
                        save_json(INVENTORY_FILE, inventory)
                        
                        new_receipt = {
                            "order_id": f"EST-ORD-{datetime.now().strftime('%m%d%H%M%S')}",
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "customer": cust_name, "destination": cust_addr, "phone": cust_phone_input,
                            "method": payment_vector, "payload": manifest_items, "total": net_total
                        }
                        
                        current_orders = load_json(ORDERS_FILE)
                        current_orders.append(new_receipt)
                        save_json(ORDERS_FILE, current_orders)
                        
                        st.session_state.shopping_cart = {}
                        st.success("Logistics process logged. Thank you!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("Validation failed: Populate all fields.")
            
            if st.button("Clear Manifest Selection", use_container_width=True):
                st.session_state.shopping_cart = {}
                st.rerun()

# ==========================================
# APPLICATION ROUTE: OPERATOR BACKEND ADMIN
# ==========================================
elif st.session_state.app_mode == "Backend Admin":
    st.markdown("## 🔒 Operational Datacore Administration Panel")
    
    orders_log = load_json(ORDERS_FILE)
    gross_rev = sum(o["total"] for o in orders_log)
    low_stock_alerts = sum(1 for i in inventory if i["stock"] <= 2)
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Gross Logged Revenue Pipeline", f"${gross_rev:,.2f}")
    m2.metric("Orders Processed Counters", f"{len(orders_log)} Orders")
    m3.metric("Critical Low Inventory Warnings", f"{low_stock_alerts} SKUs")
    
    st.write("")
    
    # ADVANCED WORKFLOW TABS STRUCTURE
    adm_t1, adm_t2, adm_t3, adm_t4 = st.tabs([
        "📊 Stock Management Matrix", 
        "➕ Ingest New Product Node", 
        "📝 Modify Asset Configuration", 
        "📦 Transaction Manifests & Order Stream"
    ])
    
    # ---------------------------------------------
    # TAB 1: STOCK MANAGEMENT MATRIX
    # ---------------------------------------------
    with adm_t1:
        st.markdown("#### Live Active Inventory Records Matrix")
        
        stock_rows = []
        for i in inventory:
            if i["stock"] == 0:
                status = "🔴 Out of Stock"
            elif i["stock"] <= 2:
                status = "⚠️ Critical Low Stock Alert"
            else:
                status = "🟢 Nominal Allocation Level"
            
            stock_rows.append({
                "SKU Code": i["id"],
                "Product Designation": i["title"],
                "Category Assignment": i["category"],
                "Available Reservoir Stock": i["stock"],
                "Health Metric Status": status
            })
        st.dataframe(pd.DataFrame(stock_rows), use_container_width=True, hide_index=True)
        
        st.markdown("<br>#### ⚡ Quick Stock Level Replenishment Adjuster", unsafe_allow_html=True)
        sku_labels = [f"{i['id']} — {i['title']} (Units Left: {i['stock']})" for i in inventory]
        target_selection = st.selectbox("Select Target Database Product Entry to Adjust", sku_labels, key="stock_adj_select")
        
        target_sku = target_selection.split(" — ")[0]
        inv_idx = next((index for index, item in enumerate(inventory) if item["id"] == target_sku), None)
        
        if inv_idx is not None:
            col_q1, col_q2 = st.columns([2, 1])
            with col_q1:
                adjusted_stock = st.number_input("Absolute Quantities Allocated to Warehouses", min_value=0, value=int(inventory[inv_idx]["stock"]), key="stock_num_input")
            with col_q2:
                st.write("<br>", unsafe_allow_html=True)
                if st.button("Commit Adjusted Reservoir Count", type="primary", use_container_width=True):
                    inventory[inv_idx]["stock"] = adjusted_stock
                    save_json(INVENTORY_FILE, inventory)
                    st.success(f"Stock altered successfully! {inventory[inv_idx]['title']} updated to {adjusted_stock} units.")
                    st.rerun()

    # ---------------------------------------------
    # TAB 2: INGEST NEW PRODUCT NODE
    # ---------------------------------------------
    with adm_t2:
        st.markdown("#### Ingest New Product Unit Asset into Storefront Databases")
        with st.form("ingest_form", clear_on_submit=True):
            c_f1, c_f2 = st.columns(2)
            with c_f1:
                new_title = st.text_input("Product Title Designator*")
                new_cat = st.selectbox("Category Allocation Class", ["Home Appliances", "Wearables", "Audio", "Home Entertainment", "Mobile Systems"])
                new_price = st.number_input("Unit Price Point Valuation ($)", min_value=0.01, value=99.99)
            with c_f2:
                new_stock = st.number_input("Initial Intake Volume Quantities", min_value=0, value=10)
                new_url = st.text_input("Asset Image Static CDN URL Path Link", value="https://images.unsplash.com/photo-1531403009284-440f080d1e12?w=500")
            
            new_desc = st.text_area("Asset Specifications / Description*")
            
            if st.form_submit_button("Publish Node Asset Item To Storefront", type="primary", use_container_width=True):
                if new_title.strip() and new_desc.strip():
                    inventory.append({
                        "id": f"EST-SKU-{len(inventory)+1:03d}", 
                        "title": new_title, 
                        "category": new_cat,
                        "price": new_price, 
                        "stock": new_stock, 
                        "desc": new_desc, 
                        "img": new_url
                    })
                    save_json(INVENTORY_FILE, inventory)
                    st.success("SKU item synchronized successfully into registry arrays.")
                    st.rerun()
                else:
                    st.error("Submission blocked. Structural parameters cannot remain empty.")

    # ---------------------------------------------
    # TAB 3: MODIFY ASSET CONFIGURATION
    # ---------------------------------------------
    with adm_t3:
        st.markdown("#### Overwrite and Modify Profiles of Registered Matrix Assets")
        modify_labels = [f"{i['id']} — {i['title']}" for i in inventory]
        modify_selection = st.selectbox("Choose Targeted Active Matrix Element", modify_labels, key="modify_profile_select")
        
        mod_sku = modify_selection.split(" — ")[0]
        mod_idx = next((idx for idx, item in enumerate(inventory) if item["id"] == mod_sku), None)
        
        if mod_idx is not None:
            current_item = inventory[mod_idx]
            
            # Sub-layout to view target product's current parameters inside management suite
            col_m1, col_m2 = st.columns([1, 4])
            with col_m1:
                st.markdown("<small style='opacity:0.7;'>Active Image Profile:</small>", unsafe_allow_html=True)
                st.image(current_item["img"], width=110)
            with col_m2:
                st.markdown(f"**Selected Identity Scope:** Item SKU Key Array: `{current_item['id']}`")
                st.markdown(f"**Operational Registry Title:** {current_item['title']}")
                
            with st.form("modify_form_suite"):
                c_mod1, c_mod2 = st.columns(2)
                with c_mod1:
                    edit_title = st.text_input("Update Operational Title Name Designator", value=current_item["title"])
                    cat_options = ["Home Appliances", "Wearables", "Audio", "Home Entertainment", "Mobile Systems"]
                    edit_cat = st.selectbox("Re-assign Portfolio Category Array", cat_options, index=cat_options.index(current_item["category"]))
                    edit_price = st.number_input("Adjust Valuation Price Point Index ($)", min_value=0.01, value=float(current_item["price"]))
                with c_mod2:
                    edit_stock = st.number_input("Modify Warehouse Reserves Capacity Counters", min_value=0, value=int(current_item["stock"]))
                    edit_url = st.text_input("Modify/Overwrite Graphical Image Static URL Vector Path Link", value=current_item["img"])
                
                edit_desc = st.text_area("Adjust Structural Details & Functional Specifications Manifest", value=current_item["desc"], height=100)
                
                c_submit, c_delete = st.columns([4, 1])
                with c_submit:
                    if st.form_submit_button("Commit Changes to Inventory Master File Node", type="primary", use_container_width=True):
                        inventory[mod_idx].update({
                            "title": edit_title,
                            "category": edit_cat,
                            "price": edit_price,
                            "stock": edit_stock,
                            "img": edit_url,
                            "desc": edit_desc
                        })
                        save_json(INVENTORY_FILE, inventory)
                        st.success(f"Modification structural configurations successfully updated for SKU {mod_sku}.")
                        st.rerun()
                        
                with c_delete:
                    if st.form_submit_button("🚨 Delete Item From Database", use_container_width=True):
                        inventory.pop(mod_idx)
                        save_json(INVENTORY_FILE, inventory)
                        st.warning(f"SKU Asset {mod_sku} completely purged from local JSON stack.")
                        st.rerun()

    # ---------------------------------------------
    # TAB 4: TRANSACTION MANIFESTS & DELETION MECHANISMS
    # ---------------------------------------------
    with adm_t4:
        st.markdown("#### Logged Storefront Orders Archive Queue")
        if not orders_log:
            st.info("Zero transactional payloads registered in deployment queue systems.")
        else:
            for tracking_ord in reversed(orders_log):
                # Wrapped inside unique boxes for atomic control blocks
                st.markdown(f"""
                <div class="admin-order-box">
                    <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid {T['border']}; padding-bottom:8px; margin-bottom:12px;">
                        <span style="font-family:'Space Grotesk',sans-serif; font-weight:700; color:{T['accent']};">📄 Order String Code ID: {tracking_ord['order_id']}</span>
                        <span style="font-size:0.8rem; font-family:monospace; opacity:0.8;">⏱ Time: {tracking_ord['timestamp']}</span>
                    </div>
                    <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px; font-size:0.88rem; margin-bottom:12px;">
                        <div><b>Customer Entity Name:</b> {tracking_ord['customer']}</div>
                        <div><b>Buyer Mobile Connection:</b> {tracking_ord.get('phone', 'N/A')}</div>
                        <div><b>Destination Target Matrix:</b> {tracking_ord['destination']}</div>
                        <div><b>Financial Channel:</b> <span style="color:#22C55E; font-weight:600;">{tracking_ord['method']}</span></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.dataframe(pd.DataFrame(tracking_ord["payload"]), use_container_width=True, hide_index=True)
                
                col_info, col_act = st.columns([3, 1])
                with col_info:
                    st.markdown(f"<h4 style='color:#22C55E; margin:4px 0;'>Aggregate Receipt Sum Valuation Total: ${tracking_ord['total']:,.2f}</h4>", unsafe_allow_html=True)
                with col_act:
                    # SECURE SPECIFIC TICKET REMOVAL TRIGGER HOOK
                    if st.button(f"❌ Delete Ticket {tracking_ord['order_id']}", key=f"del_ticket_{tracking_ord['order_id']}", use_container_width=True):
                        revised_orders = [ord_node for ord_node in orders_log if ord_node["order_id"] != tracking_ord["order_id"]]
                        save_json(ORDERS_FILE, revised_orders)
                        st.toast(f"Purged Transaction {tracking_ord['order_id']} safely from deployment tracking array streams.")
                        st.rerun()
                        
                st.markdown("<hr style='opacity:0.1; margin:16px 0 24px;'>", unsafe_allow_html=True)


# ==========================================
# UNIVERSAL FRAMEWORK ROUTING NAVIGATION FOOTER
# ==========================================
st.markdown("<br><hr style='opacity:0.15;'><br>", unsafe_allow_html=True)
st.markdown(f"<h4 style='text-align:center; color:{T['muted']}; font-weight:600; letter-spacing:1px; text-transform:uppercase; font-size:.8rem;'>🧭 Matrix Platform Navigation Switches</h4>", unsafe_allow_html=True)

c_nav1, c_nav2 = st.columns(2)
with c_nav1:
    if st.session_state.app_mode == "Storefront":
        if st.button("🔒 Hot-Swap View: Access Management System Terminal", use_container_width=True, type="primary"):
            st.session_state.app_mode = "Portal"  # Route through portal gateway to safely challenge credentials
            st.rerun()
    else:
        if st.button("🏬 Hot-Swap View: Switch back to Marketplace Dashboard", use_container_width=True, type="primary"):
            st.session_state.app_mode = "Storefront"
            st.rerun()

with c_nav2:
    if st.button("❌ Terminate Current Session: Return to Portal Base Gateway", use_container_width=True):
        st.session_state.app_mode = "Portal"
        st.rerun()

st.markdown(f"""
<div style="text-align:center; font-size:0.85rem; color:{T['muted']}; padding: 30px 0; border-top:1px solid {T['border']}; margin-top:40px;">
    © {datetime.now().year} <b>{COMPANY_NAME}</b> • Operational Node Core Hub.<br>
    <small style="color:{T['muted']}70;">{COMPANY_LOCATION} | Line: {COMPANY_PHONE}</small>
</div>
""", unsafe_allow_html=True)
