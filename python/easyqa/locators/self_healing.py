"""AI-Powered Self-Healing Locators Module."""
import logging
from typing import Optional, List, Dict, Tuple
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)


class SelfHealingLocator:
    """
    AI-powered self-healing element locator.

    Uses machine learning to automatically fix broken locators by finding
    similar elements based on multiple attributes and context.
    """

    def __init__(self, confidence_threshold: float = 0.8, learning_enabled: bool = True):
        """
        Initialize Self-Healing Locator.

        Args:
            confidence_threshold: Minimum confidence score to accept alternative locator
            learning_enabled: Enable learning from successful healings
        """
        self.confidence_threshold = confidence_threshold
        self.learning_enabled = learning_enabled
        self.healing_history = []
        self.locator_db_path = Path("data/locator_healing_history.json")
        self.locator_db_path.parent.mkdir(exist_ok=True, parents=True)
        self._load_history()

    def find_element(
        self,
        driver: WebDriver,
        by: By,
        value: str,
        context: Optional[Dict] = None
    ) -> Tuple[Optional[WebElement], Dict]:
        """
        Find element with self-healing capabilities.

        Args:
            driver: Selenium WebDriver instance
            by: Locator strategy (By.ID, By.XPATH, etc.)
            value: Locator value
            context: Additional context (page name, element role, etc.)

        Returns:
            Tuple of (WebElement or None, healing metadata)
        """
        metadata = {
            'original_locator': {'by': by, 'value': value},
            'healed': False,
            'confidence': 0.0,
            'attempts': 1,
            'timestamp': datetime.now().isoformat()
        }

        try:
            # Try original locator first
            element = driver.find_element(by, value)
            logger.debug(f"Element found with original locator: {by}={value}")
            return element, metadata

        except NoSuchElementException:
            logger.warning(f"Element not found with original locator: {by}={value}")

            # Attempt self-healing
            healed_element, healing_meta = self._heal_locator(
                driver, by, value, context
            )

            if healed_element:
                metadata.update(healing_meta)
                metadata['healed'] = True

                # Learn from successful healing
                if self.learning_enabled:
                    self._record_healing(by, value, healing_meta, context)

                logger.info(
                    f"✨ Self-healing successful! "
                    f"Confidence: {healing_meta.get('confidence', 0):.2f}"
                )

            return healed_element, metadata

    def _heal_locator(
        self,
        driver: WebDriver,
        original_by: By,
        original_value: str,
        context: Optional[Dict] = None
    ) -> Tuple[Optional[WebElement], Dict]:
        """
        Attempt to heal broken locator using AI techniques.

        Args:
            driver: Selenium WebDriver instance
            original_by: Original locator strategy
            original_value: Original locator value
            context: Additional context

        Returns:
            Tuple of (healed element or None, healing metadata)
        """
        # Check healing history for this locator
        historical_fix = self._check_history(original_by, original_value)
        if historical_fix:
            try:
                element = driver.find_element(
                    historical_fix['healed_by'],
                    historical_fix['healed_value']
                )
                return element, {
                    'healed_by': historical_fix['healed_by'],
                    'healed_value': historical_fix['healed_value'],
                    'confidence': historical_fix['confidence'],
                    'healing_method': 'historical',
                    'attempts': 1
                }
            except NoSuchElementException:
                logger.debug("Historical fix no longer works, trying AI healing")

        # Get all elements on the page
        all_elements = driver.find_elements(By.XPATH, "//*")

        # Generate features for all elements
        element_features = [self._extract_features(elem) for elem in all_elements]

        # Generate target features from original locator
        target_features = self._generate_target_features(original_by, original_value, context)

        # Find best match using ML
        best_match, confidence = self._find_best_match(
            all_elements, element_features, target_features
        )

        if best_match and confidence >= self.confidence_threshold:
            # Generate new locator for the matched element
            new_locator = self._generate_locator(best_match)

            return best_match, {
                'healed_by': new_locator['by'],
                'healed_value': new_locator['value'],
                'confidence': confidence,
                'healing_method': 'ai_matching',
                'attempts': len(all_elements)
            }

        return None, {'confidence': confidence, 'healing_method': 'failed'}

    def _extract_features(self, element: WebElement) -> Dict:
        """Extract features from a WebElement for ML comparison."""
        try:
            return {
                'tag_name': element.tag_name,
                'text': element.text[:100] if element.text else '',
                'id': element.get_attribute('id') or '',
                'class': element.get_attribute('class') or '',
                'name': element.get_attribute('name') or '',
                'type': element.get_attribute('type') or '',
                'placeholder': element.get_attribute('placeholder') or '',
                'aria_label': element.get_attribute('aria-label') or '',
                'role': element.get_attribute('role') or '',
                'data_testid': element.get_attribute('data-testid') or '',
                'href': element.get_attribute('href') or '',
                'is_displayed': element.is_displayed(),
                'is_enabled': element.is_enabled()
            }
        except Exception as e:
            logger.debug(f"Error extracting features: {e}")
            return {}

    def _generate_target_features(
        self,
        by: By,
        value: str,
        context: Optional[Dict]
    ) -> Dict:
        """Generate expected features from original locator."""
        features = {
            'locator_type': by,
            'locator_value': value,
        }

        # Extract hints from locator value
        if by == By.ID:
            features['id'] = value
        elif by == By.NAME:
            features['name'] = value
        elif by == By.CLASS_NAME:
            features['class'] = value
        elif by == By.XPATH:
            # Parse xpath for hints
            features.update(self._parse_xpath_hints(value))
        elif by == By.CSS_SELECTOR:
            features.update(self._parse_css_hints(value))

        # Add context if provided
        if context:
            features.update(context)

        return features

    def _parse_xpath_hints(self, xpath: str) -> Dict:
        """Extract hints from XPath expression."""
        hints = {}

        # Extract tag name
        if '/' in xpath:
            parts = xpath.split('/')
            for part in parts:
                if '[' in part:
                    tag = part.split('[')[0]
                    if tag and tag != '*':
                        hints['tag_name'] = tag.lower()
                        break

        # Extract attribute contains
        if '@' in xpath:
            if 'contains' in xpath:
                # Extract text contains
                if 'text()' in xpath:
                    text_part = xpath.split('text(),')[1].split(')')[0].strip('\'"')
                    hints['text'] = text_part

        return hints

    def _parse_css_hints(self, css: str) -> Dict:
        """Extract hints from CSS selector."""
        hints = {}

        # Extract ID
        if '#' in css:
            id_part = css.split('#')[1].split('[')[0].split('.')[0]
            hints['id'] = id_part

        # Extract class
        if '.' in css:
            class_part = css.split('.')[1].split('[')[0].split('#')[0]
            hints['class'] = class_part

        # Extract tag
        if not css.startswith('[') and not css.startswith('#') and not css.startswith('.'):
            tag = css.split('[')[0].split('#')[0].split('.')[0]
            if tag:
                hints['tag_name'] = tag

        return hints

    def _find_best_match(
        self,
        elements: List[WebElement],
        element_features: List[Dict],
        target_features: Dict
    ) -> Tuple[Optional[WebElement], float]:
        """Find best matching element using ML similarity."""
        if not elements:
            return None, 0.0

        # Calculate similarity scores
        scores = []
        for features in element_features:
            score = self._calculate_similarity(features, target_features)
            scores.append(score)

        # Find best match
        best_idx = np.argmax(scores)
        best_score = scores[best_idx]

        if best_score >= self.confidence_threshold:
            return elements[best_idx], best_score

        return None, best_score

    def _calculate_similarity(self, elem_features: Dict, target_features: Dict) -> float:
        """Calculate similarity score between element and target features."""
        score = 0.0
        weights = {
            'id': 0.25,
            'name': 0.20,
            'data_testid': 0.20,
            'class': 0.10,
            'tag_name': 0.05,
            'text': 0.10,
            'type': 0.05,
            'aria_label': 0.05
        }

        for attr, weight in weights.items():
            if attr in target_features and attr in elem_features:
                target_val = str(target_features[attr]).lower()
                elem_val = str(elem_features[attr]).lower()

                if target_val and elem_val:
                    # Exact match
                    if target_val == elem_val:
                        score += weight
                    # Partial match
                    elif target_val in elem_val or elem_val in target_val:
                        score += weight * 0.7
                    # Text similarity using simple comparison
                    else:
                        text_sim = self._text_similarity(target_val, elem_val)
                        score += weight * text_sim

        return score

    def _text_similarity(self, text1: str, text2: str) -> float:
        """Calculate text similarity using character overlap."""
        if not text1 or not text2:
            return 0.0

        # Simple character overlap similarity
        set1 = set(text1.lower())
        set2 = set(text2.lower())
        intersection = set1.intersection(set2)
        union = set1.union(set2)

        if not union:
            return 0.0

        return len(intersection) / len(union)

    def _generate_locator(self, element: WebElement) -> Dict:
        """Generate stable locator for an element."""
        # Priority order for locator strategies
        locator_strategies = [
            ('id', lambda e: e.get_attribute('id')),
            ('data-testid', lambda e: e.get_attribute('data-testid')),
            ('name', lambda e: e.get_attribute('name')),
            ('aria-label', lambda e: e.get_attribute('aria-label')),
        ]

        for attr, getter in locator_strategies:
            value = getter(element)
            if value:
                by_type = By.ID if attr == 'id' else By.CSS_SELECTOR
                selector = value if attr == 'id' else f"[{attr}='{value}']"
                return {'by': by_type, 'value': selector}

        # Fallback to XPath
        return {
            'by': By.XPATH,
            'value': self._generate_xpath(element)
        }

    def _generate_xpath(self, element: WebElement) -> str:
        """Generate XPath for an element."""
        # This is a simplified version - production would use JavaScript
        tag = element.tag_name
        elem_id = element.get_attribute('id')

        if elem_id:
            return f"//{tag}[@id='{elem_id}']"

        elem_class = element.get_attribute('class')
        if elem_class:
            return f"//{tag}[@class='{elem_class}']"

        return f"//{tag}"

    def _check_history(self, by: By, value: str) -> Optional[Dict]:
        """Check healing history for previously fixed locator."""
        for record in self.healing_history:
            if (record['original_by'] == by and
                record['original_value'] == value and
                record['success_count'] > 0):
                return record
        return None

    def _record_healing(
        self,
        original_by: By,
        original_value: str,
        healing_meta: Dict,
        context: Optional[Dict]
    ):
        """Record successful healing for future use."""
        record = {
            'original_by': original_by,
            'original_value': original_value,
            'healed_by': healing_meta.get('healed_by'),
            'healed_value': healing_meta.get('healed_value'),
            'confidence': healing_meta.get('confidence'),
            'context': context,
            'timestamp': datetime.now().isoformat(),
            'success_count': 1
        }

        # Check if already recorded
        for existing in self.healing_history:
            if (existing['original_by'] == original_by and
                existing['original_value'] == original_value):
                existing['success_count'] += 1
                existing['last_used'] = datetime.now().isoformat()
                self._save_history()
                return

        self.healing_history.append(record)
        self._save_history()

    def _load_history(self):
        """Load healing history from disk."""
        if self.locator_db_path.exists():
            with open(self.locator_db_path, 'r') as f:
                self.healing_history = json.load(f)

    def _save_history(self):
        """Save healing history to disk."""
        with open(self.locator_db_path, 'w') as f:
            json.dump(self.healing_history, f, indent=2)

    def get_healing_stats(self) -> Dict:
        """Get statistics about healing performance."""
        if not self.healing_history:
            return {
                'total_healings': 0,
                'success_rate': 0.0,
                'most_healed_locators': []
            }

        total = len(self.healing_history)
        successful = sum(1 for h in self.healing_history if h['success_count'] > 0)

        # Sort by success count
        sorted_history = sorted(
            self.healing_history,
            key=lambda x: x['success_count'],
            reverse=True
        )[:10]

        return {
            'total_healings': total,
            'success_rate': (successful / total * 100) if total > 0 else 0,
            'most_healed_locators': [
                {
                    'locator': f"{h['original_by']}={h['original_value']}",
                    'healed_to': f"{h['healed_by']}={h['healed_value']}",
                    'times_used': h['success_count']
                }
                for h in sorted_history
            ]
        }
