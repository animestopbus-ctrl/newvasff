import re
import requests
from typing import Dict, Optional, Tuple
from datetime import datetime

class LastPerson07API:
    def __init__(self) -> None:
        self.base_url: str = "https://api.github.com/users"
        self.timeout: int = 10
    
    def validate_username(self, username: str) -> Tuple[bool, str]:
        """Validate GitHub username format using pattern matching"""
        match username:
            case "" | None:
                return False, "Username cannot be empty"
            case _ if not re.match(r'^[a-zA-Z0-9_-]{1,39}$', username):
                return False, "Invalid GitHub username format"
            case _:
                return True, "Valid"
    
    def fetch_user_data(self, username: str) -> Tuple[Optional[Dict], Optional[str]]:
        """Fetch GitHub user data from API with enhanced error handling"""
        try:
            url: str = f"{self.base_url}/{username}"
            response: requests.Response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            data: Dict = response.json()
            
            # Use match case for status handling
            match data.get("message"):
                case "Not Found":
                    return None, f"GitHub user '{username}' not found"
                case _:
                    return data, None
            
        except requests.exceptions.Timeout:
            return None, "Request timeout. Please try again."
        except requests.exceptions.ConnectionError:
            return None, "Connection error. Please check your internet."
        except requests.exceptions.HTTPError as e:
            # Pattern matching for HTTP errors
            match e.response.status_code:
                case 403:
                    return None, "GitHub API rate limit exceeded. Try again later."
                case 404:
                    return None, f"GitHub user '{username}' not found"
                case _:
                    return None, f"GitHub API error: {e.response.status_code}"
        except Exception as e:
            return None, f"Unexpected error: {str(e)}"
