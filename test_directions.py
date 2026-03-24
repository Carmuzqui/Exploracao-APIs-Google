"""Teste para Directions API"""

from api.directions import get_directions_client

# Criar cliente
client = get_directions_client()

# Testar rota simples
print("Testando Directions API...")
rota = client.calcular_rota(
    origem=(-22.9056, -47.0608),
    destino=(-22.9100, -47.0650)
)

if rota:
    print(f"✓ Distância: {rota['distancia_texto']}")
    print(f"✓ Duração: {rota['duracao_texto']}")
    print(f"✓ Passos: {rota['passos']}")
else:
    print("✗ Erro ao calcular rota")