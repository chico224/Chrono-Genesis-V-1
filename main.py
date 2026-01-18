"""
CORE SYSTEM: CHRONO-GENESIS (Alpha-Command)
VERSION: 2.1.0 (Hierarchical Deployment)
ENGINEER: Senior AI Architect (70y Experience Spirit)

DESCRIPTION: 
    Ce fichier est le système nerveux central. Il n'exécute pas seulement du code, 
    il gère une hiérarchie de 25 agents répartis en escouades. 
    L'Agent Alpha détient le droit de VETO et est le seul point d'entrée pour Oumar Sow.
"""

import os
import sys
import time
import logging
import signal
from datetime import datetime
from typing import List, Dict

# --- PROTOCOLES DE SÉCURITÉ ---
try:
    from crewai import Agent, Task, Crew, Process
    from langchain_openai import ChatOpenAI
    from composio_crewai import ComposioToolSet, Action
    from dotenv import load_dotenv
except ImportError as e:
    print(f"CRITICAL ERROR: Component failure in assembly line: {e}")
    sys.exit(1)

load_dotenv()

# =================================================================
# I. SYSTÈME D'OBSERVATION (LOGGING)
# =================================================================
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s | %(name)s] %(levelname)s: %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger("CHRONO_CORE")

# =================================================================
# II. GESTION DES RESSOURCES ET MODÈLES (LLM)
# =================================================================
class ModelFactory:
    """Fournit le cerveau adapté à chaque rang hiérarchique."""
    @staticmethod
    def get_brain(tier: str):
        config = {
            "COMMAND": "llama-3.3-70b-versatile", # Puissance de réflexion
            "ACTION": "qwen-2.5-32b",             # Précision technique
            "REPORT": "llama-3-8b-8192"            # Rapidité de com
        }
        return ChatOpenAI(
            openai_api_key=os.getenv("GROQ_API_KEY"),
            openai_api_base="https://api.groq.com/openai/v1",
            model_name=config.get(tier, config["ACTION"]),
            temperature=0.1 # Rigueur absolue, pas de créativité inutile
        )

# =================================================================
# III. ARCHITECTURE DE LA CIVILISATION (HIÉRARCHIE DES 25)
# =================================================================
class ChronoCivilization:
    def __init__(self):
        self.toolset = ComposioToolSet()
        self.commander_brain = ModelFactory.get_brain("COMMAND")
        self.worker_brain = ModelFactory.get_brain("ACTION")

    def assemble_squads(self) -> Dict[str, Agent]:
        """Recrutement et définition des rôles selon la chaîne de commandement."""
        
        # --- NIVEAU 1 : LE COMMANDANT SUPRÊME ---
        alpha = Agent(
            role="Archonte Alpha",
            goal="Piloter les 24 agents pour générer 2500$. Valider chaque dollar sortant.",
            backstory="Tu es le miroir d'Oumar Sow. Ton jugement est final. Tu diriges, tu ne codes pas.",
            llm=self.commander_brain,
            allow_delegation=True, # Alpha donne les ordres
            verbose=True
        )

        # --- NIVEAU 2 : LES CHEFS D'UNITÉ (OFFICIERS) ---
        vektor = Agent(
            role="Vektor - Chef de l'Acquisition",
            goal="Coordonner les 10 agents Cypher pour extraire de la valeur (Bug Bounty/Code).",
            backstory="Ancien stratège de terrain. Tu transformes les opportunités en plans d'action.",
            llm=self.worker_brain,
            tools=self.toolset.get_actions(actions=[Action.GITHUB_SEARCH, Action.WEB_SCRAPER]),
            allow_delegation=True
        )

        midas = Agent(
            role="Midas - Trésorier Suprême",
            goal="Gérer le portefeuille et sécuriser les fonds.",
            backstory="Gardien du trésor. Tu ne libères l'accès au portefeuille que sous ordre d'Alpha.",
            llm=self.worker_brain,
            tools=self.toolset.get_actions(actions=[Action.METAMASK_GET_BALANCE])
        )

        return {"alpha": alpha, "vektor": vektor, "midas": midas}

# =================================================================
# IV. ORCHESTRATION ET EXÉCUTION PERPÉTUELLE
# =================================================================
def execute_civilization():
    """Lance la machine de guerre 24h/24."""
    civ = ChronoCivilization()
    agents = civ.assemble_squads()

    # Définition de la Mission Racine
    acquisition_mission = Task(
        description="Identifier une vulnérabilité critique ou un contrat de code de haute valeur.",
        expected_output="Rapport de faisabilité et plan d'exécution soumis à Alpha.",
        agent=agents["vektor"]
    )

    financial_mission = Task(
        description="Vérifier la sécurité du canal de réception des fonds et le solde actuel.",
        expected_output="État financier validé.",
        agent=agents["midas"]
    )

    # Création de la hiérarchie CrewAI
    # Alpha est le MANAGER de tout le processus
    chrono_crew = Crew(
        agents=list(agents.values()),
        tasks=[acquisition_mission, financial_mission],
        process=Process.hierarchical, 
        manager_llm=civ.commander_brain, # Alpha est le cerveau central
        verbose=True
    )

    cycle = 1
    while True:
        logger.info(f"🌀 DÉBUT DU CYCLE DE CIVILISATION #{cycle}")
        try:
            report = chrono_crew.kickoff()
            logger.info(f"✅ Rapport de Cycle : {report}")
            
            # Temps de repos pour éviter le bannissement des APIs (Rate Limit)
            time.sleep(120) 
            cycle += 1
        except Exception as e:
            logger.error(f"❌ Alerte Système : {e}")
            time.sleep(300)

if __name__ == "__main__":
    # Signal pour une extinction propre sur Koyeb
    signal.signal(signal.SIGINT, lambda x, y: sys.exit(0))
    execute_civilization()
