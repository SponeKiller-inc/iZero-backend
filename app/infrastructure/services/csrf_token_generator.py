import secrets

class CsrfTokenGenerator:
    def generate(self, length: int = 32) -> str:
        """
        Generate CSRF token
        
        Args:
            length (int): length of token
            
        Returns:
            str: CSRF token
        """
        return secrets.token_hex(length)