import secrets

class RefreshTokenGenerator:
    def generate(self, length: int = 32) -> str:
        """
        Generate refresh token
        
        Args:
            length (int): length of token
            
        Returns:
            str: hex token
        """
        return secrets.token_hex(length)