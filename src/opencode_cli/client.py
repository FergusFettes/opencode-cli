"""Wrapper around official opencode-ai SDK with helper methods for CLI"""
import os
from typing import Optional
from opencode_ai import Opencode


class OpencodeClientWrapper:
    """Wrapper for opencode-ai client with CLI-specific helpers"""
    
    def __init__(self, base_url: Optional[str] = None):
        base_url = base_url or os.getenv("OPENCODE_SERVER", "http://localhost:36000")
        self.client = Opencode(base_url=base_url)
        
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
    
    def get_session(self, session_id: str):
        """Get session by ID or title"""
        session_id = self._resolve_session(session_id)
        return self.client.session.get(path={"id": session_id})
    
    def create_session(self, title: Optional[str] = None):
        """Create a new session"""
        body = {}
        if title:
            body["title"] = title
        return self.client.session.create(body=body)
    
    def list_messages(self, session_id: str):
        """List messages in a session"""
        session_id = self._resolve_session(session_id)
        return self.client.session.messages(path={"id": session_id})
    
    def send_message(self, session_id: str, message: str):
        """Send a message to a session"""
        session_id = self._resolve_session(session_id)
        return self.client.session.prompt(
            path={"id": session_id},
            body={
                "parts": [{"type": "text", "text": message}]
            }
        )
