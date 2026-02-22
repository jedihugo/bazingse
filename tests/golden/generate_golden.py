"""
Generate golden files from the Python BaZi API for migration verification.

Calls the running Python API at http://localhost:8008 and saves responses
as JSON files. These files serve as the reference output that the TypeScript
port must match.

Usage:
    cd /Users/macbookair/GitHub/bazingse
    source api/.venv/bin/activate
    python3 tests/golden/generate_golden.py
"""

import json
import os
import sys
import urllib.request
import urllib.error
import urllib.parse

API_BASE = "http://localhost:8008/api"
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# Define all test cases: (filename, endpoint, params)
TEST_CASES = [
    # 1. Basic natal chart
    (
        "natal_basic.json",
        "/analyze_bazi",
        {
            "birth_date": "1990-01-15",
            "birth_time": "10:30",
            "gender": "male",
        },
    ),
    # 2. Natal with luck pillar (annual)
    (
        "natal_with_luck.json",
        "/analyze_bazi",
        {
            "birth_date": "1990-01-15",
            "birth_time": "10:30",
            "gender": "male",
            "analysis_year": "2026",
        },
    ),
    # 3. Natal with monthly resolution
    (
        "natal_monthly.json",
        "/analyze_bazi",
        {
            "birth_date": "1990-01-15",
            "birth_time": "10:30",
            "gender": "male",
            "analysis_year": "2026",
            "analysis_month": "6",
        },
    ),
    # 4. Natal with daily resolution
    (
        "natal_daily.json",
        "/analyze_bazi",
        {
            "birth_date": "1990-01-15",
            "birth_time": "10:30",
            "gender": "male",
            "analysis_year": "2026",
            "analysis_month": "6",
            "analysis_day": "15",
        },
    ),
    # 5. Natal with hourly resolution
    (
        "natal_hourly.json",
        "/analyze_bazi",
        {
            "birth_date": "1990-01-15",
            "birth_time": "10:30",
            "gender": "male",
            "analysis_year": "2026",
            "analysis_month": "6",
            "analysis_day": "15",
            "analysis_time": "14:30",
        },
    ),
    # 6. Unknown birth time
    (
        "natal_unknown_time.json",
        "/analyze_bazi",
        {
            "birth_date": "1985-12-25",
            "birth_time": "unknown",
            "gender": "female",
        },
    ),
    # 7. Before Li Chun (spring boundary)
    (
        "natal_lichun_before.json",
        "/analyze_bazi",
        {
            "birth_date": "2024-02-04",
            "birth_time": "03:00",
            "gender": "male",
        },
    ),
    # 8. After Li Chun (spring boundary)
    (
        "natal_lichun_after.json",
        "/analyze_bazi",
        {
            "birth_date": "2024-02-04",
            "birth_time": "17:00",
            "gender": "female",
        },
    ),
    # 9. 23:00 hour (zi hour day boundary)
    (
        "natal_23h.json",
        "/analyze_bazi",
        {
            "birth_date": "1995-08-10",
            "birth_time": "23:30",
            "gender": "male",
        },
    ),
    # 10. Physics school
    (
        "natal_physics.json",
        "/analyze_bazi",
        {
            "birth_date": "1990-01-15",
            "birth_time": "10:30",
            "gender": "male",
            "school": "physics",
        },
    ),
    # 11. Female with analysis year
    (
        "natal_female.json",
        "/analyze_bazi",
        {
            "birth_date": "2000-06-15",
            "birth_time": "14:00",
            "gender": "female",
            "analysis_year": "2026",
        },
    ),
    # 12. Dong Gong calendar - February
    (
        "dong_gong_feb.json",
        "/dong_gong_calendar",
        {
            "year": "2026",
            "month": "2",
        },
    ),
    # 13. Dong Gong calendar - June
    (
        "dong_gong_jun.json",
        "/dong_gong_calendar",
        {
            "year": "2026",
            "month": "6",
        },
    ),
]


def fetch_endpoint(endpoint: str, params: dict) -> dict:
    """Call the API and return the parsed JSON response."""
    query_string = urllib.parse.urlencode(params)
    url = f"{API_BASE}{endpoint}?{query_string}"
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        print(f"  HTTP {e.code} error for {url}")
        print(f"  Response: {body[:500]}")
        raise
    except urllib.error.URLError as e:
        print(f"  Connection error for {url}: {e.reason}")
        print("  Is the Python API running at http://localhost:8008?")
        raise


def main():
    print("=" * 60)
    print("Golden File Generator for BaZingSe API Migration")
    print("=" * 60)
    print(f"API base: {API_BASE}")
    print(f"Output dir: {OUTPUT_DIR}")
    print()

    # Check API is reachable
    try:
        health_url = "http://localhost:8008/health"
        with urllib.request.urlopen(health_url, timeout=5) as resp:
            health = json.loads(resp.read().decode("utf-8"))
            print(f"API health check: {health}")
    except Exception as e:
        print(f"ERROR: Cannot reach API at http://localhost:8008")
        print(f"  {e}")
        print("  Start the API with: cd api && python run_bazingse.py")
        sys.exit(1)

    print()
    results = []
    errors = []

    for i, (filename, endpoint, params) in enumerate(TEST_CASES, 1):
        print(f"[{i:2d}/13] {filename}...", end=" ", flush=True)
        filepath = os.path.join(OUTPUT_DIR, filename)
        try:
            data = fetch_endpoint(endpoint, params)
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            size = os.path.getsize(filepath)
            results.append((filename, size))
            print(f"OK ({size:,} bytes)")
        except Exception as e:
            errors.append((filename, str(e)))
            print(f"FAILED: {e}")

    # Summary
    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Successful: {len(results)}/13")
    print(f"  Failed:     {len(errors)}/13")
    print()

    if results:
        print("Generated files:")
        total_size = 0
        for filename, size in results:
            print(f"  {filename:30s} {size:>10,} bytes")
            total_size += size
        print(f"  {'TOTAL':30s} {total_size:>10,} bytes")

    if errors:
        print()
        print("Errors:")
        for filename, err in errors:
            print(f"  {filename}: {err}")
        sys.exit(1)

    print()
    print("All golden files generated successfully.")


if __name__ == "__main__":
    main()
