import hashlib

def to_hash(to_encode: str):
    """
    Converte uma string para um hash (SHA 256)

    Args:
        to_encode (str): string para ser criptografada e convertida em um hash.
    """
    encoded = to_encode.encode()
    return hashlib.sha256(encoded).hexdigest()

def is_valid_proof(hash, difficulty: int=4) -> bool:
    """
    Verifica a validade da nova prova testada.

    Args:
        hash: hash a ser validada
        difficulty (int): dificuldade do hash a ser validado. 4 por padrão.
    
    Returns:
        (bool): True se a prova for válida e False do contrário.
    """
    return hash.startswith("0" * difficulty)