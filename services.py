import webbrowser
import urllib.parse

def enviar_zap_logistica(os):
    # Formata a mensagem
    texto = (
        f"🚀 *NOVA ENTREGA - CAÇULA*\n\n"
        f"👤 Cliente: {os.cliente.nome}\n"
        f"📍 Endereço: {os.cliente.endereco}\n"
        f"🧺 Itens: {os.descricao}\n"
        f"💰 Valor: R$ {os.valor:.2f}"
    )
    
    texto_encoded = urllib.parse.quote(texto)
    # Coloque o número do Luis aqui (com DDD)
    link = f"https://wa.me/5541999999999?text={texto_encoded}"
    webbrowser.open(link)