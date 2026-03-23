# services/processor.py
# Reads the CSV → sends rows into your pipeline

import csv
from apps.pipeline.tasks import run_full_pipeline

class CSVProcessor:

    @staticmethod
    def process(file, user):
        """Reads CSV - converts to list of dicts - runs pipeline."""

        decoded = file.read().decode("utf-8").splitlines()
        reader = csv.DictReader(decoded)

        rows = list(reader)

        # Run the pipeline
        result = run_full_pipeline(rows)

        return result