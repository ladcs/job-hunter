from __future__ import annotations

import json
import logging
from datetime import date
from dataclasses import asdict
from pathlib import Path
from datetime import datetime, timezone

from db.firestore.Jobs_firestore import Jobs_Firestore

from Models.Job_Listing import Job_Listing
from Models.Job_Firestore import Job_Firestore

logger = logging.getLogger(__name__)


class Job_Saver:

    def __init__(self, jobs_firestore: Jobs_Firestore = None):
        self._jobs_firestore = jobs_firestore

    def filter_new(self, listings: list[Job_Listing], source: str) -> list[Job_Listing]:
        """
        Retorna apenas as vagas cujo ID ainda não foi salvo para o source.
        """
        seen_ids = self._jobs_firestore.load_seen_ids(source)
        new = [job for job in listings if str(job.id) not in seen_ids]

        logger.info(
            "Source '%s': %d total, %d novas, %d já vistas.",
            source, len(listings), len(new), len(listings) - len(new),
        )
        return new

    def save(self, listings: list[Job_Listing], source: str) -> None:
        """
        Se o arquivo do dia já existir, faz append.
        Retorna o path do arquivo ou None se não houver nada para salvar.
        """
        if not listings:
            logger.info("Nenhuma vaga nova para salvar.")
            return None

        existing = []
        for job in listings:
            existing.append(self._serialize(source, job))
        try:
            self._jobs_firestore.save_batch(existing)
            logger.info("Salvou %d vagas no Firestore.", len(existing))
        except Exception as e:
            logger.error("Erro ao salvar no Firestore: %s", e)
        output_path = f"data/temp_{source}_2.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump([asdict(job) for job in existing], f, indent=2, ensure_ascii=False)



    def _serialize(self, source: str, job: Job_Listing) -> Job_Firestore:
        data = asdict(job)
        data.pop("html", None)
        data["source"] = source
        data["is_analyzed"] = False
        data["created_at"] = datetime.now(timezone.utc).isoformat()
        return Job_Firestore(**data)
