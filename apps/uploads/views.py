import csv
import io
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from apps.analytics.models import Transaction


@login_required
def upload_view(request):
    """
    Handles CSV file uploads for the financial data ingestion pipeline.
    """

    if request.method == "POST":
        # Check if the file is present in the request
        if "csv_file" not in request.FILES:
            messages.error(request, "No file was selected.")
            return render(request, "uploads/upload.html", status=400)

        uploaded_file = request.FILES["csv_file"]

        # Basic safety check to ensure it's a CSV file
        if not uploaded_file.name.endswith(".csv"):
            messages.error(request, "The uploaded file is not a CSV.")
            return render(request, "uploads/upload.html", status=400)

        try:
            # Read the file in text mode for the CSV parser
            data_set = uploaded_file.read().decode("UTF-8")
            io_string = io.StringIO(data_set)
            reader = csv.reader(io_string, delimiter=",")

            # Skip the header row if your pipeline uses one
            header = next(reader, None)

            # Process rows (This is where your ingestion pipeline hook goes)
            for row in reader:
                if not row:
                    continue

                Transaction.objects.create(
                    user=request.user,
                    date=row[0],
                    description=row[1],
                    category=row[2],
                    amount=row[3],
                    type=row[4],
                )

            messages.success(request, "CSV data ingested successfully!")
            return redirect("analytics:dashboard")

        except Exception as e:
            messages.error(request, f"Error processing file: {str(e)}")
            return render(request, "uploads/upload.html", status=500)

    return render(request, "uploads/upload.html")
