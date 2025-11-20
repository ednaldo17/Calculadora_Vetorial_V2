from flask import request, jsonify, render_template

from utils.bibliotecaswm import (
    somar_vetores, subtrair_vetores, produto_escalar, produto_vetorial,
    vetor_unitario, projecao_vetor, componente_vetorial, norma_vetor,
    ortogonalizacao_gram_schmidt
)

from utils.RetasPlanos import equacao_reta, equacao_plano


def init_app(app):

    @app.route('/')
    def index():
        return render_template('chatbot.html')

    @app.route('/calcular', methods=['POST'])
    def calcular():
        try:
            data = request.get_json() or {}
            operacao = data.get('operacao')

            if not operacao:
                return jsonify({'erro': 'Campo "operacao" é obrigatório.'}), 400

            # Operações com DOIS vetores
            if operacao in [
                'somar', 'subtracao', 'produto_escalar', 'produto_vetorial',
                'projecao', 'componente', 'reta'
            ]:
                v1 = data.get('vetor1')
                v2 = data.get('vetor2')

                if v1 is None or v2 is None:
                    return jsonify({'erro': 'vetor1 e vetor2 são obrigatórios.'}), 400

                if not isinstance(v1, list) or not isinstance(v2, list):
                    return jsonify({'erro': 'Os vetores devem ser listas.'}), 400

                if len(v1) != len(v2) and operacao != 'reta':
                    return jsonify({'erro': 'Vetores devem ter a mesma dimensão.'}), 400

                # Conversão para float
                v1 = list(map(float, v1))
                v2 = list(map(float, v2))

            # Operações com UM vetor
            elif operacao in ['norma', 'unitario']:
                v1 = data.get('vetor1')

                if v1 is None:
                    return jsonify({'erro': 'vetor1 é obrigatório.'}), 400

                if not isinstance(v1, list):
                    return jsonify({'erro': 'vetor1 deve ser uma lista.'}), 400

                v1 = list(map(float, v1))

            # Operação: PLANO
            elif operacao == 'plano':
                v1 = data.get('vetor1')
                v2 = data.get('vetor2')
                v3 = data.get('vetor3')

                if v1 is None or v2 is None or v3 is None:
                    return jsonify({'erro': 'vetor1, vetor2 e vetor3 são obrigatórios.'}), 400

                v1 = list(map(float, v1))
                v2 = list(map(float, v2))
                v3 = list(map(float, v3))

            # Operação: GRAM-SCHMIDT
            elif operacao == 'gram_schmidt':
                vetores = data.get('vetores')

                if not isinstance(vetores, list) or len(vetores) == 0:
                    return jsonify({'erro': 'Envie uma lista de vetores válida.'}), 400

                vetores_num = [list(map(float, v)) for v in vetores]
                base = ortogonalizacao_gram_schmidt(vetores_num)
                return jsonify({'resultado': base})

            else:
                return jsonify({'erro': 'Operação inválida.'}), 400

            # Operações diretas
            funcoes = {
                'somar': lambda: somar_vetores(v1, v2),
                'subtracao': lambda: subtrair_vetores(v1, v2),
                'produto_escalar': lambda: produto_escalar(v1, v2),
                'produto_vetorial': lambda: produto_vetorial(v1, v2),
                'norma': lambda: norma_vetor(v1),
                'unitario': lambda: vetor_unitario(v1),
                'projecao': lambda: projecao_vetor(v1, v2),
                'componente': lambda: componente_vetorial(v1, v2)
            }

            # Reta
            if operacao == 'reta':
                return jsonify({'resultado': equacao_reta((v1, v2))})

            # Plano
            if operacao == 'plano':
                return jsonify({'resultado': equacao_plano((v1, v2, v3))})

            # Restante
            resultado = funcoes[operacao]()
            return jsonify({'resultado': resultado})

        except Exception as e:
            return jsonify({'erro': f'Erro interno: {str(e)}'}), 400
