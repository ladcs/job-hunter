from Ia_generative.api.Ai_model.Request_LLM import Ai_Config
from openai import OpenAI
from core.config import OPENAI_API_KEY

class Cv_Resume_extractor(Ai_Config):
    def __init__(self, content: str, title: str, project: str):
        super().__init__(prompt = f"""
Você é um assistente especializado em criação de resumo profissional para currículos.

Sua tarefa é gerar um resumo profissional curto, alinhado com a vaga, utilizando apenas as informações fornecidas.

Conteúdo da vaga:
'''
{title}
{content}
'''

Experiência profissional:
'''
AIDA - Junho 2024 -- Novembro 2025
Back-end Developer
A AIDA atua com análise de conversas de atendimento ao cliente, utilizando LLMs para gerar métricas e insights a partir de grandes volumes de dados de áudio e texto.
  - Para busca das conversas de áudio de clientes, para uma analise, usando conexão SSH ou uso de uma API, desenvolvi pipelines automatizadas, usando Python, Bash assim como serviço de nuvem (VM), seguindo filtros fornecidos, o que possibilitou o processamento de mais de 35 mil conversas por mês.
  - Para a criação de um novo cliente para o sistema. Projetei e desenvolvi uma API REST, com autenticação OAuth2, usando Python e integração com serviços Google e o desenvolvimento múltiplos CRUDs orientados a microserviços, reduzindo o tempo de onboarding de novos clientes de horas para poucos segundos.
  - Para verificar um programa com o mínimo de problemas. Analisei e corrigi falhas em fluxos de processamento e análise de conversas, utilizando inspeção de Logs, estruturas JSON e consultas SQL, aumentando a estabilidade e a confiabilidade do sistema.
  - Um dos produtos da empresa era fazer análises focado em algumas conversas recebendo parametros específicos. Para isso desenvolvi um processo automatizado para execução de prompts em interações selecionadas, com o serviço do Nuvem, eliminando atividades manuais do cliente e garantindo a execução em horários previamente definidos.
  - Um dos clientes não possuia um padrão de envio de suas conversas, para resolver isso criei scripts de filtragem, usando Python, seleção e transformação de interações de áudio e texto, adequando metadados ao padrão interno da plataforma e viabilizando a análise de mais de 80 mil conversas por mês.
  - Para um melhor contato entre cliente e empresa, trabalhei como suporte de cliente nível 1 e nível 2, trazendo soluções técnicas e trazendo soluções assim como sugestões.

SENAI - 2023
Professor
  - Ministrei aulas de Banco de Dados e Redes de Computadores para o 2º ano do Novo Ensino Médio.
  - Desenvolvi metodologias práticas e colaborativas que aumentaram o engajamento e a compreensão dos alunos.
  - Promovi um ambiente de aprendizado colaborativo, incentivando a troca de conhecimento.
'''

Projetos:
'''
{project}
'''

Formações:
'''
Engenharia Elétrica pela UEL - formado em 2023
Desenvolvimento Web Full Stack pela Trybe - formado em 2023
Pós-graduação em Engenharia de Software pela Descomplica - conclusão em 2026
'''

Exemplo de estilo esperado:
'''
Engenheiro de software com experiência em desenvolvimento back-end, análise de dados e automações, com forte atuação na validação de fluxos, análise de logs e garantia de consistência de dados. Experiência prática na criação de automações utilizando Python, Bash em ambientes Unix/Linux/macOS, além de desenvolvimento em Windows.
'''

Regras:
- texto em primeira pessoa do singular
- máximo de 5 linhas
- utilizar apenas informações presentes nos dados fornecidos
- não inventar experiências, empresas, senioridade ou tecnologias
- priorizar competências mais alinhadas à vaga
- não citar tecnologias irrelevantes para a vaga
- manter linguagem profissional e objetiva
- evitar listas
- evitar buzzwords exageradas
- devolver apenas o resumo final
""".strip())

    @property
    def model(self) -> str:
        return "gpt-4.1-mini"
    
    @property
    def reasoning(self) -> str:
        return None
    
    @property
    def temperature(self) -> float:
        return 0.4
    
    @property
    def max_tokens(self) -> int:
        return 1000
    
    @property
    def args(self) -> dict:
        return {
            "input": self.prompt,
            "model": self.model,
            "max_output_tokens": self.max_tokens,
            "temperature": self.temperature,
        }
    
    def client(self):
        return OpenAI(api_key=OPENAI_API_KEY)