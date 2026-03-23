from apps.analytics.models import Transaction

REQUIRED_FIELDS = ["date", "description", "amount", "category"]


def process_csv_rows(rows, user):
    errors = []
    imported_count = 0

    for index, row in enumerate(rows, start=1):

        # Validate required fields
        for field in REQUIRED_FIELDS:
            if field not in row or row[field] in (None, ""):
                errors.append(f"Row {index}: Missing field '{field}'")
                break

        # Convert amount
        try:
            amount = float(row["amount"])
        except ValueError:
            errors.append(f"Row {index}: Invalid amount '{row['amount']}'")
            continue

        # Create transaction
        Transaction.objects.create(
            user=user,
            date=row["date"],
            description=row["description"],
            amount=amount,
            category=row["category"],
        )

        imported_count += 1

    return errors, imported_count
