"""Simple unit tests that don't require browsers or external websites."""

import pytest
from pathlib import Path
import sys

# Add python directory to path so we can import easyqa
python_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(python_dir))


class TestDataGenerator:
    """Test AI Data Generator without external dependencies."""

    def test_import(self):
        """Test that data generator can be imported."""
        from easyqa.data_generation.ai_data_generator import AIDataGenerator

        assert AIDataGenerator is not None

    def test_generate_user_profile(self):
        """Test user profile generation."""
        from easyqa.data_generation.ai_data_generator import AIDataGenerator

        generator = AIDataGenerator(seed=42)
        profile = generator.generate_user_profile(count=1)

        assert profile is not None
        assert "username" in profile
        assert "email" in profile
        assert "@" in profile["email"]

    def test_generate_multiple_profiles(self):
        """Test generating multiple profiles."""
        from easyqa.data_generation.ai_data_generator import AIDataGenerator

        generator = AIDataGenerator(seed=42)
        profiles = generator.generate_user_profile(count=5)

        assert len(profiles) == 5
        assert all("email" in p for p in profiles)

    def test_ecommerce_data_generation(self):
        """Test e-commerce data generation."""
        from easyqa.data_generation.ai_data_generator import AIDataGenerator

        generator = AIDataGenerator(seed=42)
        data = generator.generate_ecommerce_data(product_count=3, order_count=2)

        assert "products" in data
        assert "orders" in data
        assert len(data["products"]) == 3
        assert len(data["orders"]) == 2

    def test_form_data_generation(self):
        """Test form data generation."""
        from easyqa.data_generation.ai_data_generator import AIDataGenerator

        generator = AIDataGenerator(seed=42)
        contact_form = generator.generate_form_data("contact")

        assert "name" in contact_form
        assert "email" in contact_form
        assert "message" in contact_form

    def test_edge_cases(self):
        """Test edge case generation."""
        from easyqa.data_generation.ai_data_generator import AIDataGenerator

        generator = AIDataGenerator()
        email_edges = generator.generate_edge_cases("email")

        assert len(email_edges) > 0
        assert "" in email_edges  # Empty string
        assert "invalid" in email_edges  # Invalid email


class TestMLAnalytics:
    """Test ML Analytics without external dependencies."""

    def test_import(self):
        """Test that ML analytics can be imported."""
        from easyqa.analytics.ml_analytics import MLAnalytics

        assert MLAnalytics is not None

    def test_initialization(self):
        """Test ML analytics initialization."""
        from easyqa.analytics.ml_analytics import MLAnalytics

        analytics = MLAnalytics(history_file="data/test_history_temp.json")
        assert analytics is not None
        assert analytics.test_history is not None

    def test_record_result(self):
        """Test recording test results."""
        from easyqa.analytics.ml_analytics import MLAnalytics

        analytics = MLAnalytics(history_file="data/test_history_temp.json")
        analytics.record_test_result(
            {
                "name": "test_sample",
                "status": "passed",
                "execution_time": 2.5,
                "browser": "chrome",
                "step_count": 5,
                "priority": "high",
            }
        )

        assert len(analytics.test_history) >= 1

    def test_insights_generation(self):
        """Test insights generation."""
        from easyqa.analytics.ml_analytics import MLAnalytics

        analytics = MLAnalytics(history_file="data/test_history_temp.json")

        # Add some test data
        for i in range(10):
            analytics.record_test_result(
                {
                    "name": f"test_{i}",
                    "status": "passed" if i % 2 == 0 else "failed",
                    "execution_time": 2.0 + i * 0.5,
                    "browser": "chrome",
                    "step_count": 5,
                    "priority": "medium",
                }
            )

        insights = analytics.generate_test_insights()

        assert "summary" in insights
        assert "recommendations" in insights
        assert insights["summary"]["total_tests_executed"] >= 10


class TestConfig:
    """Test configuration management."""

    def test_config_import(self):
        """Test that config can be imported."""
        from easyqa.core.config import Config

        assert Config is not None

    def test_config_initialization(self):
        """Test config initialization."""
        from easyqa.core.config import Config

        config = Config()
        assert config is not None
        assert config.config is not None

    def test_config_get(self):
        """Test getting config values."""
        from easyqa.core.config import Config

        config = Config()
        browser = config.get("browser", "default")

        assert browser is not None

    def test_config_set(self):
        """Test setting config values."""
        from easyqa.core.config import Config

        config = Config()
        config.set("test", "key", value="test_value")

        value = config.get("test", "key")
        assert value == "test_value"


class TestVisualTester:
    """Test visual testing module imports."""

    def test_import(self):
        """Test that visual tester can be imported."""
        from easyqa.visual.visual_tester import VisualTester

        assert VisualTester is not None

    def test_initialization(self):
        """Test visual tester initialization."""
        from easyqa.visual.visual_tester import VisualTester

        tester = VisualTester(threshold=0.95)
        assert tester is not None
        assert tester.threshold == 0.95


class TestSelfHealing:
    """Test self-healing locator module."""

    def test_import(self):
        """Test that self-healing locator can be imported."""
        from easyqa.locators.self_healing import SelfHealingLocator

        assert SelfHealingLocator is not None

    def test_initialization(self):
        """Test self-healing locator initialization."""
        from easyqa.locators.self_healing import SelfHealingLocator

        healer = SelfHealingLocator(confidence_threshold=0.8)
        assert healer is not None
        assert healer.confidence_threshold == 0.8

    def test_stats(self):
        """Test getting healing stats."""
        from easyqa.locators.self_healing import SelfHealingLocator

        healer = SelfHealingLocator()
        stats = healer.get_healing_stats()

        assert "total_healings" in stats
        assert "success_rate" in stats


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
