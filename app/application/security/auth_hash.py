import hashlib
import hmac

class AuthHash:
    def __init__(self, secret: str):
        self.secret = secret.encode("utf-8")

    def generate(self, current_user_id: int, secret_message: str) -> str:
        """
        Generate hash for user
        
        Args:
            current_user_id (int): currently logged in user id
            secret_message (str): secret message from hash
            
        Returns:
            str: token
        """
        data_to_sign = f"{current_user_id}:{secret_message}".encode("utf-8")
        signature = hmac.new(self.secret, data_to_sign, hashlib.sha256).hexdigest()
        
        return signature

    def verify(self, token: str, current_user_id: int, secret_message: str) -> bool:
        """
        Verify hash for user
        
        Args:
            token (str): token to verify
            current_user_id (int): currently logged in user id
            secret_message (str): secret message from hash
            
        Returns:
            bool: True if hash is valid, False otherwise
        """
        expected_token = self.generate(current_user_id, secret_message)
        
        return hmac.compare_digest(expected_token, token)