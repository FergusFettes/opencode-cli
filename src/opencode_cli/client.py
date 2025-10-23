"""Wrapper around official opencode-ai SDK with helper methods for CLI"""
import os
from typing import Optional, Any
import httpx
from opencode_ai import Opencode


class OpencodeClientWrapper:
    """Wrapper for opencode-ai client with CLI-specific helpers"""
    
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or os.getenv("OPENCODE_SERVER", "http://localhost:36000")
        self.client = Opencode(base_url=self.base_url)
        
    def _resolve_session(self, session_identifier: str) -> str:
        """Resolve session title to session ID"""
        if session_identifier.startswith("ses_"):
            return session_identifier
        
        sessions = self.client.session.list()
        matches = [s for s in sessions if s.title == session_identifier]
        
        if len(matches) == 0:
            raise ValueError(f"No session found with title '{session_identifier}'")
        elif len(matches) > 1:
            ids = [s.id for s in matches]
            raise ValueError(f"Multiple sessions found with title '{session_identifier}': {ids}")
        
        return matches[0].id
    
    def list_sessions(self):
        """List all sessions"""
        return self.client.session.list()
    
    def get_session(self, session_id: str) -> dict[str, Any]:
        """Get session by ID or title (using direct API)"""
        session_id = self._resolve_session(session_id)
        response = httpx.get(f"{self.base_url}/session/{session_id}")
        response.raise_for_status()
        return response.json()
    
    def create_session(self, title: Optional[str] = None):
        """Create a new session"""
        extra_body = {}
        if title:
            extra_body["title"] = title
        return self.client.session.create(extra_body=extra_body)
    
    def list_messages(self, session_id: str):
        """List messages in a session"""
        session_id = self._resolve_session(session_id)
        return self.client.session.messages(session_id)
    
    def send_message(self, session_id: str, message: str):
        """Send a message to a session"""
        session_id = self._resolve_session(session_id)
        session_info = self.get_session(session_id)
        
        mode = session_info.get("mode", {})
        model_id = mode.get("modelID", "claude-sonnet-4-5")
        provider_id = mode.get("providerID", "anthropic")
        
        return self.client.session.chat(
            session_id,
            model_id=model_id,
            provider_id=provider_id,
            parts=[{"type": "text", "text": message}]
        )
    
    def rename_session(self, session_id: str, new_title: str) -> dict[str, Any]:
        """Rename a session (SDK missing update method, using direct API)"""
        session_id = self._resolve_session(session_id)
        response = httpx.patch(
            f"{self.base_url}/session/{session_id}",
            json={"title": new_title}
        )
        response.raise_for_status()
        return response.json()
    
    def delete_session(self, session_id: str):
        """Delete a session"""
        session_id = self._resolve_session(session_id)
        self.client.session.delete(session_id)
