# rules_engine.py

def verificar_necessidade_alerta(cliente, clima):
    """Cruza o evento climático com o tipo de seguro do cliente."""
    evento = clima.get("evento_relevante")
    
    if not evento:
        return False, "Sem eventos críticos."

    tipo_seguro = cliente["seguro"]
    
    if tipo_seguro == "Auto" and evento in ["Chuva Forte", "Ventos Fortes"]:
        return True, "Risco de alagamento nas vias e queda de galhos/árvores sobre o veículo."
        
    if tipo_seguro == "Residencial" and evento in ["Chuva Forte", "Ventos Fortes"]:
        return True, "Risco de destelhamento, danos elétricos ou alagamento no imóvel."
        
    if tipo_seguro == "Saúde / Vida" and evento in ["Calor Extremo", "Frio Intenso"]:
        return True, "Risco à saúde por condições extremas de temperatura."
        
    return False, "Evento não afeta a apólice."