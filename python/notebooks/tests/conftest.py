from pathlib import Path

from dotenv import load_dotenv

NOTEBOOKS_DIR = Path(__file__).resolve().parent.parent

# Live tests read OVH_API_KEY from the environment; locally a gitignored .env next to the
# notebooks provides it (see .env.example). Codespaces secrets are already in the environment.
load_dotenv(NOTEBOOKS_DIR / ".env")
