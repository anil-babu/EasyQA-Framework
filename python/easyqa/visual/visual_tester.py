"""AI-Powered Visual Regression Testing Module."""
import cv2
import numpy as np
from PIL import Image, ImageDraw
import imagehash
from pathlib import Path
from typing import Tuple, Dict, Optional, List
import logging
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class VisualTester:
    """AI-powered visual regression testing with computer vision."""

    def __init__(self, baseline_dir: str = "visual_baselines", threshold: float = 0.95):
        """
        Initialize Visual Tester.

        Args:
            baseline_dir: Directory to store baseline images
            threshold: Similarity threshold (0-1, higher = more strict)
        """
        self.baseline_dir = Path(baseline_dir)
        self.baseline_dir.mkdir(exist_ok=True, parents=True)
        self.threshold = threshold
        self.results_dir = Path("visual_results")
        self.results_dir.mkdir(exist_ok=True, parents=True)

    def capture_baseline(self, screenshot_path: str, test_name: str) -> str:
        """
        Capture baseline image for visual testing.

        Args:
            screenshot_path: Path to screenshot
            test_name: Name of the test

        Returns:
            Path to saved baseline image
        """
        baseline_path = self.baseline_dir / f"{test_name}_baseline.png"
        img = Image.open(screenshot_path)
        img.save(baseline_path)

        # Store perceptual hash
        img_hash = imagehash.phash(img)
        hash_path = self.baseline_dir / f"{test_name}_hash.txt"
        with open(hash_path, 'w') as f:
            f.write(str(img_hash))

        logger.info(f"Baseline captured for {test_name} at {baseline_path}")
        return str(baseline_path)

    def compare_images(
        self,
        baseline_path: str,
        current_path: str,
        test_name: str
    ) -> Dict[str, any]:
        """
        Compare current screenshot with baseline using multiple AI techniques.

        Args:
            baseline_path: Path to baseline image
            current_path: Path to current screenshot
            test_name: Name of the test

        Returns:
            Dictionary containing comparison results
        """
        baseline_img = cv2.imread(baseline_path)
        current_img = cv2.imread(current_path)

        if baseline_img is None or current_img is None:
            raise ValueError("Could not load images for comparison")

        # Resize images to same dimensions if needed
        if baseline_img.shape != current_img.shape:
            current_img = cv2.resize(current_img,
                                    (baseline_img.shape[1], baseline_img.shape[0]))

        # 1. Structural Similarity Index (SSIM)
        ssim_score = self._calculate_ssim(baseline_img, current_img)

        # 2. Perceptual Hash Comparison
        hash_similarity = self._compare_perceptual_hash(baseline_path, current_path)

        # 3. Pixel-by-Pixel Difference
        diff_percentage = self._calculate_pixel_diff(baseline_img, current_img)

        # 4. Feature Matching (AI-based)
        feature_match_score = self._compare_features(baseline_img, current_img)

        # Generate difference image
        diff_img_path = self._generate_diff_image(
            baseline_img, current_img, test_name
        )

        # Calculate overall score
        overall_score = (
            ssim_score * 0.4 +
            hash_similarity * 0.3 +
            (1 - diff_percentage) * 0.2 +
            feature_match_score * 0.1
        )

        result = {
            'test_name': test_name,
            'timestamp': datetime.now().isoformat(),
            'passed': overall_score >= self.threshold,
            'overall_score': round(overall_score, 4),
            'ssim_score': round(ssim_score, 4),
            'hash_similarity': round(hash_similarity, 4),
            'pixel_diff_percentage': round(diff_percentage * 100, 2),
            'feature_match_score': round(feature_match_score, 4),
            'threshold': self.threshold,
            'diff_image_path': diff_img_path,
            'baseline_path': baseline_path,
            'current_path': current_path
        }

        # Save result
        self._save_result(result, test_name)

        return result

    def _calculate_ssim(self, img1: np.ndarray, img2: np.ndarray) -> float:
        """Calculate Structural Similarity Index."""
        # Convert to grayscale
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        # Calculate mean
        mu1 = cv2.GaussianBlur(gray1, (11, 11), 1.5)
        mu2 = cv2.GaussianBlur(gray2, (11, 11), 1.5)

        mu1_sq = mu1 ** 2
        mu2_sq = mu2 ** 2
        mu1_mu2 = mu1 * mu2

        # Calculate variance and covariance
        sigma1_sq = cv2.GaussianBlur(gray1 ** 2, (11, 11), 1.5) - mu1_sq
        sigma2_sq = cv2.GaussianBlur(gray2 ** 2, (11, 11), 1.5) - mu2_sq
        sigma12 = cv2.GaussianBlur(gray1 * gray2, (11, 11), 1.5) - mu1_mu2

        # SSIM formula
        c1 = (0.01 * 255) ** 2
        c2 = (0.03 * 255) ** 2

        ssim_map = ((2 * mu1_mu2 + c1) * (2 * sigma12 + c2)) / \
                   ((mu1_sq + mu2_sq + c1) * (sigma1_sq + sigma2_sq + c2))

        return float(np.mean(ssim_map))

    def _compare_perceptual_hash(self, path1: str, path2: str) -> float:
        """Compare images using perceptual hashing."""
        img1 = Image.open(path1)
        img2 = Image.open(path2)

        hash1 = imagehash.phash(img1)
        hash2 = imagehash.phash(img2)

        # Calculate similarity (0-1 scale)
        hash_diff = hash1 - hash2
        max_diff = len(hash1.hash) ** 2
        similarity = 1 - (hash_diff / max_diff)

        return similarity

    def _calculate_pixel_diff(self, img1: np.ndarray, img2: np.ndarray) -> float:
        """Calculate percentage of different pixels."""
        diff = cv2.absdiff(img1, img2)
        diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(diff_gray, 30, 255, cv2.THRESH_BINARY)

        different_pixels = np.count_nonzero(thresh)
        total_pixels = thresh.shape[0] * thresh.shape[1]

        return different_pixels / total_pixels

    def _compare_features(self, img1: np.ndarray, img2: np.ndarray) -> float:
        """Compare images using feature detection (ORB algorithm)."""
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        # Initialize ORB detector
        orb = cv2.ORB_create(nfeatures=500)

        # Find keypoints and descriptors
        kp1, des1 = orb.detectAndCompute(gray1, None)
        kp2, des2 = orb.detectAndCompute(gray2, None)

        if des1 is None or des2 is None:
            return 0.0

        # Match features
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(des1, des2)

        # Calculate match score
        if len(matches) == 0:
            return 0.0

        good_matches = [m for m in matches if m.distance < 50]
        match_score = len(good_matches) / max(len(kp1), len(kp2))

        return min(match_score, 1.0)

    def _generate_diff_image(
        self,
        baseline: np.ndarray,
        current: np.ndarray,
        test_name: str
    ) -> str:
        """Generate visual difference image highlighting changes."""
        diff = cv2.absdiff(baseline, current)

        # Create a red overlay for differences
        diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(diff_gray, 30, 255, cv2.THRESH_BINARY)

        # Create side-by-side comparison
        h, w = baseline.shape[:2]
        comparison = np.zeros((h, w * 3, 3), dtype=np.uint8)

        comparison[:, :w] = baseline
        comparison[:, w:2*w] = current

        # Highlight differences in third panel
        diff_highlight = current.copy()
        diff_highlight[mask > 0] = [0, 0, 255]  # Red overlay
        comparison[:, 2*w:] = diff_highlight

        # Add labels
        cv2.putText(comparison, 'Baseline', (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(comparison, 'Current', (w + 10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(comparison, 'Differences', (2*w + 10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Save comparison image
        diff_path = self.results_dir / f"{test_name}_diff_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        cv2.imwrite(str(diff_path), comparison)

        logger.info(f"Difference image saved to {diff_path}")
        return str(diff_path)

    def _save_result(self, result: Dict, test_name: str):
        """Save comparison result to JSON."""
        result_path = self.results_dir / f"{test_name}_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(result_path, 'w') as f:
            json.dump(result, f, indent=2)

    def get_ai_insights(self, result: Dict) -> List[str]:
        """Generate AI insights from visual comparison results."""
        insights = []

        if not result['passed']:
            insights.append(f"⚠️ Visual regression detected! Overall score: {result['overall_score']}")

            if result['pixel_diff_percentage'] > 5:
                insights.append(
                    f"🔍 Significant pixel differences detected ({result['pixel_diff_percentage']}%). "
                    "This might indicate layout changes or content updates."
                )

            if result['hash_similarity'] < 0.9:
                insights.append(
                    "📊 Perceptual hash indicates structural changes in the page."
                )

            if result['feature_match_score'] < 0.5:
                insights.append(
                    "🎯 Feature matching shows significant changes in key UI elements."
                )
        else:
            insights.append(f"✅ Visual test passed! Similarity: {result['overall_score']}")

        return insights
