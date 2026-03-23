"""
High-level orchestration tasks for the data pipeline.
Each task coordinates multiple engine components into a single workflow.
"""

from .engine.cleaner import Cleaner
from .engine.normalizer import Normalizer
from .engine.categorizer import Categorizer
from .engine.summarizer import Summarizer
from .validators.schema_detector import SchemaDetector
from .validators.transaction_model import TransactionModel


def run_full_pipeline(raw_data):
    """
    Execute the full data pipeline:
    Validate schema, Clean data, Normalize fields, Categorize transactions
    Summarize results
    """

    # Detect schema
    schema = SchemaDetector.detect(raw_data)

    # Validate each record
    validated = [TransactionModel.validate(item, schema) for item in raw_data]

    # Clean
    cleaned = Cleaner.clean(validated)

    # Normalize
    normalized = Normalizer.normalize(cleaned)

    # Categorize
    categorized = Categorizer.assign(normalized)

    # Summaries
    summary = Summarizer.generate(categorized)

    return {
        "raw": raw_data,
        "validated": validated,
        "cleaned": cleaned,
        "normalized": normalized,
        "categorized": categorized,
        "summary": summary,
    }
