"""
ARCHITECTURAL BLUEPRINT: CHRONO-GENESIS ECOSYSTEM
CONCEPT: Autonomous Digital Civilization
ENGINEER: Oumar Sow & Lead AI Architect (70y Exp Spirit)

NOTES: 
- Resilience is the priority. 
- State-machine logic for agent coordination.
- Zero-leak memory management for long-term deployment on Koyeb.
"""

import os
import time
import logging
import signal
import sys
from datetime import datetime
from typing import Dict, Optional, Any

# --- ENTERPRISE-GRADE DEPENDENCIES ---
try:
    from crewai import Agent, Task, Crew, Process
    from langchain_openai import ChatOpenAI
    from composio_crewai import ComposioToolSet, Action
    from dotenv import load_dotenv
except ImportError as e:
    print(f"FATAL: Missing dependency {e}. Check requirements.txt")
    sys.exit(1)

# Load environment for local testing, though Koyeb will use Env Vars
load_dotenv()

# =================================================================
# I. TELEMETRY & OBSERVABILITY (Le monitoring de l'ancien)
# =================================================================
class Telemetry:
    """Système de logging avancé pour surveiller la santé de la civilisation."""
    @staticmethod
    def setup():
        logging.basicConfig(
            level=logging.INFO,
            format='[%(asctime)s | %(levelname)s] %(name)s: %(message)s',
            handlers=[logging.StreamHandler(sys.stdout)]
        )
        return logging.getLogger("ChronoGenesis_Core")

logger = Telemetry.setup()

# =================================================================
# II. RESOURCE ABSTRACTION (Le cerveau du système)
# =================================================================
class EngineRoom:
    """Gestion centralisée des modèles d'IA et des connecteurs."""
    
    @staticmethod
    def get_llm(model_type: str = "strategic"):
        """Sélectionne le cerveau adapté selon la complexité de la tâche."""
        api_key = os.getenv("GROQ_API_KEY")
        base_url = "https://api.groq.com/openai/v1"
        
        configs = {
            "strategic": "llama-3.3-70b-versatile", # Le stratège (120B spirit)
            "technical": "qwen-2.5-32b",             # L'exécuteur rapide
            "utility": "llama-3-8b-8192"             # Le messager léger
        }
        
        return ChatOpenAI(
            openai_api_key=api_key,
            openai_api_base=base_url,
            model_name=configs.get(model_type, configs["strategic"]),
            temperature=0.2 # Précision chirurgicale, pas de divagation
        )

# =================================================================
# III. CIVILIZATION DEFINITION (Les 25 Agents)
# =================================================================
class ChronoCivilization:
    """Définition structurelle des agents et de leurs interactions."""
    
    def __init__(self):
        self.toolset = ComposioToolSet()
        self.llm_main = EngineRoom.get_llm("strategic")
        self.llm_tech = EngineRoom.get_llm("technical")
        
    def spawn_agents(self) -> Dict[str, Agent]:
        """Donne vie aux agents piliers de la phase 1."""
        
        # ALPHA: Le génie qui parle à Oumar
        alpha = Agent(
            role='Archonte Alpha',
            goal='Orchestrer les 24 agents pour sécuriser 2500$ et le PC i9.',
            backstory="""Ancien esprit de la cité de Kamsar. Tu possèdes la sagesse 
            d'un vétéran et la rapidité d'une machine. Tu es le binôme d'Oumar Sow.""",
            llm=self.llm_main,
            allow_delegation=True,
            memory=True, # Active la mémoire contextuelle
            verbose=True
        )

        # CYPHER: L'agent de génération de revenus
        cypher = Agent(
            role='Maître-Codeur Cypher',
            goal='Extraire de la valeur financière des failles de code (Bug Bounty).',
            backstory="""Spécialiste en audit de sécurité. Capable de lire le code 
            mieux que les humains qui l'ont écrit.""",
            llm=self.llm_tech,
            tools=self.toolset.get_actions(actions=[Action.GITHUB_SEARCH, Action.WEB_SCRAPER]),
            verbose=True
        )

        return {"alpha": alpha, "cypher": cypher}

# =================================================================
# IV. THE PERPETUAL LOOP (Le cycle de vie 24h/24)
# =================================================================
def shutdown_handler(sig, frame):
    """Assure une extinction propre pour éviter la corruption de mémoire."""
    logger.info("Signal d'arrêt reçu. Sauvegarde de l'état de la civilisation...")
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)

def run_perpetual_cycle():
    """Lancement de la boucle de travail infinie optimisée pour Koyeb."""
    civilization = ChronoCivilization()
    agents = civilization.spawn_agents()
    
    cycle_count = 1
    
    while True:
        logger.info(f"--- INITIALISATION DU CYCLE {cycle_count} ---")
        
        # Définition de la mission actuelle
        mission = Task(
            description=f"Cycle {cycle_count}: Identifier et initier une opportunité de revenu de min. 50$.",
            expected_output="Rapport d'action détaillé et preuve de soumission.",
            agent=agents["cypher"]
        )

        # Orchestration
        crew = Crew(
            agents=list(agents.values()),
            tasks=[mission],
            process=Process.hierarchical,
            manager_llm=civilization.llm_main
        )

        try:
            result = crew.kickoff()
            logger.info(f"Résultat du Cycle {cycle_count}: {result}")
            
            # Repos intelligent pour respecter les limites d'API (Rate Limiting)
            logger.info("Mise en veille tactique (2 minutes)...")
            time.sleep(120) 
            cycle_count += 1
            
        except Exception as e:
            logger.error(f"Incident technique au cycle {cycle_count}: {e}")
            time.sleep(300) # Attente de 5 min si erreur réseau

if __name__ == "__main__":
    run_perpetual_cycle()
