# KPI Intelligence Platform

A production-ready web application for automatic KPI detection, analysis, and dashboard generation from business datasets.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

## 🎯 Features

### Core Functionality
- **📁 Smart File Upload**: Supports CSV, Excel (.xlsx, .xls) up to 200 MB
- **🧹 Automatic Data Cleaning**: Intelligent type detection, missing value handling, outlier detection
- **🔍 Intelligent KPI Detection**: Heuristic-based identification of numeric, categorical, and temporal KPIs
- **📊 KPI Dictionary Generation**: Automatic generation of KPI names, definitions, and formulas
- **📈 Interactive Dashboard**: Real-time visualizations with Plotly
- **📥 Multi-Format Export**: Excel, JSON, CSV export capabilities

### Advanced Features
- **Data Quality Assessment**: Comprehensive data profiling with quality scores
- **Calculated KPIs**: Automatic generation of derived metrics (margins, ratios, growth rates)
- **Trend Analysis**: Time series analysis and forecasting
- **Correlation Analysis**: Interactive correlation heatmaps
- **Custom Visualizations**: Distribution charts, gauges, histograms

## 📋 Requirements

### System Requirements
- Python 3.11 or higher
- 4GB RAM minimum (8GB recommended for large datasets)
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Python Dependencies
See `requirements.txt` for complete list. Key packages:
- streamlit==1.32.0
- pandas==2.2.1
- plotly==5.20.0
- openpyxl==3.1.2
- xlsxwriter==3.2.0
- scikit-learn==1.4.1

## 🚀 Quick Start

### Option 1: Local Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd kpi-intelligence-platform
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
streamlit run app.py
```

5. **Access the application**
Open your browser and navigate to `http://localhost:8501`

### Option 2: Docker Deployment

1. **Build and run with Docker Compose**
```bash
docker-compose up -d
```

2. **Access the application**
Navigate to `http://localhost:8501`

3. **View logs**
```bash
docker-compose logs -f
```

4. **Stop the application**
```bash
docker-compose down
```

### Option 3: Docker Manual Build

```bash
# Build the image
docker build -t kpi-platform:latest .

# Run the container
docker run -p 8501:8501 kpi-platform:latest
```

## 📖 User Guide

### Step 1: Upload Data
1. Navigate to **"📁 Upload Data"** page
2. Upload your CSV or Excel file (max 200 MB)
3. System automatically:
   - Cleans column names
   - Detects data types
   - Handles missing values
   - Removes duplicates
   - Calculates quality score

### Step 2: Review KPI Dictionary
1. Navigate to **"📊 KPI Dictionary"** page
2. Review automatically detected KPIs:
   - Serial number
   - KPI name (human-readable)
   - Business definition
   - Calculation formula
   - Current value
   - Category and type
3. Filter KPIs by type (Numeric, Categorical, Date, Calculated)
4. Export dictionary in Excel, JSON, or CSV format

### Step 3: Analyze Data
1. Navigate to **"📈 Analytics Dashboard"** page
2. Explore four dashboard tabs:
   - **Overview**: Executive summary with key metrics
   - **Trends**: Time series analysis
   - **KPI Performance**: Individual KPI tracking
   - **Deep Dive**: Correlation and distribution analysis
3. Interactive visualizations update in real-time

### Step 4: Export Results
- Download KPI dictionary from the KPI Dictionary page
- Export includes:
  - Complete KPI catalog
  - Summary statistics
  - Metadata (generation time, counts)

## 🏗️ Architecture

```
kpi-intelligence-platform/
├── app.py                      # Main Streamlit application
├── modules/
│   ├── data_processor.py       # Data cleaning and profiling
│   ├── kpi_detector.py         # KPI detection engine
│   ├── kpi_dictionary.py       # Dictionary generation
│   ├── visualizer.py           # Dashboard visualizations
│   └── export_manager.py       # Export functionality
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Container definition
├── docker-compose.yml          # Docker Compose configuration
├── .streamlit/
│   └── config.toml            # Streamlit configuration
└── README.md                  # This file
```

## 🔧 Configuration

### Streamlit Configuration
Edit `.streamlit/config.toml` to customize:
- Theme colors
- Server port
- Max upload size
- Performance settings

### Application Settings
Access via **"⚙️ Settings"** page:
- Data processing thresholds
- KPI detection parameters
- Export preferences
- Cache management

## 📊 KPI Detection Logic

### Numeric KPIs
- Automatically detected from numeric columns
- Categorized as: Financial, Operational, Performance, Quality
- Statistics calculated: mean, median, min, max, std, sum
- Aggregation method auto-determined (sum vs. mean)

### Categorical KPIs
- Detected from object/category columns with 2-50 unique values
- Distribution analysis
- Mode identification
- Frequency counting

### Calculated KPIs
Automatically generated:
- **Revenue per Unit**: Total Revenue / Total Units
- **Profit Margin**: (Revenue - Cost) / Revenue × 100
- **Growth Rate**: (Final - Initial) / Initial × 100

### Temporal KPIs
- Date range analysis
- Trend calculation
- Period comparison

## 🔒 Security Features

- Non-root Docker user
- XSRF protection enabled
- No external data transmission
- Local processing only
- Session-based data storage

## 🚀 Deployment

### Cloud Deployment Options

#### AWS (Elastic Beanstalk)
```bash
# Initialize EB application
eb init -p python-3.11 kpi-platform

# Create environment
eb create kpi-production

# Deploy
eb deploy
```

#### Google Cloud Run
```bash
# Build and push to Container Registry
gcloud builds submit --tag gcr.io/PROJECT_ID/kpi-platform

# Deploy to Cloud Run
gcloud run deploy kpi-platform \
  --image gcr.io/PROJECT_ID/kpi-platform \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

#### Azure Container Instances
```bash
# Login to Azure
az login

# Create container instance
az container create \
  --resource-group myResourceGroup \
  --name kpi-platform \
  --image kpi-platform:latest \
  --dns-name-label kpi-platform \
  --ports 8501
```

#### Heroku
```bash
# Login to Heroku
heroku login

# Create app
heroku create kpi-platform

# Set stack to container
heroku stack:set container

# Deploy
git push heroku main
```

## 🧪 Testing

Run data quality tests:
```python
# In Python shell
from modules.data_processor import DataProcessor
import pandas as pd

# Load test data
df = pd.read_csv('sample_data.csv')

# Process
processor = DataProcessor()
clean_df, profile = processor.process_data(df)

# Check quality
print(f"Quality Score: {profile['quality_score']}")
```

## 📈 Performance Optimization

### For Large Datasets
1. **Pre-filter data**: Upload only relevant columns/rows
2. **Increase memory**: Allocate more RAM to Docker container
3. **Batch processing**: Split large files into smaller chunks
4. **Adjust settings**: Reduce max rows in Settings page

### Optimization Tips
- Use CSV instead of Excel for faster loading
- Remove unnecessary columns before upload
- Filter date ranges to reduce data volume
- Enable caching in Streamlit config

## 🐛 Troubleshooting

### Common Issues

**Issue**: File upload fails
- **Solution**: Check file size (max 200 MB), verify format (CSV/Excel)

**Issue**: KPIs not detected
- **Solution**: Ensure columns have numeric data, check column names

**Issue**: Charts not displaying
- **Solution**: Clear browser cache, check date column formats

**Issue**: Export fails
- **Solution**: Check disk space, verify write permissions

### Debug Mode
Enable debug logging:
```bash
streamlit run app.py --logger.level=debug
```

## 📝 Sample Data Format

Expected data structure:

| date       | revenue | cost  | units | region | status   |
|------------|---------|-------|-------|--------|----------|
| 2024-01-01 | 10000   | 6000  | 100   | North  | Complete |
| 2024-01-02 | 12000   | 7200  | 120   | South  | Complete |
| 2024-01-03 | 8000    | 5000  | 80    | East   | Pending  |

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 👥 Support

For issues and questions:
- Create an issue on GitHub
- Email: support@example.com
- Documentation: [Link to docs]

## 🗺️ Roadmap

### Version 1.1 (Q2 2024)
- [ ] NLP-powered KPI detection
- [ ] Multi-tenancy support
- [ ] Role-based access control
- [ ] Database integration (PostgreSQL)
- [ ] API endpoints for integration

### Version 1.2 (Q3 2024)
- [ ] Machine learning predictions
- [ ] Automated anomaly detection
- [ ] Custom KPI builder
- [ ] Scheduled reports
- [ ] Email notifications

### Version 2.0 (Q4 2024)
- [ ] Real-time data streaming
- [ ] Collaborative features
- [ ] Mobile app
- [ ] Advanced AI insights
- [ ] Enterprise SSO integration

## 📞 Contact

**Project Maintainer**: Expert Data Engineering Team
**Email**: team@example.com
**Website**: https://example.com

---

**Built with ❤️ using Python, Streamlit, and Plotly**
