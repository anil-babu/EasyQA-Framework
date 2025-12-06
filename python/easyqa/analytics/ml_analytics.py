"""ML-Powered Test Analytics and Insights."""
try:
    import numpy as np
    from sklearn.ensemble import RandomForestClassifier
    import pandas as pd
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    import warnings
    warnings.warn("scikit-learn/pandas not available. ML features will be limited. "
                  "Install with: pip install scikit-learn pandas numpy")

from typing import List, Dict, Optional
import json
from pathlib import Path
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class MLAnalytics:
    """
    Machine Learning powered test analytics.

    Provides predictive insights, failure pattern detection,
    and intelligent test recommendations.
    """

    def __init__(self, history_file: str = 'data/test_history.json'):
        """
        Initialize ML Analytics.

        Args:
            history_file: Path to test history database
        """
        self.history_file = Path(history_file)
        self.history_file.parent.mkdir(exist_ok=True, parents=True)
        self.test_history = self._load_history()
        self.model = None
        self.label_encoders = {}

    def record_test_result(self, result: Dict):
        """Record test execution result for ML training."""
        result['timestamp'] = datetime.now().isoformat()
        self.test_history.append(result)
        self._save_history()

    def predict_test_failure(self, test_metadata: Dict) -> Dict:
        """
        Predict likelihood of test failure using ML.

        Args:
            test_metadata: Test metadata (name, tags, history, etc.)

        Returns:
            Prediction with probability and insights
        """
        if not ML_AVAILABLE:
            return {
                'prediction': 'ml_unavailable',
                'probability': 0.0,
                'confidence': 'low',
                'message': 'ML libraries not installed. Install with: pip install scikit-learn pandas numpy'
            }

        if len(self.test_history) < 50:
            return {
                'prediction': 'insufficient_data',
                'probability': 0.0,
                'confidence': 'low',
                'message': 'Not enough historical data for prediction'
            }

        # Train model if not already trained
        if self.model is None:
            self._train_failure_predictor()

        if self.model is None:
            return {
                'prediction': 'error',
                'probability': 0.0,
                'confidence': 'low',
                'message': 'Model training failed'
            }

        # Prepare features
        features = self._extract_features(test_metadata)

        # Make prediction
        try:
            prediction_proba = self.model.predict_proba([features])[0]
            failure_probability = prediction_proba[1]  # Probability of failure

            prediction = {
                'prediction': 'likely_to_fail' if failure_probability > 0.7 else 'likely_to_pass',
                'probability': round(failure_probability, 3),
                'confidence': self._get_confidence_level(failure_probability),
                'insights': self._generate_prediction_insights(
                    test_metadata,
                    failure_probability
                )
            }

            return prediction

        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            return {
                'prediction': 'error',
                'probability': 0.0,
                'confidence': 'low',
                'error': str(e)
            }

    def _train_failure_predictor(self):
        """Train ML model to predict test failures."""
        if not ML_AVAILABLE:
            logger.warning("ML libraries not available")
            return

        if len(self.test_history) < 50:
            logger.warning("Insufficient data to train model")
            return

        # Prepare training data
        features_list = []
        labels = []

        for record in self.test_history:
            features = self._extract_features(record)
            features_list.append(features)
            labels.append(1 if record.get('status') == 'failed' else 0)

        X = np.array(features_list)
        y = np.array(labels)

        # Train Random Forest model
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.model.fit(X, y)

        logger.info("Failure prediction model trained successfully")

    def _extract_features(self, test_data: Dict) -> List[float]:
        """Extract numerical features from test metadata."""
        features = []

        # Feature 1: Test execution time
        exec_time = test_data.get('execution_time', 0)
        features.append(exec_time)

        # Feature 2: Number of steps
        steps = test_data.get('step_count', 0)
        features.append(steps)

        # Feature 3: Browser type (encoded)
        browser = test_data.get('browser', 'chrome')
        browser_encoded = {'chrome': 0, 'firefox': 1, 'safari': 2, 'edge': 3}.get(browser, 0)
        features.append(browser_encoded)

        # Feature 4: Test priority
        priority = test_data.get('priority', 'medium')
        priority_encoded = {'low': 0, 'medium': 1, 'high': 2, 'critical': 3}.get(priority, 1)
        features.append(priority_encoded)

        # Feature 5: Time of day (hour)
        timestamp = test_data.get('timestamp', datetime.now().isoformat())
        hour = datetime.fromisoformat(timestamp).hour
        features.append(hour)

        # Feature 6: Day of week
        day_of_week = datetime.fromisoformat(timestamp).weekday()
        features.append(day_of_week)

        # Feature 7: Recent failure rate
        recent_failures = self._calculate_recent_failure_rate(test_data.get('name', ''))
        features.append(recent_failures)

        return features

    def _calculate_recent_failure_rate(self, test_name: str, days: int = 7) -> float:
        """Calculate failure rate for a test in recent days."""
        cutoff_date = datetime.now() - timedelta(days=days)

        recent_results = [
            r for r in self.test_history
            if r.get('name') == test_name and
            datetime.fromisoformat(r.get('timestamp', datetime.now().isoformat())) > cutoff_date
        ]

        if not recent_results:
            return 0.0

        failures = sum(1 for r in recent_results if r.get('status') == 'failed')
        return failures / len(recent_results)

    def _get_confidence_level(self, probability: float) -> str:
        """Determine confidence level based on probability."""
        if probability > 0.8 or probability < 0.2:
            return 'high'
        elif probability > 0.6 or probability < 0.4:
            return 'medium'
        else:
            return 'low'

    def _generate_prediction_insights(
        self,
        test_metadata: Dict,
        failure_probability: float
    ) -> List[str]:
        """Generate insights about the prediction."""
        insights = []

        if failure_probability > 0.7:
            insights.append("⚠️ High likelihood of failure detected")

            # Check for patterns
            recent_rate = self._calculate_recent_failure_rate(test_metadata.get('name', ''))
            if recent_rate > 0.5:
                insights.append(
                    f"📊 Test has failed {recent_rate*100:.0f}% of times recently"
                )

            browser = test_metadata.get('browser', 'unknown')
            browser_failures = self._get_browser_failure_rate(browser)
            if browser_failures > 0.3:
                insights.append(
                    f"🌐 {browser} browser shows higher failure rates ({browser_failures*100:.0f}%)"
                )

        return insights

    def _get_browser_failure_rate(self, browser: str) -> float:
        """Calculate failure rate for specific browser."""
        browser_tests = [
            r for r in self.test_history
            if r.get('browser') == browser
        ]

        if not browser_tests:
            return 0.0

        failures = sum(1 for r in browser_tests if r.get('status') == 'failed')
        return failures / len(browser_tests)

    def analyze_failure_patterns(self) -> Dict:
        """Analyze patterns in test failures."""
        if not self.test_history:
            return {'message': 'No test history available'}

        if not ML_AVAILABLE:
            return self._analyze_failure_patterns_basic()

        df = pd.DataFrame(self.test_history)

        analysis = {
            'total_tests': len(df),
            'failure_rate': len(df[df['status'] == 'failed']) / len(df) if len(df) > 0 else 0,
            'most_failing_tests': self._get_most_failing_tests(df),
            'failure_by_browser': self._get_failures_by_browser(df),
            'failure_by_time': self._get_failures_by_time(df),
            'flaky_tests': self._detect_flaky_tests(df)
        }

        return analysis

    def _analyze_failure_patterns_basic(self) -> Dict:
        """Basic failure analysis without pandas (fallback)."""
        total_tests = len(self.test_history)
        failures = [t for t in self.test_history if t.get('status') == 'failed']
        failure_rate = len(failures) / total_tests if total_tests > 0 else 0

        # Count failures by test name
        test_failures = {}
        for result in self.test_history:
            name = result.get('name', 'unknown')
            status = result.get('status')
            if name not in test_failures:
                test_failures[name] = {'total': 0, 'failed': 0}
            test_failures[name]['total'] += 1
            if status == 'failed':
                test_failures[name]['failed'] += 1

        # Get most failing tests
        most_failing = sorted(
            test_failures.items(),
            key=lambda x: x[1]['failed'] / x[1]['total'] if x[1]['total'] > 0 else 0,
            reverse=True
        )[:5]

        return {
            'total_tests': total_tests,
            'failure_rate': failure_rate,
            'most_failing_tests': [
                {
                    'test_name': name,
                    'failure_rate': stats['failed'] / stats['total'] if stats['total'] > 0 else 0
                }
                for name, stats in most_failing
            ],
            'failure_by_browser': {},
            'failure_by_time': {},
            'flaky_tests': []
        }

    def _get_most_failing_tests(self, df) -> List[Dict]:
        """Get tests with highest failure rates."""
        test_stats = df.groupby('name').agg({
            'status': lambda x: (x == 'failed').sum() / len(x)
        }).reset_index()

        test_stats.columns = ['test_name', 'failure_rate']
        top_failing = test_stats.nlargest(5, 'failure_rate')

        return [
            {
                'test_name': row['test_name'],
                'failure_rate': round(row['failure_rate'], 3)
            }
            for _, row in top_failing.iterrows()
        ]

    def _get_failures_by_browser(self, df) -> Dict:
        """Analyze failures by browser."""
        if 'browser' not in df.columns:
            return {}

        browser_stats = df.groupby('browser').agg({
            'status': lambda x: (x == 'failed').sum() / len(x)
        })

        return {
            browser: round(rate, 3)
            for browser, rate in browser_stats['status'].items()
        }

    def _get_failures_by_time(self, df) -> Dict:
        """Analyze failures by time of day."""
        if 'timestamp' not in df.columns:
            return {}

        df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
        time_stats = df.groupby('hour').agg({
            'status': lambda x: (x == 'failed').sum() / len(x)
        })

        return {
            int(hour): round(rate, 3)
            for hour, rate in time_stats['status'].items()
        }

    def _detect_flaky_tests(self, df) -> List[str]:
        """Detect flaky tests (inconsistent pass/fail)."""
        flaky_tests = []

        for test_name in df['name'].unique():
            test_results = df[df['name'] == test_name]['status'].tolist()

            if len(test_results) < 5:  # Need sufficient runs
                continue

            # Check for alternating results
            passes = sum(1 for s in test_results if s == 'passed')
            total = len(test_results)

            # Flaky if 20-80% failure rate (not consistently passing or failing)
            failure_rate = (total - passes) / total
            if 0.2 < failure_rate < 0.8:
                flaky_tests.append(test_name)

        return flaky_tests

    def generate_test_insights(self) -> Dict:
        """Generate comprehensive insights from test data."""
        analysis = self.analyze_failure_patterns()

        insights = {
            'summary': {
                'total_tests_executed': analysis.get('total_tests', 0),
                'overall_failure_rate': round(analysis.get('failure_rate', 0), 3),
                'flaky_test_count': len(analysis.get('flaky_tests', []))
            },
            'recommendations': [],
            'trends': self._analyze_trends() if ML_AVAILABLE else {'message': 'ML not available'}
        }

        # Generate recommendations
        if analysis.get('failure_rate', 0) > 0.2:
            insights['recommendations'].append(
                "⚠️ High overall failure rate detected. Consider reviewing test stability."
            )

        flaky_tests = analysis.get('flaky_tests', [])
        if flaky_tests:
            insights['recommendations'].append(
                f"🔄 {len(flaky_tests)} flaky tests detected. These need investigation:"
            )
            insights['recommendations'].extend([f"  - {test}" for test in flaky_tests[:5]])

        return insights

    def _analyze_trends(self) -> Dict:
        """Analyze trends over time."""
        if len(self.test_history) < 10:
            return {'message': 'Insufficient data for trend analysis'}

        if not ML_AVAILABLE:
            return {'message': 'ML libraries required for trend analysis'}

        df = pd.DataFrame(self.test_history)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')

        # Calculate rolling failure rate
        df['is_failure'] = (df['status'] == 'failed').astype(int)
        df['rolling_failure_rate'] = df['is_failure'].rolling(window=10).mean()

        recent_trend = df['rolling_failure_rate'].tail(10).mean()
        previous_trend = df['rolling_failure_rate'].head(10).mean()

        return {
            'recent_failure_rate': round(recent_trend, 3) if not pd.isna(recent_trend) else 0.0,
            'trend': 'improving' if recent_trend < previous_trend else 'degrading'
        }

    def _load_history(self) -> List[Dict]:
        """Load test history from file."""
        if self.history_file.exists():
            with open(self.history_file, 'r') as f:
                return json.load(f)
        return []

    def _save_history(self):
        """Save test history to file."""
        with open(self.history_file, 'w') as f:
            json.dump(self.test_history, f, indent=2)
