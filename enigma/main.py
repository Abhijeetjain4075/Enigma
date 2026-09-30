"""ASGI entry point: `uvicorn enigma.main:app`."""

from enigma.api import create_app

app = create_app()
