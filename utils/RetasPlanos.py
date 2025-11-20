# Funções que aceitam listas numéricas ou tuplas de listas
from utils.bibliotecaswm import vetorcadeia_para_vetornumerico, produto_vetorial, produto_escalar


def equacao_reta(pontos):
    # pontos: (P, Q) onde P e Q são listas numéricas
    P, Q = pontos
    # garante conversão para float
    P = [float(x) for x in P]
    Q = [float(x) for x in Q]
    v = [Q[i] - P[i] for i in range(len(P))]

    if len(P) == 2:
        a = -v[1]
        b = v[0]
        c = a * P[0] + b * P[1]
        geral = f"{a}x + {b}y = {c}"
        return {
            'vetorial': f"(x,y) = ({P[0]}, {P[1]}) + t({v[0]}, {v[1]})",
            'parametricas': [f"x = {P[0]} + {v[0]} t", f"y = {P[1]} + {v[1]} t"],
            'geral': geral,
            'latex': {
                'geral': geral.replace(' ', ''),
                'parametricas': [f"x = {P[0]} + {v[0]}t", f"y = {P[1]} + {v[1]}t"]
            }
        }
    else:
        return {'erro': 'Reta em R3 ainda não implementada.'}


def equacao_plano(pontos):
    P, Q, R = pontos
    P = [float(x) for x in P]
    Q = [float(x) for x in Q]
    R = [float(x) for x in R]

    v1 = [Q[i] - P[i] for i in range(3)]
    v2 = [R[i] - P[i] for i in range(3)]
    n = produto_vetorial(v1, v2)

    a, b, c = n
    d = a*P[0] + b*P[1] + c*P[2]

    equacao = f"{a}x + {b}y + {c}z = {d}"

    return {
        'vetores_contidos': [v1, v2],
        'vetor_normal': n,
        'equacao': equacao,
        'latex': equacao.replace(' ', '')
    }
