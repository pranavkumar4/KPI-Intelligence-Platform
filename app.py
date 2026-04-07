"""
KPI Intelligence Platform
A production-ready application for automatic KPI detection, analysis, and dashboard generation.

Author: Expert Data Engineering Team
Version: 1.0.0
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io
import json
from typing import Dict, List, Tuple, Any, Optional
import re

# Page configuration
st.set_page_config(
    page_title="KPI Intelligence Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #6b7280;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .kpi-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }
    .success-box {
        background-color: #d1fae5;
        border-left: 4px solid #10b981;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fef3c7;
        border-left: 4px solid #f59e0b;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #dbeafe;
        border-left: 4px solid #3b82f6;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .stDownloadButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s;
    }
    .stDownloadButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
</style>
""", unsafe_allow_html=True)

# Import modules
from modules.data_processor import DataProcessor
from modules.kpi_detector import KPIDetector
from modules.kpi_dictionary import KPIDictionaryGenerator
from modules.visualizer import DashboardVisualizer
from modules.export_manager import ExportManager

# Initialize session state
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None
if 'kpi_dictionary' not in st.session_state:
    st.session_state.kpi_dictionary = None
if 'data_profile' not in st.session_state:
    st.session_state.data_profile = None
if 'upload_timestamp' not in st.session_state:
    st.session_state.upload_timestamp = None

def main():
    """Main application entry point"""
    
    # Sidebar navigation
    st.sidebar.title("🎯 Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["📁 Upload Data", "📊 KPI Dictionary", "📈 Analytics Dashboard", "⚙️ Settings"]
    )
    
    # Main header
    st.markdown('<div class="main-header">KPI Intelligence Platform</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Automated KPI Detection, Analysis & Insights Generation</div>', unsafe_allow_html=True)
    
    # Route to appropriate page
    if page == "📁 Upload Data":
        upload_page()
    elif page == "📊 KPI Dictionary":
        kpi_dictionary_page()
    elif page == "📈 Analytics Dashboard":
        dashboard_page()
    elif page == "⚙️ Settings":
        settings_page()

def upload_page():
    """File upload and data processing page"""
    
    st.header("📁 Upload Your Data")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="info-box">
        <strong>Supported Formats:</strong> CSV, Excel (.xlsx, .xls)<br>
        <strong>Max File Size:</strong> 200 MB<br>
        <strong>Expected Data:</strong> Business metrics, financial data, operational KPIs
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['csv', 'xlsx', 'xls'],
            help="Upload your dataset containing KPI-related information"
        )
    
    with col2:
        st.markdown("### Quick Stats")
        if st.session_state.processed_data is not None:
            data = st.session_state.processed_data
            st.metric("Total Rows", f"{len(data):,}")
            st.metric("Total Columns", len(data.columns))
            st.metric("Data Quality", f"{st.session_state.data_profile.get('quality_score', 0):.1f}%")
    
    if uploaded_file is not None:
        try:
            with st.spinner("🔄 Processing your data..."):
                # Initialize processor
                processor = DataProcessor()
                
                # Read file
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                
                st.success(f"✅ File loaded successfully: {uploaded_file.name}")
                
                # Process data
                processed_df, profile = processor.process_data(df)
                
                # Store in session state
                st.session_state.processed_data = processed_df
                st.session_state.data_profile = profile
                st.session_state.upload_timestamp = datetime.now()
                
                # Detect KPIs
                detector = KPIDetector()
                kpi_results = detector.detect_kpis(processed_df)
                
                # Generate KPI dictionary
                dict_generator = KPIDictionaryGenerator()
                kpi_dict = dict_generator.generate_dictionary(processed_df, kpi_results)
                st.session_state.kpi_dictionary = kpi_dict
                
            # Display data profile
            st.markdown("---")
            st.subheader("📋 Data Profile Summary")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h3 style="margin:0; font-size:1rem;">Rows Processed</h3>
                    <h2 style="margin:0.5rem 0 0 0;">{len(processed_df):,}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h3 style="margin:0; font-size:1rem;">Columns</h3>
                    <h2 style="margin:0.5rem 0 0 0;">{len(processed_df.columns)}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <h3 style="margin:0; font-size:1rem;">KPIs Detected</h3>
                    <h2 style="margin:0.5rem 0 0 0;">{len(kpi_results)}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                quality_score = profile.get('quality_score', 0)
                st.markdown(f"""
                <div class="metric-card">
                    <h3 style="margin:0; font-size:1rem;">Data Quality</h3>
                    <h2 style="margin:0.5rem 0 0 0;">{quality_score:.1f}%</h2>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Data quality details
            with st.expander("🔍 Detailed Data Quality Report", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### Missing Values Analysis")
                    missing_df = pd.DataFrame({
                        'Column': profile['missing_values'].keys(),
                        'Missing Count': profile['missing_values'].values(),
                        'Missing %': [f"{(v/len(processed_df)*100):.2f}%" for v in profile['missing_values'].values()]
                    })
                    st.dataframe(missing_df, use_container_width=True)
                
                with col2:
                    st.markdown("#### Data Type Distribution")
                    type_counts = pd.Series(profile['data_types']).value_counts()
                    fig = px.pie(
                        values=type_counts.values,
                        names=type_counts.index,
                        title="Column Data Types"
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            # Sample data preview
            with st.expander("👀 Data Preview (First 100 rows)", expanded=False):
                st.dataframe(processed_df.head(100), use_container_width=True)
            
            # Warnings and recommendations
            if profile.get('warnings'):
                st.markdown("---")
                st.markdown("### ⚠️ Data Quality Warnings")
                for warning in profile['warnings']:
                    st.warning(warning)
            
            if profile.get('recommendations'):
                st.markdown("### 💡 Recommendations")
                for rec in profile['recommendations']:
                    st.info(rec)
                    
        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")
            st.exception(e)
    
    else:
        # Show example/instructions when no file is uploaded
        st.markdown("---")
        st.markdown("### 📖 How to Use")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            #### 1️⃣ Upload Data
            - Select your CSV or Excel file
            - File is automatically validated
            - Data profiling runs instantly
            """)
        
        with col2:
            st.markdown("""
            #### 2️⃣ Review KPIs
            - Navigate to KPI Dictionary
            - Review detected KPIs
            - Download KPI catalog
            """)
        
        with col3:
            st.markdown("""
            #### 3️⃣ Analyze
            - Explore analytics dashboard
            - Interactive visualizations
            - Export insights
            """)

def kpi_dictionary_page():
    """KPI dictionary display and management page"""
    
    st.header("📊 KPI Dictionary")
    
    if st.session_state.kpi_dictionary is None:
        st.warning("⚠️ Please upload data first from the 'Upload Data' page.")
        return
    
    kpi_dict = st.session_state.kpi_dictionary
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total KPIs", len(kpi_dict))
    with col2:
        numeric_kpis = sum(1 for kpi in kpi_dict if kpi.get('type') == 'numeric')
        st.metric("Numeric KPIs", numeric_kpis)
    with col3:
        categorical_kpis = sum(1 for kpi in kpi_dict if kpi.get('type') == 'categorical')
        st.metric("Categorical KPIs", categorical_kpis)
    with col4:
        calculated_kpis = sum(1 for kpi in kpi_dict if kpi.get('is_calculated', False))
        st.metric("Calculated KPIs", calculated_kpis)
    
    st.markdown("---")
    
    # Filters
    col1, col2 = st.columns([1, 3])
    
    with col1:
        filter_type = st.selectbox(
            "Filter by Type",
            ["All", "Numeric", "Categorical", "Date", "Calculated"]
        )
    
    # Filter KPIs
    filtered_kpis = kpi_dict
    if filter_type != "All":
        filtered_kpis = [kpi for kpi in kpi_dict if kpi.get('type', '').lower() == filter_type.lower()]
    
    # Display KPI cards
    st.markdown("### KPI Catalog")
    
    for idx, kpi in enumerate(filtered_kpis, 1):
        with st.container():
            st.markdown(f"""
            <div class="kpi-card">
                <h4 style="margin:0 0 0.5rem 0; color: #667eea;">
                    {idx}. {kpi['name']}
                </h4>
                <p style="margin:0 0 0.5rem 0; color: #6b7280;">
                    <strong>Definition:</strong> {kpi['definition']}
                </p>
                <p style="margin:0 0 0.5rem 0; color: #6b7280;">
                    <strong>Formula:</strong> <code>{kpi['formula']}</code>
                </p>
                <div style="display: flex; gap: 1rem; margin-top: 0.5rem;">
                    <span style="background: #e0e7ff; padding: 0.25rem 0.75rem; border-radius: 12px; font-size: 0.85rem;">
                        Type: {kpi['type']}
                    </span>
                    <span style="background: #fef3c7; padding: 0.25rem 0.75rem; border-radius: 12px; font-size: 0.85rem;">
                        Category: {kpi.get('category', 'General')}
                    </span>
                    {f'<span style="background: #d1fae5; padding: 0.25rem 0.75rem; border-radius: 12px; font-size: 0.85rem;">Current Value: {kpi.get("current_value", "N/A")}</span>' if kpi.get('current_value') else ''}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Export section
    st.markdown("---")
    st.markdown("### 📥 Export KPI Dictionary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Download Excel", use_container_width=True):
            export_manager = ExportManager()
            excel_buffer = export_manager.export_kpi_dictionary(kpi_dict)
            
            st.download_button(
                label="💾 Save KPI Dictionary.xlsx",
                data=excel_buffer,
                file_name=f"KPI_Dictionary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    
    with col2:
        if st.button("📄 Download JSON", use_container_width=True):
            json_str = json.dumps(kpi_dict, indent=2)
            st.download_button(
                label="💾 Save KPI Dictionary.json",
                data=json_str,
                file_name=f"KPI_Dictionary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    with col3:
        if st.button("📋 Download CSV", use_container_width=True):
            df = pd.DataFrame(kpi_dict)
            csv_buffer = df.to_csv(index=False)
            st.download_button(
                label="💾 Save KPI Dictionary.csv",
                data=csv_buffer,
                file_name=f"KPI_Dictionary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

def dashboard_page():
    """Analytics dashboard with interactive visualizations"""
    
    st.header("📈 Analytics Dashboard")
    
    if st.session_state.processed_data is None:
        st.warning("⚠️ Please upload data first from the 'Upload Data' page.")
        return
    
    data = st.session_state.processed_data
    kpi_dict = st.session_state.kpi_dictionary
    
    # Initialize visualizer
    visualizer = DashboardVisualizer(data, kpi_dict)
    
    # Dashboard tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Overview",
        "📈 Trends",
        "🎯 KPI Performance",
        "🔍 Deep Dive"
    ])
    
    with tab1:
        overview_dashboard(visualizer, data, kpi_dict)
    
    with tab2:
        trends_dashboard(visualizer, data, kpi_dict)
    
    with tab3:
        kpi_performance_dashboard(visualizer, data, kpi_dict)
    
    with tab4:
        deep_dive_dashboard(visualizer, data, kpi_dict)

def overview_dashboard(visualizer, data, kpi_dict):
    """Overview dashboard tab"""
    
    st.subheader("📊 Executive Overview")
    
    # Top-level metrics
    numeric_kpis = [kpi for kpi in kpi_dict if kpi.get('type') == 'numeric']
    
    if numeric_kpis:
        cols = st.columns(min(4, len(numeric_kpis)))
        
        for idx, kpi in enumerate(numeric_kpis[:4]):
            with cols[idx]:
                value = kpi.get('current_value', 'N/A')
                st.metric(
                    label=kpi['name'],
                    value=value,
                    delta=kpi.get('change', None)
                )
    
    st.markdown("---")
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Data Distribution")
        fig = visualizer.create_distribution_chart()
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### KPI Category Breakdown")
        fig = visualizer.create_category_breakdown()
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    # Data summary table
    st.markdown("---")
    st.markdown("#### Data Summary Statistics")
    st.dataframe(visualizer.get_summary_statistics(), use_container_width=True)

def trends_dashboard(visualizer, data, kpi_dict):
    """Trends analysis dashboard tab"""
    
    st.subheader("📈 Trend Analysis")
    
    # Date column selection
    date_columns = visualizer.get_date_columns()
    
    if not date_columns:
        st.info("ℹ️ No date columns detected in the dataset. Trend analysis requires temporal data.")
        return
    
    selected_date_col = st.selectbox("Select Date Column", date_columns)
    
    # Metric selection
    numeric_cols = visualizer.get_numeric_columns()
    selected_metrics = st.multiselect(
        "Select Metrics to Track",
        numeric_cols,
        default=numeric_cols[:3] if len(numeric_cols) >= 3 else numeric_cols
    )
    
    if selected_metrics:
        # Time series visualization
        fig = visualizer.create_time_series(selected_date_col, selected_metrics)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        
        # Trend statistics
        st.markdown("---")
        st.markdown("#### Trend Statistics")
        
        trend_stats = visualizer.calculate_trend_statistics(selected_date_col, selected_metrics)
        if trend_stats is not None:
            st.dataframe(trend_stats, use_container_width=True)

def kpi_performance_dashboard(visualizer, data, kpi_dict):
    """KPI performance tracking dashboard tab"""
    
    st.subheader("🎯 KPI Performance Tracking")
    
    # KPI selector
    kpi_names = [kpi['name'] for kpi in kpi_dict if kpi.get('type') == 'numeric']
    
    if not kpi_names:
        st.info("ℹ️ No numeric KPIs available for performance tracking.")
        return
    
    selected_kpi = st.selectbox("Select KPI", kpi_names)
    
    # Find corresponding column
    kpi_data = next((kpi for kpi in kpi_dict if kpi['name'] == selected_kpi), None)
    
    if kpi_data:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"#### {selected_kpi}")
            st.markdown(f"**Definition:** {kpi_data['definition']}")
            st.markdown(f"**Formula:** `{kpi_data['formula']}`")
        
        with col2:
            st.metric(
                "Current Value",
                kpi_data.get('current_value', 'N/A'),
                delta=kpi_data.get('change', None)
            )
        
        # Performance visualization
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = visualizer.create_kpi_gauge(kpi_data)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = visualizer.create_kpi_histogram(kpi_data)
            if fig:
                st.plotly_chart(fig, use_container_width=True)

def deep_dive_dashboard(visualizer, data, kpi_dict):
    """Deep dive analysis dashboard tab"""
    
    st.subheader("🔍 Deep Dive Analysis")
    
    # Correlation analysis
    st.markdown("#### Correlation Matrix")
    
    numeric_cols = visualizer.get_numeric_columns()
    
    if len(numeric_cols) >= 2:
        selected_cols = st.multiselect(
            "Select Variables for Correlation Analysis",
            numeric_cols,
            default=numeric_cols[:5] if len(numeric_cols) >= 5 else numeric_cols
        )
        
        if len(selected_cols) >= 2:
            fig = visualizer.create_correlation_heatmap(selected_cols)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("ℹ️ Need at least 2 numeric columns for correlation analysis.")
    
    st.markdown("---")
    
    # Distribution comparison
    st.markdown("#### Distribution Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        x_col = st.selectbox("X-Axis", numeric_cols, key="x_axis")
    
    with col2:
        y_col = st.selectbox("Y-Axis", [col for col in numeric_cols if col != x_col], key="y_axis")
    
    if x_col and y_col:
        fig = visualizer.create_scatter_plot(x_col, y_col)
        if fig:
            st.plotly_chart(fig, use_container_width=True)

def settings_page():
    """Application settings and configuration page"""
    
    st.header("⚙️ Settings")
    
    st.markdown("### Application Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Data Processing")
        
        st.number_input(
            "Max Rows to Process",
            min_value=1000,
            max_value=1000000,
            value=100000,
            step=10000,
            help="Maximum number of rows to process from uploaded files"
        )
        
        st.number_input(
            "Missing Value Threshold (%)",
            min_value=0,
            max_value=100,
            value=50,
            help="Maximum acceptable percentage of missing values per column"
        )
        
        st.checkbox(
            "Auto-detect Date Columns",
            value=True,
            help="Automatically detect and parse date columns"
        )
        
        st.checkbox(
            "Remove Duplicates",
            value=True,
            help="Automatically remove duplicate rows during processing"
        )
    
    with col2:
        st.markdown("#### KPI Detection")
        
        st.number_input(
            "Min Unique Values for Categorical",
            min_value=2,
            max_value=100,
            value=10,
            help="Minimum unique values to classify as categorical"
        )
        
        st.number_input(
            "Max Unique Values for Categorical",
            min_value=10,
            max_value=1000,
            value=50,
            help="Maximum unique values to classify as categorical"
        )
        
        st.checkbox(
            "Enable Advanced KPI Detection",
            value=True,
            help="Use advanced heuristics for KPI detection"
        )
        
        st.checkbox(
            "Generate Calculated KPIs",
            value=True,
            help="Automatically generate calculated/derived KPIs"
        )
    
    st.markdown("---")
    
    st.markdown("### Export Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_input(
            "Default Export Filename Prefix",
            value="KPI_Report",
            help="Prefix for exported files"
        )
        
        st.selectbox(
            "Default Export Format",
            ["Excel (.xlsx)", "CSV", "JSON"],
            help="Default format for data exports"
        )
    
    with col2:
        st.checkbox(
            "Include Metadata in Exports",
            value=True,
            help="Include processing metadata in exported files"
        )
        
        st.checkbox(
            "Include Visualizations in Excel",
            value=True,
            help="Embed charts in Excel exports"
        )
    
    st.markdown("---")
    
    # System info
    st.markdown("### System Information")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Version:** 1.0.0")
    with col2:
        st.markdown("**Build:** 2024.04.07")
    with col3:
        st.markdown("**Status:** 🟢 Operational")
    
    # Clear cache button
    st.markdown("---")
    if st.button("🗑️ Clear Cache & Reset", type="secondary"):
        st.session_state.clear()
        st.success("✅ Cache cleared successfully!")
        st.experimental_rerun()

if __name__ == "__main__":
    main()
