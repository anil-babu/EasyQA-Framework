"""AI-Powered Test Data Generator."""

import random
from typing import List, Dict, Any, Optional
from faker import Faker
import json
from datetime import datetime, timedelta
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class AIDataGenerator:
    """
    AI-powered test data generator using ML patterns.

    Generates realistic test data for various scenarios including
    user registration, e-commerce transactions, forms, etc.
    """

    def __init__(self, locale: str = "en_US", seed: Optional[int] = None):
        """
        Initialize AI Data Generator.

        Args:
            locale: Locale for data generation
            seed: Random seed for reproducibility
        """
        self.fake = Faker(locale)
        if seed:
            Faker.seed(seed)
            random.seed(seed)

        self.generation_history = []

    def generate_user_profile(
        self, count: int = 1, user_type: str = "standard"
    ) -> List[Dict]:
        """
        Generate realistic user profiles.

        Args:
            count: Number of profiles to generate
            user_type: Type of user (standard, premium, admin)

        Returns:
            List of user profile dictionaries
        """
        profiles = []

        for _ in range(count):
            profile = {
                "username": self.fake.user_name(),
                "email": self.fake.email(),
                "password": self._generate_secure_password(),
                "first_name": self.fake.first_name(),
                "last_name": self.fake.last_name(),
                "phone": self.fake.phone_number(),
                "date_of_birth": self.fake.date_of_birth(
                    minimum_age=18, maximum_age=80
                ).isoformat(),
                "address": {
                    "street": self.fake.street_address(),
                    "city": self.fake.city(),
                    "state": self.fake.state(),
                    "zip_code": self.fake.zipcode(),
                    "country": self.fake.country(),
                },
                "user_type": user_type,
                "created_at": datetime.now().isoformat(),
                "metadata": {
                    "ip_address": self.fake.ipv4(),
                    "user_agent": self.fake.user_agent(),
                    "locale": self.fake.locale(),
                },
            }

            profiles.append(profile)

        logger.info(f"Generated {count} user profile(s)")
        self._record_generation("user_profile", count)

        return profiles if count > 1 else profiles[0]

    def generate_ecommerce_data(
        self, product_count: int = 10, order_count: int = 5
    ) -> Dict:
        """
        Generate e-commerce test data.

        Args:
            product_count: Number of products to generate
            order_count: Number of orders to generate

        Returns:
            Dictionary with products and orders
        """
        # Generate products
        categories = [
            "Electronics",
            "Clothing",
            "Books",
            "Home & Garden",
            "Sports",
            "Toys",
            "Beauty",
            "Food",
        ]

        products = []
        for i in range(product_count):
            product = {
                "id": f"PROD-{i+1:04d}",
                "name": self.fake.catch_phrase(),
                "description": self.fake.text(max_nb_chars=200),
                "category": random.choice(categories),
                "price": round(random.uniform(9.99, 999.99), 2),
                "stock": random.randint(0, 500),
                "rating": round(random.uniform(3.0, 5.0), 1),
                "reviews_count": random.randint(0, 1000),
                "sku": self.fake.bothify(text="SKU-####-????").upper(),
                "weight": round(random.uniform(0.1, 50.0), 2),
                "dimensions": {
                    "length": random.randint(5, 100),
                    "width": random.randint(5, 100),
                    "height": random.randint(5, 100),
                },
                "images": [self.fake.image_url() for _ in range(random.randint(1, 5))],
                "in_stock": random.choice([True, False]),
            }
            products.append(product)

        # Generate orders
        orders = []
        for i in range(order_count):
            num_items = random.randint(1, 5)
            order_products = random.sample(products, min(num_items, len(products)))

            items = [
                {
                    "product_id": p["id"],
                    "product_name": p["name"],
                    "quantity": random.randint(1, 3),
                    "price": p["price"],
                }
                for p in order_products
            ]

            subtotal = sum(item["quantity"] * item["price"] for item in items)
            tax = round(subtotal * 0.08, 2)
            shipping = round(random.uniform(5.99, 19.99), 2)
            total = round(subtotal + tax + shipping, 2)

            order = {
                "id": f"ORD-{i+1:06d}",
                "user_id": f"USER-{random.randint(1, 1000):04d}",
                "order_date": (
                    datetime.now() - timedelta(days=random.randint(0, 30))
                ).isoformat(),
                "status": random.choice(
                    ["pending", "processing", "shipped", "delivered", "cancelled"]
                ),
                "items": items,
                "payment": {
                    "method": random.choice(["credit_card", "paypal", "bank_transfer"]),
                    "card_type": random.choice(["Visa", "Mastercard", "Amex"]),
                    "last_4_digits": f"{random.randint(1000, 9999)}",
                },
                "shipping_address": {
                    "name": self.fake.name(),
                    "street": self.fake.street_address(),
                    "city": self.fake.city(),
                    "zip_code": self.fake.zipcode(),
                },
                "pricing": {
                    "subtotal": subtotal,
                    "tax": tax,
                    "shipping": shipping,
                    "total": total,
                },
                "tracking_number": self.fake.bothify(text="TRK-##########"),
            }
            orders.append(order)

        data = {
            "products": products,
            "orders": orders,
            "generated_at": datetime.now().isoformat(),
        }

        logger.info(f"Generated {product_count} products and {order_count} orders")
        self._record_generation("ecommerce_data", product_count + order_count)

        return data

    def generate_form_data(self, form_type: str = "contact") -> Dict:
        """
        Generate form test data.

        Args:
            form_type: Type of form (contact, registration, survey, feedback)

        Returns:
            Form data dictionary
        """
        form_generators = {
            "contact": self._generate_contact_form,
            "registration": self._generate_registration_form,
            "survey": self._generate_survey_form,
            "feedback": self._generate_feedback_form,
        }

        generator = form_generators.get(form_type, self._generate_contact_form)
        return generator()

    def _generate_contact_form(self) -> Dict:
        """Generate contact form data."""
        return {
            "name": self.fake.name(),
            "email": self.fake.email(),
            "phone": self.fake.phone_number(),
            "subject": self.fake.sentence(),
            "message": self.fake.text(max_nb_chars=500),
            "preferred_contact": random.choice(["email", "phone"]),
            "department": random.choice(["Sales", "Support", "General Inquiry"]),
        }

    def _generate_registration_form(self) -> Dict:
        """Generate registration form data."""
        return {
            "username": self.fake.user_name(),
            "email": self.fake.email(),
            "password": self._generate_secure_password(),
            "confirm_password": self._generate_secure_password(),  # Same as password in real test
            "first_name": self.fake.first_name(),
            "last_name": self.fake.last_name(),
            "company": self.fake.company(),
            "job_title": self.fake.job(),
            "agree_terms": True,
            "newsletter_subscription": random.choice([True, False]),
        }

    def _generate_survey_form(self) -> Dict:
        """Generate survey form data."""
        return {
            "age_group": random.choice(["18-24", "25-34", "35-44", "45-54", "55+"]),
            "satisfaction_rating": random.randint(1, 5),
            "recommend_likelihood": random.randint(1, 10),
            "product_quality": random.choice(["Excellent", "Good", "Average", "Poor"]),
            "comments": self.fake.text(max_nb_chars=300),
            "would_purchase_again": random.choice(["Yes", "No", "Maybe"]),
        }

    def _generate_feedback_form(self) -> Dict:
        """Generate feedback form data."""
        return {
            "rating": random.randint(1, 5),
            "experience": random.choice(["Excellent", "Good", "Fair", "Poor"]),
            "feedback_text": self.fake.text(max_nb_chars=400),
            "category": random.choice(["Product", "Service", "Website", "Support"]),
            "email_for_followup": self.fake.email(),
        }

    def _generate_secure_password(
        self, length: int = 12, include_special: bool = True
    ) -> str:
        """Generate secure password."""
        import string

        chars = string.ascii_letters + string.digits
        if include_special:
            chars += "!@#$%^&*"

        password = "".join(random.choice(chars) for _ in range(length))

        # Ensure password has required complexity
        password = (
            random.choice(string.ascii_uppercase)
            + random.choice(string.ascii_lowercase)
            + random.choice(string.digits)
            + password[3:]
        )

        return password

    def generate_edge_cases(self, data_type: str) -> List[Any]:
        """
        Generate edge case test data.

        Args:
            data_type: Type of data (email, string, number, date)

        Returns:
            List of edge case values
        """
        edge_cases = {
            "email": [
                "",  # Empty
                "invalid",  # No @
                "@example.com",  # No local part
                "test@",  # No domain
                "test..test@example.com",  # Double dots
                "test@example",  # No TLD
                "a" * 256 + "@example.com",  # Too long
                "test+tag@example.com",  # Valid with tag
                "test@subdomain.example.com",  # Valid subdomain
            ],
            "string": [
                "",  # Empty
                " ",  # Single space
                "a",  # Single character
                "a" * 10000,  # Very long
                '<script>alert("xss")</script>',  # XSS attempt
                "'; DROP TABLE users; --",  # SQL injection
                "../../etc/passwd",  # Path traversal
                "\n\r\t",  # Special characters
                "🎉😀💻",  # Emojis
                "Тест",  # Unicode
            ],
            "number": [
                0,
                -1,
                1,
                999999999,
                -999999999,
                0.1,
                1.7976931348623157e308,  # Max float
                float("inf"),
                float("-inf"),
            ],
            "date": [
                "0000-00-00",
                "9999-12-31",
                "2024-02-30",  # Invalid date
                "2024-13-01",  # Invalid month
                "",
                "not-a-date",
            ],
        }

        return edge_cases.get(data_type, [])

    def generate_dataset(
        self, schema: Dict, count: int = 100, output_format: str = "json"
    ) -> Any:
        """
        Generate custom dataset based on schema.

        Args:
            schema: Data schema definition
            count: Number of records to generate
            output_format: Output format (json, csv, dict)

        Returns:
            Generated dataset
        """
        dataset = []

        for _ in range(count):
            record = {}
            for field, config in schema.items():
                field_type = config.get("type", "string")
                record[field] = self._generate_field_value(field_type, config)

            dataset.append(record)

        if output_format == "json":
            return json.dumps(dataset, indent=2)
        elif output_format == "csv":
            # Convert to CSV format
            import csv
            import io

            output = io.StringIO()
            if dataset:
                writer = csv.DictWriter(output, fieldnames=dataset[0].keys())
                writer.writeheader()
                writer.writerows(dataset)
            return output.getvalue()
        else:
            return dataset

    def _generate_field_value(self, field_type: str, config: Dict) -> Any:
        """Generate value for a specific field type."""
        generators = {
            "string": lambda: self.fake.text(max_nb_chars=config.get("max_length", 50)),
            "email": lambda: self.fake.email(),
            "name": lambda: self.fake.name(),
            "phone": lambda: self.fake.phone_number(),
            "address": lambda: self.fake.address(),
            "date": lambda: self.fake.date(),
            "datetime": lambda: self.fake.date_time().isoformat(),
            "integer": lambda: random.randint(
                config.get("min", 0), config.get("max", 100)
            ),
            "float": lambda: round(
                random.uniform(config.get("min", 0.0), config.get("max", 100.0)), 2
            ),
            "boolean": lambda: random.choice([True, False]),
            "url": lambda: self.fake.url(),
            "uuid": lambda: self.fake.uuid4(),
        }

        generator = generators.get(field_type, lambda: self.fake.text(max_nb_chars=50))
        return generator()

    def save_to_file(self, data: Any, filename: str, format: str = "json"):
        """Save generated data to file."""
        output_dir = Path("test_data")
        output_dir.mkdir(exist_ok=True)

        filepath = output_dir / filename

        if format == "json":
            with open(filepath, "w") as f:
                json.dump(data, f, indent=2, default=str)
        elif format == "csv":
            with open(filepath, "w") as f:
                f.write(data if isinstance(data, str) else json.dumps(data))

        logger.info(f"Data saved to {filepath}")
        return str(filepath)

    def _record_generation(self, data_type: str, count: int):
        """Record data generation for analytics."""
        self.generation_history.append(
            {"type": data_type, "count": count, "timestamp": datetime.now().isoformat()}
        )

    def get_generation_stats(self) -> Dict:
        """Get statistics about data generation."""
        total_generated = sum(h["count"] for h in self.generation_history)

        return {
            "total_records_generated": total_generated,
            "generation_sessions": len(self.generation_history),
            "history": self.generation_history,
        }
