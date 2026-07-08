import unittest

from editorial_ai.core.models import MarketSnapshot, TrendSignal
from editorial_ai.core.scoring import score_opportunity


class ScoringTest(unittest.TestCase):
    def test_lower_competition_improves_score(self) -> None:
        signal = TrendSignal(
            niche="guias de prompts de IA para profesores",
            source="test",
            demand_score=80,
            momentum_score=75,
            audience_hint="profesores",
            keywords=("prompts", "ia", "profesores"),
        )
        high_competition = MarketSnapshot(
            niche=signal.niche,
            title_angle="high",
            audience="profesores",
            competition_score=80,
            margin_score=70,
            seo_score=70,
            source="test",
        )
        low_competition = MarketSnapshot(
            niche=signal.niche,
            title_angle="low",
            audience="profesores",
            competition_score=20,
            margin_score=70,
            seo_score=70,
            source="test",
        )

        self.assertGreater(
            score_opportunity(signal, low_competition),
            score_opportunity(signal, high_competition),
        )

