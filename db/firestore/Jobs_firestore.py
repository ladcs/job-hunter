from __future__ import annotations

import logging
from datetime import datetime, timezone
from dataclasses import asdict
from db.firestore.firestore_client import Firestore_Client
from google.cloud.firestore_v1.base_query import FieldFilter

from Models.Job_Firestore import Job_Firestore

logger = logging.getLogger(__name__)

COLLECTION = "vagas"


class Jobs_Firestore:

    def __init__(self, client: Firestore_Client):
        self._db = client._db

    def save(self, job: Job_Firestore) -> str:
        """
        Insere ou atualiza uma vaga no Firestore.
        Retorna o ID do documento.
        """
        doc_id = self._make_doc_id(job.source, job.id)
        doc_ref = self._db.collection(COLLECTION).document(doc_id)
        doc_ref.set(asdict(job))
        return doc_id

    def save_batch(self, jobs: list[Job_Firestore]) -> list[str]:
        """
        Insere ou atualiza uma lista de vagas usando batch write.
        Mais eficiente que salvar uma a uma — menos operações de escrita.
        Retorna lista de IDs salvos.
        """
        if not jobs:
            return []

        batch = self._db.batch()
        doc_ids = []

        for job in jobs:
            doc_id = self._make_doc_id(job.source, job.id)
            doc_ref = self._db.collection(COLLECTION).document(doc_id)
            batch.set(doc_ref, asdict(job))
            doc_ids.append(doc_id)

        batch.commit()
        return doc_ids

    def load_seen_ids(self, source: str) -> set[str]:
        """
        Retorna os job IDs (originais, sem prefixo de source) já existentes
        no Firestore para o source informado.
        Usa apenas o campo 'id' — evita ler o documento inteiro.
        """
        docs = (
            self._db.collection(COLLECTION)
            .where(filter=FieldFilter("source", "==", source))
            .select(["id"])
            .stream()
        )

        seen = {doc.get("id") for doc in docs}
        return seen

    def get(self, job_id: str, source: str) -> dict | None:
        """
        Retorna os dados de uma vaga pelo ID original e source.
        Retorna None se não encontrada.
        """
        doc_id = self._make_doc_id(source, job_id)
        doc = self._db.collection(COLLECTION).document(doc_id).get()

        if doc.exists:
            return doc.to_dict()
        return None

    def get_pending_analysis(self) -> list[dict]:
        """
        Retorna todas as vagas com is_analyzed=False.
        """
        docs = (
            self._db.collection(COLLECTION)
            .where(filter=FieldFilter("is_analyzed", "==", False))
            .stream()
        )
        return [doc.to_dict() for doc in docs]
    
    def get_ids_by_date(self, date: datetime) -> list[dict]:
        """
        Retorna os ids das vagas com created_at <= date.
        """
        docs = (
            self._db.collection(COLLECTION)
            .where(filter=FieldFilter("created_at", "<=", date))
            .stream()
        )
        return [doc.id for doc in docs]

    def mark_analyzed(self, job_id: str, source: str) -> None:
        """
        Marca uma vaga como analisada.
        """
        doc_id = self._make_doc_id(source, job_id)
        self._db.collection(COLLECTION).document(doc_id).update({
            "is_analyzed": True,
            "updated_at": datetime.now(timezone.utc),
        })

    def delete(self, document_id: str) -> None:
        """
        Remove uma vaga do Firestore.
        """
        self._db.collection(COLLECTION).document(document_id).delete()

    def delete_batch(self, documents_id: list[str]) -> None:
        """
        Remove múltiplas vagas usando batch delete.
        """
        if not documents_id:
            return

        batch = self._db.batch()
        for doc_id in documents_id:
            doc_ref = self._db.collection(COLLECTION).document(doc_id)
            batch.delete(doc_ref)
        batch.commit()

    @staticmethod
    def _make_doc_id(source: str, job_id: str) -> str:
        """
        Gera o ID do documento no formato {source}_{job_id}.
        """
        return f"{source}_{job_id}"