from typing import Protocol

class TokenGenerator(Protocol):
    """Interface for token generator"""
    def generate(self, length: int) -> str:
        """
        Generate token
        
        Args:
            length (int): length of token
            
        Returns:
            str: token
        """
        ...