"""Python client for opencode server API"""
import os
from typing import Optional, Any
import httpx

__version__ = "0.1.0"


class OpencodeClient:
    """Client for interacting with opencode server API"""
    
    def __init__(self, base_url: Optional[str] = None, timeout: float = 120.0):
        self.base_url = base_url or os.getenv("OPENCODE_SERVER", "http://localhost:36000")
        self.timeout = timeout
        
    def _resolve_session(self, session_identifier: str) -> str:
        """Resolve session title to session ID"""
        if session_identifier.startswith("ses_"):
            return session_identifier
        
        sessions = self.list_sessions()
        matches = [s for s in sessions if s.get("title") == session_identifier]
        
        if len(matches) == 0:
            raise ValueError(f"No session found with title '{session_identifier}'")
        elif len(matches) > 1:
            ids = [s.get("id") for s in matches]
            raise ValueError(f"Multiple sessions found with title '{session_identifier}': {ids}")
        
        return matches[0].get("id")
    
    def list_sessions(self) -> list[dict[str, Any]]:
        """List all sessions on the server"""
        url = f"{self.base_url}/session"
        response = httpx.get(url, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
    
    def get_session(self, session_id: str) -> dict[str, Any]:
        """Get session info by ID or title"""
        session_id = self._resolve_session(session_id)
        url = f"{self.base_url}/session/{session_id}"
        response = httpx.get(url, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
    
    def create_session(self, title: Optional[str] = None) -> dict[str, Any]:
        """Create a new session"""
        url = f"{self.base_url}/session"
        payload = {}
        if title:
            payload["title"] = title
        response = httpx.post(url, json=payload, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
    
    def list_messages(self, session_id: str) -> list[dict[str, Any]]:
        """List all messages in a session"""
        session_id = self._resolve_session(session_id)
        url = f"{self.base_url}/session/{session_id}/message"
        response = httpx.get(url, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
    
    def send_message(self, session_id: str, message: str) -> dict[str, Any]:
        """Send a message to a session"""
        session_id = self._resolve_session(session_id)
        url = f"{self.base_url}/session/{session_id}/message"
        payload = {
            "parts": [
                {
                    "type": "text",
                    "text": message
                }
            ]
        }
        response = httpx.post(url, json=payload, timeout=self.timeout)
        response.raise_for_status()
        return response.json()


__all__ = ["OpencodeClient"]
