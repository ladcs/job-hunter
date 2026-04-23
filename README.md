# job-hunter

Agente de monitoramento de vagas de emprego com filtragem inteligente por perfil técnico.

O projeto faz scraping periódico de páginas de carreira de empresas selecionadas, filtra as vagas por palavras-chave de inclusão e exclusão, e entrega apenas as oportunidades relevantes para o perfil configurado.

## Estrutura

```
job-hunter/
├── main.py
├── Models/
│   ├── __init__.py
│   └── job_listing.py          # estrutura de dados de uma vaga
└── Fetchers/
    ├── __init__.py
    ├── Fetch_Config.py          # contrato abstrato (ABC)
    ├── Job_Fetch.py             # motor de scraping e filtragem
    └── WebSites/
        ├── __init__.py
        └── Nubank_Config.py     # implementação concreta para o Nubank
```

## Como funciona

Cada site monitorado é representado por uma subclasse de `Fetch_Config` que define:

- `url` — página de listagem de vagas
- `base_job_url` — prefixo para montar a URL de detalhe
- `exclude_keywords` — vagas descartadas se o título contiver qualquer uma dessas palavras
- `include_keywords` — vagas aceitas se o título contiver ao menos uma dessas palavras
- `parse_listings(soup)` — como extrair as vagas do HTML específico daquele site

`Job_Fetcher` recebe qualquer `Fetch_Config` e não conhece nenhum site em particular. A filtragem usa `\b` (word boundary) para evitar falsos positivos de substring — `"TI"` não bate em `"Specialist"`.

## Instalação

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install requests beautifulsoup4
```

## Uso

```bash
# sempre rodar da raiz do projeto
python3 main.py
```

```python
# main.py
from Fetchers.Job_Fetch import Job_Fetcher
from Fetchers.WebSites.Nubank_Config import Nubank_Config

fetcher = Job_Fetcher(config=Nubank_Config())
jobs = fetcher.fetch()

print(f"Total na listagem : {fetcher.raw_count}")
print(f"Após filtro       : {fetcher.filtered_count}\n")

for job in jobs:
    print(f"[{job.id}] {job.title}")
    print(f"         {job.location}")
    print(f"         {job.url}\n")
```

## Adicionando um novo site

Crie um arquivo em `Fetchers/WebSites/` herdando de `Fetch_Config`:

```python
from bs4 import BeautifulSoup
from Fetchers.Fetch_Config import Fetch_Config
from Models.job_listing import Job_Listing


class Gupy_Config(Fetch_Config):

    @property
    def url(self) -> str:
        return "https://empresa.gupy.io/..."

    @property
    def base_job_url(self) -> str:
        return "https://empresa.gupy.io/job"

    @property
    def exclude_keywords(self) -> list[str]:
        return ["senior", "lead", "staff", "principal"]

    @property
    def include_keywords(self) -> list[str]:
        return ["engineer", "engenheiro", "engenheira", "IT"]

    def parse_listings(self, soup: BeautifulSoup) -> list[Job_Listing]:
        # lógica específica do HTML do Gupy
        ...
```

Nenhuma outra classe precisa ser modificada.

## Roadmap

- [ ] Busca de detalhes de cada vaga (`Job_Details_Fetcher`)
- [ ] Análise de match por perfil via LLM
- [ ] Geração de CV e cover letter personalizados por vaga
- [ ] Notificação por e-mail ou Telegram
- [ ] Persistência de vagas já vistas (evitar duplicatas entre execuções)
- [ ] Agendamento via Cloud Scheduler no GCP
