"""
Transaction Model Validator:
Validates a single transaction dict using a detected schema mapping.
"""

class TransactionModel:

    REQUIRED_FIELDS = ["date", "description", "amount"]

    @classmethod
    def validate(cls, row, schema):
        """
        Validate a single raw row using the schema mapping.
        Returns a clean dict with canonical field names.
        Raises ValueError on validation failure.
        """

        if not schema:
            raise ValueError("Schema not detected.")

        validated = {}

        # Map fields using schema
        for canonical in cls.REQUIRED_FIELDS:
            source_field = schema.get(canonical)

            if not source_field:
                raise ValueError(f"Missing schema mapping for '{canonical}'")

            value = row.get(source_field)

            if value is None or (isinstance(value, str) and value.strip() == ""):
                raise ValueError(f"Missing required field '{canonical}'")

            validated[canonical] = value

        # Optional category field
        category_field = schema.get("category")
        if category_field and category_field in row:
            validated["category"] = row.get(category_field, "")
        else:
            validated["category"] = ""

        return validated
