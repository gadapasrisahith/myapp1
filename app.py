import streamlit as st
import pandas as pd
import bst
import ai_model

# --- Page Config ---
st.set_page_config(page_title="IntelliStock", layout="wide")

# --- CRITICAL: Initialize Session State ---
if 'inventory' not in st.session_state:
    st.session_state.inventory = bst.BinarySearchTree()
    # Load initial fake data
    st.session_state.inventory.insert(101, "Apples", 50, "Aisle A - Rack 1")
    st.session_state.inventory.insert(102, "Bananas", 70, "Aisle A - Rack 2")
    st.session_state.inventory.insert(50, "Oranges", 30, "Aisle B - Rack 1")
    st.session_state.inventory.insert(200, "Grapes", 100, "Fridge Section")

# --- Sidebar ---
st.sidebar.title("IntelliStock Menu")
page_choice = st.sidebar.radio("Go to:", ["View Inventory", "Find Product", "Add Product", "Demand Forecast"])

# ==========================================
# PAGE 1: VIEW ALL INVENTORY
# ==========================================
if page_choice == "View Inventory":
    st.title("📦 All Inventory Items")
    
    all_products = st.session_state.inventory.get_all_products()
    
    if not all_products:
        st.warning("Inventory is empty.")
    else:
        # Display data including LOCATION
        data = [{"ID": p.id, "Name": p.name, "Stock": p.stock, "Location": p.location} for p in all_products]
        st.dataframe(data, use_container_width=True)

# ==========================================
# PAGE 2: FIND PRODUCT
# ==========================================
elif page_choice == "Find Product":
    st.title("🔎 Find Product")
    product_id_input = st.text_input("Enter Product ID:")
    
    if st.button("Search"):
        if product_id_input:
            product = st.session_state.inventory.find_product(product_id_input)
            if product:
                st.success("Product Found!")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(label=product.name, value=f"{product.stock} units", delta=f"ID: {product.id}")
                with col2:
                    st.info(f"📍 **Location:** {product.location}")
            else:
                st.error("Product not found.")

# ==========================================
# PAGE 3: ADD PRODUCT
# ==========================================
elif page_choice == "Add Product":
    st.title("➕ Add New Product")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        new_id = st.text_input("New ID (e.g., 305)")
    with col2:
        new_name = st.text_input("Product Name")
    with col3:
        new_stock = st.text_input("Stock Count")
    with col4:
        new_loc = st.text_input("Location (e.g. Aisle 5)")
        
    if st.button("Add to Inventory"):
        if new_id and new_name and new_stock and new_loc:
            try:
                # Try to add. If it returns True, success. If False, error.
                is_added = st.session_state.inventory.insert(int(new_id), new_name, int(new_stock), new_loc)
                
                if is_added:
                    st.success(f"Successfully added {new_name} at {new_loc}!")
                else:
                    st.error(f"⚠️ Error: Product ID {new_id} already exists! Please choose a different number.")
                    
            except ValueError:
                st.error("ID and Stock must be numbers.")
        else:
            st.warning("Please fill in all fields.")

# ==========================================
# PAGE 4: DEMAND FORECAST
# ==========================================
elif page_choice == "Demand Forecast":
    st.title("📈 AI Demand Forecast")
    
    product_list = ["Apples", "Bananas", "Oranges", "Grapes"]
    product_name = st.selectbox("Select Product:", product_list)
    
    if st.button("Predict Next Week"):
        prediction = ai_model.get_demand_prediction(product_name)
        if isinstance(prediction, str) and prediction.startswith("Error:"):
            st.error(prediction)
        else:
            st.success(f"Predicted Demand for {product_name}:")
            st.subheader(f"{prediction} units")