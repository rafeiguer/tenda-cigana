"""Contorno dos cavalos na vardo-cavalos-112.png (1536x640), medido à mão numa grade.
Usado por separar_cavalos.py (repinta a carroça sem eles) e por ../preparar_rodada7.py (monta a carroça com os
cavalos à frente dos varais e corta as pernas para balançarem)."""

# do alto da garupa, pela linha das costas e da crina, orelhas, cabeças, peito e chão
CAVALOS = [
    (694, 320), (706, 290), (760, 278), (850, 276), (930, 268), (985, 242), (1030, 208), (1080, 184), (1120, 164),
    (1160, 145), (1195, 135), (1208, 113), (1220, 128), (1236, 112), (1250, 135), (1262, 152), (1290, 186), (1335, 176),
    (1352, 160), (1368, 178), (1400, 210), (1414, 232), (1410, 300), (1400, 340), (1392, 362), (1360, 368),
    (1330, 380), (1320, 420), (1316, 470), (1320, 560), (1330, 610), (1300, 628), (1100, 640), (800, 636), (690, 630),
    (694, 520), (697, 440),
]
# a perna solta que a imagem pôs na frente da roda da carroça (não é de nenhum dos cavalos): sai junto
PERNA_SOLTA = [(548, 410), (606, 410), (612, 520), (640, 600), (640, 625), (570, 625), (548, 520)]

# faixas das pernas (x no chão) e a altura do pivô (ombro/quadril) de cada uma; fase do passo em trote
# (diagonais juntas: traseira do cavalo de perto com dianteira do de longe)
PERNAS = [
    {"x0": 684, "x1": 850, "pivo": (760, 430), "fase": 0.0},    # traseiras do cavalo de perto
    {"x0": 850, "x1": 975, "pivo": (900, 440), "fase": 0.5},    # traseiras do cavalo de longe
    {"x0": 975, "x1": 1135, "pivo": (1050, 450), "fase": 0.5},  # dianteiras do cavalo de perto
    {"x0": 1135, "x1": 1330, "pivo": (1230, 450), "fase": 0.0}, # dianteiras do cavalo de longe
]
CORTE_PERNAS = 455   # abaixo disto é perna; acima é corpo (o corpo cobre o topo das pernas até CORTE_PERNAS + 30)
