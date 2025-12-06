#!/usr/bin/env python3
"""
EasyQA Framework CLI

Command-line interface for managing and running AI-powered tests.
"""
import argparse
import sys
import asyncio
from pathlib import Path
import logging

from easyqa.core.config import config
from easyqa.visual.visual_tester import VisualTester
from easyqa.data_generation.ai_data_generator import AIDataGenerator
from easyqa.analytics.ml_analytics import MLAnalytics
from easyqa.locators.self_healing import SelfHealingLocator

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class EasyQACLI:
    """Main CLI class for EasyQA Framework."""

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="EasyQA AI Testing Framework CLI",
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )
        self._setup_commands()

    def _setup_commands(self):
        """Setup CLI commands."""
        subparsers = self.parser.add_subparsers(
            dest="command", help="Available commands"
        )

        # Generate test data
        generate_parser = subparsers.add_parser("generate", help="Generate test data")
        generate_parser.add_argument(
            "type",
            choices=["users", "ecommerce", "forms", "dataset"],
            help="Type of data to generate",
        )
        generate_parser.add_argument(
            "--count", type=int, default=10, help="Number of records to generate"
        )
        generate_parser.add_argument("--output", type=str, help="Output file path")

        # Visual testing
        visual_parser = subparsers.add_parser(
            "visual", help="Visual regression testing"
        )
        visual_parser.add_argument(
            "action", choices=["baseline", "compare"], help="Visual testing action"
        )
        visual_parser.add_argument(
            "--screenshot", type=str, required=True, help="Screenshot path"
        )
        visual_parser.add_argument(
            "--test-name", type=str, required=True, help="Test name"
        )
        visual_parser.add_argument(
            "--baseline", type=str, help="Baseline image path (for compare)"
        )

        # Analytics
        analytics_parser = subparsers.add_parser(
            "analytics", help="View test analytics and insights"
        )
        analytics_parser.add_argument(
            "action", choices=["insights", "predict", "stats"], help="Analytics action"
        )

        # Self-healing stats
        subparsers.add_parser(
            "healing-stats", help="View self-healing locator statistics"
        )

        # Config
        config_parser = subparsers.add_parser(
            "config", help="View or update configuration"
        )
        config_parser.add_argument(
            "action", choices=["show", "set"], help="Config action"
        )
        config_parser.add_argument(
            "--key", type=str, help="Config key (dot notation: browser.default)"
        )
        config_parser.add_argument("--value", type=str, help="Config value")

        # Run tests
        run_parser = subparsers.add_parser("run", help="Run tests")
        run_parser.add_argument(
            "--browser",
            type=str,
            choices=["chrome", "firefox", "safari", "edge", "chromium", "webkit"],
            help="Browser to use",
        )
        run_parser.add_argument(
            "--headless", action="store_true", help="Run in headless mode"
        )
        run_parser.add_argument(
            "--test-path", type=str, help="Specific test file or directory"
        )

    def generate_data(self, args):
        """Generate test data."""
        generator = AIDataGenerator()

        if args.type == "users":
            data = generator.generate_user_profile(count=args.count)
            logger.info(f"Generated {args.count} user profile(s)")

        elif args.type == "ecommerce":
            data = generator.generate_ecommerce_data(
                product_count=args.count, order_count=args.count // 2
            )
            logger.info(f"Generated e-commerce data with {args.count} products")

        elif args.type == "forms":
            data = [generator.generate_form_data("contact") for _ in range(args.count)]
            logger.info(f"Generated {args.count} form data records")

        else:
            logger.error(f"Unknown data type: {args.type}")
            return

        # Save to file
        if args.output:
            output_file = generator.save_to_file(data, args.output, format="json")
            logger.info(f"Data saved to {output_file}")
        else:
            import json

            print(json.dumps(data, indent=2, default=str))

    def visual_testing(self, args):
        """Perform visual testing."""
        tester = VisualTester()

        if args.action == "baseline":
            baseline_path = tester.capture_baseline(args.screenshot, args.test_name)
            logger.info(f"✅ Baseline captured: {baseline_path}")

        elif args.action == "compare":
            if not args.baseline:
                logger.error("--baseline required for compare action")
                sys.exit(1)

            result = tester.compare_images(
                args.baseline, args.screenshot, args.test_name
            )

            insights = tester.get_ai_insights(result)

            print("\n" + "=" * 60)
            print("VISUAL REGRESSION TEST RESULTS")
            print("=" * 60)
            print(f"Test: {args.test_name}")
            print(f"Status: {'✅ PASSED' if result['passed'] else '❌ FAILED'}")
            print(f"Overall Score: {result['overall_score']:.4f}")
            print(f"SSIM Score: {result['ssim_score']:.4f}")
            print(f"Hash Similarity: {result['hash_similarity']:.4f}")
            print(f"Pixel Diff: {result['pixel_diff_percentage']:.2f}%")
            print(f"\nDiff Image: {result['diff_image_path']}")
            print("\n💡 AI Insights:")
            for insight in insights:
                print(f"  {insight}")
            print("=" * 60)

    def show_analytics(self, args):
        """Show analytics and insights."""
        analytics = MLAnalytics()

        if args.action == "insights":
            insights = analytics.generate_test_insights()
            print("\n" + "=" * 60)
            print("📊 TEST ANALYTICS INSIGHTS")
            print("=" * 60)
            print(f"\nSummary:")
            for key, value in insights["summary"].items():
                print(f"  {key}: {value}")

            print(f"\n💡 Recommendations:")
            for rec in insights.get("recommendations", []):
                print(f"  {rec}")

            print(f"\n📈 Trends:")
            for key, value in insights.get("trends", {}).items():
                print(f"  {key}: {value}")
            print("=" * 60)

        elif args.action == "stats":
            analysis = analytics.analyze_failure_patterns()
            print("\n" + "=" * 60)
            print("📈 FAILURE PATTERN ANALYSIS")
            print("=" * 60)
            print(f"\nTotal Tests: {analysis['total_tests']}")
            print(f"Failure Rate: {analysis['failure_rate']:.2%}")

            print("\n🔝 Most Failing Tests:")
            for test in analysis.get("most_failing_tests", [])[:5]:
                print(f"  {test['test_name']}: {test['failure_rate']:.2%}")

            print("\n🌐 Failures by Browser:")
            for browser, rate in analysis.get("failure_by_browser", {}).items():
                print(f"  {browser}: {rate:.2%}")

            print("\n🔄 Flaky Tests:")
            for test in analysis.get("flaky_tests", [])[:5]:
                print(f"  {test}")
            print("=" * 60)

    def show_healing_stats(self):
        """Show self-healing locator statistics."""
        healer = SelfHealingLocator()
        stats = healer.get_healing_stats()

        print("\n" + "=" * 60)
        print("✨ SELF-HEALING LOCATOR STATISTICS")
        print("=" * 60)
        print(f"\nTotal Healings: {stats['total_healings']}")
        print(f"Success Rate: {stats['success_rate']:.2f}%")

        print("\n🔝 Most Healed Locators:")
        for loc in stats["most_healed_locators"][:10]:
            print(f"  {loc['locator']}")
            print(f"    → {loc['healed_to']}")
            print(f"    Times used: {loc['times_used']}")
        print("=" * 60)

    def show_config(self, args):
        """Show or update configuration."""
        if args.action == "show":
            import json

            print(json.dumps(config.config, indent=2))

        elif args.action == "set":
            if not args.key or not args.value:
                logger.error("--key and --value required for set action")
                sys.exit(1)

            keys = args.key.split(".")
            config.set(*keys, value=args.value)
            logger.info(f"✅ Config updated: {args.key} = {args.value}")

    def run_tests(self, args):
        """Run tests."""
        import subprocess

        cmd = ["pytest", "python/easyqa/tests/", "-v"]

        if args.test_path:
            cmd = ["pytest", args.test_path, "-v"]

        if args.browser:
            cmd.extend(["--browser", args.browser])

        if args.headless:
            cmd.append("--headless")

        logger.info(f"Running: {' '.join(cmd)}")
        subprocess.run(cmd)

    def run(self):
        """Run CLI."""
        args = self.parser.parse_args()

        if not args.command:
            self.parser.print_help()
            return

        try:
            if args.command == "generate":
                self.generate_data(args)

            elif args.command == "visual":
                self.visual_testing(args)

            elif args.command == "analytics":
                self.show_analytics(args)

            elif args.command == "healing-stats":
                self.show_healing_stats()

            elif args.command == "config":
                self.show_config(args)

            elif args.command == "run":
                self.run_tests(args)

        except Exception as e:
            logger.error(f"Error: {e}", exc_info=True)
            sys.exit(1)


def main():
    """Main entry point."""
    cli = EasyQACLI()
    cli.run()


if __name__ == "__main__":
    main()
