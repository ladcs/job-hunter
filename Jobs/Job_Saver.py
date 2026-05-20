from __future__ import annotations

import logging
from dataclasses import asdict
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
        ids_coming = [job.id for job in listings]
        new = [job for job in listings if f"{source}_{job.id}" not in seen_ids]
        not_seen = [id for id in seen_ids if id not in ids_coming]

        test = ['gupy_11172732',
        'gupy_11164240',
        'gupy_11139404',
        'gupy_1000005742',
        'gupy_11274335',
        'gupy_11258809',
        'gupy_11243329',
        'gupy_11217214',
        'gupy_11259340',
        'gupy_11251061',
        'gupy_11106286']

        if any(test) not in seen_ids:
            print("_____________________________________________ MERDA")
            print([f"{source}_{job.id}" for job in new])

        logger.info(
            "Source '%s': %d total, %d novas, %d já vistas.",
            source, len(listings), len(new), len(listings) - len(new),
        )
        return new, not_seen

    def save(self, listings: list[Job_Listing]) -> None:
        """
        Se o arquivo do dia já existir, faz append.
        Retorna o path do arquivo ou None se não houver nada para salvar.
        """
        if not listings:
            logger.info("Nenhuma vaga nova para salvar.")
            return None

        existing = []
        for job in listings:
            existing.append(self._serialize(job))
        try:
            self._jobs_firestore.save_batch(existing)
            logger.info("Salvou %d vagas no Firestore.", len(existing))
        except Exception as e:
            logger.error("Erro ao salvar no Firestore: %s", e)

    def mark_analized(self, job_id: str, source: str) -> None:
        try:
            self._jobs_firestore.mark_analyzed(job_id, source)
        except Exception as e:
            logger.error("Erro ao salvar no Firestore: %s", e)

    def delete_jobs(self, jobs_id: list[str], source: str) -> None:
        try:
            docs_id = [source + "_" + id for id in jobs_id]
            self._jobs_firestore.delete_batch(docs_id)
        except Exception as e:
            logger.error("Erro ao salvar no Firestore: %s", e)

    def _serialize(self, job: Job_Listing) -> Job_Firestore:
        data = asdict(job)
        data.pop("html", None)
        data.pop("content_to_llm", None)
        data["is_analyzed"] = False
        data["created_at"] = datetime.now(timezone.utc).isoformat()
        if not data["requirements"]:
            data["is_analyzed"] = True
        return Job_Firestore(**data)
