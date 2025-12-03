#!/bin/bash

# Test script for /analyze_bazi endpoint using curl

BASE_URL="http://localhost:8008"
PASSED=0
FAILED=0

echo "============================================================"
echo "BAZI ANALYSIS ENDPOINT TEST SUITE"
echo "============================================================"

# Test 1: Natal only
echo ""
echo "============================================================"
echo "TEST 1: Natal Chart Only"
echo "============================================================"
RESPONSE=$(curl -s "${BASE_URL}/analyze_bazi?birth_date=1990-01-15&gender=male&birth_time=13:45")
NODE_COUNT=$(echo "$RESPONSE" | python3 -c "import sys, json; data = json.load(sys.stdin); nodes = [k for k in data if k.startswith('hs_') or k.startswith('eb_')]; print(len(nodes))")
HAS_LUCK=$(echo "$RESPONSE" | python3 -c "import sys, json; data = json.load(sys.stdin); print(data['analysis_info']['has_luck_pillar'])")

echo "Total nodes: $NODE_COUNT"
echo "Has luck pillar: $HAS_LUCK"

if [ "$NODE_COUNT" == "8" ] && [ "$HAS_LUCK" == "False" ]; then
    echo "✅ PASSED"
    ((PASSED++))
else
    echo "❌ FAILED: Expected 8 nodes and no luck pillar"
    ((FAILED++))
fi

# Test 2: Natal + Year
echo ""
echo "============================================================"
echo "TEST 2: Natal + Year (Luck + Annual)"
echo "============================================================"
RESPONSE=$(curl -s "${BASE_URL}/analyze_bazi?birth_date=1990-01-15&gender=male&birth_time=13:45&analysis_year=2024")
NODE_COUNT=$(echo "$RESPONSE" | python3 -c "import sys, json; data = json.load(sys.stdin); nodes = [k for k in data if k.startswith('hs_') or k.startswith('eb_')]; print(len(nodes))")
HAS_LUCK=$(echo "$RESPONSE" | python3 -c "import sys, json; data = json.load(sys.stdin); print(data['analysis_info']['has_luck_pillar'])")
HAS_ANNUAL=$(echo "$RESPONSE" | python3 -c "import sys, json; data = json.load(sys.stdin); print(data['analysis_info']['has_annual'])")

echo "Total nodes: $NODE_COUNT"
echo "Has luck pillar: $HAS_LUCK"
echo "Has annual: $HAS_ANNUAL"

if [ "$NODE_COUNT" == "12" ] && [ "$HAS_LUCK" == "True" ] && [ "$HAS_ANNUAL" == "True" ]; then
    echo "✅ PASSED"
    ((PASSED++))
else
    echo "❌ FAILED: Expected 12 nodes with luck and annual pillars"
    ((FAILED++))
fi

# Test 3: Natal + Year + Month
echo ""
echo "============================================================"
echo "TEST 3: Natal + Year + Month"
echo "============================================================"
RESPONSE=$(curl -s "${BASE_URL}/analyze_bazi?birth_date=1990-01-15&gender=female&birth_time=08:30&analysis_year=2024&analysis_month=11")
NODE_COUNT=$(echo "$RESPONSE" | python3 -c "import sys, json; data = json.load(sys.stdin); nodes = [k for k in data if k.startswith('hs_') or k.startswith('eb_')]; print(len(nodes))")
HAS_MONTHLY=$(echo "$RESPONSE" | python3 -c "import sys, json; data = json.load(sys.stdin); print(data['analysis_info']['has_monthly'])")

echo "Total nodes: $NODE_COUNT"
echo "Has monthly: $HAS_MONTHLY"

if [ "$NODE_COUNT" == "14" ] && [ "$HAS_MONTHLY" == "True" ]; then
    echo "✅ PASSED"
    ((PASSED++))
else
    echo "❌ FAILED: Expected 14 nodes with monthly pillar"
    ((FAILED++))
fi

# Test 4: Full comparison
echo ""
echo "============================================================"
echo "TEST 4: Full Comparison (All Pillars)"
echo "============================================================"
RESPONSE=$(curl -s "${BASE_URL}/analyze_bazi?birth_date=1990-01-15&gender=male&birth_time=13:45&analysis_year=2024&analysis_month=11&analysis_day=25&analysis_time=14:30")
NODE_COUNT=$(echo "$RESPONSE" | python3 -c "import sys, json; data = json.load(sys.stdin); nodes = [k for k in data if k.startswith('hs_') or k.startswith('eb_')]; print(len(nodes))")
HAS_DAILY=$(echo "$RESPONSE" | python3 -c "import sys, json; data = json.load(sys.stdin); print(data['analysis_info']['has_daily'])")
HAS_HOURLY=$(echo "$RESPONSE" | python3 -c "import sys, json; data = json.load(sys.stdin); print(data['analysis_info']['has_hourly'])")

echo "Total nodes: $NODE_COUNT"
echo "Has daily: $HAS_DAILY"
echo "Has hourly: $HAS_HOURLY"

if [ "$NODE_COUNT" == "18" ] && [ "$HAS_DAILY" == "True" ] && [ "$HAS_HOURLY" == "True" ]; then
    echo "✅ PASSED"
    ((PASSED++))
else
    echo "❌ FAILED: Expected 18 nodes with all pillars"
    ((FAILED++))
fi

# Test 5: Interactions
echo ""
echo "============================================================"
echo "TEST 5: Interactions Calculated"
echo "============================================================"
RESPONSE=$(curl -s "${BASE_URL}/analyze_bazi?birth_date=1990-01-15&gender=male&birth_time=13:45&analysis_year=2024")
INTERACTION_COUNT=$(echo "$RESPONSE" | python3 -c "import sys, json; data = json.load(sys.stdin); print(len(data.get('interactions', [])))")
HAS_DAYMASTER=$(echo "$RESPONSE" | python3 -c "import sys, json; data = json.load(sys.stdin); print('daymaster_analysis' in data)")

echo "Interactions found: $INTERACTION_COUNT"
echo "Has daymaster analysis: $HAS_DAYMASTER"

if [ "$INTERACTION_COUNT" -gt "0" ] && [ "$HAS_DAYMASTER" == "True" ]; then
    echo "✅ PASSED"
    ((PASSED++))
else
    echo "❌ FAILED: Expected interactions and daymaster analysis"
    ((FAILED++))
fi

# Summary
echo ""
echo "============================================================"
echo "TEST SUMMARY"
echo "============================================================"
echo "Passed: $PASSED"
echo "Failed: $FAILED"

if [ $FAILED -eq 0 ]; then
    echo ""
    echo "✅ ALL TESTS PASSED"
    echo "============================================================"
    exit 0
else
    echo ""
    echo "❌ SOME TESTS FAILED"
    echo "============================================================"
    exit 1
fi
