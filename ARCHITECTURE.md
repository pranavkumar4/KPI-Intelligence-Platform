# System Architecture & Design

## 🏗️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                      (Streamlit Web App)                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │  Upload  │  │   KPI    │  │Analytics │  │ Settings │      │
│  │   Page   │  │Dictionary│  │Dashboard │  │   Page   │      │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘      │
│                                                                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      BUSINESS LOGIC LAYER                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │     Data     │  │     KPI      │  │     KPI      │        │
│  │  Processor   │─▶│   Detector   │─▶│  Dictionary  │        │
│  └──────────────┘  └──────────────┘  │  Generator   │        │
│         │                             └──────────────┘        │
│         │                                      │               │
│         └──────────────────┬──────────────────┘               │
│                            │                                    │
│                            ▼                                    │
│         ┌──────────────────────────────────┐                  │
│         │      Dashboard Visualizer        │                  │
│         └──────────────────────────────────┘                  │
│                            │                                    │
│                            ▼                                    │
│         ┌──────────────────────────────────┐                  │
│         │       Export Manager             │                  │
│         └──────────────────────────────────┘                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                        DATA LAYER                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │  CSV     │  │  Excel   │  │  JSON    │  │  Session │      │
│  │  Files   │  │  Files   │  │  Export  │  │  State   │      │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🔄 Data Flow

### 1. Upload & Processing Flow
```
User Upload → File Validation → Type Detection → Data Cleaning
                                                        │
                                                        ▼
                                    ┌──────────────────────────┐
                                    │  Remove Duplicates       │
                                    │  Handle Missing Values   │
                                    │  Detect Outliers         │
                                    │  Calculate Quality Score │
                                    └──────────────────────────┘
                                                        │
                                                        ▼
                                              Cleaned DataFrame
```

### 2. KPI Detection Flow
```
Cleaned Data → Column Analysis → Pattern Matching → Categorization
                                                            │
                                                            ▼
                                    ┌────────────────────────────────┐
                                    │  Numeric KPIs (sum/mean/etc)   │
                                    │  Categorical KPIs (counts)     │
                                    │  Temporal KPIs (date ranges)   │
                                    │  Calculated KPIs (formulas)    │
                                    └────────────────────────────────┘
                                                            │
                                                            ▼
                                                    KPI Results List
```

### 3. Dictionary Generation Flow
```
KPI Results → Name Generation → Definition Creation → Formula Building
                                                              │
                                                              ▼
                                    ┌─────────────────────────────────┐
                                    │  Serial Number Assignment       │
                                    │  Business Definition            │
                                    │  Calculation Formula            │
                                    │  Category & Type                │
                                    │  Current Value Computation      │
                                    └─────────────────────────────────┘
                                                              │
                                                              ▼
                                                    KPI Dictionary
```

## 🧩 Module Breakdown

### 1. DataProcessor (`data_processor.py`)
**Responsibilities:**
- File parsing (CSV, Excel)
- Column name standardization
- Data type detection and conversion
- Missing value handling
- Duplicate removal
- Outlier detection
- Quality scoring

**Key Methods:**
- `process_data()`: Main processing pipeline
- `_clean_column_names()`: Standardize column names
- `_detect_and_convert_types()`: Auto type conversion
- `_handle_missing_values()`: Missing data strategy
- `_calculate_quality_score()`: 0-100 quality metric

### 2. KPIDetector (`kpi_detector.py`)
**Responsibilities:**
- Identify KPI candidates
- Categorize KPIs
- Calculate statistics
- Determine aggregation methods

**Key Methods:**
- `detect_kpis()`: Main detection engine
- `_detect_numeric_kpis()`: Find numeric metrics
- `_detect_categorical_kpis()`: Find categorical metrics
- `_detect_calculated_kpis()`: Generate derived KPIs
- `_categorize_kpi()`: Assign business category

### 3. KPIDictionaryGenerator (`kpi_dictionary.py`)
**Responsibilities:**
- Generate KPI names
- Create business definitions
- Build calculation formulas
- Format current values

**Key Methods:**
- `generate_dictionary()`: Create full catalog
- `_generate_kpi_name()`: Human-readable names
- `_generate_definition()`: Business descriptions
- `_generate_formula()`: Calculation expressions
- `_get_current_value()`: Compute current state

### 4. DashboardVisualizer (`visualizer.py`)
**Responsibilities:**
- Create interactive charts
- Generate visualizations
- Provide data summaries

**Key Methods:**
- `create_distribution_chart()`: Histogram
- `create_time_series()`: Trend lines
- `create_correlation_heatmap()`: Correlation matrix
- `create_kpi_gauge()`: Gauge chart
- `create_scatter_plot()`: XY scatter

### 5. ExportManager (`export_manager.py`)
**Responsibilities:**
- Excel export with formatting
- JSON serialization
- CSV generation
- Multi-sheet workbooks

**Key Methods:**
- `export_kpi_dictionary()`: Excel with formatting
- `export_data_with_kpis()`: Data + KPIs export
- `_prepare_dictionary_df()`: Format for export
- `_prepare_summary_df()`: Summary statistics

## 🎨 UI Design

### Page Structure
```
app.py
├── main()
│   ├── Sidebar Navigation
│   │   ├── 📁 Upload Data
│   │   ├── 📊 KPI Dictionary
│   │   ├── 📈 Analytics Dashboard
│   │   └── ⚙️ Settings
│   │
│   └── Page Router
│       ├── upload_page()
│       ├── kpi_dictionary_page()
│       ├── dashboard_page()
│       └── settings_page()
│
├── Dashboard Sub-tabs
│   ├── overview_dashboard()
│   ├── trends_dashboard()
│   ├── kpi_performance_dashboard()
│   └── deep_dive_dashboard()
```

### Component Hierarchy
```
App
├── Header
│   ├── Title
│   └── Subtitle
├── StepBar (Progress Indicator)
├── Page Content
│   ├── Upload Page
│   │   ├── File Upload Zone
│   │   ├── Data Profile Summary
│   │   └── Quality Report
│   │
│   ├── KPI Dictionary Page
│   │   ├── Summary Metrics
│   │   ├── Filter Controls
│   │   ├── KPI Cards
│   │   └── Export Buttons
│   │
│   ├── Analytics Dashboard
│   │   ├── Tab Navigation
│   │   ├── Charts (Plotly)
│   │   ├── Tables (Pandas)
│   │   └── Filters
│   │
│   └── Settings Page
│       ├── Configuration Forms
│       └── System Info
```

## 🔐 Security Architecture

### Defense Layers
```
┌─────────────────────────────────────┐
│   Input Validation                  │
│   - File type check                 │
│   - Size limits                     │
│   - Content validation              │
└───────────┬─────────────────────────┘
            │
            ▼
┌─────────────────────────────────────┐
│   Application Security              │
│   - XSRF protection                 │
│   - Session isolation               │
│   - No external API calls           │
└───────────┬─────────────────────────┘
            │
            ▼
┌─────────────────────────────────────┐
│   Container Security                │
│   - Non-root user                   │
│   - Minimal base image              │
│   - Health checks                   │
└───────────┬─────────────────────────┘
            │
            ▼
┌─────────────────────────────────────┐
│   Network Security                  │
│   - Firewall rules                  │
│   - HTTPS/SSL                       │
│   - Rate limiting (production)      │
└─────────────────────────────────────┘
```

## 📊 Performance Considerations

### Optimization Strategies

1. **Data Processing**
   - Pandas vectorization for speed
   - Efficient type conversions
   - Lazy evaluation where possible

2. **Memory Management**
   - Chunked file reading for large files
   - Garbage collection optimization
   - Session state management

3. **Rendering**
   - Streamlit caching (`@st.cache_data`)
   - Lazy chart rendering
   - Progressive loading

4. **Export**
   - Streaming Excel generation
   - BytesIO for memory efficiency
   - Batch processing for large datasets

## 🔄 State Management

### Session State Variables
```python
st.session_state = {
    'processed_data': DataFrame,      # Cleaned data
    'kpi_dictionary': List[Dict],     # KPI catalog
    'data_profile': Dict,             # Quality metrics
    'upload_timestamp': datetime,     # Processing time
    'thresholds': Dict,              # Filter settings
    'selected_kpis': List[str]       # User selections
}
```

## 🚀 Deployment Architecture

### Production Stack
```
                    ┌──────────────┐
                    │  Load        │
                    │  Balancer    │
                    └──────┬───────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
         ▼                 ▼                 ▼
    ┌─────────┐      ┌─────────┐      ┌─────────┐
    │ App     │      │ App     │      │ App     │
    │Instance1│      │Instance2│      │Instance3│
    └────┬────┘      └────┬────┘      └────┬────┘
         │                │                 │
         └────────────────┼─────────────────┘
                          │
                          ▼
                   ┌─────────────┐
                   │  Database   │
                   │  (Optional) │
                   └─────────────┘
```

## 📈 Scalability

### Horizontal Scaling
- Multiple app instances behind load balancer
- Session state stored in Redis (optional)
- Containerized with Docker

### Vertical Scaling
- Increase memory allocation
- Add CPU cores
- Optimize pandas operations

## 🧪 Testing Strategy

### Test Pyramid
```
                  ┌──────────────┐
                  │  Integration │  ← test_integration()
                  │    Tests     │
                  └──────────────┘
                 ┌────────────────┐
                 │  Component     │  ← test_*_module()
                 │    Tests       │
                 └────────────────┘
                ┌──────────────────┐
                │  Unit Tests      │  ← Individual functions
                └──────────────────┘
```

### Coverage Areas
- Data processing accuracy
- KPI detection correctness
- Dictionary generation completeness
- Visualization rendering
- Export functionality
- End-to-end workflow

---

**This architecture ensures scalability, maintainability, and production-readiness.**
