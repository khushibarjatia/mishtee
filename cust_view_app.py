import gradio as gr
import pandas as pd
import requests
from supabase import create_client, Client

# --- 1. ASSETS & CREDENTIALS ---
URL = "https://zgyasgdmhkpyblztzbdz.supabase.co"
KEY = "sb_publishable_EdhxrfmlsK1RUQMntED1zQ_Ap2vDQAN"
LOGO_URL = "https://github.com/khushibarjatia/mishtee/blob/main/logo.jpg?raw=true"
CSS_URL = "https://raw.githubusercontent.com/khushibarjatia/mishtee/refs/heads/main/style.css"

# Initialize Supabase Client
supabase: Client = create_client(URL, KEY)

# Fetch Remote CSS
try:
    response = requests.get(CSS_URL)
    mishtee_css = response.text if response.status_code == 200 else ""
except Exception:
    mishtee_css = ""

# --- 2. LOGIC FUNCTIONS ---

def get_trending_products():
    """Fetches top 4 best-selling products."""
    try:
        response = supabase.table("orders").select("qty_kg, products(sweet_name, variant_type)").execute()
        if not response.data or len(response.data) == 0:
            return pd.DataFrame(columns=["Rank", "Sweet Name", "Variant", "Total Kg Sold"])
        
        df = pd.json_normalize(response.data)
        trending = df.groupby(['products.sweet_name', 'products.variant_type'])['qty_kg'].sum().reset_index()
        trending = trending.sort_values(by='qty_kg', ascending=False).head(4)
        trending.insert(0, 'Rank', range(1, len(trending) + 1))
        trending.columns = ["Rank", "Sweet Name", "Variant", "Total Kg Sold"]
        return trending
    except Exception:
        return pd.DataFrame({"Error": ["Could not load trending data"]})

def handle_login(phone_number):
    """Main Orchestrator for the Login logic."""
    if not phone_number or len(phone_number) < 10:
        return "Please enter a valid 10-digit mobile number.", pd.DataFrame(), get_trending_products()

    # Fetch Customer Name
    cust_res = supabase.table("customers").select("full_name").eq("phone", phone_number).execute()
    
    if not cust_res.data:
        greeting = "### Namaste! Welcome to MishTee-Magic. Please register to see your history."
        history_df = pd.DataFrame(columns=["Order ID", "Date", "Item", "Status"])
    else:
        name = cust_res.data[0]['full_name']
        greeting = f"### Namaste, {name} ji! Great to see you again."
        
        # Fetch Order History
        order_res = supabase.table("orders").select(
            "order_id, order_date, qty_kg, order_value_inr, status, products(sweet_name)"
        ).eq("cust_phone", phone_number).order("order_date", desc=True).execute()

        if order_res.data:
            flat_orders = []
            for r in order_res.data:
                flat_orders.append({
                    "Order ID": r['order_id'],
                    "Date": r['order_date'],
                    "Item": r['products']['sweet_name'],
                    "Qty (kg)": r['qty_kg'],
                    "Value (INR)": r['order_value_inr'],
                    "Status": r['status']
                })
            history_df = pd.DataFrame(flat_orders)
        else:
            history_df = pd.DataFrame(columns=["No orders found yet."])

    # Always refresh trending on login
    trending_df = get_trending_products()
    
    return greeting, history_df, trending_df

# --- 3. UI ARCHITECTURE (GRADIO BLOCKS) ---

with gr.Blocks(css=mishtee_css, title="MishTee-Magic | Artisanal Sweets") as app:
    
    # Header Section
    with gr.Row():
        with gr.Column(scale=1): pass
        with gr.Column(scale=2):
            gr.Image(LOGO_URL, show_label=False, container=False, interactive=False, height=120)
            gr.Markdown("<h3 style='text-align: center; color: #C06C5C;'>PURITY AND HEALTH</h3>")
        with gr.Column(scale=1): pass

    gr.HTML("<div style='height: 20px;'></div>") # Whitespace padding

    # Login Input
    with gr.Row():
        with gr.Column(scale=1): pass
        with gr.Column(scale=2):
            phone_input = gr.Textbox(label="LOGIN", placeholder="Enter mobile number (e.g. 9876543210)")
            login_btn = gr.Button("ACCESS THE MAGIC", variant="primary")
        with gr.Column(scale=1): pass

    # Welcome Message Area
    welcome_msg = gr.Markdown(visible=True)

    # Content Tabs
    with gr.Tabs():
        with gr.TabItem("MY ORDER HISTORY"):
            order_history_table = gr.Dataframe(interactive=False)
            
        with gr.TabItem("TRENDING TODAY"):
            trending_table = gr.Dataframe(value=get_trending_products(), interactive=False)

    # Footer
    gr.Markdown("<p style='text-align: center; font-size: 11px; margin-top: 50px;'>MODERN HERITAGE • A2 PURITY • ORGANIC INGREDIENTS</p>")

    # --- 4. EVENT TRIGGERS ---
    login_btn.click(
        fn=handle_login,
        inputs=[phone_input],
        outputs=[welcome_msg, order_history_table, trending_table]
    )

if __name__ == "__main__":
    app.launch()
