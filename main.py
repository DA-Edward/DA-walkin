import streamlit as st
import json
import os
from datetime import datetime
import pandas as pd
from PIL import Image
import base64

# Page configuration
st.set_page_config(
    page_title="Customer Management System",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for iPad optimization and navy blue theme
st.markdown("""
<style>
    .main {
        background-color: #1e3a8a;
        color: white;
    }
    
    .stApp {
        background-color: #1e3a8a;
    }
    
    .customer-form {
        background-color: #2563eb;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .queue-item {
        background-color: #3b82f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #60a5fa;
    }
    
    .queue-item-assigned {
        background-color: #059669;
        border-left: 4px solid #10b981;
    }
    
    .logo-container {
        text-align: center;
        margin: 1rem 0 2rem 0;
    }
    
    .logo-container img {
        max-width: 300px;
        height: auto;
        border-radius: 10px;
    }
    
    .stButton button {
        background-color: #dc2626;
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-size: 16px;
        font-weight: bold;
        width: 100%;
    }
    
    .stButton button:hover {
        background-color: #b91c1c;
    }
    
    .success-button {
        background-color: #059669 !important;
    }
    
    .success-button:hover {
        background-color: #047857 !important;
    }
    
    .stTextInput input, .stTextArea textarea {
        background-color: #1e40af;
        color: white;
        border: 2px solid #3b82f6;
        border-radius: 8px;
        font-size: 16px;
        padding: 12px;
    }
    
    .stSelectbox select {
        background-color: #1e40af;
        color: white;
        border: 2px solid #3b82f6;
        border-radius: 8px;
        font-size: 16px;
        padding: 12px;
    }
    
    /* iPad optimizations */
    @media (max-width: 1024px) {
        .main .block-container {
            padding-top: 2rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }
        
        .customer-form {
            padding: 1.5rem;
        }
        
        .queue-item {
            padding: 1rem;
        }
        
        .stButton button {
            padding: 1rem 2rem;
            font-size: 18px;
        }
        
        .stTextInput input, .stTextArea textarea {
            font-size: 18px;
            padding: 16px;
        }
    }
    
    .metric-container {
        background-color: #2563eb;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem;
    }
    
    h1, h2, h3 {
        color: white !important;
    }
    
    .stMarkdown {
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Data file paths
QUEUE_FILE = "live_queue.json"
CUSTOMERS_FILE = "customers.json"
LOGO_FILES = ["logo.png", "logo.jpg", "logo.jpeg"]  # Supported logo formats

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'public'

# Data management functions
def load_data(filename):
    """Load data from JSON file"""
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_data(data, filename):
    """Save data to JSON file"""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def add_to_queue(customer_data):
    """Add customer to live queue"""
    queue = load_data(QUEUE_FILE)
    customer_data['id'] = len(queue) + 1
    customer_data['timestamp'] = datetime.now().isoformat()
    customer_data['status'] = 'waiting'
    queue.append(customer_data)
    save_data(queue, QUEUE_FILE)
    return True

def add_to_customers(customer_data):
    """Add customer to general customer list"""
    customers = load_data(CUSTOMERS_FILE)
    customer_data['id'] = len(customers) + 1
    customer_data['timestamp'] = datetime.now().isoformat()
    customers.append(customer_data)
    save_data(customers, CUSTOMERS_FILE)
    return True

def remove_from_queue(customer_id):
    """Remove customer from queue"""
    queue = load_data(QUEUE_FILE)
    queue = [customer for customer in queue if customer['id'] != customer_id]
    save_data(queue, QUEUE_FILE)

def display_logo():
    """Display logo if available"""
    logo_file = None
    for logo in LOGO_FILES:
        if os.path.exists(logo):
            logo_file = logo
            break
    
    if logo_file:
        try:
            image = Image.open(logo_file)
            st.markdown('<div class="logo-container">', unsafe_allow_html=True)
            st.image(image, width=300)
            st.markdown('</div>', unsafe_allow_html=True)
        except:
            st.markdown('<div class="logo-container"><h2>📝 Customer Management</h2></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="logo-container"><h2>📝 Customer Management</h2></div>', unsafe_allow_html=True)

# Authentication
def authenticate():
    """Handle authentication"""
    st.title("🔐 Backend Access")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        password = st.text_input("Enter Password", type="password", key="auth_password")
        
        if st.button("Login", key="login_btn"):
            if password == "admin123":  # Change this password as needed
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Invalid password!")

# Public form page
def public_form():
    """Display public customer form"""
    display_logo()
    
    st.title("🌟 Welcome! Please fill out your information")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="customer-form">', unsafe_allow_html=True)
        
        with st.form("customer_form", clear_on_submit=True):
            name = st.text_input("Full Name *", placeholder="Enter your full name")
            phone = st.text_input("Phone Number *", placeholder="Enter your phone number")
            
            col_date, col_time = st.columns(2)
            with col_date:
                date = st.date_input("Preferred Date")
            with col_time:
                time = st.time_input("Preferred Time")
            
            notes = st.text_area("Additional Notes", placeholder="Any special requests or notes?")
            
            submit_btn = st.form_submit_button("Submit Information")
            
            if submit_btn:
                if name and phone:
                    customer_data = {
                        'name': name,
                        'phone': phone,
                        'date': date.isoformat(),
                        'time': time.isoformat(),
                        'notes': notes
                    }
                    
                    # Add to both queue and customer list
                    add_to_queue(customer_data)
                    add_to_customers(customer_data)
                    
                    st.success("✅ Thank you! Your information has been submitted successfully.")
                    st.balloons()
                else:
                    st.error("Please fill in all required fields (Name and Phone)")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Navigation to backend (hidden button)
    if st.button("🔧", help="Backend Access", key="backend_access"):
        st.session_state.current_page = 'auth'
        st.rerun()

# Backend dashboard
def backend_dashboard():
    """Display backend dashboard"""
    display_logo()
    
    # Navigation
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("📋 Live Queue", key="nav_queue"):
            st.session_state.current_page = 'queue'
            st.rerun()
    with col2:
        if st.button("👥 All Customers", key="nav_customers"):
            st.session_state.current_page = 'customers'
            st.rerun()
    with col3:
        if st.button("🌐 Public Form", key="nav_public"):
            st.session_state.current_page = 'public'
            st.rerun()
    with col4:
        if st.button("🚪 Logout", key="logout"):
            st.session_state.authenticated = False
            st.session_state.current_page = 'public'
            st.rerun()
    
    st.markdown("---")
    
    # Display current page content
    if st.session_state.current_page == 'queue':
        display_live_queue()
    elif st.session_state.current_page == 'customers':
        display_all_customers()

def display_live_queue():
    """Display live queue management"""
    st.title("📋 Live Queue Management")
    
    queue = load_data(QUEUE_FILE)
    waiting_customers = [c for c in queue if c.get('status') == 'waiting']
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="metric-container"><h3>{len(waiting_customers)}</h3><p>Waiting</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-container"><h3>{len(queue)}</h3><p>Total Today</p></div>', unsafe_allow_html=True)
    with col3:
        avg_wait = "5-10 min" if len(waiting_customers) < 3 else "15-20 min"
        st.markdown(f'<div class="metric-container"><h3>{avg_wait}</h3><p>Est. Wait</p></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    if waiting_customers:
        st.subheader("🎯 Current Queue")
        
        for customer in waiting_customers:
            st.markdown('<div class="queue-item">', unsafe_allow_html=True)
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{customer['name']}**")
                st.markdown(f"📱 {customer['phone']}")
                st.markdown(f"📅 {customer['date']} at {customer['time']}")
                if customer.get('notes'):
                    st.markdown(f"📝 {customer['notes']}")
                st.markdown(f"⏰ Added: {datetime.fromisoformat(customer['timestamp']).strftime('%H:%M')}")
            
            with col2:
                if st.button("✅ Assign", key=f"assign_{customer['id']}"):
                    remove_from_queue(customer['id'])
                    st.success(f"Customer {customer['name']} has been assigned!")
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No customers in queue at the moment.")
        
    # Clear queue button
    if queue:
        st.markdown("---")
        if st.button("🗑️ Clear All Queue", key="clear_queue"):
            save_data([], QUEUE_FILE)
            st.success("Queue cleared!")
            st.rerun()

def display_all_customers():
    """Display all customers management"""
    st.title("👥 Customer Management")
    
    customers = load_data(CUSTOMERS_FILE)
    
    if customers:
        # Search functionality
        search_term = st.text_input("🔍 Search customers...", placeholder="Search by name or phone")
        
        if search_term:
            customers = [c for c in customers if 
                        search_term.lower() in c['name'].lower() or 
                        search_term.lower() in c['phone'].lower()]
        
        st.markdown(f"**Total Customers: {len(customers)}**")
        
        # Display customers in a table format
        if customers:
            df = pd.DataFrame(customers)
            df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d %H:%M')
            df = df[['name', 'phone', 'date', 'time', 'notes', 'timestamp']]
            df.columns = ['Name', 'Phone', 'Date', 'Time', 'Notes', 'Added']
            
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Export functionality
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"customers_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        else:
            st.info("No customers found matching your search.")
    else:
        st.info("No customers registered yet.")
    
    # Clear customers button
    if customers:
        st.markdown("---")
        if st.button("🗑️ Clear All Customers", key="clear_customers"):
            save_data([], CUSTOMERS_FILE)
            st.success("All customers cleared!")
            st.rerun()

# Main app logic
def main():
    if not st.session_state.authenticated and st.session_state.current_page in ['auth', 'queue', 'customers']:
        if st.session_state.current_page == 'auth':
            authenticate()
        else:
            st.session_state.current_page = 'public'
            st.rerun()
    elif st.session_state.authenticated and st.session_state.current_page in ['queue', 'customers']:
        backend_dashboard()
    else:
        public_form()

if __name__ == "__main__":
    main()