from __future__ import annotations

import logging
from dataclasses import asdict
from typing import Any

from db.firestore.firestore_client import Firestore_Client
from google.cloud.firestore_v1.base_query import FieldFilter

from Models.Project_Llm_Firestore import Project_Llm_Firestore

logger = logging.getLogger(__name__)

COLLECTION = "projects_to_llm"


class Projects_Firestore:

    def __init__(self, client: Firestore_Client):
        self._db = client._db

    def save(self, project: Project_Llm_Firestore) -> str:
        doc_ref = self._db.collection(COLLECTION).document(project.id)
        doc_ref.set(asdict(project))
        return project.id

    def save_batch(self, projects: list[Project_Llm_Firestore]) -> list[str]:
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
        doc = self._db.collection(COLLECTION).document(project_id).get()
        if doc.exists:
            return doc.to_dict()
        return None

    def get_all(self) -> list[dict[str, Any]]:
        docs = self._db.collection(COLLECTION).stream()
        return [doc.to_dict() for doc in docs]

    def get_by_skill(self, skill: str) -> list[dict[str, Any]]:
        docs = (
            self._db
            .collection(COLLECTION)
            .where("skills", "array_contains", skill.lower())
            .stream()
        )
        return [doc.to_dict() for doc in docs]

    def get_by_title(self, title: str) -> dict:
        doc = (
            self._db
            .collection(COLLECTION)
            .where(filter=FieldFilter("title", "==", title))
            .get()
        )
        return doc[0].to_dict()

    def get_by_skills(self, skills: list[str]) -> list[dict[str, Any]]:
        """
        Retorna projetos que possuem ao menos uma das skills informadas.
        """
        projects = {}

        for skill in skills:
            docs = (
                self._db
                .collection(COLLECTION)
                .where("skills", "array_contains", skill.lower())
                .stream()
            )
            for doc in docs:
                projects[doc.id] = doc.to_dict()

        return list(projects.values())

    def get_latex_by_skills(self, skills: list[str]) -> list[str]:
        """
        Retorna apenas os campos latex dos projetos
        que possuem ao menos uma das skills informadas.
        """
        projects = self.get_by_skills(skills)
        return [p["latex"] for p in projects if p.get("latex")]

    def update_latex(self, project_id: str, latex: str) -> None:
        """
        Atualiza apenas o campo latex de um projeto.
        """
        if not self.get(project_id):
            logger.warning(f"Projeto {project_id} não encontrado para atualizar latex.")
            return
        self._db.collection(COLLECTION).document(project_id).update({
            "latex": latex
        })

    def delete(self, project_id: str) -> None:
        self._db.collection(COLLECTION).document(project_id).delete()

    def delete_batch(self, project_ids: list[str]) -> None:
        if not project_ids:
            return

        batch = self._db.batch()
        for project_id in project_ids:
            doc_ref = self._db.collection(COLLECTION).document(project_id)
            batch.delete(doc_ref)
        batch.commit()


if __name__ == "__main__":
    PROJECTS = [
        {
            "id": "web-chat-bot",
            "latex": "\\textbf{Web Chat Bot} \\hfill 2023\\\\ \n \\textit{Aplicação fullstack de chatbot web integrada com IA generativa: \\faGithub~\\href{https://github.com/ladcs/web-chat-bot}{web-chat-bot}}\n\n \\begin{itemize}\n\n  \\item Desenvolvi uma aplicação fullstack para interação conversacional com modelos LLM, utilizando Next.js no frontend e Node.js com Express no backend.\n\n  \\item Implementei uma API REST em TypeScript para processamento de mensagens e comunicação entre interface web e serviços de IA generativa.\n\n  \\item Estruturei persistência e gerenciamento de dados utilizando Prisma ORM e banco de dados relacional, facilitando integração e manutenção da camada de acesso a dados.\n\n  \\item Desenvolvi fluxos de envio e processamento de prompts para modelos LLM, permitindo geração automatizada de respostas contextualizadas em tempo real.\n\n  \\item Containerizei os serviços da aplicação utilizando Docker e Docker Compose, padronizando o ambiente de desenvolvimento e integração entre frontend, backend e banco de dados.\n\n  \\item Estruturei a arquitetura da aplicação visando expansão futura para autenticação, histórico de conversas e múltiplos provedores de IA.\n\n\\end{itemize}",
        },
        {
            "id": "clipping-news",
            "latex": "\\textbf{Clipping News} \\hfill 2025 \\\\\n\\textit{Sistema automatizado de clipping financeiro com análise de notícias utilizando IA: \\faGithub~\\href{https://github.com/ladcs/Clipping_News}{Clipping News}}\n\n\\begin{itemize}\n\n  \\item Desenvolvi um pipeline automatizado para coleta e processamento de notícias financeiras utilizando Python, RSS feeds e FastAPI, centralizando conteúdos de múltiplas fontes em uma base estruturada.\n\n  \\item Modelei e implementei um banco de dados relacional utilizando PostgreSQL e SQLAlchemy, estruturando relacionamentos entre notícias, ativos financeiros e variações de mercado para suportar análises históricas e expansão futura do sistema.\n\n  \\item Estruturei o ambiente da aplicação utilizando Docker e Docker Compose, facilitando execução local, isolamento de serviços e escalabilidade do projeto.\n\n  \\item Desenvolvi mecanismos de classificação e sumarização automática de notícias utilizando LLMs, permitindo identificar setores potencialmente impactados e gerar resumos contextualizados para análise financeira.\n\n  \\item Implementei processos automatizados de atualização e organização de dados, incluindo controle de versionamento temporal, soft delete e triggers de atualização no banco de dados.\n\n  \\item Projetei a arquitetura do sistema visando integração futura com ferramentas de automação e IA generativa, permitindo expansão para análise de impacto financeiro, dashboards e processamento inteligente de notícias, nesse momento a IA generativa esta apenas indicando qual setor mas não o impacto total.\n\n\\end{itemize}",
        },
        {
            "id": "discord-chatbot-n8n",
            "latex": "\\textbf{Discord Chat Bot + n8n Integration}\\hfill 2025 \\\\\n\\textit{Sistema de integração entre Discord, workflows automatizados e IA generativa utilizando LLMs: \\faGithub~\\href{https://github.com/ladcs/chatbot-discord}{chatbot-discord}} \\hfill 2025\n\n\\begin{itemize}\n\n  \\item Desenvolvi um bot para Discord utilizando Python para criação de bot no Discord, permitindo interação via comandos customizados e integração com workflows automatizados baseados em n8n.\n\n  \\item Implementei comunicação entre Discord e serviços de IA via webhooks HTTP e APIs REST, possibilitando envio e processamento automatizado de prompts utilizando modelos LLM através do OpenRouter.\n\n  \\item Estruturei workflows automatizados no n8n para processamento de mensagens, geração de respostas com IA e extração de métricas de utilização, incluindo contagem de tokens consumidos.\n\n  \\item Containerizei a aplicação utilizando Docker e Docker Compose, integrando serviços de automação, bot e processamento de IA em ambiente isolado e facilmente reproduzível.\n\n  \\item Desenvolvi mecanismos de autenticação e restrição de uso por usuário, controlando acesso aos comandos de geração de prompts e reduzindo consumo indevido de recursos computacionais.\n\n  \\item Estruturei a aplicação visando extensibilidade para novos fluxos automatizados, integração com múltiplos modelos de IA e expansão para outros canais de comunicação.\n\n\\end{itemize}",
        },
        {
            "id": "job-hunter-ai",
            "latex": "\\textbf{Job Hunter AI} \\hfill 2026 -- Atual\\\\\n\\textit{Sistema automatizado de coleta de vagas e adaptação curricular utilizando IA generativa: \\faGithub~\\href{https://github.com/ladcs/job-hunter}{job hunter}}\n\n\\begin{itemize}\n\n  \\item Desenvolvi pipelines automatizados para coleta e processamento de vagas de múltiplas plataformas utilizando Python, parsing HTML, APIs e extração estruturada de dados.\n\n  \\item Implementei mecanismos de análise semântica de requisitos utilizando LLMs, identificando hard skills, senioridade e competências obrigatórias a partir de descrições de vagas.\n\n    \\item Desenvolvi fluxos de geração de descrições profissionais utilizando IA generativa, alinhando experiências e projetos às tecnologias e competências exigidas pelas vagas analisadas.\n\n  \\item Modelei a aplicação utilizando arquitetura modular orientada a serviços, facilitando escalabilidade, manutenção e reutilização de componentes de coleta, análise e geração de conteúdo.\n\n  \\item Estruturei mecanismos de armazenamento e processamento visando integração futura com serviços em nuvem, bancos NoSQL e pipelines automatizados de candidatura.\n\n\\end{itemize}",
        },
    ]

    client = Firestore_Client()
    repo = Projects_Firestore(client)

    for data in PROJECTS:
        doc_id = repo.update_latex(data["id"], data["latex"])
        print(f"Saved: {doc_id}")