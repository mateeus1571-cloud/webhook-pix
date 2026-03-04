from flask import Flask, request, jsonify

app = Flask(__name__)
pagamentos_pagos = []

@app.route('/')
def home():
    return "✅ Servidor Webhook do Toty está ONLINE!"

# Rota que a Pixup vai acessar para avisar do pagamento
@app.route('/webhook', methods=['POST'])
def receber_webhook():
    dados = request.json
    print("🔔 NOTIFICAÇÃO DA PIXUP:", dados)
    
    if dados:
        st = str(dados.get('status', '')).upper()
        if st in ['PAID', 'COMPLETED', 'SETTLED', 'APPROVED', 'APROVADO', 'CONCLUIDO', 'PAGO', 'RECEBIDO', 'SUCCESS']:
            tid = dados.get('transactionId')
            # Salva o ID da transacao na memoria para o bot pegar depois
            if tid not in [p.get('transactionId') for p in pagamentos_pagos]:
                pagamentos_pagos.append(dados)
                
    return jsonify({"status": "ok"}), 200

# Rota que o seu Bot na Discloud vai acessar para pegar os pagamentos
@app.route('/pegar_pagamentos', methods=['GET'])
def enviar_para_bot():
    return jsonify({"pagamentos": pagamentos_pagos}), 200

# Rota que o seu Bot vai acessar para limpar o pagamento depois de entregar o saldo
@app.route('/limpar_pagamento/<tid>', methods=['GET'])
def limpar(tid):
    global pagamentos_pagos
    pagamentos_pagos = [p for p in pagamentos_pagos if p.get('transactionId') != tid]
    return jsonify({"status": "limpo"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
