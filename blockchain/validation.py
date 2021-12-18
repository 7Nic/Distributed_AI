import hashlib

def to_hash(to_encode: str):
    """
    Converte uma string para um hash (SHA 256)

    Args:
        to_encode (str): string para ser criptografada e convertida em um hash.
    """
    encoded = to_encode.encode()
    return hashlib.sha256(encoded).hexdigest()

def proof_of_work(proof: int):
    """
    Encontra um novo número para ser utilizado como Proof of Work.
    O algoritmo consiste em encontrar new_proof tal que a o hash
    da concanteção de proof e new_proof possuam 4 zeros no começo
    da cadeia.

    Args:
        proof (int): valor a ser utilizado como prova anterior
    
    Returns:
        new_proof (int): novo valor para ser utilizado como Proof of Work.
    """
    new_proof = 0
    while not valid_proof(proof, new_proof):
        new_proof += 1
    return new_proof

def valid_proof(proof: int, new_proof: int) -> bool:
    """
    Verifica a validade da nova prova testada.

    Args:
        proof (int): prova anterior.
        new_proof (int): nova prova a ser verificada.
    
    Returns:
        (bool): True se a prova for válida e False do contrário.
    """
    hash = hashlib.sha256(f"{proof}{new_proof}".encode()).hexdigest()
    return hash.startswith("0000")