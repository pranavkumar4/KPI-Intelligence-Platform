#!/usr/bin/env python3
"""
Test Suite for KPI Intelligence Platform
Validates core functionality
"""

import sys
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def test_data_processor():
    """Test DataProcessor module"""
    print("Testing Data Processor...")
    
    from modules.data_processor import DataProcessor
    
    # Create test data
    df = pd.DataFrame({
        'date': pd.date_range('2024-01-01', periods=100),
        'revenue': np.random.uniform(1000, 5000, 100),
        'cost': np.random.uniform(500, 3000, 100),
        'quantity': np.random.randint(10, 100, 100),
        'region': np.random.choice(['North', 'South'], 100)
    })
    
    processor = DataProcessor()
    cleaned_df, profile = processor.process_data(df)
    
    assert len(cleaned_df) > 0, "❌ No rows returned"
    assert 'quality_score' in profile, "❌ No quality score"
    assert profile['quality_score'] > 0, "❌ Invalid quality score"
    
    print("✅ Data Processor tests passed")
    return True

def test_kpi_detector():
    """Test KPIDetector module"""
    print("Testing KPI Detector...")
    
    from modules.kpi_detector import KPIDetector
    
    # Create test data
    df = pd.DataFrame({
        'revenue': np.random.uniform(1000, 5000, 100),
        'cost': np.random.uniform(500, 3000, 100),
        'quantity': np.random.randint(10, 100, 100),
        'status': np.random.choice(['Active', 'Inactive'], 100)
    })
    
    detector = KPIDetector()
    kpis = detector.detect_kpis(df)
    
    assert len(kpis) > 0, "❌ No KPIs detected"
    assert any(k['type'] == 'numeric' for k in kpis), "❌ No numeric KPIs"
    
    print(f"✅ KPI Detector tests passed - {len(kpis)} KPIs detected")
    return True

def test_kpi_dictionary():
    """Test KPIDictionaryGenerator module"""
    print("Testing KPI Dictionary Generator...")
    
    from modules.kpi_detector import KPIDetector
    from modules.kpi_dictionary import KPIDictionaryGenerator
    
    # Create test data
    df = pd.DataFrame({
        'revenue': np.random.uniform(1000, 5000, 100),
        'cost': np.random.uniform(500, 3000, 100)
    })
    
    detector = KPIDetector()
    kpis = detector.detect_kpis(df)
    
    generator = KPIDictionaryGenerator()
    dictionary = generator.generate_dictionary(df, kpis)
    
    assert len(dictionary) > 0, "❌ No dictionary entries"
    assert all('name' in d for d in dictionary), "❌ Missing KPI names"
    assert all('definition' in d for d in dictionary), "❌ Missing definitions"
    assert all('formula' in d for d in dictionary), "❌ Missing formulas"
    
    print(f"✅ KPI Dictionary tests passed - {len(dictionary)} entries")
    return True

def test_visualizer():
    """Test DashboardVisualizer module"""
    print("Testing Dashboard Visualizer...")
    
    from modules.visualizer import DashboardVisualizer
    
    # Create test data
    df = pd.DataFrame({
        'date': pd.date_range('2024-01-01', periods=100),
        'revenue': np.random.uniform(1000, 5000, 100),
        'cost': np.random.uniform(500, 3000, 100)
    })
    
    kpi_dict = [
        {'name': 'Revenue', 'type': 'numeric', 'category': 'Financial', 'current_value': '1000'}
    ]
    
    visualizer = DashboardVisualizer(df, kpi_dict)
    
    assert len(visualizer.get_numeric_columns()) > 0, "❌ No numeric columns found"
    assert len(visualizer.get_date_columns()) > 0, "❌ No date columns found"
    
    # Test chart creation
    fig = visualizer.create_distribution_chart()
    assert fig is not None, "❌ Failed to create distribution chart"
    
    print("✅ Visualizer tests passed")
    return True

def test_export_manager():
    """Test ExportManager module"""
    print("Testing Export Manager...")
    
    from modules.export_manager import ExportManager
    
    # Create test dictionary
    kpi_dict = [
        {
            'serial_number': 1,
            'name': 'Total Revenue',
            'definition': 'Sum of all revenue',
            'formula': 'SUM(revenue)',
            'type': 'numeric',
            'category': 'Financial',
            'current_value': '$10,000'
        }
    ]
    
    manager = ExportManager()
    excel_buffer = manager.export_kpi_dictionary(kpi_dict)
    
    assert excel_buffer is not None, "❌ Failed to create Excel buffer"
    assert excel_buffer.getbuffer().nbytes > 0, "❌ Empty Excel file"
    
    print("✅ Export Manager tests passed")
    return True

def test_integration():
    """Test full integration workflow"""
    print("Testing Full Integration...")
    
    from modules.data_processor import DataProcessor
    from modules.kpi_detector import KPIDetector
    from modules.kpi_dictionary import KPIDictionaryGenerator
    from modules.export_manager import ExportManager
    
    # Create realistic test data
    df = pd.DataFrame({
        'transaction_date': pd.date_range('2024-01-01', periods=100),
        'revenue': np.random.uniform(1000, 5000, 100),
        'cost': np.random.uniform(500, 3000, 100),
        'quantity': np.random.randint(10, 100, 100),
        'region': np.random.choice(['North', 'South', 'East', 'West'], 100)
    })
    
    # Step 1: Process data
    processor = DataProcessor()
    cleaned_df, profile = processor.process_data(df)
    assert len(cleaned_df) > 0, "❌ Data processing failed"
    
    # Step 2: Detect KPIs
    detector = KPIDetector()
    kpis = detector.detect_kpis(cleaned_df)
    assert len(kpis) > 0, "❌ KPI detection failed"
    
    # Step 3: Generate dictionary
    generator = KPIDictionaryGenerator()
    dictionary = generator.generate_dictionary(cleaned_df, kpis)
    assert len(dictionary) > 0, "❌ Dictionary generation failed"
    
    # Step 4: Export
    manager = ExportManager()
    excel_buffer = manager.export_kpi_dictionary(dictionary)
    assert excel_buffer.getbuffer().nbytes > 0, "❌ Export failed"
    
    print("✅ Full integration test passed")
    print(f"   - Processed {len(cleaned_df)} rows")
    print(f"   - Detected {len(kpis)} KPIs")
    print(f"   - Generated dictionary with {len(dictionary)} entries")
    print(f"   - Exported {excel_buffer.getbuffer().nbytes} bytes")
    
    return True

def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("KPI Intelligence Platform - Test Suite")
    print("=" * 60)
    print()
    
    tests = [
        test_data_processor,
        test_kpi_detector,
        test_kpi_dictionary,
        test_visualizer,
        test_export_manager,
        test_integration
    ]
    
    results = []
    
    for test in tests:
        try:
            result = test()
            results.append((test.__name__, result, None))
            print()
        except Exception as e:
            results.append((test.__name__, False, str(e)))
            print(f"❌ {test.__name__} failed: {e}")
            print()
    
    # Summary
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result, _ in results if result)
    total = len(results)
    
    for name, result, error in results:
        status = "✅ PASSED" if result else f"❌ FAILED: {error}"
        print(f"{name:.<50} {status}")
    
    print()
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("⚠️  Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(run_all_tests())
