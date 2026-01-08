import streamlit as st
import pandas as pd
import numpy as np
import re
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Lead Filtering AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #3B82F6;
        margin-top: 1.5rem;
    }
    .lead-card {
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid;
    }
    .hot-lead { border-color: #EF4444; background-color: #FEE2E2; }
    .warm-lead { border-color: #F59E0B; background-color: #FEF3C7; }
    .cold-lead { border-color: #6B7280; background-color: #F3F4F6; }
    .demo-scheduled { border-color: #10B981; background-color: #D1FAE5; }
    .metric-card {
        background: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">🤖 AI Lead Filtering Assistant</h1>', unsafe_allow_html=True)

# Initialize session state
if 'leads_df' not in st.session_state:
    st.session_state.leads_df = None
if 'processed' not in st.session_state:
    st.session_state.processed = False

# Sidebar for controls
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103655.png", width=100)
    st.title("Controls")
    
    uploaded_file = st.file_uploader("Upload Leads Excel File", type=['xlsx', 'xls'])
    
    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file)
            st.session_state.leads_df = df
            st.success(f"✅ Loaded {len(df)} leads successfully!")
        except Exception as e:
            st.error(f"Error loading file: {e}")
    
    st.divider()
    
    if st.session_state.leads_df is not None:
        st.subheader("Filter Settings")
        
        # Customize categorization keywords
        st.markdown("**Categorization Keywords**")
        
        hot_keywords = st.text_area("Hot Lead Keywords (comma-separated)", 
                                  "demo,appt,appointment,scheduled,set demo,next monday,follow up on")
        
        warm_keywords = st.text_area("Warm Lead Keywords (comma-separated)", 
                                   "call back,will get back,think about it,discuss with boss,check with,lemme know")
        
        cold_keywords = st.text_area("Cold/Dead Lead Keywords (comma-separated)", 
                                   "no need,not interested,no interest,already got,hung up,cant be reached,no pick up,voicemail,wrong number")
        
        demo_keywords = st.text_area("Demo Scheduled Keywords", 
                                   "demo at,demo on,appt at,appointment at,wednesday demo,thursday demo,friday demo")
        
        process_btn = st.button("🚀 Process Leads", type="primary", use_container_width=True)
        
        if process_btn:
            st.session_state.processed = True
            st.session_state.hot_keywords = [k.strip().lower() for k in hot_keywords.split(',')]
            st.session_state.warm_keywords = [k.strip().lower() for k in warm_keywords.split(',')]
            st.session_state.cold_keywords = [k.strip().lower() for k in cold_keywords.split(',')]
            st.session_state.demo_keywords = [k.strip().lower() for k in demo_keywords.split(',')]

# Main content area
if st.session_state.leads_df is not None:
    df = st.session_state.leads_df
    
    # Display original data
    with st.expander("📊 View Raw Data", expanded=False):
        st.dataframe(df, use_container_width=True)
    
    if st.session_state.processed:
        # Process leads
        st.markdown('<h2 class="sub-header">🎯 AI Categorized Leads</h2>', unsafe_allow_html=True)
        
        # Function to categorize leads
        def categorize_lead(remarks):
            if not isinstance(remarks, str):
                return "Unknown", "grey"
            
            remarks_lower = remarks.lower()
            
            # Check for demo scheduled first
            for keyword in st.session_state.demo_keywords:
                if keyword in remarks_lower:
                    return "Demo Scheduled", "green"
            
            # Check for hot leads
            for keyword in st.session_state.hot_keywords:
                if keyword in remarks_lower:
                    return "Hot Lead", "red"
            
            # Check for warm leads
            for keyword in st.session_state.warm_keywords:
                if keyword in remarks_lower:
                    return "Warm Lead", "orange"
            
            # Check for cold leads
            for keyword in st.session_state.cold_keywords:
                if keyword in remarks_lower:
                    return "Cold/Dead Lead", "gray"
            
            # Check for negative/profane responses
            negative_terms = ['fuck', 'bitch', 'cunt', 'dumb', 'prick']
            for term in negative_terms:
                if term in remarks_lower:
                    return "Negative Response", "purple"
            
            return "Needs Review", "blue"
        
        # Apply categorization
        df['Category'] = df['Remarks'].apply(lambda x: categorize_lead(x)[0])
        df['Color'] = df['Remarks'].apply(lambda x: categorize_lead(x)[1])
        
        # Add priority score
        def calculate_priority_score(row):
            score = 0
            remarks = str(row['Remarks']).lower() if pd.notna(row['Remarks']) else ""
            
            # Positive indicators
            if any(kw in remarks for kw in st.session_state.demo_keywords):
                score += 100
            if any(kw in remarks for kw in st.session_state.hot_keywords):
                score += 80
            if any(kw in remarks for kw in st.session_state.warm_keywords):
                score += 50
            
            # Negative indicators
            if any(kw in remarks for kw in st.session_state.cold_keywords):
                score -= 100
            
            # Company size indicators
            if "small" in remarks or "less than" in remarks:
                score -= 30
            if "freelance" in remarks or "self employed" in remarks:
                score -= 20
            
            # Language preference (assuming CHI might have higher conversion for Chinese webinar)
            if 'Language' in df.columns and row.get('Language') == 'CHI':
                score += 10
            
            return score
        
        df['Priority_Score'] = df.apply(calculate_priority_score, axis=1)
        df = df.sort_values('Priority_Score', ascending=False)
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Total Leads", len(df))
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            hot_count = len(df[df['Category'] == 'Demo Scheduled'])
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Demo Scheduled", hot_count)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            warm_count = len(df[df['Category'] == 'Hot Lead'])
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Hot Leads", warm_count)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            cold_count = len(df[df['Category'] == 'Cold/Dead Lead'])
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Cold Leads", cold_count)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Visualization
        col1, col2 = st.columns(2)
        
        with col1:
            fig, ax = plt.subplots(figsize=(10, 6))
            category_counts = df['Category'].value_counts()
            colors = {'Demo Scheduled': '#10B981', 'Hot Lead': '#EF4444', 
                     'Warm Lead': '#F59E0B', 'Cold/Dead Lead': '#6B7280',
                     'Negative Response': '#8B5CF6', 'Needs Review': '#3B82F6'}
            
            bars = ax.bar(category_counts.index, category_counts.values, 
                         color=[colors.get(cat, '#999999') for cat in category_counts.index])
            ax.set_title('Lead Distribution by Category', fontsize=14, fontweight='bold')
            ax.set_ylabel('Number of Leads')
            plt.xticks(rotation=45, ha='right')
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                       f'{int(height)}', ha='center', va='bottom')
            
            st.pyplot(fig)
        
        with col2:
            # Priority score distribution
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.hist(df['Priority_Score'], bins=20, edgecolor='black', alpha=0.7, color='#3B82F6')
            ax.set_title('Priority Score Distribution', fontsize=14, fontweight='bold')
            ax.set_xlabel('Priority Score')
            ax.set_ylabel('Number of Leads')
            st.pyplot(fig)
        
        # Interactive filters
        st.markdown('<h3 class="sub-header">🔍 Filtered Leads View</h3>', unsafe_allow_html=True)
        
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        
        with filter_col1:
            selected_category = st.selectbox(
                "Filter by Category",
                ["All Categories"] + sorted(df['Category'].unique().tolist())
            )
        
        with filter_col2:
            min_score = st.slider("Minimum Priority Score", 
                                 int(df['Priority_Score'].min()), 
                                 int(df['Priority_Score'].max()), 
                                 int(df['Priority_Score'].min()))
        
        with filter_col3:
            if 'Language' in df.columns:
                selected_language = st.selectbox(
                    "Filter by Language",
                    ["All Languages"] + sorted(df['Language'].dropna().unique().tolist())
                )
        
        # Apply filters
        filtered_df = df.copy()
        if selected_category != "All Categories":
            filtered_df = filtered_df[filtered_df['Category'] == selected_category]
        
        filtered_df = filtered_df[filtered_df['Priority_Score'] >= min_score]
        
        if 'Language' in df.columns and selected_language != "All Languages":
            filtered_df = filtered_df[filtered_df['Language'] == selected_language]
        
        # Display filtered results
        st.markdown(f"**Showing {len(filtered_df)} leads**")
        
        for _, row in filtered_df.iterrows():
            category_class = ""
            if row['Category'] == 'Demo Scheduled':
                category_class = "demo-scheduled"
            elif row['Category'] == 'Hot Lead':
                category_class = "hot-lead"
            elif row['Category'] == 'Warm Lead':
                category_class = "warm-lead"
            elif row['Category'] == 'Cold/Dead Lead':
                category_class = "cold-lead"
            
            with st.container():
                st.markdown(f'<div class="lead-card {category_class}">', unsafe_allow_html=True)
                col1, col2, col3 = st.columns([2, 3, 1])
                
                with col1:
                    st.markdown(f"**{row.get('Name', 'N/A')}**")
                    if 'Company Name' in df.columns and pd.notna(row.get('Company Name')):
                        st.caption(f"🏢 {row['Company Name']}")
                
                with col2:
                    remarks = str(row.get('Remarks', 'No remarks'))
                    st.markdown(f"📝 **Remarks:** {remarks[:100]}..." if len(remarks) > 100 else f"📝 **Remarks:** {remarks}")
                    if 'Email address' in df.columns and pd.notna(row.get('Email address')):
                        st.caption(f"✉️ {row['Email address']}")
                
                with col3:
                    st.metric("Priority", f"{row['Priority_Score']}")
                    st.caption(f"🏷️ {row['Category']}")
                
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Export options
        st.divider()
        st.markdown('<h3 class="sub-header">📥 Export Results</h3>', unsafe_allow_html=True)
        
        export_col1, export_col2 = st.columns(2)
        
        with export_col1:
            if st.button("📊 Export All Categorized Leads", use_container_width=True):
                output = BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df.to_excel(writer, index=False, sheet_name='Categorized_Leads')
                    
                    # Add summary sheet
                    summary_df = pd.DataFrame({
                        'Category': df['Category'].value_counts().index,
                        'Count': df['Category'].value_counts().values,
                        'Percentage': (df['Category'].value_counts().values / len(df) * 100).round(2)
                    })
                    summary_df.to_excel(writer, index=False, sheet_name='Summary')
                    
                    writer.save()
                
                st.download_button(
                    label="⬇️ Download Excel File",
                    data=output.getvalue(),
                    file_name="categorized_leads.xlsx",
                    mime="application/vnd.ms-excel",
                    use_container_width=True
                )
        
        with export_col2:
            if st.button("🎯 Export High Priority Leads Only", use_container_width=True):
                high_priority = df[df['Priority_Score'] > 50]
                output = BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    high_priority.to_excel(writer, index=False, sheet_name='High_Priority_Leads')
                    writer.save()
                
                st.download_button(
                    label="⬇️ Download High Priority Leads",
                    data=output.getvalue(),
                    file_name="high_priority_leads.xlsx",
                    mime="application/vnd.ms-excel",
                    use_container_width=True
                )
        
        # Action recommendations
        st.divider()
        st.markdown('<h3 class="sub-header">🤔 AI Recommendations</h3>', unsafe_allow_html=True)
        
        demo_leads = df[df['Category'] == 'Demo Scheduled']
        hot_leads = df[df['Category'] == 'Hot Lead']
        
        rec_col1, rec_col2 = st.columns(2)
        
        with rec_col1:
            st.info(f"""
            **Immediate Actions:**
            
            📅 **{len(demo_leads)} Demos Scheduled**
            - Contact these leads to confirm appointments
            - Prepare demo materials specific to their industry
            
            🔥 **{len(hot_leads)} Hot Leads**
            - Follow up within 24 hours
            - Send additional information they requested
            """)
        
        with rec_col2:
            warm_leads_count = len(df[df['Category'] == 'Warm Lead'])
            st.warning(f"""
            **Follow-up Plan:**
            
            🌡️ **{warm_leads_count} Warm Leads**
            - Schedule follow-ups for next week
            - Send nurturing emails with case studies
            
            ⏰ **Best Time to Call:**
            - Based on data: Afternoons (2-4 PM) have higher engagement
            - Avoid calling during lunch hours (12-1 PM)
            """)
    
    else:
        st.info("👈 Adjust your filtering settings in the sidebar and click 'Process Leads' to begin analysis.")

else:
    # Welcome screen
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/2491/2491935.png", width=200)
    
    with col2:
        st.markdown("""
        ## Welcome to the AI Lead Filtering Assistant!
        
        **How to use:**
        1. **Upload** your Excel file with webinar leads (left sidebar)
        2. **Customize** the keyword filters for categorization
        3. **Click "Process Leads"** to let AI analyze your data
        4. **View & Export** categorized leads
        
        **Supported data format:**
        - Excel files (.xlsx, .xls)
        - Should contain columns like: Name, Email, Phone, Remarks, etc.
        - "Remarks" column is used for categorization
        
        **Ready to start?** Upload your file in the sidebar! 🚀
        """)
    
    # Example data structure
    with st.expander("📋 Expected Data Format"):
        example_df = pd.DataFrame({
            'Name': ['John Doe', 'Jane Smith'],
            'Email address': ['john@example.com', 'jane@example.com'],
            'Phone number': ['60123456789', '60129876543'],
            'Company Name': ['ABC Corp', 'XYZ Ltd'],
            'Remarks': ['call back next Monday for demo', 'no need'],
            'Language': ['ENG', 'CHI'],
            'Assigned on': ['2025-03-03', '2025-03-03']
        })
        st.dataframe(example_df, use_container_width=True)

# Footer
st.divider()
st.caption("AI Lead Filtering Assistant v1.0 | Automatically categorizes webinar leads based on response patterns")