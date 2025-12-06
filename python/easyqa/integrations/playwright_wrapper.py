"""Playwright Integration with AI Enhancements."""

import asyncio
from typing import Optional, Dict, List
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from pathlib import Path
import logging
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class PlaywrightAI:
    """
    Enhanced Playwright wrapper with AI capabilities.

    Provides modern browser automation with built-in AI features like
    auto-waiting, network monitoring, and intelligent element interaction.
    """

    def __init__(
        self, browser_type: str = "chromium", headless: bool = False, slow_mo: int = 0
    ):
        """
        Initialize Playwright AI wrapper.

        Args:
            browser_type: Browser to use (chromium, firefox, webkit)
            headless: Run in headless mode
            slow_mo: Slow down operations by specified milliseconds
        """
        self.browser_type = browser_type
        self.headless = headless
        self.slow_mo = slow_mo
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.playwright = None
        self.performance_data = []
        self.network_logs = []

    async def start(
        self,
        viewport: Optional[Dict] = None,
        user_agent: Optional[str] = None,
        record_video: bool = False,
    ):
        """
        Start browser instance with enhanced capabilities.

        Args:
            viewport: Custom viewport size {'width': 1920, 'height': 1080}
            user_agent: Custom user agent string
            record_video: Enable video recording
        """
        self.playwright = await async_playwright().start()

        browser_launcher = {
            "chromium": self.playwright.chromium,
            "firefox": self.playwright.firefox,
            "webkit": self.playwright.webkit,
        }[self.browser_type]

        # Browser launch options
        launch_options = {
            "headless": self.headless,
            "slow_mo": self.slow_mo,
            "args": ["--disable-dev-shm-usage", "--no-sandbox"],
        }

        self.browser = await browser_launcher.launch(**launch_options)

        # Context options with AI enhancements
        context_options = {
            "viewport": viewport or {"width": 1920, "height": 1080},
            "user_agent": user_agent,
            "record_har_path": f'logs/network_{datetime.now().strftime("%Y%m%d_%H%M%S")}.har',
            "record_video_dir": "videos" if record_video else None,
        }

        self.context = await self.browser.new_context(**context_options)

        # Enable network monitoring
        self.context.on("request", self._on_request)
        self.context.on("response", self._on_response)

        self.page = await self.context.new_page()

        # Enable console logging
        self.page.on(
            "console", lambda msg: logger.debug(f"Browser console: {msg.text}")
        )

        # Performance monitoring
        self.page.on("load", self._on_load)

        logger.info(f"Playwright browser started: {self.browser_type}")

    async def navigate(self, url: str, wait_until: str = "load"):
        """
        Navigate to URL with intelligent waiting.

        Args:
            url: URL to navigate to
            wait_until: Wait strategy ('load', 'domcontentloaded', 'networkidle')
        """
        logger.info(f"Navigating to: {url}")

        start_time = datetime.now()
        await self.page.goto(url, wait_until=wait_until)
        load_time = (datetime.now() - start_time).total_seconds()

        # Record performance
        performance = await self.get_performance_metrics()
        performance["page_load_time"] = load_time
        self.performance_data.append(performance)

        logger.info(f"Page loaded in {load_time:.2f}s")

    async def ai_click(
        self, selector: str, smart_wait: bool = True, retry_count: int = 3
    ):
        """
        AI-enhanced click with smart waiting and retries.

        Args:
            selector: Element selector
            smart_wait: Enable smart waiting for element
            retry_count: Number of retry attempts
        """
        for attempt in range(retry_count):
            try:
                if smart_wait:
                    await self.page.wait_for_selector(selector, state="visible")

                await self.page.click(selector)
                logger.debug(f"Clicked element: {selector}")
                return

            except Exception as e:
                if attempt < retry_count - 1:
                    logger.warning(f"Click attempt {attempt + 1} failed, retrying...")
                    await asyncio.sleep(1)
                else:
                    logger.error(f"Failed to click {selector}: {e}")
                    raise

    async def ai_fill(
        self, selector: str, text: str, clear_first: bool = True, delay: int = 50
    ):
        """
        AI-enhanced form filling with human-like typing.

        Args:
            selector: Input selector
            text: Text to type
            clear_first: Clear field before typing
            delay: Delay between keystrokes (ms)
        """
        await self.page.wait_for_selector(selector, state="visible")

        if clear_first:
            await self.page.fill(selector, "")

        # Human-like typing
        await self.page.type(selector, text, delay=delay)
        logger.debug(f"Filled {selector} with text")

    async def smart_wait_for_element(
        self, selector: str, timeout: int = 30000, state: str = "visible"
    ):
        """
        Smart wait for element with multiple strategies.

        Args:
            selector: Element selector
            timeout: Timeout in milliseconds
            state: Element state to wait for
        """
        try:
            await self.page.wait_for_selector(selector, timeout=timeout, state=state)
            return True
        except Exception as e:
            logger.error(f"Element not found: {selector} - {e}")
            return False

    async def capture_screenshot(
        self, filename: Optional[str] = None, full_page: bool = True
    ) -> str:
        """
        Capture screenshot with AI metadata.

        Args:
            filename: Output filename
            full_page: Capture full scrollable page

        Returns:
            Path to screenshot
        """
        if not filename:
            filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

        screenshot_path = Path("screenshots") / filename
        screenshot_path.parent.mkdir(exist_ok=True, parents=True)

        await self.page.screenshot(path=str(screenshot_path), full_page=full_page)

        logger.info(f"Screenshot saved: {screenshot_path}")
        return str(screenshot_path)

    async def get_performance_metrics(self) -> Dict:
        """Get comprehensive performance metrics."""
        try:
            metrics = await self.page.evaluate(
                """() => {
                const perfData = window.performance.timing;
                const navigation = performance.getEntriesByType('navigation')[0];

                return {
                    domContentLoaded: perfData.domContentLoadedEventEnd - perfData.navigationStart,
                    loadComplete: perfData.loadEventEnd - perfData.navigationStart,
                    firstPaint: navigation ? navigation.responseStart - navigation.requestStart : 0,
                    domInteractive: perfData.domInteractive - perfData.navigationStart,
                    resourceLoadTime: perfData.responseEnd - perfData.requestStart
                };
            }"""
            )

            return metrics
        except Exception as e:
            logger.error(f"Failed to get performance metrics: {e}")
            return {}

    async def run_lighthouse_audit(self) -> Dict:
        """
        Run Lighthouse performance audit.

        Returns:
            Lighthouse audit results
        """
        # This would require lighthouse integration
        # For now, return basic performance metrics
        metrics = await self.get_performance_metrics()

        # Calculate basic scores
        load_time = metrics.get("loadComplete", 0) / 1000
        performance_score = max(0, 100 - (load_time * 10))  # Simplified scoring

        return {
            "performance": performance_score,
            "metrics": metrics,
            "timestamp": datetime.now().isoformat(),
        }

    async def get_accessibility_violations(self) -> List[Dict]:
        """
        Check for accessibility violations using axe-core.

        Returns:
            List of accessibility violations
        """
        try:
            # Inject axe-core
            await self.page.add_script_tag(
                url="https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.7.2/axe.min.js"
            )

            # Run axe analysis
            violations = await self.page.evaluate(
                """async () => {
                const results = await axe.run();
                return results.violations;
            }"""
            )

            logger.info(f"Found {len(violations)} accessibility violations")
            return violations

        except Exception as e:
            logger.error(f"Accessibility check failed: {e}")
            return []

    async def ai_extract_data(self, schema: Dict) -> Dict:
        """
        AI-powered data extraction from page.

        Args:
            schema: Data schema defining what to extract

        Returns:
            Extracted data matching schema
        """
        data = {}

        for field, selector_info in schema.items():
            try:
                selector = selector_info.get("selector")
                extract_type = selector_info.get("type", "text")

                if extract_type == "text":
                    element = await self.page.query_selector(selector)
                    if element:
                        data[field] = await element.inner_text()

                elif extract_type == "attribute":
                    attribute = selector_info.get("attribute")
                    element = await self.page.query_selector(selector)
                    if element:
                        data[field] = await element.get_attribute(attribute)

                elif extract_type == "list":
                    elements = await self.page.query_selector_all(selector)
                    data[field] = [await elem.inner_text() for elem in elements]

            except Exception as e:
                logger.warning(f"Failed to extract {field}: {e}")
                data[field] = None

        return data

    async def network_idle_wait(self, timeout: int = 30000):
        """Wait for network to be idle (no requests for 500ms)."""
        await self.page.wait_for_load_state("networkidle", timeout=timeout)

    def _on_request(self, request):
        """Handle network request."""
        self.network_logs.append(
            {
                "type": "request",
                "method": request.method,
                "url": request.url,
                "timestamp": datetime.now().isoformat(),
            }
        )

    def _on_response(self, response):
        """Handle network response."""
        self.network_logs.append(
            {
                "type": "response",
                "status": response.status,
                "url": response.url,
                "timestamp": datetime.now().isoformat(),
            }
        )

    def _on_load(self):
        """Handle page load event."""
        logger.debug("Page loaded successfully")

    async def get_network_summary(self) -> Dict:
        """Get network activity summary."""
        requests = [log for log in self.network_logs if log["type"] == "request"]
        responses = [log for log in self.network_logs if log["type"] == "response"]

        failed_requests = [r for r in responses if r["status"] >= 400]

        return {
            "total_requests": len(requests),
            "total_responses": len(responses),
            "failed_requests": len(failed_requests),
            "failed_urls": [r["url"] for r in failed_requests],
        }

    async def close(self):
        """Close browser and save artifacts."""
        if self.context:
            # Save network logs
            log_path = (
                Path("logs")
                / f"network_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )
            log_path.parent.mkdir(exist_ok=True, parents=True)

            with open(log_path, "w") as f:
                json.dump(
                    {
                        "network_logs": self.network_logs,
                        "performance_data": self.performance_data,
                    },
                    f,
                    indent=2,
                )

            await self.context.close()

        if self.browser:
            await self.browser.close()

        if self.playwright:
            await self.playwright.stop()

        logger.info("Browser closed and artifacts saved")

    async def __aenter__(self):
        """Context manager entry."""
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        await self.close()
