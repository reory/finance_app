from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import UploadCSVForm
from .models import UploadedFile
from .services.processor import CSVProcessor

from apps.logs.pipeline_logger import log_pipeline_step
from apps.logs.security_logger import log_suspicious_activity


@login_required
def upload_csv(request):
    if request.method == "POST":
        form = UploadCSVForm(request.POST, request.FILES)

        if form.is_valid():
            file = form.cleaned_data["file"]

            # Save file
            uploaded = UploadedFile.objects.create(
                user=request.user,
                file=file
            )

            # Process file
            try:
                result = CSVProcessor.process(uploaded.file, request.user)
                log_pipeline_step(
                    f"CSV processed for user {request.user.username}")

                # Store result in session for redirect
                request.session["upload_result"] = result

                return redirect("uploads:result")

            except Exception as e:
                log_suspicious_activity(f"CSV processing failed: {str(e)}")
                messages.error(
                    request, "There was an error processing your CSV file.")
                return redirect("uploads:upload")

    else:
        form = UploadCSVForm()

    return render(request, "uploads/upload.html", {"form": form})


@login_required
def upload_result(request):
    """Displays the result of the CSV processing."""
    
    result = request.session.get("upload_result")

    if not result:
        messages.error(
            request, 
            "No results available." \
            "Please upload a CSV first."
        )
        return redirect("uploads:upload")
    
    # Log that the user viewed thier upload result
    log_pipeline_step(f"Upload results viewed by {request.user.username}")

    return render(request, "uploads/result.html", {"result": result})
