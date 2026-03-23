"""
Schema Detector:
Identifies field names in incoming transaction data and maps them
to a consistent internal schema for the pipeline.
"""

class SchemaDetector:

    # Possible variations of each field name
    FIELD_ALIASES = {
        "date": ["date", "transaction_date", "posted", "day"],
        "description": ["description", "desc", "merchant", "details", "narrative"],
        "amount": ["amount", "value", "amt", "transaction_amount"],
        "category": ["category", "type", "group"],
    }

    @classmethod
    def detect(cls, rows):
        """
        Detect schema from the first non-empty row.
        Returns a mapping:
        {
            "date": "Date",
            "description": "Description",
            "amount": "Amount",
            "category": "Category"
        }
        """

        if not rows:
            return {}

        # Find the first row with actual data
        first_row = next((r for r in rows if r), {})

        detected = {}

        for canonical, aliases in cls.FIELD_ALIASES.items():
            detected_field = cls._match_field(first_row, aliases)
            detected[canonical] = detected_field

        return detected

    @staticmethod
    def _match_field(row, aliases):
        """
        Return the first matching field name from the row based on aliases.
        Case-insensitive.
        """

        lower_map = {k.lower(): k for k in row.keys()}

        for alias in aliases:
            if alias.lower() in lower_map:
                return lower_map[alias.lower()]

        return None
