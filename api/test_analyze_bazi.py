#!/usr/bin/env python3
"""
Test script for /analyze_bazi endpoint
Demonstrates various usage scenarios
"""

import requests
import json
from datetime import date

# Base URL
BASE_URL = "http://localhost:8008"

def test_natal_only():
    """Test 1: Generate natal chart only (no analysis date)"""
    print("\n" + "="*60)
    print("TEST 1: Natal Chart Only")
    print("="*60)
    
    params = {
        "birth_date": "1990-01-15",
        "gender": "male",
        "birth_time": "13:45"
    }
    
    response = requests.get(f"{BASE_URL}/analyze_bazi", params=params)
    data = response.json()
    
    # Count nodes
    nodes = [k for k in data.keys() if k.startswith('hs_') or k.startswith('eb_')]
    
    print(f"Status: {response.status_code}")
    print(f"Total nodes: {len(nodes)}")
    print(f"Analysis info: {json.dumps(data['analysis_info'], indent=2)}")
    
    assert len(nodes) == 8, f"Expected 8 nodes, got {len(nodes)}"
    assert not data['analysis_info']['has_luck_pillar'], "Should not have luck pillar"
    print("✅ PASSED")


def test_natal_with_year():
    """Test 2: Generate natal + 10-year luck + annual"""
    print("\n" + "="*60)
    print("TEST 2: Natal + Year (Luck + Annual)")
    print("="*60)
    
    params = {
        "birth_date": "1990-01-15",
        "gender": "male",
        "birth_time": "13:45",
        "analysis_year": 2024,
        "include_annual_luck": True
    }
    
    response = requests.get(f"{BASE_URL}/analyze_bazi", params=params)
    data = response.json()
    
    nodes = [k for k in data.keys() if k.startswith('hs_') or k.startswith('eb_')]
    
    print(f"Status: {response.status_code}")
    print(f"Total nodes: {len(nodes)}")
    print(f"Has luck pillar: {data['analysis_info']['has_luck_pillar']}")
    print(f"Has annual: {data['analysis_info']['has_annual']}")
    
    # Check for specific nodes
    assert 'hs_10yl' in data, "Missing 10-year luck HS node"
    assert 'eb_10yl' in data, "Missing 10-year luck EB node"
    assert 'hs_yl' in data, "Missing annual HS node"
    assert 'eb_yl' in data, "Missing annual EB node"
    
    assert len(nodes) == 12, f"Expected 12 nodes, got {len(nodes)}"
    print("✅ PASSED")


def test_natal_with_year_month():
    """Test 3: Generate natal + luck + annual + monthly"""
    print("\n" + "="*60)
    print("TEST 3: Natal + Year + Month")
    print("="*60)
    
    params = {
        "birth_date": "1990-01-15",
        "gender": "female",
        "birth_time": "08:30",
        "analysis_year": 2024,
        "analysis_month": 11
    }
    
    response = requests.get(f"{BASE_URL}/analyze_bazi", params=params)
    data = response.json()
    
    nodes = [k for k in data.keys() if k.startswith('hs_') or k.startswith('eb_')]
    
    print(f"Status: {response.status_code}")
    print(f"Total nodes: {len(nodes)}")
    print(f"Has monthly: {data['analysis_info']['has_monthly']}")
    
    assert 'hs_ml' in data, "Missing monthly HS node"
    assert 'eb_ml' in data, "Missing monthly EB node"
    assert len(nodes) == 14, f"Expected 14 nodes, got {len(nodes)}"
    print("✅ PASSED")


def test_full_comparison():
    """Test 4: Generate all pillars (maximum 18 nodes)"""
    print("\n" + "="*60)
    print("TEST 4: Full Analysis (All Pillars)")
    print("="*60)
    
    params = {
        "birth_date": "1990-01-15",
        "gender": "male",
        "birth_time": "13:45",
        "analysis_year": 2024,
        "analysis_month": 11,
        "analysis_day": 25,
        "analysis_time": "14:30"
    }
    
    response = requests.get(f"{BASE_URL}/analyze_bazi", params=params)
    data = response.json()
    
    nodes = [k for k in data.keys() if k.startswith('hs_') or k.startswith('eb_')]
    
    print(f"Status: {response.status_code}")
    print(f"Total nodes: {len(nodes)}")
    print(f"Analysis info: {json.dumps(data['analysis_info'], indent=2)}")
    
    # Check all nodes exist
    expected_nodes = [
        'hs_y', 'eb_y', 'hs_m', 'eb_m', 'hs_d', 'eb_d', 'hs_h', 'eb_h',  # Natal
        'hs_10yl', 'eb_10yl',  # 10-year luck
        'hs_yl', 'eb_yl',  # Annual
        'hs_ml', 'eb_ml',  # Monthly
        'hs_dl', 'eb_dl',  # Daily
        'hs_hl', 'eb_hl'   # Hourly
    ]
    
    for node in expected_nodes:
        assert node in data, f"Missing node: {node}"
    
    assert len(nodes) == 18, f"Expected 18 nodes, got {len(nodes)}"
    print("✅ PASSED")


def test_interactions():
    """Test 5: Verify interactions are calculated"""
    print("\n" + "="*60)
    print("TEST 5: Interactions Calculated")
    print("="*60)
    
    params = {
        "birth_date": "1990-01-15",
        "gender": "male",
        "birth_time": "13:45",
        "analysis_year": 2024,
        "analysis_month": 11,
        "analysis_day": 25,
        "analysis_time": "14:00"
    }
    
    response = requests.get(f"{BASE_URL}/analyze_bazi", params=params)
    data = response.json()
    
    print(f"Status: {response.status_code}")
    print(f"Interactions found: {len(data.get('interactions', []))}")
    print(f"Has daymaster analysis: {'daymaster_analysis' in data}")
    print(f"Has element scores: {'post_element_score' in data}")
    
    # Check that interactions exist between nodes
    interactions = data.get('interactions', {})
    print(f"\nSample interactions (first 3):")
    
    # Interactions is a dict, convert values to list to slice
    interaction_list = list(interactions.values())
    for i, interaction in enumerate(interaction_list[:3]):
        print(f"  {i+1}. Type: {interaction.get('type')}, Pattern: {interaction.get('pattern')}")
    
    assert 'interactions' in data, "Missing interactions"
    assert 'daymaster_analysis' in data, "Missing daymaster analysis"
    assert 'base_element_score' in data, "Missing base element scores"
    assert 'post_element_score' in data, "Missing post element scores"
    print("✅ PASSED")


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("ANALYZE BAZI ENDPOINT TEST SUITE")
    print("="*60)
    
    try:
        test_natal_only()
        test_natal_with_year()
        test_natal_with_year_month()
        test_full_comparison()
        test_interactions()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED")
        print("="*60)
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return False
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to server at http://localhost:8008")
        print("Please start the server with: python run_bazingse.py")
        return False
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        return False
    
    return True


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
