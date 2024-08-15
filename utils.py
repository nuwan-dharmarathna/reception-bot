import re

def extract_session_id(session_str: str):
    matcher = re.search(r"/sessions/(.*?)/contexts", session_str)
    if matcher:
        session_id = matcher.group(1)
        return session_id
    return None