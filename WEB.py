import streamlit as st
import pandas as pd
import os
import base64
import json
from PIL import Image
from datetime import datetime

# 1. Page Configuration & Setup
st.set_page_config(page_title="FUTURE TECHNOLOGY RWANDA", page_icon="⚡", layout="wide")

IMAGE_DIR = "uploaded_images"
INVENTORY_FILE = "company_inventory.json"  
ORDERS_FILE = "company_orders.json"  # Permanent order ledger registry database

if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

# Initialize Session State Machine Variables
if 'app_mode' not in st.session_state:
    st.session_state.app_mode = "Portal"

if 'shopping_cart' not in st.session_state: 
    st.session_state.shopping_cart = {}

# --- PERMANENT INVENTORY SYSTEM IO FUNCTIONS ---
def load_inventory():
    if os.path.exists(INVENTORY_FILE):
        try:
            with open(INVENTORY_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"⚠️ Core Inventory Database Read Error: {e}")
    return []

def save_inventory():
    try:
        with open(INVENTORY_FILE, "w") as f:
            json.dump(st.session_state.company_inventory, f, indent=4)
    except Exception as e:
        st.error(f"⚠️ Core Inventory Database Write Error: {e}")

# --- PERMANENT ORDERING SYSTEM IO FUNCTIONS ---
def load_orders():
    if os.path.exists(ORDERS_FILE):
        try:
            with open(ORDERS_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"⚠️ Core Orders Database Read Error: {e}")
    return []

def save_order(new_order):
    current_orders = load_orders()
    current_orders.append(new_order)
    try:
        with open(ORDERS_FILE, "w") as f:
            json.dump(current_orders, f, indent=4)
        return True
    except Exception as e:
        st.error(f"⚠️ Failed to commit order validation: {e}")
        return False

def save_all_orders(orders_list):
    try:
        with open(ORDERS_FILE, "w") as f:
            json.dump(orders_list, f, indent=4)
        return True
    except Exception as e:
        st.error(f"⚠️ Failed to update database logs: {e}")
        return False

# Initialize inventory data parameters into memory cache
if 'company_inventory' not in st.session_state:
    st.session_state.company_inventory = load_inventory()

# Safe Base64 Core File Encoder for CSS Background Insertion
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

# 2. Dynamic Portal Visual Styles & Color Themes
if st.session_state.app_mode != "Portal":
    st.sidebar.title("🇷🇼 Corporate Control Room")
    theme_selection = st.sidebar.radio("🎨 Select Visual UI Theme:", ["Dark Mode 🌙", "Light Mode ☀️"])
    
    if theme_selection == "Dark Mode 🌙":
        bg_app, bg_card, text_main, text_sub, border_color = "#0f172a", "#1e293b", "#f8fafc", "#94a3b8", "#334155"
    else:
        bg_app, bg_card, text_main, text_sub, border_color = "#f8fafc", "#ffffff", "#0f172a", "#475569", "#e2e8f0"
else:
    bg_app, bg_card, text_main, text_sub, border_color = "#0f172a", "#1e293b", "#f8fafc", "#94a3b8", "#334155"

# Inject Global Visual Layout Component Styling via CSS
st.markdown(f"""
    <style>
        .stApp {{ background-color: {bg_app} !important; color: {text_main} !important; }}
        .top-ribbon {{
            background-color: #1e3a8a; color: #ffffff; padding: 8px 40px; font-size: 0.85rem;
            display: flex; justify-content: space-between; margin: -6rem -5rem 1.5rem -5rem;
        }}
        .navbar-strip {{
            background-color: #111827; padding: 15px 40px; display: flex; align-items: center;
            margin: -2rem -5rem 1rem -5rem; border-bottom: 3px solid #ff6b00; justify-content: space-between;
        }}
        .brand-logo {{ color: #ff6b00; font-size: 1.8rem; font-weight: 900; font-family: 'Arial Black', sans-serif; margin-right: 15px; }}
        .brand-title {{ color: #ffffff; font-size: 1.4rem; font-weight: 700; letter-spacing: 1.5px; }}
        .hero-headline {{ font-size: 3.5rem; font-weight: 900; color: {text_main}; line-height: 1.1; font-family: 'Impact', sans-serif; text-transform: uppercase; margin-bottom: 10px; }}
        .hero-sub {{ font-size: 1.15rem; color: {text_sub}; margin-bottom: 25px; }}
        .highlight-orange {{ color: #ff6b00; font-weight: bold; }}
        .product-card {{ background-color: {bg_card}; padding: 24px; border-radius: 12px; box-shadow: 0px 4px 20px rgba(0,0,0,0.03); border: 1px solid {border_color}; margin-bottom: 15px; }}
        .product-title {{ font-size: 1.3rem; font-weight: 800; color: {text_main}; margin: 12px 0 4px 0; }}
        .product-price {{ font-size: 1.25rem; font-weight: 700; color: #ff6b00; margin-bottom: 12px; }}
        .image-fallback-placeholder {{
            background-color: {bg_app}; height: 180px; border-radius: 8px; border: 2px dashed {border_color};
            display: flex; flex-direction: column; justify-content: center; align-items: center; color: {text_sub}; text-align: center; padding: 10px;
        }}
        .empty-catalog-box {{
            background-color: {bg_card}; padding: 40px; border-radius: 12px; text-align: center;
            border: 1px dashed {border_color}; margin-top: 20px;
        }}
        .corporate-footer {{
            text-align: center; padding: 25px; color: {text_sub}; font-size: 0.85rem;
            border-top: 1px solid {border_color}; margin-top: 40px; font-family: sans-serif;
        }}
        .order-manifest-box {{
            background-color: {bg_card}; padding: 20px; border-radius: 8px; border: 1px solid {border_color};
            margin-bottom: 15px; border-left: 5px solid #ff6b00;
        }}
    </style>
""", unsafe_allow_html=True)


# --- 1. FULL SCREEN ENTRY PORTAL LANDING VIEW ---
if st.session_state.app_mode == "Portal":
    portal_bg_b64 = get_base64_image("Gemini_Generated_Image_515e3d515e3d515e.png")
    
    st.markdown(f"""
        <style>
            .stApp {{
                background-image: linear-gradient(rgba(15, 23, 42, 0.65), rgba(15, 23, 42, 0.85)), url("data:image/png;base64,{portal_bg_b64}");
                background-size: cover;
                background-position: center center;
                background-attachment: fixed;
                background-repeat: no-repeat;
            }}
            [data-testid="stSidebar"] {{
                display: none !important;
            }}
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div style="text-align: center; margin-top: 6rem; margin-bottom: 4rem;">
            <h1 style="font-size: 4.5rem; color: #ffffff; font-family: 'Impact', sans-serif; letter-spacing: 2px; text-transform: uppercase; line-height: 1.1; text-shadow: 0px 4px 15px rgba(0,0,0,0.6);">
                Future Technology<br><span style="color: #ff6b00;">Rwanda Hub</span>
            </h1>
            <p style="font-size: 1.35rem; color: #e2e8f0; max-width: 750px; margin: 18px auto 0 auto; font-weight: 500; text-shadow: 0px 2px 8px rgba(0,0,0,0.8);">
                Enter our enterprise ecosystem. Select an authorization tier framework gateway below to interface with production lifecycles and product deployment channels.
            </p>
        </div>
    """, unsafe_allow_html=True)

    portal_col1, portal_col2 = st.columns(2)
    
    with portal_col1:
        st.markdown("""
            <div style="background-color: rgba(15, 23, 42, 0.85); padding: 45px 35px; border-radius: 16px; border: 2px solid #ff6b00; text-align: center; box-shadow: 0 15px 35px rgba(0,0,0,0.6); min-height: 250px; display: flex; flex-direction: column; justify-content: space-between; backdrop-filter: blur(8px);">
                <div>
                    <div style="font-size: 3.5rem; margin-bottom: 12px;">🏬</div>
                    <h2 style="color: #ffffff; font-weight: 800; margin-bottom: 10px; letter-spacing: 0.5px;">Customer Marketplace</h2>
                    <p style="color: #94a3b8; font-size: 0.95rem; margin: 0 0 25px 0; line-height: 1.5;">Examine engineering blueprints, filter active portfolios, and provision component acquisition carts directly to operations logistics teams.</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Launch Customer Marketplace", type="primary", use_container_width=True):
            st.session_state.app_mode = "🏬 Consumer View"
            st.rerun()

    with portal_col2:
        st.markdown("""
            <div style="background-color: rgba(15, 23, 42, 0.85); padding: 45px 35px; border-radius: 16px; border: 2px solid #475569; text-align: center; box-shadow: 0 15px 35px rgba(0,0,0,0.6); min-height: 250px; display: flex; flex-direction: column; justify-content: space-between; backdrop-filter: blur(8px);">
                <div>
                    <div style="font-size: 3.5rem; margin-bottom: 12px;">🔒</div>
                    <h2 style="color: #ffffff; font-weight: 800; margin-bottom: 10px; letter-spacing: 0.5px;">Admin Terminal</h2>
                    <p style="color: #94a3b8; font-size: 0.95rem; margin: 0 0 25px 0; line-height: 1.5;">Authenticate security overrides, ingest fresh technical inventory items, edit pricing modules, and control global data states live.</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Launch Ingestion Terminal", type="secondary", use_container_width=True):
            st.session_state.app_mode = "🔒 Admin Dashboard"
            st.rerun()


# --- 2. ACTIVATED TARGET SUBSYSTEMS VIEW ---
else:
    st.markdown('<div class="top-ribbon"><span>Support & Returns</span><span>Warranty Information</span><span>Kigali Core Delivery</span></div>', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="navbar-strip">
            <div>
                <span class="brand-logo">🗲 FTR</span>
                <span class="brand-title">FUTURE TECHNOLOGY RWANDA</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # --- PORTAL WORKSPACE A: CONSUMER FRAMEWORK ---
    if st.session_state.app_mode == "🏬 Consumer View":
        nav_tabs = st.tabs(["🏬 Storefront Marketplace", "ℹ️ About Us", "⚙️ How It Works", "👨‍💻 Developer Profile"])

        # TAB 1: STOREFRONT MARKETPLACE
        with nav_tabs[0]:
            st.markdown('<h1 class="hero-headline">Future Technology<br>Rwanda Systems</h1>', unsafe_allow_html=True)
            st.markdown('<p class="hero-sub">Providing elite engineering components in <span class="highlight-orange">Electronics, Telecommunication networks</span>, and Hardware Infrastructure components.</p>', unsafe_allow_html=True)
            st.write("---")
            
            if not st.session_state.company_inventory:
                st.markdown(f"""
                    <div class="empty-catalog-box">
                        <div style="font-size: 3.5rem; margin-bottom: 10px;">📦</div>
                        <h3 style="color: {text_main}; margin: 0 0 8px 0;">No Systems Currently Cataloged</h3>
                        <p style="color: {text_sub}; font-size: 0.95rem; margin: 0;">
                            Our inventory databases are resting clean. Please exit to the <b>Landing Portal</b> and log into the <b>Admin Terminal</b> to ingest network stock units.
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                selected_division = st.radio("Filter Portfolio:", ["All Portfolios", "Electronics & Telecom", "Electrical Technology", "Software Development"], horizontal=True)
                filtered_items = st.session_state.company_inventory if selected_division == "All Portfolios" else [i for i in st.session_state.company_inventory if i["category"] == selected_division]
                
                if not filtered_items:
                    st.info("No items cataloged in this specific tier selection.")
                else:
                    prod_cols = st.columns(3)
                    for idx, item in enumerate(filtered_items):
                        col_target = prod_cols[idx % 3]
                        with col_target:
                            is_out_of_stock = item["stock"] <= 0
                            
                            if item["img_path"] and os.path.exists(item["img_path"]):
                                st.image(item["img_path"], use_container_width=True)
                            else:
                                st.markdown(f'<div class="image-fallback-placeholder"><div style="font-size: 2rem;">🔧</div><b>{item["id"]} Preview</b><br><span style="font-size:0.75rem; opacity:0.6;">No Image Uploaded</span></div>', unsafe_allow_html=True)
                            
                            st.markdown(f"""
                                <div class="product-card">
                                    <div style="display: flex; justify-content: space-between; font-size: 0.75rem; font-weight: bold; color: {'#ef4444' if is_out_of_stock else '#22c55e'}">
                                        <span>{'🔴 OUT OF STOCK' if is_out_of_stock else f'🍏 IN STOCK ({item["stock"]} Units)'}</span>
                                        <span style="color:#9ca3af;">{item['category']}</span>
                                    </div>
                                    <div class="product-title">{item['title']}</div>
                                    <div class="product-price">${item['price']:,.2f}</div>
                                    <p style="color: {text_sub}; font-size: 0.85rem; min-height: 45px;">{item['desc']}</p>
                                    <div style="background-color: {bg_app}; padding: 8px 12px; border-radius: 6px; font-size: 0.8rem; border: 1px solid {border_color}; color: {text_main}; font-family: monospace;">
                                        <b>Specs:</b> {item['specs']}
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                            
                            btn_col, _ = st.columns(2)
                            with btn_col:
                                if is_out_of_stock:
                                    st.button("Unavailable", key=f"shop_btn_{item['id']}", disabled=True, use_container_width=True)
                                else:
                                    if st.button("Procure Item", key=f"shop_btn_{item['id']}", type="primary", use_container_width=True):
                                        cart_current = st.session_state.shopping_cart.get(item["id"], 0)
                                        if cart_current < item["stock"]:
                                            st.session_state.shopping_cart[item["id"]] = cart_current + 1
                                            st.toast("🛒 Item added to procurement stack!")
                                            st.rerun()

            # Sidebar Procurement Order Processing Form
            st.sidebar.markdown("---")
            st.sidebar.markdown("### 🛒 Active Orders Summary")
            if not st.session_state.shopping_cart:
                st.sidebar.info("Procurement cart is empty.")
            else:
                subtotal = 0.0
                item_summary_list = []
                for item_id, qty in list(st.session_state.shopping_cart.items()):
                    item = next((x for x in st.session_state.company_inventory if x["id"] == item_id), None)
                    if item:
                        line_total = item["price"] * qty
                        subtotal += line_total
                        st.sidebar.write(f"🔹 **{item['title']}** (x{qty})")
                        item_summary_list.append({"title": item["title"], "qty": qty, "unit_price": item["price"]})
                
                st.sidebar.subheader(f"Total: ${subtotal:,.2f}")
                
                st.sidebar.markdown("#### 👤 Operational Shipping Dossier")
                with st.sidebar.form("checkout_dispatch_form"):
                    cust_name = st.text_input("Full Name / Enterprise*")
                    cust_phone = st.text_input("Contact Phone Number*")
                    cust_addr = st.text_input("Kigali Sector / Province Delivery Destination*")
                    
                    pay_method = st.selectbox("Preferred Payment Method*", [
                        "Mobile Money (MTN MoMo / Airtel Money)", 
                        "Bank Transfer (BK / I&M / Equity)", 
                        "Cash on Delivery", 
                        "Credit / Debit Card"
                    ])
                    
                    submit_order = st.form_submit_button("🚀 Finalize & Submit Order Request", type="primary", use_container_width=True)
                    if submit_order:
                        if cust_name and cust_phone and cust_addr:
                            order_ticket = {
                                "order_id": f"FTR-ORD-{datetime.now().strftime('%m%d%H%M%S')}",
                                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "customer_name": cust_name,
                                "customer_phone": cust_phone,
                                "customer_address": cust_addr,
                                "payment_method": pay_method,
                                "items": item_summary_list,
                                "total_amount": subtotal
                            }
                            
                            for cart_id, cart_qty in st.session_state.shopping_cart.items():
                                for inv_item in st.session_state.company_inventory:
                                    if inv_item["id"] == cart_id:
                                        inv_item["stock"] = max(0, inv_item["stock"] - cart_qty)
                            save_inventory()
                            
                            if save_order(order_ticket):
                                st.session_state.shopping_cart = {}
                                st.success("🎉 Order successfully logged into the database tracking manifest!")
                                st.balloons()
                                st.rerun()
                        else:
                            st.error("Please fill all mandatory validation entries.")

                if st.sidebar.button("Clear Order Queue", type="secondary", use_container_width=True):
                    st.session_state.shopping_cart = {}
                    st.rerun()

        # TAB 2: ABOUT US
        with nav_tabs[1]:
            st.markdown('<h1 class="hero-headline">About Future Technology Rwanda</h1>', unsafe_allow_html=True)
            st.write("""
            **Future Technology Rwanda (FTR)** is a premier technology manufacturer and enterprise distributor headquartered in Kigali, Rwanda. 
            We bridge engineering gaps across Sub-Saharan Africa by fabricating top-tier industrial electrical infrastructure, advanced 
            telecommunication telemetry modules, and production-grade software frameworks.
            """)

        # TAB 3: HOW IT WORKS
        with nav_tabs[2]:
            st.markdown('<h1 class="hero-headline">How Procurement Works</h1>', unsafe_allow_html=True)
            st.write("""
            Our specialized platform organizes high-level tech inventory acquisitions into three direct deployment stages:
            1. **Catalog Ingestion**: System engineers log into the encrypted authorization backend console panel to provision fresh devices.
            2. **Procurement Reservation**: Clients browse the storefront matrix via customizable filters.
            3. **Order Finalization**: B2B accounts confirm item quantities against active warehouse ceilings.
            """)

        # TAB 4: DEVELOPER PROFILE
        with nav_tabs[3]:
            st.markdown('<h1 class="hero-headline">System Architecture Profile</h1>', unsafe_allow_html=True)
            st.write("""
            ### Technical Stack Specifications:
            * **Framework Pipeline**: Streamlit Open-Source Framework
            * **Language Backbone**: Python 3.13 Production Ecosystem
            * **Contacts**: 0796286768
            * **Fullstack**: Ineza sangwa remy cedrick
            """)


    # --- PORTAL WORKSPACE B: ENCRYPTED MANAGEMENT FRAMEWORK ---
    elif st.session_state.app_mode == "🔒 Admin Dashboard":
        st.title("⚙️ FTR Overrides & Ingestion Terminal")
        password_input = st.text_input("Enter Engineer Authorization Key*", type="password")
        
        if password_input == "admin123":
            st.success("🔓 Access Authenticated.")
            
            tab_add, tab_edit, tab_stock, tab_orders = st.tabs(["➕ Ingest New Product", "📝 Modify Product & Image", "📊 Stock Management", "📦 View Orders Log"])
            
            # SUB-TAB 1: INGEST NEW PRODUCT
            with tab_add:
                st.write("### Register a New Product or Service Offering")
                with st.form("add_new_product_form", clear_on_submit=True):
                    new_title = st.text_input("Product Name*", placeholder="e.g., Fiber Optic Fusion Splicer Box")
                    new_category = st.selectbox("Classification*", ["Electronics & Telecom", "Electrical Technology", "Software Development"])
                    
                    col_p, col_s = st.columns(2)
                    with col_p:
                        new_price = st.number_input("Target Sales Price ($)", min_value=0.0, value=150.00)
                    with col_s:
                        new_stock = st.number_input("Initial Warehouse Qty", min_value=0, value=10)
                        
                    new_specs = st.text_input("Technical Specifications Sheet*", placeholder="e.g., Input 220V, Core Splicing 0.02dB")
                    new_desc = st.text_area("Detailed Scope/Description*")
                    uploaded_image_file = st.file_uploader("Upload Presentation Image (JPG/PNG)", type=["jpg", "jpeg", "png"], key="add_upload_img")
                    
                    if st.form_submit_button("Publish New Offering System", type="primary"):
                        if new_title and new_specs and new_desc:
                            new_id = f"PROD-0{len(st.session_state.company_inventory) + 1}"
                            saved_img_path = ""
                            
                            if uploaded_image_file is not None:
                                try:
                                    img = Image.open(uploaded_image_file)
                                    filename = f"{new_id}_{uploaded_image_file.name.replace(' ', '_')}"
                                    saved_img_path = os.path.join(IMAGE_DIR, filename)
                                    img.save(saved_img_path)
                                except Exception as e:
                                    st.error(f"Image saving failure: {e}")
                            
                            st.session_state.company_inventory.append({
                                "id": new_id, "title": new_title, "category": new_category, "price": new_price,
                                "specs": new_specs, "desc": new_desc, "stock": new_stock, "img_path": saved_img_path
                            })
                            
                            save_inventory()
                            st.success(f"🎉 System Ingested! Assigned SKU: {new_id}")
                            st.rerun()

            # SUB-TAB 2: MODIFY EXISTING PRODUCT
            with tab_edit:
                if not st.session_state.company_inventory:
                    st.info("The catalog database is empty. Ingest items first to unlock modifications.")
                else:
                    item_labels = [f"{i['id']} - {i['title']}" for i in st.session_state.company_inventory]
                    target_label = st.selectbox("Select Target SKU Registry to Modify:", item_labels)
                    target_id = target_label.split(" - ")[0]
                    item_idx = next((idx for idx, i in enumerate(st.session_state.company_inventory) if i["id"] == target_id), None)
                    
                    if item_idx is not None:
                        curr_item = st.session_state.company_inventory[item_idx]
                        with st.form("edit_product_overhaul_form"):
                            edit_title = st.text_input("Product Name", value=curr_item["title"])
                            edit_category = st.selectbox("Category", ["Electronics & Telecom", "Electrical Technology", "Software Development"], index=["Electronics & Telecom", "Electrical Technology", "Software Development"].index(curr_item["category"]))
                            edit_price = st.number_input("Unit Price ($)", min_value=0.0, value=float(curr_item["price"]))
                            edit_stock = st.number_input("Warehouse Stock Count", min_value=0, value=int(curr_item["stock"]))
                            edit_specs = st.text_input("Technical Specifications", value=curr_item["specs"])
                            edit_desc = st.text_area("Detailed System Description", value=curr_item["desc"])
                            new_uploaded_image = st.file_uploader("Upload replacement image file", type=["jpg", "jpeg", "png"], key="edit_upload_img")
                            
                            if st.form_submit_button("Save Modification Adjustments", type="primary"):
                                st.session_state.company_inventory[item_idx]["title"] = edit_title
                                st.session_state.company_inventory[item_idx]["category"] = edit_category
                                st.session_state.company_inventory[item_idx]["price"] = edit_price
                                st.session_state.company_inventory[item_idx]["stock"] = edit_stock
                                st.session_state.company_inventory[item_idx]["specs"] = edit_specs
                                st.session_state.company_inventory[item_idx]["desc"] = edit_desc
                                
                                if new_uploaded_image is not None:
                                    if curr_item["img_path"] and os.path.exists(curr_item["img_path"]):
                                        try: os.remove(curr_item["img_path"])
                                        except: pass
                                    try:
                                        img = Image.open(new_uploaded_image)
                                        new_filename = f"{curr_item['id']}_{new_uploaded_image.name.replace(' ', '_')}"
                                        new_path = os.path.join(IMAGE_DIR, new_filename)
                                        img.save(new_path)
                                        st.session_state.company_inventory[item_idx]["img_path"] = new_path
                                    except: pass
                                
                                save_inventory()
                                st.success("Registry overrides saved successfully!")
                                st.rerun()

            # SUB-TAB 3: STOCK MANAGEMENT FEATURE
            with tab_stock:
                st.write("### 📊 Warehouse Stock Control & Alerts")
                if not st.session_state.company_inventory:
                    st.info("No system components cataloged. Ingest items first to view metrics.")
                else:
                    stock_data = []
                    for i in st.session_state.company_inventory:
                        status = "🍏 Normal Operations"
                        if i["stock"] == 0:
                            status = "🔴 OUT OF STOCK"
                        elif i["stock"] <= 3:
                            status = "⚠️ LOW STOCK WARNING"
                        
                        stock_data.append({
                            "SKU ID": i["id"],
                            "Product Name": i["title"],
                            "Classification Category": i["category"],
                            "Units Available": i["stock"],
                            "Status Threshold": status
                        })
                    
                    st.dataframe(pd.DataFrame(stock_data), use_container_width=True, hide_index=True)
                    st.write("---")
                    
                    st.markdown("#### ⚡ Express Component Restock Panel")
                    stock_labels = [f"{i['id']} - {i['title']} (Current Qty: {i['stock']})" for i in st.session_state.company_inventory]
                    selected_stock_label = st.selectbox("Choose Target Component to Restock:", stock_labels)
                    target_stock_id = selected_stock_label.split(" - ")[0]
                    target_stock_idx = next((idx for idx, i in enumerate(st.session_state.company_inventory) if i["id"] == target_stock_id), None)
                    
                    if target_stock_idx is not None:
                        stock_item = st.session_state.company_inventory[target_stock_idx]
                        col_adj1, col_adj2 = st.columns(2)
                        with col_adj1:
                            new_qty_level = st.number_input("Set Absolute Warehouse Level", min_value=0, value=int(stock_item["stock"]), key="abs_stock")
                        with col_adj2:
                            st.write("<br>", unsafe_allow_html=True)
                            if st.button("Commit New Stock Target", type="primary", use_container_width=True):
                                st.session_state.company_inventory[target_stock_idx]["stock"] = new_qty_level
                                save_inventory()
                                st.success(f"Successfully updated warehouse stock levels for {stock_item['title']} to {new_qty_level} units.")
                                st.rerun()

            # SUB-TAB 4: VIEW & DELETE ORDERED PRODUCTS
            with tab_orders:
                st.write("### 📜 System Dispatch Manifest & Customer Invoices Log")
                orders_log = load_orders()
                
                if not orders_log:
                    st.info("No incoming customer orders have been logged by the database registry yet.")
                else:
                    col_clear, _ = st.columns([1, 2])
                    with col_clear:
                        if st.button("🗑️ Clear All Invoices Permanently", type="secondary", use_container_width=True):
                            if save_all_orders([]):
                                st.success("All historical database transaction registries cleared out safely.")
                                st.rerun()
                    st.write("---")

                    for order in reversed(orders_log):
                        st.markdown(f"""
                            <div class="order-manifest-box">
                                <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid {border_color}; padding-bottom:8px; margin-bottom:12px;">
                                    <span style="font-size:1.15rem; font-weight:800; color:#ff6b00;">📄 {order['order_id']}</span>
                                    <span style="font-size:0.85rem; color:{text_sub}; font-family:monospace;">⏳ logged: {order['timestamp']}</span>
                                </div>
                                <div style="margin-bottom:12px;">
                                    <h4 style="margin:0 0 5px 0; color:{text_main};">👤 Customer Identity & Contact Dossier:</h4>
                                    <table style="width:100%; font-size:0.9rem; color:{text_sub}; border-collapse:collapse;">
                                        <tr><td style="width:150px; font-weight:bold; padding:2px 0;">Name / Entity:</td><td>{order['customer_name']}</td></tr>
                                        <tr><td style="font-weight:bold; padding:2px 0;">Phone Access Line:</td><td>{order['customer_phone']}</td></tr>
                                        <tr><td style="font-weight:bold; padding:2px 0;">Destination Address:</td><td>{order['customer_address']}</td></tr>
                                        <tr><td style="font-weight:bold; padding:2px 0; color:#ff6b00;">Payment Gateway:</td><td style="font-weight:bold;">{order.get('payment_method', 'Cash / Unspecified (Legacy)')}</td></tr>
                                    </table>
                                </div>
                                <div style="margin-bottom: 12px;">
                                    <h4 style="margin:0 0 5px 0; color:{text_main};">📦 Procured System Equipment List:</h4>
                        """, unsafe_allow_html=True)
                        
                        df_items = pd.DataFrame(order["items"])
                        df_items.columns = ["Equipment Title", "Qty Requested", "Unit Price Base ($)"]
                        st.dataframe(df_items, use_container_width=True, hide_index=True)
                        
                        st.markdown(f"""
                                    <div style="text-align:right; font-size:1.1rem; font-weight:bold; margin-top:10px; color:{text_main};">
                                        Gross Transaction Invoiced: <span style="color:#22c55e;">${order['total_amount']:,.2f}</span>
                                    </div>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button(f"🗑️ Delete Record {order['order_id']}", key=f"del_{order['order_id']}", type="secondary"):
                            filtered_logs = [o for o in orders_log if o["order_id"] != order["order_id"]]
                            if save_all_orders(filtered_logs):
                                st.toast(f"Invoice {order['order_id']} removed from persistent files.")
                                st.rerun()

    # --- 3. NEW: NAVIGATION CONTROLS DASHBOARD PLACED PERMANENTLY AT THE BOTTOM ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.write("---")
    st.markdown("<h4 style='text-align: center; color: #94a3b8; font-weight: 700; letter-spacing: 0.5px;'>🧭 Platform Navigation Dashboard</h4>", unsafe_allow_html=True)
    
    nav_col1, nav_col2 = st.columns(2)
    with nav_col1:
        if st.session_state.app_mode == "🏬 Consumer View":
            if st.button("🔒 Switch Framework to Admin Dashboard Terminal", use_container_width=True, type="primary"):
                st.session_state.app_mode = "🔒 Admin Dashboard"
                st.rerun()
        else:
            if st.button("🏬 Switch Framework to Customer Marketplace View", use_container_width=True, type="primary"):
                st.session_state.app_mode = "🏬 Consumer View"
                st.rerun()
                
    with nav_col2:
        if st.button("❌ Terminate Current Session & Exit to Portal", use_container_width=True, type="secondary"):
            st.session_state.app_mode = "Portal"
            st.rerun()


# 4. RE-USABLE CORPORATE COPYRIGHT FOOTER NOTE AT THE VERY END
st.markdown(f"""
    <div class="corporate-footer">
        © {datetime.now().year} <b>Future Technology Rwanda Ltd.</b> All Rights Reserved.<br>
        <span style="opacity: 0.6; font-size: 0.75rem;">Providing Elite Hardware, Telecommunications Architecture, and Enterprise Software Systems. Kigali, Rwanda.</span>
    </div>
""", unsafe_allow_html=True)