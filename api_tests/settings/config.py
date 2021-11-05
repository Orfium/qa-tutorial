import os

from dotenv import load_dotenv

load_dotenv()

ENVIRONMENTS = {
    "local": {"api_url": "http://localhost:8000/api"}
    "staging": {
        "api_url": "https://application-staging/api"
    },
    "live": {"api_url": "https://application-live/api"},
}


class AppEnvSettings:

    def __init__(self, environment):
        self.api_url = os.getenv("API_URL") or self._get_environment_dict(environment).get("api_url")

    @staticmethod
    def _get_environment_dict(environment: str) -> dict:
        """Get all environment related settings in a dictionary"""
        try:
            return ENVIRONMENTS[environment]
        except KeyError:
            # In case a review app name is given as ENV from the environment
            return {
                "api_url": f"https://{environment}/api",
            }