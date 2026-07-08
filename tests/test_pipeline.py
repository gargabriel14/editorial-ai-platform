from pathlib import Path
import unittest

from editorial_ai.core.platform import build_default_platform
from editorial_ai.core.storage import SQLiteOpportunityRepository


class PipelineTest(unittest.TestCase):
    def test_pipeline_persists_opportunities(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "editorial.sqlite"
            platform = build_default_platform(db_path)

            result = platform.run_opportunity_pipeline(["guias de prompts de IA para profesores"])

            self.assertEqual(len(result.opportunities), 1)
            self.assertEqual(result.structures[0].opportunity_id, result.opportunities[0].id)
            self.assertEqual(result.seo_packs[0].opportunity_id, result.opportunities[0].id)

            repository = SQLiteOpportunityRepository(db_path)
            stored = repository.list_opportunities()

            self.assertEqual(len(stored), 1)
            self.assertEqual(stored[0].id, result.opportunities[0].id)

