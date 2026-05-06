"""
skill_firestore.py not implemented yet, but it will be responsible for communication the skills of user to Firestore.
"""
from __future__ import annotations
from dataclasses import asdict
import uuid

from db.firestore.firestore_client import Firestore_Client
from Models.Skill_Firestore import Skill_Firestore
from db.firestore.firestore_client import Firestore_Client
from google.cloud.firestore_v1.base_query import FieldFilter

SKILLS = "user_skills"

class Skills_Firestore:
    def __init__(self, client: Firestore_Client):
        self._db = client._db

    def save_new_user(self, user_name: str) -> str:
        user_id = uuid.uuid4().hex
        doc_ref = self._db.collection("users").document(user_id)
        doc_ref.set({"name": user_name, "user_id": user_id, "skills": []})
        return user_id

    def save_new_skill(self, user_id: str, skill: Skill_Firestore) -> str:
        doc_ref = (
            self._db
            .collection("users")
            .document(user_id)
            .collection("skills")
            .document(self._make_skill_id(skill.skill_name))
        )
        doc_ref.set(asdict(skill), merge=True)
        return doc_ref.id
    
    def save_new_skill_batch(self, user_id: str, skills: list[Skill_Firestore]) -> list[str]:
        batch = self._db.batch()
        doc_ids = []
        for skill in skills:
            doc_ref = (
                self._db
                .collection("users")
                .document(user_id)
                .collection("skills")
                .document(self._make_skill_id(skill.skill_name))
            )
            batch.set(doc_ref, asdict(skill), merge=True)
            doc_ids.append(doc_ref.id)
        batch.commit()
        return doc_ids

    def load_user_id_by_name(self, user_name: str) -> str | None:
        docs = (
            self._db
            .collection("users")
            .where(filter=FieldFilter("name", "==", user_name))
            .stream()
        )
        for doc in docs:
            return doc.to_dict().get("user_id")
        return None

    def load_skills_by_user_id(self, user_id: str) -> list[Skill_Firestore]:
        docs = (
            self._db
            .collection("users")
            .document(user_id)
            .collection("skills")
            .stream()
        )
        return [Skill_Firestore(**doc.to_dict()) for doc in docs]
        
    def delete_skill(self, user_id: str, skill_name: str) -> None:
        doc_id = self._make_skill_id(skill_name)
        (
            self._db
            .collection("users")
            .document(user_id)
            .collection("skills")
            .document(doc_id)
            .delete()
        )

    def delete_user(self, user_id: str) -> None:
        docs = list(
            self._db
            .collection("users")
            .document(user_id)
            .collection("skills")
            .stream()
        )

        docs_ids = [doc.id for doc in docs]

        batch = self._db.batch()
        for doc_id in docs_ids:
            doc_ref = (
                self._db
                .collection("users")
                .document(user_id)
                .collection("skills")
                .document(doc_id)
            )
            batch.delete(doc_ref)
        batch.commit()

        (
            self._db
            .collection("users")
            .document(user_id)
            .delete()
        )

    def _make_skill_id(self, skill_name: str) -> str:
        return skill_name.lower().replace(" ", "_")