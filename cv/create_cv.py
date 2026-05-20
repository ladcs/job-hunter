from __future__ import annotations

import io
import zipfile
from pathlib import Path

from Models.Personal_Project import Personal_Project

class Make_Cv:
    def generate_latex(self, content: Personal_Project):
        resume = content.resume
        projects = "\n".join(content.latex)
        latex = f"""%{content.url}
\\documentclass[11pt,a4paper]{{article}}

% ----------------
% Pacotes
% ----------------
\\usepackage[a4paper,margin=1.6cm]{{geometry}}
\\usepackage{{fontspec}}
\\usepackage{{titlesec}}
\\usepackage{{enumitem}}
\\usepackage{{hyperref}}
\\usepackage{{tabularx}}
\\usepackage{{xcolor}}
\\usepackage{{fancyhdr}}
\\usepackage{{fontawesome5}}
\\usepackage{{graphicx}}
\\usepackage{{multicol}}
\\usepackage{{ulem}}

% ----------------
% Fonte
% ----------------
\\setmainfont{{TeX Gyre Heros}}

% ----------------
% Cores
% ----------------
\\definecolor{{primary}}{{HTML}}{{1F1F1F}}
\\definecolor{{secondary}}{{HTML}}{{555555}}

% ----------------
% Header / Footer
% ----------------
\\pagestyle{{fancy}}
\\fancyhf{{}}
\\renewcommand{{\\headrulewidth}}{{0pt}}
\\fancyfoot[C]{{\\textcolor{{secondary}}{{\\thepage}}}}

% ----------------
% Seções
% ----------------
\\titleformat{{\\section}}
  {{\\Large\\bfseries\\color{{primary}}}}
  {{}}{{0pt}}{{}}
  [\\vspace{{-0.3em}}\\titlerule]

\\titlespacing*{{\\section}}{{0pt}}{{1em}}{{0.6em}}

\\setlist[itemize]{{leftmargin=1.2em,itemsep=0.3em}}

% ================================
\\begin{{document}}

% ----------------
% CABEÇALHO
% ----------------
\\begin{{minipage}}[c]{{0.22\\textwidth}}
    \\centering
\\end{{minipage}}
\\hfill
\\begin{{minipage}}[c]{{1\\textwidth}}
    {{\\Huge\\bfseries Luciano Augusto de Castro Silva}}\\\\[-0.2em]
    {{\\large\\bfseries\\color{{secondary}} Engenheiro de Software}}\\\\[0.6em]

    {{\\small
    \\faMapMarker*~São Paulo, SP -- Brasil \\quad
    \\faPhone~+55 (43) 99616-2473\\\\
    \\faEnvelope~\\href{{mailto:hpladcs@gmail.com}}{{hpladcs@gmail.com}}\\\\
    \\faGithub~\\href{{https://github.com/ladcs}}{{github.com/ladcs}}\\quad
    \\faLinkedin~\\href{{https://linkedin.com/in/ladcs}}{{linkedin.com/in/ladcs}}
    }}
\\end{{minipage}}

\\vspace{{1em}}

% ----------------
% SUMMARY
% ----------------
\\section*{{Resumo}}
{resume}

% ----------------
% SKILLS
% ----------------
\\section*{{Habilidades}}
% adicionar palavras chaves aqui
\\begin{{tabularx}}{{\\textwidth}}{{l X}}
\\textbf{{Linguagens de Programação}} & Python, C\\#, JavaScript, TypeScript, Java \\\\
\\textbf{{Cloud}} & GCP (Compute Engine, Cloud Jobs, Cloud Storage), AWS (Lambda, DynamoDB, S3, SQS, SNS) \\\\
\\textbf{{Frameworks E Ferramentas}} & RabbitMQ, ASP.Net, xUnit, FastAPI, Flask, Pandas, Docker, N8N, LLMs, React, express \\\\
\\textbf{{Práticas}} & Programação Orientada a Objetos, Microserviços, mensageria, SOLID, Programação Funcional, Agile, APIs REST, GOF \\\\
\\textbf{{Banco de Dados}} & PostgreSQL, MySQL, MongoDB, DynamoDB, SQL Server \\\\
\\textbf{{OS}} & Linux, Windons, MacOs \\\\
\\textbf{{Idiomas}} & Português, Inglês

\\end{{tabularx}}

% ----------------
% EXPERIENCE
% ----------------
\\section*{{Experiencia}}

\\textbf{{AIDA}} \\hfill Junho 2024 -- Novembro 2025\\\\
\\textit{{Back-end Developer}}
A AIDA atua com análise de conversas de atendimento ao cliente, utilizando LLMs para gerar métricas e insights a partir de grandes volumes de dados de áudio e texto.
% mudar para STAR
\\begin{{itemize}}
  \\item Para busca das conversas de áudio de clientes, para uma analise, usando conexão SSH ou uso de uma API, desenvolvi pipelines automatizadas, usando Python, Bash assim como serviço de nuvem (VM), seguindo filtros fornecidos, o que possibilitou o processamento de mais de 35 mil conversas por mês.
  
  \\item Para a criação de um novo cliente para o sistema. Projetei e desenvolvi uma API REST, com autenticação OAuth2, usando Python e integração com serviços Google e o desenvolvimento múltiplos CRUDs orientados a microserviços, reduzindo o tempo de onboarding de novos clientes de horas para poucos segundos.
  
  \\item Para verificar um programa com o mínimo de problemas. Analisei e corrigi falhas em fluxos de processamento e análise de conversas, utilizando inspeção de Logs, estruturas JSON e consultas SQL, aumentando a estabilidade e a confiabilidade do sistema.
  
  \\item Um dos produtos da empresa era fazer análises focado em algumas conversas recebendo parametros específicos. Para isso desenvolvi um processo automatizado para execução de prompts em interações selecionadas, com o serviço do Nuvem, eliminando atividades manuais do cliente e garantindo a execução em horários previamente definidos.
  
  \\item Um dos clientes não possuia um padrão de envio de suas conversas, para resolver isso criei scripts de filtragem, usando Python, seleção e transformação de interações de áudio e texto, adequando metadados ao padrão interno da plataforma e viabilizando a análise de mais de 80 mil conversas por mês.

  \\item Para um melhor contato entre cliente e empresa, trabalhei como suporte de cliente nível 1 e nível 2, trazendo soluções técnicas e trazendo soluções assim como sugestões.
\\end{{itemize}}


\\textbf{{SENAI}} \\hfill 2023 \\\\
\\textit{{Professor}}
\\begin{{itemize}}
  \\item Ministrei aulas de Banco de Dados e Redes de Computadores para o 2º ano do Novo Ensino Médio.
  \\item Desenvolvi metodologias práticas e colaborativas que aumentaram o engajamento e a compreensão dos alunos.
  \\item Promovi um ambiente de aprendizado colaborativo, incentivando a troca de conhecimento.
\\end{{itemize}}

% ----------------
% EDUCATION
% ----------------
\\section*{{Educação}}

\\textbf{{Universidade Estadual de Londrina (UEL)}}\\\\
Bacharel em Engenharia Elétrica — Concluído em 2021

\\noindent\\textbf{{Trybe}}\\\\
Desenvolvedor web full-stack - concluído em 2021

\\noindent\\textbf{{Trybe}}\\\\
Aceleração C\\# - concluído em 2026

\\noindent\\textbf{{Faculdade Descomplica}}\\\\
Pós-graduação em Engenharia de Software — Em andamento
% ----------------
% PROJECTS
% ----------------
\\section*{{Projetos}}
{projects}
\\end{{document}}
"""
        return latex
    
    
    def save_tex(self, latex: str, filename: str = "cv") -> bytes:
        # pega a primeira linha
        first_line = latex.splitlines()[0].strip()

        # remove o "%" do começo
        url = first_line[1:] if first_line.startswith("%") else ""

        # cria zip em memória
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
            # adiciona o .tex
            zipf.writestr(f"{filename}.tex", latex)

            # adiciona o .txt com a url
            zipf.writestr(f"{filename}.txt", url)

        # volta pro começo do buffer
        zip_buffer.seek(0)

        # retorna bytes do zip
        return zip_buffer.getvalue()
    
    def create_zip(self, latex: str, filename: str = "cv") -> str:
        first_line = latex.splitlines()[0].strip()
        url = first_line[1:] if first_line.startswith("%") else ""

        zip_path = Path(f"{filename}.zip")

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            # cria o .tex dentro do zip
            zipf.writestr(f"{filename}.tex", latex)

            # cria o .txt dentro do zip
            zipf.writestr(f"{filename}.txt", url)

        return str(zip_path)
            