from pathlib import Path
import unittest

from editorial_ai.core.storage import SQLiteOpportunityRepository
from editorial_ai.modules.market_intelligence.service import MarketIntelligenceService


class MarketIntelligenceTest(unittest.TestCase):
    def test_refresh_creates_top_10_for_each_window(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            repository = SQLiteOpportunityRepository(Path(tmp) / "editorial.sqlite")
            repository.setup()

            service = MarketIntelligenceService(repository)
            snapshot = service.refresh()
            top_by_window = service.top_by_window(snapshot, limit=10)

            self.assertEqual(set(top_by_window), {"1y", "6m", "1m", "15d"})
            self.assertEqual(len(top_by_window["1y"]), 10)
            self.assertGreater(top_by_window["1y"][0]["estimated_views"], 0)
            self.assertEqual(repository.latest_market_intelligence_snapshot().provider, snapshot.provider)

