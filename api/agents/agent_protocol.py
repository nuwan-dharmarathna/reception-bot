from typing import Dict, List, Any, Protocol

class AgentProtocol(Protocol):
    
    def get_response(self, messages:List[Dict[str, Any]]) -> Dict[str, Any]:
        ...