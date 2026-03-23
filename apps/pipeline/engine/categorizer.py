"""
Categorizer module:
Assigns categories to transactions based on simple rules or keyword matching.
"""

class Categorizer:

    # Basic keyword rules (can be expanded later)
    RULES = {
        "food": ["mcdonald", "kfc", "burger", "pizza", "restaurant", "cafe"],
        "transport": ["uber", "taxi", "bus", "train", "fuel", "petrol"],
        "shopping": ["amazon", "ebay", "store", "shop"],
        "utilities": ["electric", "water", "gas", "internet", "broadband"],
        "rent": ["rent", "landlord"],
        "salary": ["salary", "payroll", "wage"],
    }

    @classmethod
    def assign(cls, transactions):
        """
        Assign categories to a list of transaction dicts.
        Each transaction must have a 'description' field.
        """

        categorized = []

        for tx in transactions:
            description = tx.get("description", "").lower()
            category = cls._detect_category(description)
            tx["category"] = category
            categorized.append(tx)

        return categorized

    @classmethod
    def _detect_category(cls, description):
        """Return the first matching category based on keyword rules."""

        for category, keywords in cls.RULES.items():
            if any(keyword in description for keyword in keywords):
                return category

        return "other"
