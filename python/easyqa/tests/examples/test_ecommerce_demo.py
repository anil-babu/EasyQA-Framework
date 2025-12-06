"""
Example E-commerce Test Suite using AI-Powered Framework.

This example demonstrates testing an e-commerce website (demo.playwright.dev)
using the AI-enhanced capabilities of EasyQA Framework.
"""

import pytest
import asyncio
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from easyqa.integrations.playwright_wrapper import PlaywrightAI
from easyqa.visual.visual_tester import VisualTester
from easyqa.data_generation.ai_data_generator import AIDataGenerator
from easyqa.analytics.ml_analytics import MLAnalytics


class TestEcommerceDemo:
    """
    E-commerce demo website test suite with AI capabilities.

    Tests: https://demo.playwright.dev (Playwright demo site)
    or https://www.saucedemo.com (Sauce Labs demo)
    """

    @pytest.fixture(autouse=True)
    async def setup_teardown(self):
        """Setup and teardown for each test."""
        self.browser = PlaywrightAI(browser_type="chromium", headless=False)
        await self.browser.start()

        self.visual_tester = VisualTester(threshold=0.95)
        self.data_gen = AIDataGenerator(seed=42)
        self.analytics = MLAnalytics()

        yield

        await self.browser.close()

    @pytest.mark.asyncio
    async def test_homepage_load_and_visual(self):
        """Test homepage loads correctly with visual regression."""
        # Navigate to homepage
        await self.browser.navigate("https://www.saucedemo.com")

        # Capture screenshot
        screenshot_path = await self.browser.capture_screenshot("homepage_current.png")

        # Get performance metrics
        performance = await self.browser.get_performance_metrics()
        print(f"\n📊 Performance Metrics:")
        print(f"   DOM Content Loaded: {performance.get('domContentLoaded', 0)}ms")
        print(f"   Load Complete: {performance.get('loadComplete', 0)}ms")

        # Visual regression test
        baseline_path = "visual_baselines/homepage_baseline.png"

        if Path(baseline_path).exists():
            # Compare with baseline
            result = self.visual_tester.compare_images(
                baseline_path, screenshot_path, "homepage"
            )

            insights = self.visual_tester.get_ai_insights(result)
            print(f"\n🎯 Visual Testing Insights:")
            for insight in insights:
                print(f"   {insight}")

            assert result[
                "passed"
            ], f"Visual regression detected! Score: {result['overall_score']}"
        else:
            # Create baseline
            self.visual_tester.capture_baseline(screenshot_path, "homepage")
            print("\n✅ Baseline captured for future comparisons")

        # Record test result for ML
        self.analytics.record_test_result(
            {
                "name": "test_homepage_load_and_visual",
                "status": "passed",
                "execution_time": performance.get("loadComplete", 0) / 1000,
                "browser": "chromium",
                "step_count": 2,
                "priority": "high",
            }
        )

    @pytest.mark.asyncio
    async def test_login_with_generated_data(self):
        """Test login functionality with AI-generated test data."""
        await self.browser.navigate("https://www.saucedemo.com")

        # Use standard credentials for sauce demo
        username = "standard_user"
        password = "secret_sauce"

        # Perform login
        await self.browser.ai_fill('[data-test="username"]', username)
        await self.browser.ai_fill('[data-test="password"]', password)
        await self.browser.ai_click('[data-test="login-button"]')

        # Wait for products page
        await self.browser.smart_wait_for_element(".inventory_list", timeout=5000)

        # Capture screenshot of logged-in state
        await self.browser.capture_screenshot("after_login.png")

        # Verify we're on products page
        current_url = self.browser.page.url
        assert "/inventory.html" in current_url, "Login failed!"

        print("\n✅ Login successful!")

        # Record result
        self.analytics.record_test_result(
            {
                "name": "test_login_with_generated_data",
                "status": "passed",
                "execution_time": 2.5,
                "browser": "chromium",
                "step_count": 4,
                "priority": "critical",
            }
        )

    @pytest.mark.asyncio
    async def test_add_to_cart_workflow(self):
        """Test add to cart workflow with AI data extraction."""
        # Login first
        await self.browser.navigate("https://www.saucedemo.com")
        await self.browser.ai_fill('[data-test="username"]', "standard_user")
        await self.browser.ai_fill('[data-test="password"]', "secret_sauce")
        await self.browser.ai_click('[data-test="login-button"]')

        # Wait for products
        await self.browser.smart_wait_for_element(".inventory_list")

        # Extract product data using AI
        products_data = await self.browser.ai_extract_data(
            {
                "product_names": {"selector": ".inventory_item_name", "type": "list"},
                "product_prices": {"selector": ".inventory_item_price", "type": "list"},
            }
        )

        print(f"\n🛍️  Found {len(products_data.get('product_names', []))} products")

        # Add first item to cart
        await self.browser.ai_click('[data-test="add-to-cart-sauce-labs-backpack"]')

        # Verify cart badge
        cart_badge = await self.browser.page.query_selector(".shopping_cart_badge")
        assert cart_badge is not None, "Cart badge not found!"

        badge_text = await cart_badge.inner_text()
        assert badge_text == "1", f"Expected 1 item in cart, got {badge_text}"

        print("✅ Item successfully added to cart!")

        # Record result
        self.analytics.record_test_result(
            {
                "name": "test_add_to_cart_workflow",
                "status": "passed",
                "execution_time": 3.2,
                "browser": "chromium",
                "step_count": 6,
                "priority": "high",
            }
        )

    @pytest.mark.asyncio
    async def test_checkout_flow(self):
        """Test complete checkout flow."""
        # Login and add item
        await self.browser.navigate("https://www.saucedemo.com")
        await self.browser.ai_fill('[data-test="username"]', "standard_user")
        await self.browser.ai_fill('[data-test="password"]', "secret_sauce")
        await self.browser.ai_click('[data-test="login-button"]')
        await self.browser.smart_wait_for_element(".inventory_list")
        await self.browser.ai_click('[data-test="add-to-cart-sauce-labs-backpack"]')

        # Go to cart
        await self.browser.ai_click(".shopping_cart_link")
        await self.browser.smart_wait_for_element(".cart_list")

        # Proceed to checkout
        await self.browser.ai_click('[data-test="checkout"]')

        # Generate checkout data
        checkout_data = self.data_gen.generate_user_profile()

        # Fill checkout information
        await self.browser.ai_fill(
            '[data-test="firstName"]', checkout_data["first_name"]
        )
        await self.browser.ai_fill('[data-test="lastName"]', checkout_data["last_name"])
        await self.browser.ai_fill(
            '[data-test="postalCode"]', checkout_data["address"]["zip_code"]
        )

        await self.browser.ai_click('[data-test="continue"]')

        # Verify we're on overview page
        await self.browser.smart_wait_for_element(".summary_info")

        # Complete checkout
        await self.browser.ai_click('[data-test="finish"]')

        # Verify success
        success_element = await self.browser.page.query_selector(".complete-header")
        assert success_element is not None, "Checkout completion not confirmed!"

        success_text = await success_element.inner_text()
        assert "Thank you" in success_text or "complete" in success_text.lower()

        print("✅ Checkout completed successfully!")

        # Capture final screenshot
        await self.browser.capture_screenshot("checkout_complete.png")

        # Record result
        self.analytics.record_test_result(
            {
                "name": "test_checkout_flow",
                "status": "passed",
                "execution_time": 5.8,
                "browser": "chromium",
                "step_count": 12,
                "priority": "critical",
            }
        )

    @pytest.mark.asyncio
    async def test_performance_audit(self):
        """Test page performance using AI analytics."""
        await self.browser.navigate("https://www.saucedemo.com")

        # Run Lighthouse audit
        audit_results = await self.browser.run_lighthouse_audit()

        print(f"\n🚀 Performance Audit Results:")
        print(f"   Performance Score: {audit_results.get('performance', 0):.2f}")
        print(f"   Metrics: {audit_results.get('metrics', {})}")

        # Assert performance threshold
        assert (
            audit_results.get("performance", 0) > 50
        ), "Performance score below acceptable threshold!"

        # Get network summary
        network_summary = await self.browser.get_network_summary()
        print(f"\n🌐 Network Summary:")
        print(f"   Total Requests: {network_summary.get('total_requests', 0)}")
        print(f"   Failed Requests: {network_summary.get('failed_requests', 0)}")

        # Record result
        self.analytics.record_test_result(
            {
                "name": "test_performance_audit",
                "status": "passed",
                "execution_time": 2.1,
                "browser": "chromium",
                "step_count": 3,
                "priority": "medium",
            }
        )

    @pytest.mark.asyncio
    async def test_accessibility_check(self):
        """Test accessibility compliance using AI."""
        await self.browser.navigate("https://www.saucedemo.com")

        # Check accessibility
        violations = await self.browser.get_accessibility_violations()

        print(f"\n♿ Accessibility Check:")
        print(f"   Violations Found: {len(violations)}")

        if violations:
            print("\n   Top Violations:")
            for i, violation in enumerate(violations[:5]):
                print(f"   {i+1}. {violation.get('description', 'Unknown')}")
                print(f"      Impact: {violation.get('impact', 'N/A')}")

        # Assert no critical violations
        critical_violations = [v for v in violations if v.get("impact") == "critical"]

        assert (
            len(critical_violations) == 0
        ), f"Found {len(critical_violations)} critical accessibility violations!"

        # Record result
        self.analytics.record_test_result(
            {
                "name": "test_accessibility_check",
                "status": "passed",
                "execution_time": 1.8,
                "browser": "chromium",
                "step_count": 2,
                "priority": "high",
            }
        )


@pytest.mark.asyncio
async def test_ml_predictions():
    """Test ML predictions for test failures."""
    analytics = MLAnalytics()

    # Generate some test history data if needed
    if len(analytics.test_history) < 10:
        print("\n📊 Generating sample test history for ML demo...")
        for i in range(20):
            analytics.record_test_result(
                {
                    "name": f"test_sample_{i % 5}",
                    "status": "failed" if i % 4 == 0 else "passed",
                    "execution_time": 2.5 + (i % 5),
                    "browser": ["chrome", "firefox"][i % 2],
                    "step_count": 5 + (i % 3),
                    "priority": ["low", "medium", "high"][i % 3],
                }
            )

    # Get analytics insights
    insights = analytics.generate_test_insights()

    print("\n🤖 ML Analytics Insights:")
    print(f"   Total Tests: {insights['summary']['total_tests_executed']}")
    print(f"   Overall Failure Rate: {insights['summary']['overall_failure_rate']}")
    print(f"   Flaky Tests: {insights['summary']['flaky_test_count']}")

    print("\n💡 Recommendations:")
    for rec in insights.get("recommendations", []):
        print(f"   {rec}")

    # Make prediction
    prediction = analytics.predict_test_failure(
        {
            "name": "test_checkout_flow",
            "execution_time": 5.8,
            "browser": "chrome",
            "step_count": 12,
            "priority": "critical",
        }
    )

    print(f"\n🔮 Failure Prediction:")
    print(f"   Prediction: {prediction.get('prediction')}")
    print(f"   Probability: {prediction.get('probability')}")
    print(f"   Confidence: {prediction.get('confidence')}")


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v", "-s"])
