"""Environment-based configuration for Roboflow inference."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    api_key: str
    api_url: str
    stock_model_id: str
    theft_model_id: str

    @classmethod
    def from_env(cls) -> "Settings":
        """Load required settings from the environment and local .env file."""
        load_dotenv()
        values = {
            "ROBOFLOW_API_KEY": os.getenv("ROBOFLOW_API_KEY", "").strip(),
            "STOCK_MODEL_ID": os.getenv("STOCK_MODEL_ID", "").strip(),
            "THEFT_MODEL_ID": os.getenv("THEFT_MODEL_ID", "").strip(),
        }
        missing = [name for name, value in values.items() if not value]
        if missing:
            raise ValueError(
                "Missing configuration: "
                + ", ".join(missing)
                + ". Copy .env.example to .env and fill in your values."
            )

        return cls(
            api_key=values["ROBOFLOW_API_KEY"],
            api_url=os.getenv(
                "ROBOFLOW_API_URL", "https://serverless.roboflow.com"
            ).strip(),
            stock_model_id=values["STOCK_MODEL_ID"],
            theft_model_id=values["THEFT_MODEL_ID"],
        )
