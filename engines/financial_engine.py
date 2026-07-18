"""
Deterministic Financial Engine

AI NEVER performs financial calculations.
"""


class FinancialEngine:

    def calculate_roi(self, investment, annual_return):

        if investment == 0:
            return 0

        return round((annual_return / investment) * 100, 2)

    def calculate_payback(self, investment, annual_return):

        if annual_return <= 0:
            return None

        return round(investment / annual_return, 2)

    def calculate_npv(
        self,
        investment,
        annual_return,
        years=10,
        discount_rate=.08
    ):

        pv = 0

        for year in range(1, years + 1):

            pv += annual_return / ((1 + discount_rate) ** year)

        return round(pv - investment, 2)