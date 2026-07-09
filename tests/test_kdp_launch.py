import unittest

from editorial_ai.core.models import Opportunity
from editorial_ai.core.utils import utc_now_iso
from editorial_ai.modules.kdp_launch.service import KDPLaunchReadinessService
from editorial_ai.modules.seo_amazon.service import AmazonSEOService


class KDPLaunchReadinessTest(unittest.TestCase):
    def test_freelance_opportunity_gets_actionable_kdp_plan(self) -> None:
        opportunity = Opportunity(
            id="opp_test",
            niche="habitos de productividad para freelancers",
            title_angle="habitos de productividad para freelancers: guia practica en 30 dias",
            audience="profesionales independientes",
            demand_score=74.5,
            trend_score=78,
            competition_score=37,
            margin_score=74,
            seo_score=69,
            total_score=73.2,
            status="discovered",
            source="test",
            rationale="test",
            keywords=("habitos", "productividad", "freelancers"),
            created_at=utc_now_iso(),
        )
        seo_pack = AmazonSEOService().build_pack(opportunity)

        readiness = KDPLaunchReadinessService().assess(opportunity, seo_pack)

        self.assertEqual(len(readiness.optimization.backend_keywords), 7)
        self.assertTrue(readiness.series.can_be_series)
        self.assertIn(readiness.recommendation, {"Aprobar piloto", "Convertir en serie"})
        self.assertIn("Reviews may not be required", readiness.compliance.review_policy_warning)

