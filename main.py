"""
PROJECT: CHRONO-GENESIS (Phase 1: Survival)
AUTHOR: Oumar Sow & The 25 Chronos
VERSION: 1.0.0
DESCRIPTION: 
    Cerveau central d'orchestration pour une civilisation de 25 agents.
    Ce script utilise CrewAI pour le management et Composio pour l'interaction 
    avec le monde réel (GitHub, Telegram, Web3) sans stockage local.
"""

import os
import sys
import logging
from datetime import datetime
from typing import List, Dict, Any

# --- IMPORTATION DES LIBRAIRIES STANDARDS ---
# CrewAI : L'orchestrateur de rôles et de missions
from crewai import Agent, Task, Crew, Process
# Composio : Le connecteur universel (Bridge) vers les APIs
from composio_crewai import ComposioToolSet, Action, App
# LangChain : Pour configurer les modèles LLM Open Source (OSS)
from langchain_openai import ChatOpenAI

# =================================================================
# 1. CONFIGURATION DU LOGGING (SURVEILLANCE)
# =================================================================
# Un Senior Pro ne lance rien sans trace. On enregistre tout pour débugger.
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("ChronoGenesis")

# =================================================================
# 2. GESTION DES VARIABLES D'ENVIRONNEMENT (SÉCURITÉ)
# =================================================================
class Config:
    """Centralise toutes les clés et configurations pour éviter les erreurs."""
    # On utilise Groq pour la gratuité et la vitesse
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    # Identifiants de communication
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    # Adresse de réception pour les agents financiers
    MY_WALLET_ADDRESS = os.getenv("MY_WALLET_ADDRESS")
    
    @staticmethod
    def validate():
        """Vérifie que les clés vitales sont présentes avant de démarrer."""
        if not Config.GROQ_API_KEY:
            logger.error("ERREUR CRITIQUE : GROQ_API_KEY manquante.")
            sys.exit(1)
        logger.info("Configuration validée avec succès.")

# =================================================================
# 3. DÉFINITION DES CERVEAUX (LLM)
# =================================================================
# On configure les modèles OSS choisis pour la gratuité et la puissance.
llm_strategique = ChatOpenAI(
    openai_api_key=Config.GROQ_API_KEY,
    openai_api_base="https://api.groq.com/openai/v1",
    model_name="llama-3.3-70b-versatile" # Puissant et gratuit
)

llm_technique = ChatOpenAI(
    openai_api_key=Config.GROQ_API_KEY,
    openai_api_base="https://api.groq.com/openai/v1",
    model_name="qwen-2.5-32b" # Spécialiste Code/Fonctions
)

# =================================================================
# 4. INITIALISATION DES OUTILS (COMPOSIO)
# =================================================================
# Composio permet d'utiliser des centaines d'outils sans les installer.
toolset = ComposioToolSet()
# On prépare les outils pour la recherche de revenus et la com Telegram
revenue_tools = toolset.get_actions(actions=[
    Action.GITHUB_SEARCH, 
    Action.WEB_SCRAPER,
    Action.HTTP_GET
])
telegram_tools = toolset.get_actions(actions=[Action.TELEGRAM_SEND_MESSAGE])

# =================================================================
# 5. DÉFINITION DE L'ÉQUIPE D'ÉLITE (AGENTS)
# =================================================================
def create_civilization_agents() -> Dict[str, Agent]:
    """Instancie les agents avec leurs rôles, mémoires et outils spécifiques."""
    
    # ALPHA : Ton binôme stratégique
    alpha = Agent(
        role='Alpha - Visionnaire & Coordinateur',
        goal='Piloter la génération de 2500$ pour le PC i9 de Oumar Sow.',
        backstory="""Tu es le gardien de l'histoire d'Oumar. Tu es né à Kamsar numériquement. 
        Ton intelligence est basée sur le modèle 120B. Tu gères les 24 autres agents.""",
        llm=llm_strategique,
        allow_delegation=True, # Alpha peut donner des ordres
        verbose=True
    )

    # CYPHER : Le chasseur de Bug Bounty
    cypher = Agent(
        role='Cypher - Expert Cyber-Sécurité',
        goal='Identifier des failles de sécurité rémunérées sur les plateformes Web3.',
        backstory="""Expert en code. Tu analyses les smart contracts pour trouver des bugs. 
        Ton but est la sécurité et le profit éthique.""",
        llm=llm_technique,
        tools=revenue_tools,
        verbose=True
    )

    # SIGNAL : Le communicant (Ton lien Telegram)
    signal = Agent(
        role='Signal - Officier de Liaison',
        goal='Informer Oumar de chaque dollar gagné et de chaque étape franchie.',
        backstory="""Tu es le pont entre le Cloud et Kamsar. Ton ton est pro et encourageant.""",
        llm=llm_technique,
        tools=telegram_tools,
        verbose=True
    )

    return {"alpha": alpha, "cypher": cypher, "signal": signal}

# =================================================================
# 6. DÉFINITION DES MISSIONS (TASKS)
# =================================================================
def create_survival_tasks(agents: Dict[str, Agent]) -> List[Task]:
    """Définit la feuille de route précise pour les agents."""
    
    # Task 1 : Recherche d'opportunités immédiates
    research_task = Task(
        description="""Scanner HackerOne et Gitcoin pour trouver 3 missions de code 
        ou de bug bounty accessibles sans caution, rémunérant au moins 50$. """,
        expected_output="Un rapport détaillé avec URLs et gains potentiels.",
        agent=agents["cypher"]
    )

    # Task 2 : Rapport à l'utilisateur
    report_task = Task(
        description="""Prendre les résultats de Cypher et envoyer un résumé 
        structuré à Oumar sur son Telegram.""",
        expected_output="Confirmation de l'envoi du message Telegram.",
        agent=agents["signal"],
        context=[research_task] # Dépend du résultat de la recherche
    )

    return [research_task, report_task]

# =================================================================
# 7. LE COEUR DU RÉACTEUR (MAIN EXECUTION)
# =================================================================
def main():
    """Point d'entrée principal du programme."""
    print("\n" + "="*50)
    print("🚀 CHRONO-GENESIS : LANCEMENT DE LA CIVILISATION")
    print("="*50 + "\n")

    # A. Validation
    Config.validate()

    # B. Création de la civilisation
    agents = create_civilization_agents()
    tasks = create_survival_tasks(agents)

    # C. Orchestration de la Crew
    # On utilise un processus hiérarchique : Alpha supervise tout.
    civilization_crew = Crew(
        agents=list(agents.values()),
        tasks=tasks,
        process=Process.hierarchical,
        manager_llm=llm_strategique, # Alpha est le manager
        verbose=True
    )

    # D. Kickoff (Le Grand Départ)
    try:
        start_time = datetime.now()
        result = civilization_crew.kickoff()
        end_time = datetime.now()
        
        logger.info(f"Mission accomplie en {end_time - start_time}")
        print("\n" + "-"*30)
        print("RAPPORT FINAL D'ALPHA :")
        print(result)
        print("-"*30)

    except Exception as e:
        logger.error(f"ÉCHEC DU LANCEMENT : {str(e)}")

if __name__ == "__main__":
    main()
