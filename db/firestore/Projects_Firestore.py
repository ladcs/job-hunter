from __future__ import annotations

import logging
from db.firestore.firestore_client import Firestore_Client

logger = logging.getLogger(__name__)

COLLECTION = "projects"


class Projects_Firestore:

    def __init__(self, client: Firestore_Client):
        self._db = client._db

    def save(self, project_name: str, latex: str, skills: list[str]) -> str:
        """
        Insere ou atualiza um projeto no Firestore.
        Retorna o ID do documento.
        """
        doc_ref = self._db.collection(COLLECTION).document(project_name)
        doc_ref.set({
            "latex": latex,
            "skills": skills,
        })
        return project_name

    def get(self, project_name: str) -> dict | None:
        doc = self._db.collection(COLLECTION).document(project_name).get()
        if doc.exists:
            return doc.to_dict()
        return None

    def get_by_skill(self, skill: str) -> list[dict]:
        """
        Retorna todos os projetos que contêm a skill informada.
        """
        from google.cloud.firestore_v1.base_query import FieldFilter
        docs = (
            self._db.collection(COLLECTION)
            .where(filter=FieldFilter("skills", "array_contains", skill))
            .stream()
        )
        return [{"name": doc.id, **doc.to_dict()} for doc in docs]

    def get_all(self) -> list[dict]:
        docs = self._db.collection(COLLECTION).stream()
        return [{"name": doc.id, **doc.to_dict()} for doc in docs]

    def delete(self, project_name: str) -> None:
        self._db.collection(COLLECTION).document(project_name).delete()


if __name__ == "__main__":
    from db.firestore.firestore_client import Firestore_Client

    DATA = {
        "web_chat_bot": {
            "latex": "\\textbf{Web Chat Bot} \\hfill 2023\\\\\n...",
            "skills": ["react", "javascript", "typescript", "sql", "api", "rest api", "docker"]
        },
        "clipping_news": {
            "latex": "\\textbf{Clipping News} \\hfill 2025 \\\\\n...",
            "skills": ["python", "postgresql", "sqlalchemy", "fastapi", "sql", "docker", "rest api", "api", "microservices", "poo", "git", "github"]
        },
        "discord_bot": {
            "latex": "\\textbf{Discord Chat Bot + n8n Integration}\\hfill 2025 \\\\\n...",
            "skills": ["python", "docker", "microservices", "git", "github"]
        },
        "job_hunter": {
            "latex": "\\textbf{Job Hunter AI} \\hfill 2026 -- Atual\\\\\n...",
            "skills": ["python", "gcp", "cloud", "firestore", "nosql", "solid", "poo", "testing"]
        },
    }

    client = Firestore_Client()
    repo = Projects_Firestore(client)

    for name, data in DATA.items():
        doc_id = repo.save(name, data["latex"], data["skills"])
        print(f"Saved: {doc_id}")