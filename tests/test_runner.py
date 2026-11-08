#!/usr/bin/env python3
"""Budapest Adventures Staging Architecture E2E Test Runner.

A high-performance, zero-dependency Python 3 test harness for Tiers 1-4.
Evaluates static files, DOM structure, schemas, routing configs, link decoration,
and optional live HTTP endpoints on preview_server.py.
"""

import argparse
import inspect
import json
import os
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Add parent directory to sys.path to enable imports
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tests.common import BaseTestCase
from tests.tier1_feature_coverage import Tier1FeatureTests
from tests.tier2_boundary_corner import Tier2BoundaryCornerTests
from tests.tier3_cross_feature import Tier3CrossFeatureTests
from tests.tier4_real_world_scenarios import Tier4RealWorldScenarioTests


class TestResult:
    def __init__(self, name: str, tier: int, feature: Optional[int] = None):
        self.name = name
        self.tier = tier
        self.feature = feature
        self.passed = False
        self.skipped = False
        self.error_message: Optional[str] = None
        self.traceback_str: Optional[str] = None
        self.duration_seconds: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "tier": self.tier,
            "feature": self.feature,
            "passed": self.passed,
            "skipped": self.skipped,
            "error_message": self.error_message,
            "duration_seconds": round(self.duration_seconds, 4),
        }


def extract_feature_number(test_name: str) -> Optional[int]:
    """Extract feature number from test method name (e.g., test_f15_... -> 15)."""
    match = re.search(r"test_f0*([1-9][0-9]*)_", test_name)
    if match:
        return int(match.group(1))
    return None


import re


def collect_test_methods(cls: Any, tier: int) -> List[Tuple[str, Any, int, Optional[int]]]:
    """Collect test methods from a test class."""
    methods = []
    instance = cls(cls.__name__)
    for attr_name in sorted(dir(instance)):
        if attr_name.startswith("test_"):
            attr = getattr(instance, attr_name)
            if callable(attr):
                feature = extract_feature_number(attr_name)
                methods.append((attr_name, attr, tier, feature))
    return methods


def run_single_test(test_name: str, test_func: Any, tier: int, feature: Optional[int]) -> TestResult:
    """Run an individual test and record outcome."""
    result = TestResult(test_name, tier, feature)
    start_time = time.perf_counter()
    try:
        test_func()
        result.passed = True
    except AssertionError as ae:
        result.passed = False
        result.error_message = str(ae)
        result.traceback_str = traceback.format_exc()
    except Exception as ex:
        result.passed = False
        result.error_message = f"Unhandled Exception: {ex}"
        result.traceback_str = traceback.format_exc()
    finally:
        result.duration_seconds = time.perf_counter() - start_time
    return result


def main():
    parser = argparse.ArgumentParser(
        description="Budapest Adventures Staging Architecture E2E Test Runner (Tiers 1-4)"
    )
    parser.add_argument(
        "--tier",
        type=str,
        default="all",
        choices=["1", "2", "3", "4", "all"],
        help="Filter execution by specific test tier (1, 2, 3, 4, or all)",
    )
    parser.add_argument(
        "--feature",
        type=str,
        default=None,
        help="Filter execution by specific feature number(s) (e.g. 1 or 1,2,3,21,22,23)",
    )
    parser.add_argument(
        "--server-url",
        type=str,
        default=None,
        help="Live server URL for live HTTP tests (e.g. http://localhost:3000)",
    )
    parser.add_argument(
        "--json-report",
        type=str,
        default=None,
        help="File path to write JSON test results report",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Verbose test execution output",
    )
    parser.add_argument(
        "--fail-fast",
        "-x",
        action="store_true",
        help="Stop on first test failure",
    )

    args = parser.parse_args()

    # Determine which tiers to run
    tiers_to_run = [1, 2, 3, 4] if args.tier == "all" else [int(args.tier)]

    all_tests = []
    if 1 in tiers_to_run:
        all_tests.extend(collect_test_methods(Tier1FeatureTests, 1))
    if 2 in tiers_to_run:
        all_tests.extend(collect_test_methods(Tier2BoundaryCornerTests, 2))
    if 3 in tiers_to_run:
        all_tests.extend(collect_test_methods(Tier3CrossFeatureTests, 3))
    if 4 in tiers_to_run:
        all_tests.extend(collect_test_methods(Tier4RealWorldScenarioTests, 4))

    # Apply feature filter if specified
    feature_filter: Optional[set] = None
    if args.feature is not None:
        try:
            feature_filter = {int(f.strip()) for f in args.feature.split(",") if f.strip()}
        except ValueError:
            parser.error(
                f"Invalid feature value: {args.feature!r}. Must be an integer or comma-separated integers (e.g. 1 or 1,2,3)."
            )

    if feature_filter is not None:
        all_tests = [t for t in all_tests if t[3] in feature_filter]

    print("=" * 78)
    print(" BUDAPEST ADVENTURES — STAGING ARCHITECTURE E2E TEST RUNNER")
    print(f" Timestamp: {datetime.now(timezone.utc).isoformat()}")
    print(f" Project Root: {PROJECT_ROOT}")
    print(f" Execution Mode: {'Live Server (' + args.server_url + ')' if args.server_url else 'Static Filesystem Inspection'}")
    print(f" Selected Tiers: {tiers_to_run} | Feature Filter: {args.feature or 'None'}")
    print(f" Total Tests Discovered: {len(all_tests)}")
    print("=" * 78)

    results: List[TestResult] = []
    start_total_time = time.perf_counter()

    current_tier = None
    for name, func, tier, feature in all_tests:
        if tier != current_tier:
            current_tier = tier
            tier_names = {
                1: "Tier 1: Feature Coverage (Category-Partition)",
                2: "Tier 2: Boundary & Corner Cases (BVA)",
                3: "Tier 3: Cross-Feature Interactions (Pairwise)",
                4: "Tier 4: Real-World Scenarios (End-to-End)",
            }
            print(f"\n--- {tier_names.get(tier, f'Tier {tier}')} ---")

        res = run_single_test(name, func, tier, feature)
        results.append(res)

        status_str = "PASS" if res.passed else "FAIL"
        if args.verbose or not res.passed:
            color_mark = "✓" if res.passed else "✗"
            feat_tag = f"[F{feature:02d}] " if feature else ""
            print(f" {color_mark} {status_str:4s} | {feat_tag}{name} ({res.duration_seconds*1000:.1f}ms)")
            if not res.passed and res.error_message:
                print(f"      ERROR: {res.error_message}")
        else:
            # Compact dot progression
            sys.stdout.write("." if res.passed else "F")
            sys.stdout.flush()

        if not res.passed and args.fail_fast:
            print("\n[!] Stopping execution due to --fail-fast flag.")
            break

    total_duration = time.perf_counter() - start_total_time
    total_count = len(results)
    passed_count = sum(1 for r in results if r.passed)
    failed_count = sum(1 for r in results if not r.passed)
    pass_rate = (passed_count / total_count * 100.0) if total_count > 0 else 0.0

    print("\n\n" + "=" * 78)
    print(" TEST EXECUTION SUMMARY")
    print("=" * 78)
    print(f" Total Tests:  {total_count}")
    print(f" Passed:       {passed_count} ({pass_rate:.1f}%)")
    print(f" Failed:       {failed_count}")
    print(f" Duration:     {total_duration:.2f} seconds")
    print("=" * 78)

    # Detailed Failure Breakdown
    if failed_count > 0:
        print("\nFAILURE BREAKDOWN BY TIER & FEATURE:")
        for res in results:
            if not res.passed:
                feat_tag = f" [Feature {res.feature}]" if res.feature else ""
                print(f"\n[Tier {res.tier}]{feat_tag} {res.name}:")
                print(f"  {res.error_message}")

    # Generate JSON report if requested
    if args.json_report:
        report_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "project_root": str(PROJECT_ROOT),
            "summary": {
                "total": total_count,
                "passed": passed_count,
                "failed": failed_count,
                "pass_rate_percent": round(pass_rate, 2),
                "duration_seconds": round(total_duration, 4),
            },
            "results": [r.to_dict() for r in results],
        }
        report_path = Path(args.json_report)
        if not report_path.is_absolute():
            report_path = PROJECT_ROOT / report_path
        report_path.write_text(json.dumps(report_data, indent=2), encoding="utf-8")
        print(f"\nJSON report generated: {report_path}")

    # Exit code
    if failed_count > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
