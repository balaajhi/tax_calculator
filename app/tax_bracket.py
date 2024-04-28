class TaxBracket:
    """Represents a tax bracket with minimum and maximum income thresholds and the corresponding tax rate."""

    def __init__(self, min_income, max_income=None, rate=0):
        """Initialize TaxBracket with min_income, max_income, and rate."""
        self.min_income = min_income
        self.max_income = max_income
        self.rate = rate
