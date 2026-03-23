
class Cleaner:
    """
    Cleaner module:
    Removes noise, trims whitespace, and ensures consistent basic formatting.
    """

    REQUIRED_FIELDS = ["date", "amount", "description"]

    @classmethod
    def clean(cls, transactions):
        """
        Clean a list of transaction dicts.
        - Trim whitespace
        - Remove empty or null fields
        - Ensure required fields exist
        """

        cleaned = []

        for tx in transactions:
            cleaned_tx = cls._clean_single(tx)
            cleaned.append(cleaned_tx)

        return cleaned

    @classmethod
    def _clean_single(cls, tx):
        """Clean a single transaction dict."""

        # Trim whitespace from string fields
        for key, value in tx.items():
            if isinstance(value, str):
                tx[key] = value.strip()

        # Ensure required fields exist
        for field in cls.REQUIRED_FIELDS:
            tx.setdefault(field, "")

        return tx
