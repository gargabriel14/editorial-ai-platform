from pathlib import Path
import unittest

from editorial_ai.core.platform import build_default_platform
from editorial_ai.web.dashboard import build_dashboard_data


class DashboardTest(unittest.TestCase):
    def test_dashboard_builds_detail_rows_from_database(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "editorial.sqlite"
            platform = build_default_platform(db_path)
            platform.run_opportunity_pipeline(["guias de prompts de IA para profesores"])

            dashboard = build_dashboard_data(db_path)

            self.assertEqual(dashboard["kpis"]["opportunities"], 1)
            self.assertEqual(len(dashboard["items"]), 1)
            self.assertIn("seo_pack", dashboard["items"][0])
            self.assertIn("structure", dashboard["items"][0])
            self.assertIn("kdp_launch_readiness", dashboard["items"][0])
            self.assertIn("top_kdp_score", dashboard["kpis"])
            self.assertIn("ceo_cto_protocol", dashboard)

