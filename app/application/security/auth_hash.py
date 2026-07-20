import hashlib
import hmac

class AuthHash:
    def __init__(self, secret: str):
        self.secret = secret.encode("utf-8")

    def generate(self, current_user_id: int, secret_message: str, entities_methods: list[tuple[str, str]]) -> list[str]:
        """
        Generate list of hashes for user
        
        Args:
            current_user_id (int): currently logged in user id
            secret_message (str): secret message for hash (To make sure
                it will be used only for single request from user)
            
        Returns:
            list[str]: list of hashes
        """
        signatures = []
        for entity, method in entities_methods:
            data_to_sign = f"{current_user_id}:{secret_message}:{entity}:{method}".encode("utf-8")
            signature = hmac.new(self.secret, data_to_sign, hashlib.sha256).hexdigest()
            signatures.append(signature)
            
        return signatures

    def verify(self, tokens: list[str], current_user_id: int, secret_message: str, entity: str, method: str) -> bool:
        """
        Verify list of hashes for user
        
        Args:
            tokens (list[str]): list of hashes to verify
            current_user_id (int): currently logged in user id
            secret_message (str): secret message from hash
            entity (str): entity for which hash is generated
            method (str): method for which hash is generated
            
        Returns:
            bool: True if hash is valid, False otherwise
        """
        expected_tokens = self.generate(current_user_id, secret_message, [(entity, method)])
        
        for token in tokens:
            if hmac.compare_digest(expected_tokens[0], token):
                return True
                
        return False