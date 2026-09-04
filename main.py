# main.py
from mock_db import get_clientes
from weather_service import obter_dados_climaticos
from rules_engine import verificar_necessidade_alerta
from ai_agent import gerar_mensagem_ia

def iniciar_pipeline_alertas():
    print("🌤️ Iniciando varredura climática proativa para a base de segurados...\n")
    print("=" * 60)
    
    clientes = get_clientes()
    
    for cliente in clientes:
        print(f"👤 Analisando cliente: {cliente['nome']} ({cliente['cidade']}) | Seguro: {cliente['seguro']}")
        
        # 1. Coleta
        clima = obter_dados_climaticos(cliente['cidade'])
        if not clima:
            continue
            
        print(f"   ☁️ Clima atual: {clima['descricao'].capitalize()} | {clima['temperatura']}°C")
        
        # 2 e 3. Identificação e Regras
        enviar_alerta, motivo = verificar_necessidade_alerta(cliente, clima)
        
        if enviar_alerta:
            print(f"   ⚠️  [ALERTA GERADO] Motivo: {motivo}")
            print("   🧠 Acionando Agente de IA para redigir mensagem...")
            
            # 4. Geração
            mensagem = gerar_mensagem_ia(cliente, clima, motivo)
            
            # 5. Simulação de Envio
            print("\n   📱 SIMULAÇÃO DE DISPARO (SMS / Push):")
            print(f"   ➡️ Para: {cliente['nome']}")
            print(f"   💬 Mensagem: {mensagem}\n")
        else:
            print("   ✅ Condições seguras. Nenhum alerta necessário.\n")
            
        print("-" * 60)

if __name__ == "__main__":
    iniciar_pipeline_alertas()