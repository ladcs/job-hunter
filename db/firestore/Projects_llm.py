from __future__ import annotations

import logging
from dataclasses import asdict
from typing import Any

from db.firestore.firestore_client import Firestore_Client
from google.cloud.firestore_v1.base_query import FieldFilter

from Models.Project_To_Llm import Project_To_Llm

logger = logging.getLogger(__name__)

COLLECTION = "projects_to_llm"


class Projects_to_Llm:

    def __init__(self, client: Firestore_Client):
        self._db = client._db

    def save(self, project: Project_To_Llm) -> str:
        """
        Insere ou atualiza um projeto no Firestore.
        Retorna o ID do documento.
        """
        doc_ref = self._db.collection(COLLECTION).document(project.id)

        doc_ref.set(asdict(project))

        return project.id

    def save_batch(self, projects: list[Project_To_Llm]) -> list[str]:
        """
        Insere ou atualiza múltiplos projetos utilizando batch write.
        """
        if not projects:
            return []

        batch = self._db.batch()
        ids = []

        for project in projects:
            doc_ref = self._db.collection(COLLECTION).document(project.id)

            batch.set(doc_ref, asdict(project))

            ids.append(project.id)

        batch.commit()

        return ids

    def get(self, project_id: str) -> dict[str, Any] | None:
        """
        Retorna um projeto pelo ID.
        """
        doc = (
            self._db
            .collection(COLLECTION)
            .document(project_id)
            .get()
        )

        if doc.exists:
            return doc.to_dict()

        return None

    def get_all(self) -> list[dict[str, Any]]:
        """
        Retorna todos os projetos.
        """
        docs = (
            self._db
            .collection(COLLECTION)
            .stream()
        )

        return [doc.to_dict() for doc in docs]

    def get_by_skill(self, skill: str) -> list[dict[str, Any]]:
        """
        Retorna projetos que possuem determinada skill.
        """
        docs = (
            self._db
            .collection(COLLECTION)
            .where("skills", "array_contains", skill.lower())
            .stream()
        )

        return [doc.to_dict() for doc in docs]
    
    def get_by_title(self, title: str) -> dict:
        """
        Retorna projetos pelo título.
        """
        doc = (
            self._db
            .collection(COLLECTION)
            .where(filter=FieldFilter("title", "==", title))
            .get()
        )

        return doc[0].to_dict()

    def get_by_skills(
        self,
        skills: list[str]
    ) -> list[dict[str, Any]]:
        """
        Retorna projetos que possuem ao menos uma
        das skills informadas.
        """
        projects = {}

        for skill in skills:
            docs = (
                self._db
                .collection(COLLECTION)
                .where(
                    "skills",
                    "array_contains",
                    skill.lower()
                )
                .stream()
            )

            for doc in docs:
                projects[doc.id] = doc.to_dict()

        return list(projects.values())

    def delete(self, project_id: str) -> None:
        """
        Remove um projeto.
        """
        (
            self._db
            .collection(COLLECTION)
            .document(project_id)
            .delete()
        )

    def delete_batch(self, project_ids: list[str]) -> None:
        """
        Remove múltiplos projetos.
        """
        if not project_ids:
            return

        batch = self._db.batch()

        for project_id in project_ids:
            doc_ref = (
                self._db
                .collection(COLLECTION)
                .document(project_id)
            )

            batch.delete(doc_ref)

        batch.commit()