# apps/uploads/views.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import DatabaseError
from django.shortcuts import redirect, render

from apps.analytics.models import Transaction
from apps.pipeline.csv_cleaner import clean_csv_content


@login_required
def upload_view(request):
    """
    Handles CSV file uploads by delegating parsing to the pipeline cleaner module.
    """

    if request.method == "POST":
        if "csv_file" not in request.FILES:
            messages.error(request, "No file was selected.")
            return render(request, "uploads/upload.html", status=400)

        uploaded_file = request.FILES["csv_file"]

        if not uploaded_file.name.endswith(".csv"):
            messages.error(request, "The uploaded file is not a CSV.")
            return render(request, "uploads/upload.html", status=400)

        try:
            file_bytes = uploaded_file.read()
            valid_dicts, skipped_rows = clean_csv_content(file_bytes)

            if not valid_dicts:
                messages.error(
                    request, "No valid transaction rows found in the uploaded file."
                )
                return render(request, "uploads/upload.html", status=400)

            # Convert cleaned dicts into Transaction model instances
            valid_transactions = [
                Transaction(
                    user=request.user,
                    date=d["date"],
                    description=d["description"],
                    category=d["category"],
                    amount=d["amount"],
                    type=d["type"]
                )
                for d in valid_dicts
            ]

            # Bulk save all valid transactions to PostgreSQL
            Transaction.objects.bulk_create(valid_transactions)

            if skipped_rows:
                messages.warning(
                    request, 
                    f"Imported {len(valid_transactions)} transactions successfully. " 
                    f"Skipped {len(skipped_rows)} invalid rows."
                )
            else:
                messages.success(request, f"Successfully ingested all {len(valid_transactions)} transactions!")

            return redirect("analytics:dashboard")

        except (UnicodeDecodeError, DatabaseError) as e:
            messages.error(request, f"Error processing file: {e!s}")
            return render(request, "uploads/upload.html", status=500)

    return render(request, "uploads/upload.html")