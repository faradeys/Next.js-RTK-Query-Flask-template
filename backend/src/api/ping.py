"""Ping API."""
from flask_restful import Resource

from src.lib.access import allow

class PingAPI(Resource):
    """Test ping API."""

    # @allow(["user"])
    def get(self):
        """Ensure API is up."""
        return "pong"
