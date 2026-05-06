from __future__ import annotations

import logging

from google.cloud import firestore

logger = logging.getLogger(__name__)

class Firestore_Client:

    def __init__(self, project_id: str = "job-hunter-494620"):
        self._db = firestore.Client(project=project_id)