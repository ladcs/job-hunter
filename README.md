# Job Hunter
<details>
<summary>🇧🇷 Português</summary>
Pipeline com IA para matching de vagas e geração dinâmica de currículos com base nos requisitos das vagas e nas habilidades do candidato.
</details>
<details>
<summary>🇺🇸 English</summary>
AI-powered pipeline for job matching and dynamic CV generation based on job requirements and candidate skills.
</details>

## Visão Geral / Overview
<details>
<summary>🇧🇷 Português</summary>
Job Hunter é um projeto de portfólio pessoal criado para automatizar parte do fluxo de candidatura a vagas.
Em vez de se candidatar automaticamente, o projeto foca em:

coletar oportunidades de múltiplas plataformas;
filtrar vagas com base no perfil do candidato;
extrair requisitos técnicos utilizando LLMs;
gerar currículos personalizados para cada vaga;
criar CVs em LaTeX;
organizar e ranquear oportunidades.

O projeto foi intencionalmente desenhado para evitar candidaturas automáticas, devido a questões legais e políticas das plataformas.
</details>
<details>
<summary>🇺🇸 English</summary>
Job Hunter is a personal portfolio project designed to automate part of the job application workflow.
Instead of automatically applying to jobs, the project focuses on:

collecting job opportunities from multiple platforms;
filtering jobs based on candidate profile;
extracting technical requirements using LLMs;
generating customized resumes for each position;
creating LaTeX-based CVs;
organizing and ranking opportunities.

The project was intentionally designed to avoid automated applications due to legal and platform policy concerns.
</details>

## Funcionalidades Principais / Main Features
### Coleta de Vagas / Job Collection
<details>
<summary>🇧🇷 Português</summary>
Coleta listagens de vagas de múltiplas fontes:

Gupy
Greenhouse
Nubank Careers
XP Inc
BTG Pactual
B3 Careers

</details>
<details>
<summary>🇺🇸 English</summary>
Collects job listings from multiple sources:

Gupy
Greenhouse
Nubank Careers
XP Inc
BTG Pactual
B3 Careers

</details>

### Pipeline de Filtragem / Smart Filtering Pipeline
<details>
<summary>🇧🇷 Português</summary>
O pipeline filtra vagas utilizando:

análise de título;
filtro de localização;
filtro por palavras-chave;
tecnologias requeridas;
anos de experiência;
skills normalizadas;
extração de requisitos via LLM.

</details>
<details>
<summary>🇺🇸 English</summary>
The pipeline filters jobs using:

title analysis;
location filtering;
keyword filtering;
required technologies;
years of experience;
normalized skills;
LLM requirement extraction.

</details>

### Extração de Requisitos com IA / AI Requirement Extraction
<details>
<summary>🇧🇷 Português</summary>
Utiliza modelos da OpenAI para:

extrair tecnologias das descrições de vagas;
resumir requisitos;
identificar skills relevantes;
enriquecer o matching candidato-vaga.

Modelo atual: GPT-4.1-mini
</details>
<details>
<summary>🇺🇸 English</summary>
Uses OpenAI models to:

extract technologies from job descriptions;
summarize requirements;
identify relevant skills;
enrich candidate-job matching.

Current model: GPT-4.1-mini
</details>

### Geração Dinâmica de CV / Dynamic CV Generation
<details>
<summary>🇧🇷 Português</summary>
Gera currículos personalizados com base em:

projetos do candidato;
habilidades pessoais;
experiência profissional;
requisitos da vaga.

Saídas geradas:

.tex
.txt
.zip

</details>
<details>
<summary>🇺🇸 English</summary>
Generates customized resumes based on:

candidate projects;
personal skills;
professional experience;
job requirements.

Outputs:

.tex
.txt
.zip

</details>

### Integração com Firestore / Firestore Integration
<details>
<summary>🇧🇷 Português</summary>
Armazena:

listagens de vagas;
habilidades do usuário;
projetos pessoais;
metadados gerados.

</details>
<details>
<summary>🇺🇸 English</summary>
Stores:

job listings;
user skills;
personal projects;
generated metadata.

</details>

### Notificações via Discord / Planned Discord Notifications
<details>
<summary>🇧🇷 Português</summary>
Próximo passo:

notificações automáticas no Discord com vagas processadas e currículos gerados.

</details>
<details>
<summary>🇺🇸 English</summary>
Next step:

automatic Discord notifications with processed jobs and generated resumes.

</details>

## Arquitetura do Pipeline / Pipeline Architecture
#mermaid-r1f5{font-family:inherit;font-size:16px;fill:#E5E5E5;}@keyframes edge-animation-frame{from{stroke-dashoffset:0;}}@keyframes dash{to{stroke-dashoffset:0;}}#mermaid-r1f5 .edge-animation-slow{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 50s linear infinite;stroke-linecap:round;}#mermaid-r1f5 .edge-animation-fast{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 20s linear infinite;stroke-linecap:round;}#mermaid-r1f5 .error-icon{fill:#CC785C;}#mermaid-r1f5 .error-text{fill:#3387a3;stroke:#3387a3;}#mermaid-r1f5 .edge-thickness-normal{stroke-width:1px;}#mermaid-r1f5 .edge-thickness-thick{stroke-width:3.5px;}#mermaid-r1f5 .edge-pattern-solid{stroke-dasharray:0;}#mermaid-r1f5 .edge-thickness-invisible{stroke-width:0;fill:none;}#mermaid-r1f5 .edge-pattern-dashed{stroke-dasharray:3;}#mermaid-r1f5 .edge-pattern-dotted{stroke-dasharray:2;}#mermaid-r1f5 .marker{fill:#A1A1A1;stroke:#A1A1A1;}#mermaid-r1f5 .marker.cross{stroke:#A1A1A1;}#mermaid-r1f5 svg{font-family:inherit;font-size:16px;}#mermaid-r1f5 p{margin:0;}#mermaid-r1f5 .label{font-family:inherit;color:#E5E5E5;}#mermaid-r1f5 .cluster-label text{fill:#3387a3;}#mermaid-r1f5 .cluster-label span{color:#3387a3;}#mermaid-r1f5 .cluster-label span p{background-color:transparent;}#mermaid-r1f5 .label text,#mermaid-r1f5 span{fill:#E5E5E5;color:#E5E5E5;}#mermaid-r1f5 .node rect,#mermaid-r1f5 .node circle,#mermaid-r1f5 .node ellipse,#mermaid-r1f5 .node polygon,#mermaid-r1f5 .node path{fill:transparent;stroke:#A1A1A1;stroke-width:1px;}#mermaid-r1f5 .rough-node .label text,#mermaid-r1f5 .node .label text,#mermaid-r1f5 .image-shape .label,#mermaid-r1f5 .icon-shape .label{text-anchor:middle;}#mermaid-r1f5 .node .katex path{fill:#000;stroke:#000;stroke-width:1px;}#mermaid-r1f5 .rough-node .label,#mermaid-r1f5 .node .label,#mermaid-r1f5 .image-shape .label,#mermaid-r1f5 .icon-shape .label{text-align:center;}#mermaid-r1f5 .node.clickable{cursor:pointer;}#mermaid-r1f5 .root .anchor path{fill:#A1A1A1!important;stroke-width:0;stroke:#A1A1A1;}#mermaid-r1f5 .arrowheadPath{fill:#0b0b0b;}#mermaid-r1f5 .edgePath .path{stroke:#A1A1A1;stroke-width:2.0px;}#mermaid-r1f5 .flowchart-link{stroke:#A1A1A1;fill:none;}#mermaid-r1f5 .edgeLabel{background-color:transparent;text-align:center;}#mermaid-r1f5 .edgeLabel p{background-color:transparent;}#mermaid-r1f5 .edgeLabel rect{opacity:0.5;background-color:transparent;fill:transparent;}#mermaid-r1f5 .labelBkg{background-color:rgba(0, 0, 0, 0.5);}#mermaid-r1f5 .cluster rect{fill:#CC785C;stroke:hsl(15, 12.3364485981%, 48.0392156863%);stroke-width:1px;}#mermaid-r1f5 .cluster text{fill:#3387a3;}#mermaid-r1f5 .cluster span{color:#3387a3;}#mermaid-r1f5 div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:inherit;font-size:12px;background:#CC785C;border:1px solid hsl(15, 12.3364485981%, 48.0392156863%);border-radius:2px;pointer-events:none;z-index:100;}#mermaid-r1f5 .flowchartTitleText{text-anchor:middle;font-size:18px;fill:#E5E5E5;}#mermaid-r1f5 rect.text{fill:none;stroke-width:0;}#mermaid-r1f5 .icon-shape,#mermaid-r1f5 .image-shape{background-color:transparent;text-align:center;}#mermaid-r1f5 .icon-shape p,#mermaid-r1f5 .image-shape p{background-color:transparent;padding:2px;}#mermaid-r1f5 .icon-shape rect,#mermaid-r1f5 .image-shape rect{opacity:0.5;background-color:transparent;fill:transparent;}#mermaid-r1f5 .label-icon{display:inline-block;height:1em;overflow:visible;vertical-align:-0.125em;}#mermaid-r1f5 .node .label-icon path{fill:currentColor;stroke:revert;stroke-width:revert;}#mermaid-r1f5 :root{--mermaid-font-family:inherit;}Job FetchHTML CleaningNormalizationPre FiltersLLM Requirement ExtractionSkill MatchingFirestore StorageResume GenerationLaTeX CVZIP ExportDiscord Notification

## Estrutura do Projeto / Project Structure
textjob-hunter/
├── cv/
├── db/
├── Filter_job/
├── Ia_generative/
├── Job_listing/
├── Jobs/
├── Models/
├── rank_generation/
├── skills/
├── data/
└── main.py
<details>
<summary>🇧🇷 Português</summary>
Conceitos de arquitetura utilizados:

Programação Orientada a Objetos (POO)
Princípios SOLID
Arquitetura em camadas
Serviços modulares

</details>
<details>
<summary>🇺🇸 English</summary>
Architecture concepts used:

Object-Oriented Programming (OOP)
SOLID principles
Layered architecture
Modular services

</details>

## Stack de Tecnologias / Tech Stack
Camada / LayerTecnologia / TechnologyBackendPythonIA / AIOpenAI API — GPT-4.1-miniBanco de Dados / DatabaseFirebase FirestoreParsingBeautifulSoupGeração de CV / CV GenerationLaTeX

Variáveis de Ambiente / Environment Variables
envOPENAI_API_KEY=
BOT_TOKEN=

Como Executar / Running the Project
bash# Instalar dependências / Install dependencies
pip install -r Requirements.txt

## Executar / Run
python main.py

Fluxo Atual / Current Workflow
<details>
<summary>🇧🇷 Português</summary>

Buscar listagens de vagas
Normalizar dados das vagas
Filtrar oportunidades relevantes
Extrair requisitos com LLM
Remover posições incompatíveis
Armazenar vagas no Firestore
Gerar currículos contextuais
Exportar arquivos LaTeX/TXT/ZIP
Preparar notificações no Discord

</details>
<details>
<summary>🇺🇸 English</summary>

Fetch job listings
Normalize job data
Filter relevant opportunities
Extract requirements using LLM
Remove incompatible positions
Store jobs in Firestore
Generate contextual resumes
Export LaTeX/TXT/ZIP files
Prepare Discord notifications

</details>

## Melhorias Futuras / Future Improvements
<details>
<summary>🇧🇷 Português</summary>

Deploy em nuvem
Execução agendada
Integração com Discord
Dashboard de monitoramento
Ranqueamento semântico
Matching baseado em embeddings
Suporte a banco de dados vetorial
Analytics para recrutadores
Pontuação de currículos
Deploy no GCP Cloud Functions

</details>
<details>
<summary>🇺🇸 English</summary>

Cloud deployment
Scheduled execution
Discord integration
Dashboard for monitoring
Semantic ranking
Embedding-based matching
Vector database support
Recruiter analytics
Resume scoring
GCP Cloud Functions deployment

</details>

## Notas de Deploy / Deployment Notes
<details>
<summary>🇧🇷 Português</summary>
A ideia original era fazer o deploy usando GCP Cloud Functions com recursos do free tier.

</details>
<details>
<summary>🇺🇸 English</summary>
The original idea was to deploy using GCP Cloud Functions with free tier resources.
</details>

## Observações Importantes / Important Notes
<details>
<summary>🇧🇷 Português</summary>
Este projeto não realiza candidaturas automáticas.
A ideia inicial incluía candidaturas automatizadas, mas a direção do projeto mudou devido a:

questões legais;
políticas das plataformas;
considerações éticas sobre automação e scraping.

O foco atual é:

inteligência sobre vagas;
filtragem inteligente;
geração contextual de currículos.

Ele é personalizado para o usuário, deve haver algumas modificações para poder ser aplicado para outros usuários.

</details>
<details>
<summary>🇺🇸 English</summary>
This project does NOT perform automatic job applications.
The initial idea included automated applications, but the project direction changed due to:

legal concerns;
platform policies;
ethical considerations regarding automation and scraping.

The current focus is:

job intelligence;
smart filtering;
contextual resume generation.

It is personalized for the user, some modifications will be required to apply it to other users.
</details>

## Por que este projeto? / Why This Project?
<details>
<summary>🇧🇷 Português</summary>
O objetivo principal é explorar:

IA aplicada a fluxos de trabalho reais;
automação de baixo custo;
pipelines de processamento escaláveis;
geração contextual de documentos;
boas práticas de engenharia de software.

</details>
<details>
<summary>🇺🇸 English</summary>
The main goal is to explore:

AI applied to real-world workflows;
low-cost automation;
scalable processing pipelines;
contextual document generation;
software engineering best practices.

</details>

Autor / Author
Luciano Augusto
GitHub: https://github.com/ladcs/job-hunter