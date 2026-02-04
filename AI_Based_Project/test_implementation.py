"""
Test script for Database and Pydantic Models
Run this to test both components.
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from database.db_manager import DatabaseManager
from models.validation_models import ReportValidationModel, AnalysisMetadataModel
from datetime import datetime


def test_pydantic_models():
    """Test Pydantic validation models."""
    print("=" * 60)
    print("🧪 Testing Pydantic Models")
    print("=" * 60)
    
    # Test 1: ReportValidationModel
    print("\n1️⃣ Testing ReportValidationModel...")
    
    sample_report = """
# Apple Inc. (AAPL) - Business Analysis Report

## Executive Summary
Apple Inc. is a leading technology company with strong financial performance.
The company shows consistent growth and market leadership.

## Company Overview
Apple designs and manufactures consumer electronics, software, and services.

## Financial Analysis
- Current Price: $175.50
- P/E Ratio: 28.5
- Market Cap: $2.8T
- Revenue Growth: 5.2%

## Key Takeaways
1. Strong brand value
2. Consistent revenue growth
3. High profit margins
4. Strong cash position
5. Innovation leadership
"""
    
    try:
        report_model = ReportValidationModel(
            ticker="AAPL",
            company_name="Apple Inc.",
            report_content=sample_report,
            report_type="Full Analysis"
        )
        
        print("✅ ReportValidationModel created successfully!")
        print(f"   Ticker: {report_model.ticker}")
        print(f"   Word Count: {report_model.word_count}")
        print(f"   Completeness Score: {report_model.completeness_score:.2%}")
        print(f"   Structure Score: {report_model.structure_score:.2%}")
        print(f"   Sections Found: {len(report_model.sections_found)}")
        print(f"   Sections: {', '.join(report_model.sections_found[:5])}")
        
    except Exception as e:
        print(f"❌ ReportValidationModel failed: {e}")
        return False
    
    # Test 2: AnalysisMetadataModel
    print("\n2️⃣ Testing AnalysisMetadataModel...")
    
    try:
        metadata_model = AnalysisMetadataModel(
            ticker="AAPL",
            summary="Apple Inc. shows strong financial performance with consistent growth. The company maintains market leadership in technology sector.",
            key_decisions="Financial Analyst: Strong profitability. Competitor Analyst: Market leader. Report Writer: Positive outlook.",
            data_completeness=0.85,
            confidence_score=0.90
        )
        
        print("✅ AnalysisMetadataModel created successfully!")
        print(f"   Ticker: {metadata_model.ticker}")
        print(f"   Data Completeness: {metadata_model.data_completeness:.2%}")
        print(f"   Confidence Score: {metadata_model.confidence_score:.2%}")
        print(f"   Overall Quality: {metadata_model.calculate_overall_quality():.2%}")
        
    except Exception as e:
        print(f"❌ AnalysisMetadataModel failed: {e}")
        return False
    
    # Test 3: Validation Errors
    print("\n3️⃣ Testing Validation (Error Cases)...")
    
    try:
        # This should fail - ticker too long
        ReportValidationModel(
            ticker="A" * 20,  # Too long
            report_content="Test",
            report_type="Full Analysis"
        )
        print("❌ Should have failed validation!")
        return False
    except Exception as e:
        print(f"✅ Correctly caught validation error: {type(e).__name__}")
    
    try:
        # This should fail - report too short
        ReportValidationModel(
            ticker="AAPL",
            report_content="Short",  # Too short
            report_type="Full Analysis"
        )
        print("❌ Should have failed validation!")
        return False
    except Exception as e:
        print(f"✅ Correctly caught validation error: {type(e).__name__}")
    
    print("\n✅ All Pydantic model tests passed!")
    return True


def test_database():
    """Test database operations."""
    print("\n" + "=" * 60)
    print("🗄️  Testing Database Operations")
    print("=" * 60)
    
    db = DatabaseManager("test_business_analyst.db")  # Use test database
    
    try:
        # Test 1: Create Query
        print("\n1️⃣ Creating test query...")
        query_id = db.create_query(
            ticker="TSLA",
            company_name="Tesla Inc.",
            analysis_type="Full Analysis",
            period="1y"
        )
        print(f"✅ Query created with ID: {query_id}")
        
        # Test 2: Log Agent Actions
        print("\n2️⃣ Logging agent actions...")
        log_id1 = db.log_agent_action(
            query_id=query_id,
            agent_name="Stock Data Agent",
            action_summary="Fetched stock data for TSLA successfully"
        )
        log_id2 = db.log_agent_action(
            query_id=query_id,
            agent_name="Financial Analyst",
            action_summary="Analyzed financial metrics"
        )
        print(f"✅ Logged {log_id2 - log_id1 + 1} agent actions")
        
        # Test 3: Save Report
        print("\n3️⃣ Saving test report...")
        test_report = """
# Tesla Inc. (TSLA) - Business Analysis Report

## Executive Summary
Tesla is a leading electric vehicle manufacturer.

## Financial Analysis
- Current Price: $250.00
- Market Cap: $800B
- Revenue Growth: 15%

## Key Takeaways
1. Market leader in EVs
2. Strong growth trajectory
3. Innovation focus
"""
        report_id = db.save_report(
            query_id=query_id,
            ticker="TSLA",
            report_content=test_report,
            word_count=50
        )
        print(f"✅ Report saved with ID: {report_id}")
        
        # Test 4: Save Metadata
        print("\n4️⃣ Saving metadata...")
        metadata_id = db.save_metadata(
            query_id=query_id,
            key_decisions="Financial Analyst: Strong growth. Competitor Analyst: Market leader.",
            data_completeness=0.80,
            confidence_score=0.85,
            summary="Tesla shows strong performance in EV market with consistent growth."
        )
        print(f"✅ Metadata saved with ID: {metadata_id}")
        
        # Test 5: Update Query Status
        print("\n5️⃣ Updating query status...")
        db.update_query_status(query_id, "completed")
        print("✅ Query status updated to 'completed'")
        
        # Test 6: Retrieve Data
        print("\n6️⃣ Retrieving stored data...")
        
        query = db.get_query(query_id)
        print(f"✅ Retrieved query: {query['ticker']} - {query['status']}")
        
        report = db.get_report(report_id)
        print(f"✅ Retrieved report: {len(report['report_content'])} chars")
        
        metadata = db.get_metadata(query_id)
        print(f"✅ Retrieved metadata: {metadata['confidence_score']:.2%} confidence")
        
        logs = db.get_agent_logs(query_id)
        print(f"✅ Retrieved {len(logs)} agent logs")
        
        # Test 7: Get Reports by Ticker
        print("\n7️⃣ Getting reports by ticker...")
        reports = db.get_reports_by_ticker("TSLA", limit=5)
        print(f"✅ Found {len(reports)} reports for TSLA")
        
        # Test 8: Get Recent Queries
        print("\n8️⃣ Getting recent queries...")
        recent = db.get_recent_queries(limit=5)
        print(f"✅ Found {len(recent)} recent queries")
        
        # Test 9: Get Statistics
        print("\n9️⃣ Getting database statistics...")
        stats = db.get_stats()
        print("✅ Database Statistics:")
        for key, value in stats.items():
            print(f"   {key}: {value}")
        
        print("\n✅ All database tests passed!")
        
        # Cleanup test database
        import os
        if os.path.exists("test_business_analyst.db"):
            os.remove("test_business_analyst.db")
            print("\n🧹 Cleaned up test database")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Database test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_integration():
    """Test integration of validation + database."""
    print("\n" + "=" * 60)
    print("🔗 Testing Integration")
    print("=" * 60)
    
    db = DatabaseManager("test_integration.db")
    
    try:
        # Create query
        query_id = db.create_query("MSFT", "Microsoft", "Full Analysis", "1y")
        print(f"✅ Created query: {query_id}")
        
        # Create and validate report
        sample_report = """
# Microsoft (MSFT) - Business Analysis Report

## Executive Summary
Microsoft is a technology leader with strong cloud services.

## Financial Analysis
- Current Price: $380.00
- P/E Ratio: 32.0
- Revenue: $200B

## Key Takeaways
1. Cloud leadership
2. Strong financials
3. Innovation focus
"""
        
        report_model = ReportValidationModel(
            ticker="MSFT",
            company_name="Microsoft",
            report_content=sample_report,
            report_type="Full Analysis"
        )
        
        print(f"✅ Report validated - Completeness: {report_model.completeness_score:.2%}")
        
        # Save validated report
        report_id = db.save_report(
            query_id=query_id,
            ticker="MSFT",
            report_content=report_model.report_content,
            word_count=report_model.word_count
        )
        print(f"✅ Saved validated report: {report_id}")
        
        # Create and validate metadata
        metadata_model = AnalysisMetadataModel(
            ticker="MSFT",
            summary="Microsoft shows strong performance in cloud services with consistent revenue growth.",
            key_decisions="Financial Analyst: Strong profitability. Report Writer: Positive outlook.",
            data_completeness=report_model.completeness_score,
            confidence_score=(report_model.completeness_score + report_model.structure_score) / 2
        )
        
        metadata_id = db.save_metadata(
            query_id=query_id,
            key_decisions=metadata_model.key_decisions,
            data_completeness=metadata_model.data_completeness,
            confidence_score=metadata_model.confidence_score,
            summary=metadata_model.summary
        )
        print(f"✅ Saved validated metadata: {metadata_id}")
        
        # Update status
        db.update_query_status(query_id, "completed")
        print("✅ Integration test completed!")
        
        # Cleanup
        import os
        if os.path.exists("test_integration.db"):
            os.remove("test_integration.db")
            print("🧹 Cleaned up test database")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("\n" + "🚀 " * 20)
    print("TESTING DATABASE & PYDANTIC MODELS")
    print("🚀 " * 20 + "\n")
    
    results = []
    
    # Test Pydantic Models
    results.append(("Pydantic Models", test_pydantic_models()))
    
    # Test Database
    results.append(("Database", test_database()))
    
    # Test Integration
    results.append(("Integration", test_integration()))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    for name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{name}: {status}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\n🎉 All tests passed!")
    else:
        print("\n⚠️  Some tests failed. Check output above.")
    
    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

