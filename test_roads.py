"""Teste para Roads API"""

from api.roads import get_roads_client

# Criar cliente
client = get_roads_client()

# Pontos ao longo de uma via em Campinas
pontos_via = [
    (-22.9056, -47.0608),
    (-22.9070, -47.0620),
    (-22.9085, -47.0635),
    (-22.9100, -47.0650)
]

print("Testando Roads API...")

# Teste 1: Snap to roads
pontos_ajustados = client.snap_to_roads(pontos_via)
print(f"✓ Pontos ajustados: {len(pontos_ajustados)}")

# Teste 2: Nearest roads
vias_proximas = client.nearest_roads([pontos_via[0]])
print(f"✓ Vias próximas: {len(vias_proximas)}")

# Teste 3: Análise completa
analise = client.analisar_via(pontos_via)
if analise:
    print(f"✓ Análise completa:")
    print(f"  - Total pontos: {analise['total_pontos']}")
    print(f"  - Place IDs: {len(analise['place_ids'])}")
    if analise['velocidade_media_kmh']:
        print(f"  - Velocidade média: {analise['velocidade_media_kmh']:.1f} km/h")