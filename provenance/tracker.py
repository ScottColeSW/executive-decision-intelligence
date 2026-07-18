"""
Provenance Tracking
"""

from datetime import datetime
from dataclasses import asdict


class ProvenanceTracker:

    def create(self, engine, function):

        return {

            "timestamp": datetime.utcnow().isoformat(),

            "engine": engine,

            "function": function,

            "version": "0.1.0"

        }