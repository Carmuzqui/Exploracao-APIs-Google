"""Teste para Distance Matrix API"""

from api.distance_matrix import get_distance_matrix_client

# Criar cliente
client = get_distance_matrix_client()

# Pontos de teste em Campinas
origens = [
    (-22.9056, -47.0608),  # Centro
    (-22.9100, -47.0650)   # Próximo
]

destinos = [
    (-22.9200, -47.0700),
    (-22.9000, -47.0500)
]

print("Testando Distance Matrix API...")

# Teste 1: Matriz simples
resultado = client.calcular_matriz(origens, destinos)
print(f"✓ Matriz calculada: {resultado['total_pares']} pares")

# Teste 2: Cobertura
pontos_cobertos = client.calcular_cobertura(
    ponto_central=origens[0],
    pontos_candidatos=destinos,
    raio_max_metros=5000
)
print(f"✓ Pontos cobertos: {len(pontos_cobertos)}/{len(destinos)}")

# Teste 3: Conectividade
conectividade = client.calcular_conectividade(origens + destinos)
print(f"✓ Taxa de conectividade: {conectividade['taxa_conectividade']:.2%}")