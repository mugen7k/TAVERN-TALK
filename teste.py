import ctypes
import os
import random
import sys

import pygame

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

LARGURA, ALTURA = 1920, 1080
FPS = 12
PASSO_FADE = 50
MS_ROLAGEM_DADOS = 1500
MS_RESULTADO_DADOS = 1500
MS_CENA_NARRATIVA = 1500
MS_CENA_RESULTADO_COMBATE = 2000
COMBATE_BOTOES_Y = ALTURA - 200
BOTAO_VOLTAR_TAM = 128
BOTAO_VOLTAR_MARGEM = 16
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
DOURADO = (218, 165, 32)
PAINEL_COR = (20, 15, 10, 220)
BOTAO_COR = (60, 45, 30)
BOTAO_HOVER = (90, 65, 40)
ERRO_COR = (200, 80, 80)
BANNER_COR = (0, 0, 0, 160)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE_DIR, "assets")
DICES_DIR = os.path.join(ASSETS, "DICES")


def jogador_inicial():
    return {"grana": 77, "mochila": [], "nome": ""}


COISAS_DO_BAR = [
    ("Hidromel do Vale", 5),
    ("Ensopado de raiz", 8),
    ("Pão de centeio", 2),
]

MAPINHA_DO_MOLEQUE = [
    ("Mapa das Ruínas de Ferro", 12),
    ("Mapa das Rotas do Sal", 6),
    ("Mapa rabiscado de uma caverna", 4),
]

TRALHA_DO_BRABO = [
    ("Dica: esconderijo na doca", 7),
    ("Faca de caça (usada)", 10),
]

ORIGENS = [
    "Montanhas Milenares",
    "Litoral Lamuriante",
    "Vale Venerável",
    "Cidade Cinzenta",
    "Lugar nenhum!",
]

FRASES_BEBADO = [
    '"Escuta aqui, meu chapa... o meu cavalo lá fora tem um motor 1.5 VTEC manual, tá duvidando? Hic... ele bebe bem menos que eu!"',
    '"O problema do mundo é que os elfos roubaram todo o nosso queijo... e o rei não faz nada a respeito..."',
    '"Eu levanto peso três vezes na semana inteirinha só pra ter força de conseguir... hic... levantar essa caneca de novo. Enche aí, chefia!"',
    '"Eu juro por todos os deuses, aquela cadeira ali no canto olhou pra mim torto. Ela sabe muito bem o que fez."',
    '"Se eu fechar os olhos e der um soco giratório agora mesmo, o vento da minha mão me leva voando direto pra minha cama."',
    '"Sabe qual é a grande verdade do universo? Hic... Se você plantar uma moeda de ouro num barril de cerveja, no mês que vem nasce uma árvore de canecas! Eu juro, um gnomo me contou..."',
    '"Garçom, traz mais uma rodada! E faz um brinde praquela parede ali no fundo... ela é a única nessa sala inteira que tá conseguindo ficar em pé sem se apoiar em nada hoje."',
]

ARQUIVOS_SPRITES = {
    "lobby": "lobby.png",
    "dialogo_candidus": "DIALOGO COM CANDIDUS.png",
    "dialogo_bardo": "DIALOGO COM O BARDO.png",
    "dialogo_bebado": "DIALOGO COM O BEBADO.png",
    "dialogo_viajante": "DIALOGO COM O VIAJANTE.png",
    "mesa_de_jogos": "MESA DE JOGOS.png",
    "dialogo_bandido": "DIALOGO COM O BANDIDO.png",
    "janela": "JANELA DA TAVERNA.png",
    "bebado_esbarra": "BEBADO ESBARRA EM VOCE.png",
    "combate_inicio": "COMBATE COM O BANDIDO.png",
    "combate_atk_player": "ATAQUE AO BANDIDO.png",
    "combate_atk_enemy": "ATAQUE DO BANDIDO.png",
    "combate_vitoria": "BANDIDO DERROTADO.png",
    "combate_derrota": "DERROTADO PELO BANDIDO 1.png",
}

ORIGEM_ARQUIVOS = {
    1: ["MONTANHAS MILENARES.png"],
    2: ["LITORAL LAMURIANTE.png"],
    3: ["VALE VENERAVEL.png", "VALE VENERÁVEL.png"],
    4: ["CIDADE CINZENTA.png"],
}

FASE_PARA_CENA = {
    "candidus_main": "dialogo_candidus",
    "candidus_shop": "dialogo_candidus",
    "viajante_main": "dialogo_viajante",
    "viajante_shop": "dialogo_viajante",
    "bardo_main": "dialogo_bardo",
    "bebado_main": "dialogo_bebado",
    "dados_main": "mesa_de_jogos",
    "dados_bet": "mesa_de_jogos",
    "dados_animacao": "mesa_de_jogos",
    "cacador_main": "dialogo_bandido",
    "cacador_shop": "dialogo_bandido",
}

CENAS_DIALOGUE_NPC = set(FASE_PARA_CENA.values())


def texto_grana(state):
    c = state["grana"]
    if c == 0:
        return "Não sobrou nada..."
    if c == 1:
        return "Você só tem mais uma moeda."
    return f"Você tem {c} moedas."


def texto_inventario(state):
    inv = state["mochila"]
    if not inv:
        return "Seu inventário está vazio."
    return "Itens:\n" + "\n".join(f"  - {i}" for i in inv)


class ControleJogo:
    def __init__(self):
        self.jogador = jogador_inicial()
        self.etapa = "intro_arrival"
        self.mensagens = []
        self.duelo = None
        self.resultado_turno = None
        self.resultado_dados = None

    def montar_interface(self):
        tela = {
            "textos": list(self.mensagens),
            "botoes": [],
            "pedir_texto": False,
            "dica_texto": "",
            "pedir_numero": None,
            "dica_numero": "",
            "no_salao": self.etapa == "lobby",
            "acabou": False,
        }
        fase = self.etapa

        if fase == "intro_arrival":
            if not tela["textos"]:
                tela["textos"] = [
                    "Você avista a fumaça da taverna de longe.",
                    "Um hidromel esquentaria bem essa noite fria.",
                ]
            tela["botoes"] = [("Continuar", "continuar")]

        elif fase == "intro_door":
            tela["botoes"] = [
                ("Entrar", "intro_door_enter"),
                ("Ver pela janela", "intro_door_window"),
            ]

        elif fase == "intro_bebado":
            if not tela["textos"]:
                tela["textos"] = [
                    "Você empurra a porta pesada. Uma onda de calor atinge seu corpo.",
                    "Um homem bêbado esbarra em você — ele nem pede desculpas.",
                ]
            tela["botoes"] = [("Continuar", "continuar")]

        elif fase == "intro_name":
            if not tela["textos"]:
                tela["textos"] = ['"Qual o seu nome?"', "Digite e pressione Enter:"]
            tela["pedir_texto"] = True
            tela["dica_texto"] = "Me chamo..."

        elif fase == "intro_window":
            tela["botoes"] = [("Voltar à porta", "intro_window_back")]

        elif fase == "intro_origin":
            tela["botoes"] = []

        elif fase == "intro_welcome":
            tela["botoes"] = [("Entrar no salão", "intro_to_lobby")]

        elif fase == "lobby":
            if not tela["textos"]:
                tela["textos"] = ["Clique nos personagens para interagir."]
            tela["botoes"] = [("Sair da taverna", "sair_taverna")]

        elif fase == "candidus_main":
            tela["botoes"] = [
                ("Cardápio", "candidus_shop"),
                ("Moedas", "candidus_grana"),
                ("Inventário", "candidus_inv"),
            ]

        elif fase == "candidus_shop":
            tela["botoes"] = [
                *[(f"{n} — {p} moedas", f"candidus_buy_{i}") for i, (n, p) in enumerate(COISAS_DO_BAR, 1)],
                ("Cancelar", "shop_cancel"),
            ]

        elif fase == "viajante_main":
            tela["botoes"] = [
                ("Mapas", "viajante_shop"),
                ("Boato grátis", "viajante_boato"),
            ]

        elif fase == "viajante_shop":
            tela["botoes"] = [
                *[(f"{n} — {p} moedas", f"viajante_buy_{i}") for i, (n, p) in enumerate(MAPINHA_DO_MOLEQUE, 1)],
                ("Cancelar", "shop_cancel"),
            ]

        elif fase == "bardo_main":
            tela["botoes"] = [
                ("Canção alegre (3)", "bardo_alegre"),
                ("Balada (2)", "bardo_sombria"),
                ("Ouvir grátis", "bardo_ouvir"),
            ]

        elif fase == "bebado_main":
            tela["botoes"] = [('"O quê?"', "bebado_oque"), ("Ignorar", "bebado_ignorar")]

        elif fase == "dados_main":
            tela["botoes"] = [
                ("Apostar", "dados_apostar"),
                ("Moedas", "dados_grana"),
            ]

        elif fase == "dados_bet":
            tela["pedir_numero"] = (1, self.jogador["grana"])
            tela["dica_numero"] = "Aposta:"

        elif fase == "dados_animacao":
            tela["botoes"] = []

        elif fase == "cacador_main":
            tela["botoes"] = [
                ("Ofertas", "cacador_shop"),
                ("Duelo", "cacador_combate"),
            ]

        elif fase == "cacador_shop":
            tela["botoes"] = [
                *[(f"{n} — {p} moedas", f"cacador_buy_{i}") for i, (n, p) in enumerate(TRALHA_DO_BRABO, 1)],
                ("Cancelar", "shop_cancel"),
            ]

        elif fase == "combat_intro":
            tela["botoes"] = []

        elif fase == "combat":
            tela["botoes"] = [
                ("Atacar (1–6 dano)", "combat_atacar"),
                ("Postura defensiva", "combat_defender"),
            ]

        elif fase == "combat_animacao":
            tela["botoes"] = []

        elif fase == "ended":
            tela["acabou"] = True

        return tela

    def executar_escolha(self, escolha):
        if escolha == "continuar":
            if self.etapa == "intro_arrival":
                self.mudar_fase("intro_door", ["Você chega à porta da taverna.", "O que você faz?"])
            elif self.etapa == "intro_bebado":
                self.mudar_fase(
                    "intro_name",
                    ['"Qual o seu nome, jovem?"', "Digite e pressione Enter:"],
                )
            return

        if escolha == "intro_door_enter":
            self.mudar_fase("intro_bebado", [])
        elif escolha == "intro_door_window":
            self.mudar_fase("intro_window", [])
        elif escolha == "intro_window_back":
            self.mudar_fase("intro_door", ["Você chega à porta da taverna.", "O que você faz?"])
        elif escolha == "origin_1":
            self.escolher_origem(1)
        elif escolha == "origin_2":
            self.escolher_origem(2)
        elif escolha == "origin_3":
            self.escolher_origem(3)
        elif escolha == "origin_4":
            self.escolher_origem(4)
        elif escolha == "origin_5":
            self.escolher_origem(5)
        elif escolha == "intro_to_lobby":
            self.mudar_fase("lobby", [])
        elif escolha == "sair_taverna":
            self.mudar_fase(
                "ended",
                ["Você atravessa a porta e enfrenta o frio da noite.", "Até a próxima!"],
            )
        elif escolha == "candidus_shop":
            self.mudar_fase("candidus_shop", ['"Eis o que temos hoje:"'])
        elif escolha == "candidus_grana":
            self.mensagens.append(texto_grana(self.jogador))
        elif escolha == "candidus_inv":
            self.mensagens.append(texto_inventario(self.jogador))
        elif escolha.startswith("candidus_buy_"):
            i = int(escolha.split("_")[-1])
            nome, preco = COISAS_DO_BAR[i - 1]
            self.comprar_item(nome, preco, "candidus")
        elif escolha == "viajante_shop":
            self.mudar_fase("viajante_shop", [])
        elif escolha == "viajante_boato":
            self.mensagens.append(
                '"Patrulhas reais dobraram na estrada leste. Cuidado ao amanhecer."'
            )
        elif escolha.startswith("viajante_buy_"):
            i = int(escolha.split("_")[-1])
            nome, preco = MAPINHA_DO_MOLEQUE[i - 1]
            self.comprar_item(nome, preco, "viajante")
        elif escolha == "bardo_alegre":
            self.pagar_musica_alegre()
        elif escolha == "bardo_sombria":
            self.pagar_musica_triste()
        elif escolha == "bardo_ouvir":
            self.mensagens.append("Você escuta um refrão distante.")
        elif escolha == "bebado_oque":
            self.mensagens.append('Você murmura: "O quê?"')
        elif escolha == "bebado_ignorar":
            self.enter_npc("lobby")
        elif escolha == "dados_apostar":
            self.comecar_aposta()
        elif escolha == "dados_grana":
            self.mensagens.append(texto_grana(self.jogador))
        elif escolha == "cacador_shop":
            self.mudar_fase("cacador_shop", [])
        elif escolha == "cacador_combate":
            self.comecar_duelo()
        elif escolha.startswith("cacador_buy_"):
            i = int(escolha.split("_")[-1])
            nome, preco = TRALHA_DO_BRABO[i - 1]
            self.comprar_item(nome, preco, "cacador")
        elif escolha == "combat_atacar":
            self.jogar_turno_duelo("1")
        elif escolha == "combat_defender":
            self.jogar_turno_duelo("2")
        elif escolha == "shop_cancel":
            self.cancelar_loja()
        else:
            self.mensagens.append("Não entendi essa escolha.")

    def submit_text(self, text):
        if self.etapa == "intro_name":
            self.jogador["nome"] = text.strip().title() or "Forasteiro"
            self.mudar_fase(
                "intro_origin",
                [f'"De que bandas você vem, {self.jogador["nome"]}?"'],
            )

    def submit_number(self, value):
        if self.etapa == "dados_bet":
            g = self.jogador["grana"]
            if not (1 <= value <= g):
                return f"Aposte entre 1 e {g} moedas."
            self.sortear_dados(value)
            return None
        return None

    def enter_npc(self, npc):
        self.duelo = None
        if npc == "lobby":
            self.etapa = "lobby"
            self.mensagens = []
            return
        intros = {
            "candidus": ("candidus_main", ["Candidus limpa um copo.", '"Quer gastar suas moedas?"']),
            "viajante": ("viajante_main", ['"Mapas confiáveis — ou quase."']),
            "bardo": ("bardo_main", ['"Uma canção aquece a alma — ou esvazia a bolsa."']),
            "bebado": ("bebado_main", self.fala_bebado()),
            "dados": ("dados_main", ['"Quer tentar a sorte nos dados?"']),
            "cacador": (
                "cacador_main",
                ['"Posso vender informação... ou te arrumar problema."'],
            ),
        }
        etapa, textos = intros[npc]
        self.mudar_fase(etapa, textos)

    def mudar_fase(self, etapa, textos):
        self.etapa = etapa
        self.mensagens = list(textos)

    def escolher_origem(self, n):
        if n in (1, 3):
            r = '"Ha, já imaginava. Essa cara de bebê não engana ninguém! Haha!"'
        elif n in (2, 4):
            r = '"Hmm, relatos sombrios dessas bandas..."'
        else:
            r = '"Ahh, vai ser assim então. Ok."'
        nm = self.jogador["nome"]
        self.mudar_fase(
            "intro_welcome",
            [
                r,
                f'"Me chamo Candidus, sou dono deste estabelecimento. Não me cause problemas aqui, {nm},',
                'senão irá conhecer meu lado não tão receptivo."',
                '"Clique nos personagens para interagir."',
            ],
        )

    def comprar_item(self, nome, preco, ctx):
        if self.jogador["grana"] < preco:
            msgs = {
                "candidus": '"Moedas não bastam."',
                "viajante": '"Sem moedas, sem mapa."',
                "cacador": '"Moedas curtas."',
            }
            self.mensagens.append(msgs[ctx])
            return
        self.jogador["grana"] -= preco
        self.jogador["mochila"].append(nome)
        self.mensagens.append(f"Você guarda: {nome}.")

    def cancelar_loja(self):
        m = {
            "candidus_shop": "candidus",
            "viajante_shop": "viajante",
            "cacador_shop": "cacador",
        }
        if self.etapa in m:
            self.enter_npc(m[self.etapa])

    def pagar_musica_alegre(self):
        if self.jogador["grana"] < 3:
            self.mensagens.append('"Moedas faltando..."')
        else:
            self.jogador["grana"] -= 3
            self.mensagens.append("Melodia saltitante — o mundo parece mais leve.")

    def pagar_musica_triste(self):
        if self.jogador["grana"] < 2:
            self.mensagens.append('"Sem gorjeta, sem sombras cantadas."')
        else:
            self.jogador["grana"] -= 2
            self.mensagens.append("A voz desce como névoa.")

    def comecar_aposta(self):
        if self.jogador["grana"] < 1:
            self.mensagens.append('"Sem dinheiro, zé ruela!"')
            return
        self.mudar_fase("dados_bet", [f'"Quanto aposta?" (máx. {self.jogador["grana"]})'])

    def sortear_dados(self, aposta):
        d1, d2 = random.randint(1, 6), random.randint(1, 6)
        d3, d4 = random.randint(1, 6), random.randint(3, 6)
        self.resultado_dados = {
            "aposta": aposta,
            "player": (d1, d2),
            "npc": (d3, d4),
        }
        self.etapa = "dados_animacao"
        self.mensagens = []

    def finalizar_animacao_dados(self):
        if not self.resultado_dados:
            return
        aposta = self.resultado_dados["aposta"]
        d1, d2 = self.resultado_dados["player"]
        d3, d4 = self.resultado_dados["npc"]
        sp, sn = d1 + d2, d3 + d4
        linhas = []
        if aposta == self.jogador["grana"]:
            linhas.append('"Tudo isso?!"')
        linhas.append(f"Você tirou {d1} e {d2}. A soma é {sp}.")
        linhas.append(f"O estranho tirou {d3} e {d4}. A soma é {sn}.")
        if sn > sp:
            self.jogador["grana"] -= aposta
            linhas.append('"Hahaha, talvez você tenha mais sorte da próxima vez"')
            linhas.append(f"Você perdeu {aposta} moedas.")
        elif sn < sp:
            self.jogador["grana"] += aposta
            linhas.append('"Você está com sorte, jovem"')
            linhas.append(f"Você ganhou {aposta} moedas.")
        else:
            linhas.append('"Olha! Parece que empatamos."')
        self.resultado_dados = None
        self.mudar_fase("dados_main", linhas)

    def comecar_duelo(self):
        self.duelo = {"player_hp": 16, "enemy_hp": 12}
        self.resultado_turno = None
        self.etapa = "combat_intro"
        self.mensagens = []

    def finalizar_intro_combate(self):
        if not self.duelo:
            return
        ph, eh = self.duelo["player_hp"], self.duelo["enemy_hp"]
        self.etapa = "combat"
        self.mensagens = [
            "Um sujeito largo cutuca sua cadeira.",
            '"Esse lugar é apertado demais pra dois heróis", rosna ele.',
            f"Seu vigor: {ph} | Bandido: {eh}",
        ]

    def jogar_turno_duelo(self, acao):
        if not self.duelo:
            return
        ph, eh = self.duelo["player_hp"], self.duelo["enemy_hp"]
        linhas = []
        if acao == "1":
            d = random.randint(1, 6)
            eh -= d
            linhas.append(f"Você acerta um golpe por {d} de dano.")
        elif acao == "2":
            d = random.randint(1, 3)
            eh -= d
            linhas.append(f"Você avança com cautela, causando {d} de dano.")
        else:
            linhas.append("Hesitação custa cara: você tropeça e erra o timing.")

        self.duelo["enemy_hp"] = max(eh, 0)
        ended = eh <= 0
        victory = False
        multa = 0

        if not ended:
            if acao == "1":
                di = random.randint(1, 6)
            elif acao == "2":
                di = random.randint(0, 3)
            else:
                di = random.randint(2, 5)
            ph -= di
            self.duelo["player_hp"] = max(ph, 0)
            linhas.append(
                f"O bandido revida com {di} de dano. "
                f"Seu vigor: {max(ph, 0)} | Bandido: {max(eh, 0)}"
            )
            if ph <= 0:
                ended = True
                multa = min(8, self.jogador["grana"])
                linhas.append(
                    "Você apaga no chão da taverna. O caçador puxa você pelo colarinho a tempo."
                )
                linhas.append(f"Você perde {multa} moedas (ou o que tinha).")
        else:
            linhas.append(
                "O bandido cai. O caçador acena com aprovação. Você encontra 15 moedas na bolsa dele."
            )
            victory = True

        self.resultado_turno = {
            "linhas": linhas,
            "ended": ended,
            "victory": victory,
            "multa": multa,
        }
        self.etapa = "combat_animacao"

    def finalizar_animacao_combate(self):
        r = self.resultado_turno
        if not r:
            return
        if r["ended"]:
            if r["victory"]:
                self.jogador["grana"] += 15
            else:
                self.jogador["grana"] -= r["multa"]
            self.duelo = None
            self.resultado_turno = None
            self.enter_npc("cacador")
            self.mensagens = r["linhas"]
        else:
            self.resultado_turno = None
            self.etapa = "combat"
            self.mensagens = r["linhas"]

    def fala_bebado(self):
        nome = self.jogador["nome"]
        todas = FRASES_BEBADO + [
            f'"Ouça {nome}, quem tem um porquê suporta quase qualquer como."',
            f'"Ouça {nome}, importa como você reage."',
            f'"Ouça {nome}, age como lei universal."',
        ]
        return ["O bêbado diz:", random.choice(todas)]


def rodar_modo_console():
    controle = ControleJogo()
    while not controle.montar_interface()["acabou"]:
        tela = controle.montar_interface()
        for ln in tela["textos"]:
            print(ln)
        if tela["textos"]:
            print()
        if tela["pedir_texto"]:
            controle.submit_text(input(f'{tela["dica_texto"]} '))
            continue
        if tela["pedir_numero"]:
            mn, mx = tela["pedir_numero"]
            while True:
                try:
                    n = int(input(f'{tela["dica_numero"]} ({mn}-{mx}): '))
                except ValueError:
                    print("Número inválido.")
                    continue
                err = controle.submit_number(n)
                if err:
                    print(err)
                else:
                    break
            continue
        if tela["no_salao"]:
            print("1=Candidus 2=Viajante 3=Bêbado 4=Bardo 5=Dados 6=Caçador 7=Sair")
            m = {"1": "candidus", "2": "viajante", "3": "bebado", "4": "bardo", "5": "dados", "6": "cacador"}
            e = input("> ").strip()
            if e == "7":
                controle.executar_escolha("sair_taverna")
            elif e in m:
                controle.enter_npc(m[e])
            continue
        if controle.etapa == "intro_origin":
            for i, o in enumerate(ORIGENS, 1):
                print(f"{i} = {o}")
            try:
                idx = int(input("> ").strip())
                if 1 <= idx <= 5:
                    controle.executar_escolha(f"origin_{idx}")
            except ValueError:
                print("Opção inválida.")
            continue
        if not tela["botoes"]:
            if controle.etapa.startswith("intro"):
                controle.executar_escolha("continuar")
            continue
        for i, (lb, _) in enumerate(tela["botoes"], 1):
            print(f"{i} = {lb}")
        try:
            idx = int(input("> ")) - 1
            if 0 <= idx < len(tela["botoes"]):
                controle.executar_escolha(tela["botoes"][idx][1])
        except ValueError:
            print("Opção inválida.")


def carregar_asset(nome_arquivo):
    caminho = os.path.join(ASSETS, nome_arquivo)
    return pygame.image.load(caminho).convert_alpha()


def carregar_asset_opcional(nomes):
    for nome in nomes:
        caminho = os.path.join(ASSETS, nome)
        if os.path.isfile(caminho):
            return pygame.image.load(caminho).convert_alpha()
    return None


EXTENSOES_AUDIO = (".mp3", ".ogg", ".wav", ".mpeg", ".mpga", ".flac")
VOLUME_MUSICA = 0.4
VOLUME_SFX = min(1.1, 1.33)

SONS_DIR = os.path.join(ASSETS, "sons")

ARQUIVOS_SOM = {
    "porta": "PORTA ABRINDO.wav",
    "candidus": "FALA CANDIDUS.wav",
    "viajante": "FALA VIAJANTE.wav",
    "bardo": "FALA BARDO.wav",
    "bebado": "FALA BEBADO.wav",
    "dados": "FALA MESA DE JOGOS.wav",
    "bandido": "FALA BANDIDO.wav",
    "moeda": "MOEDA.wav",
    "interacao": "INTERAÇÃO.wav",
    "espada": "BARULHO ESPADA BATENDO.wav",
    "vitoria": "BANDIDO DERROTADO.wav",
}

SOM_NPC = {
    "candidus": "candidus",
    "viajante": "viajante",
    "bardo": "bardo",
    "bebado": "bebado",
    "dados": "dados",
    "cacador": "bandido",
}


def preparar_audio():
    if not pygame.mixer.get_init():
        pygame.mixer.init()


def caminho_musica_fundo():
    for nome in sorted(os.listdir(ASSETS)):
        caminho = os.path.join(ASSETS, nome)
        if os.path.isfile(caminho) and nome.lower().endswith(EXTENSOES_AUDIO):
            return caminho
    return None


def iniciar_musica_fundo():
    caminho = caminho_musica_fundo()
    if not caminho:
        return
    try:
        preparar_audio()
        pygame.mixer.music.load(caminho)
        pygame.mixer.music.set_volume(VOLUME_MUSICA)
        pygame.mixer.music.play(-1)
    except pygame.error:
        pass


def parar_musica_fundo():
    if pygame.mixer.get_init():
        pygame.mixer.music.stop()


def carregar_efeitos():
    preparar_audio()
    cache = {}
    for chave, arquivo in ARQUIVOS_SOM.items():
        caminho = os.path.join(SONS_DIR, arquivo)
        if not os.path.isfile(caminho):
            continue
        try:
            som = pygame.mixer.Sound(caminho)
            som.set_volume(VOLUME_SFX)
            cache[chave] = som
        except pygame.error:
            pass
    return cache


def tocar_efeito(efeitos, chave):
    som = efeitos.get(chave)
    if som:
        som.play()


def escalar_tela_cheia(imagem):
    if imagem.get_size() == (LARGURA, ALTURA):
        return imagem
    return pygame.transform.smoothscale(imagem, (LARGURA, ALTURA))


def criar_card_lugar_nenhum(largura, altura, fonte):
    card = pygame.Surface((largura, altura))
    card.fill((8, 6, 5))
    pygame.draw.rect(card, (45, 40, 35), card.get_rect(), 3, border_radius=8)
    linha1 = fonte.render("Lugar", True, BRANCO)
    linha2 = fonte.render("nenhum", True, BRANCO)
    cx = largura // 2
    cy = altura // 2
    card.blit(linha1, (cx - linha1.get_width() // 2, cy - linha1.get_height() - 4))
    card.blit(linha2, (cx - linha2.get_width() // 2, cy + 4))
    return card.convert_alpha()


def escalar_caber(imagem, largura, altura):
    w, h = imagem.get_size()
    escala = min(largura / w, altura / h)
    nw, nh = max(1, int(w * escala)), max(1, int(h * escala))
    return pygame.transform.smoothscale(imagem, (nw, nh))


def carregar_sprites_dados():
    rolling_path = os.path.join(DICES_DIR, "DADOS ROLANDO.png")
    rolling = pygame.image.load(rolling_path).convert_alpha()
    rolling = escalar_caber(rolling, int(LARGURA), int(ALTURA))

    cache = {}
    for a in range(1, 7):
        for b in range(a, 7):
            nome = f"DADOS {a} E {b}.png"
            caminho = os.path.join(DICES_DIR, nome)
            if os.path.isfile(caminho):
                img = pygame.image.load(caminho).convert_alpha()
                cache[(a, b)] = escalar_caber(img, int(LARGURA), int(ALTURA))

    return rolling, cache


def executar_fade_out(tela, relogio, desenhar, fps=FPS):
    fade = pygame.Surface(tela.get_size())
    fade.fill(PRETO)
    for alpha in range(0, 255, PASSO_FADE):
        desenhar()
        fade.set_alpha(alpha)
        tela.blit(fade, (0, 0))
        pygame.display.flip()
        relogio.tick(fps)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                return False
    return True


def executar_fade_in(tela, relogio, desenhar, fps=FPS):
    fade = pygame.Surface(tela.get_size())
    fade.fill(PRETO)
    for alpha in range(255, 0, -PASSO_FADE):
        desenhar()
        fade.set_alpha(alpha)
        tela.blit(fade, (0, 0))
        pygame.display.flip()
        relogio.tick(fps)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                return False
    return True


class JanelaJogo:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption("Tavern Talk")
        self.relogio = pygame.time.Clock()
        self.fonte = pygame.font.SysFont("Courier", 28)
        self.fonte_btn = pygame.font.SysFont("Courier", 22)
        self.fonte_hud = pygame.font.SysFont("Courier", 32, bold=True)
        self.fonte_titulo = pygame.font.SysFont("Courier", 34, bold=True)

        telas_cheias = {
            "bebado_esbarra",
            "combate_inicio",
            "combate_atk_player",
            "combate_atk_enemy",
            "combate_vitoria",
            "combate_derrota",
            "janela",
        }
        self.sprites = {}
        for chave, arquivo in ARQUIVOS_SPRITES.items():
            img = carregar_asset(arquivo)
            if chave in telas_cheias:
                img = escalar_tela_cheia(img)
            self.sprites[chave] = img

        self.sprite_voltar = carregar_asset("BACKBUTTON.png")
        self.dado_rolando, self.sprites_dados = carregar_sprites_dados()
        self.animacao = None

        self.sprites_origem = {}
        self.rects_origem = {}
        self.montar_cartoes_origem()

        self.controle = ControleJogo()
        self.cena_atual = "intro"
        self.botoes_ui = []
        self.input_buffer = ""
        self.erro_input = ""
        self.rodando = True

        self.hotspots = {
            "candidus": pygame.Rect(760, 215, 360, 380),
            "bardo": pygame.Rect(128, 630, 250, 250),
            "viajante": pygame.Rect(475, 450, 200, 200),
            "bebado": pygame.Rect(590, 630, 240, 240),
            "dados": pygame.Rect(820, 860, 450, 220),
            "cacador": pygame.Rect(1340, 520, 260, 280),
        }
        self.botao_voltar = pygame.Rect(0, 0, BOTAO_VOLTAR_TAM, BOTAO_VOLTAR_TAM)
        iniciar_musica_fundo()
        self.sons = carregar_efeitos()

    def tocar(self, chave):
        tocar_efeito(self.sons, chave)

    def em_animacao(self):
        return self.animacao is not None

    def mostra_botao_voltar_lobby(self):
        if self.cena_atual == "lobby":
            return False
        if self.em_combate() or self.em_animacao():
            return False
        if self.cena_atual in ("intro", "bebado_esbarra", "janela", "origem_select", "combate_inicio"):
            return False
        if self.controle.etapa.startswith("intro"):
            return False
        return self.cena_atual in CENAS_DIALOGUE_NPC

    def calcular_metricas_painel(self, tela):
        if not (tela["textos"] or tela["botoes"] or tela["pedir_texto"] or tela["pedir_numero"]):
            return None
        linhas_txt = self.coletar_linhas_texto(tela)
        n_btn = len(tela["botoes"])
        colunas = 2 if n_btn > 3 else 1
        linhas_btn = (n_btn + colunas - 1) // colunas if n_btn else 0
        altura_texto = len(linhas_txt) * 28 + (16 if linhas_txt else 0)
        altura_botoes = linhas_btn * 52 + (12 if linhas_btn else 0)
        altura_input = 44 if (tela["pedir_texto"] or tela["pedir_numero"] or self.erro_input) else 0
        altura_painel = min(400, 28 + altura_texto + altura_botoes + altura_input)
        painel_y = ALTURA - altura_painel
        return painel_y, altura_painel

    def desenhar_botao_voltar(self, painel_y):
        if not self.mostra_botao_voltar_lobby():
            return
        x = LARGURA - BOTAO_VOLTAR_TAM - 48
        y = painel_y - BOTAO_VOLTAR_TAM - BOTAO_VOLTAR_MARGEM
        self.botao_voltar = pygame.Rect(x, y, BOTAO_VOLTAR_TAM, BOTAO_VOLTAR_TAM)
        self.tela.blit(self.sprite_voltar, self.botao_voltar.topleft)

    def montar_cartoes_origem(self):
        slot_larg, slot_alt = 340, 520
        espaco = 24
        total_larg = 5 * slot_larg + 4 * espaco
        x0 = (LARGURA - total_larg) // 2
        y_slot = 200

        for i in range(1, 6):
            if i == 5:
                img = criar_card_lugar_nenhum(slot_larg, slot_alt, self.fonte_titulo)
            else:
                img = carregar_asset_opcional(ORIGEM_ARQUIVOS[i])
                if img is None:
                    continue
                img = escalar_caber(img, slot_larg, slot_alt)
            self.sprites_origem[i] = img
            sw, sh = self.sprites_origem[i].get_size()
            x = x0 + (i - 1) * (slot_larg + espaco) + (slot_larg - sw) // 2
            y = y_slot + (slot_alt - sh) // 2
            self.rects_origem[i] = pygame.Rect(x, y, sw, sh)

    def fase_para_cena(self):
        fase = self.controle.etapa
        if fase == "intro_window":
            return "janela"
        if fase == "intro_origin":
            return "origem_select"
        if fase in ("intro_name", "intro_welcome"):
            return "dialogo_candidus"
        if fase == "intro_bebado":
            return "bebado_esbarra"
        if fase in ("combat_intro", "combat", "combat_animacao"):
            return "combate_inicio"
        if fase == "lobby":
            return "lobby"
        if fase.startswith("intro") or fase == "ended":
            return "intro"
        return FASE_PARA_CENA.get(fase, "lobby")

    def em_combate(self):
        return self.controle.etapa in ("combat_intro", "combat", "combat_animacao")

    def blit_tela_cheia(self, chave_sprite):
        self.tela.blit(self.sprites[chave_sprite], (0, 0))

    def sprite_par_dados(self, d1, d2):
        chave = (min(d1, d2), max(d1, d2))
        if chave in self.sprites_dados:
            return self.sprites_dados[chave]
        surf = pygame.Surface((400, 200))
        surf.fill((40, 80, 40))
        txt = self.fonte_titulo.render(f"Dados {d1} + {d2}", True, BRANCO)
        surf.blit(txt, (surf.get_width() // 2 - txt.get_width() // 2, 80))
        return surf

    def blit_centro(self, superficie):
        x = (LARGURA - superficie.get_width()) // 2
        y = (ALTURA - superficie.get_height()) // 2 - 40
        self.tela.blit(superficie, (x, y))

    def desenhar_overlay_animacao(self):
        if not self.animacao or self.animacao["modo"] != "dados":
            return
        etapa = self.animacao["etapa"]
        if etapa["tipo"] == "rolling":
            self.blit_centro(self.dado_rolando)
        elif etapa["tipo"] == "result":
            quem, d1, d2 = etapa["quem"], etapa["d1"], etapa["d2"]
            self.blit_centro(self.sprite_par_dados(d1, d2))
            rotulo = "Sua jogada" if quem == "player" else "Jogada do estranho"
            txt = self.fonte_titulo.render(rotulo, True, DOURADO)
            self.tela.blit(txt, (LARGURA // 2 - txt.get_width() // 2, 40))

    def desenhar_hover_retangulo(self, rect):
        brilho = pygame.Surface(rect.size, pygame.SRCALPHA)
        brilho.fill((255, 220, 120, 55))
        self.tela.blit(brilho, rect.topleft)
        pygame.draw.rect(self.tela, DOURADO, rect, 4, border_radius=6)

    def desenhar_hover_lobby(self):
        if self.controle.etapa != "lobby":
            return
        mouse = pygame.mouse.get_pos()
        for rect in self.hotspots.values():
            if rect.collidepoint(mouse):
                self.desenhar_hover_retangulo(rect)

    def desenhar_cena_base(self):
        self.tela.fill(PRETO)

        if self.animacao and self.animacao["modo"] == "sprites":
            etapa = self.animacao.get("etapa", {})
            chave = etapa.get("sprite_key", "combate_inicio")
            if chave in self.sprites:
                self.blit_tela_cheia(chave)
            return

        if self.cena_atual == "intro":
            return

        if self.cena_atual in ("janela", "bebado_esbarra", "combate_inicio"):
            self.blit_tela_cheia(self.cena_atual)
            return

        if self.cena_atual == "origem_select":
            self.tela.blit(self.sprites["dialogo_candidus"], (0, 0))
            mouse = pygame.mouse.get_pos()
            for i, img in self.sprites_origem.items():
                rect = self.rects_origem[i]
                if rect.collidepoint(mouse):
                    brilho = pygame.Surface(rect.size, pygame.SRCALPHA)
                    brilho.fill((255, 220, 120, 50))
                    self.tela.blit(img, rect.topleft)
                    self.tela.blit(brilho, rect.topleft)
                    pygame.draw.rect(self.tela, DOURADO, rect, 3, border_radius=4)
                else:
                    self.tela.blit(img, rect.topleft)
            return

        self.tela.blit(self.sprites[self.cena_atual], (0, 0))
        if self.cena_atual == "lobby":
            self.desenhar_hover_lobby()
        self.desenhar_overlay_animacao()

    def desenhar_banner_superior(self, linhas):
        if not linhas:
            return
        banner = pygame.Surface((LARGURA, 110), pygame.SRCALPHA)
        banner.fill(BANNER_COR)
        self.tela.blit(banner, (0, 0))
        y = 14
        for linha in linhas[:3]:
            txt = self.fonte_titulo.render(linha, True, DOURADO)
            self.tela.blit(txt, (40, y))
            y += 34

    def desenhar_hud(self):
        if self.controle.etapa.startswith("intro") and not self.controle.jogador["nome"]:
            return
        st = self.controle.jogador
        nome = st["nome"] or "Forasteiro"
        txt = self.fonte_hud.render(f"{nome}  |  {st['grana']} moedas", True, DOURADO)
        self.tela.blit(txt, (20, 120 if self.cena_atual == "origem_select" else 16))

    def quebrar_texto(self, texto, largura):
        palavras, linhas, atual = texto.split(), [], ""
        for p in palavras:
            t = f"{atual} {p}".strip()
            if self.fonte.size(t)[0] <= largura:
                atual = t
            else:
                if atual:
                    linhas.append(atual)
                atual = p
        if atual:
            linhas.append(atual)
        return linhas or [""]

    def coletar_linhas_texto(self, tela, max_linhas=5):
        linhas = []
        for linha in tela["textos"][-max_linhas:]:
            linhas.extend(self.quebrar_texto(linha, LARGURA - 100))
        return linhas[:max_linhas]

    def montar_botoes(self, tela, y_inicio):
        self.botoes_ui.clear()
        if not tela["botoes"]:
            return
        largura_btn = 340
        altura_btn = 42
        colunas = 2 if len(tela["botoes"]) > 3 else 1
        for i, (rotulo, aid) in enumerate(tela["botoes"]):
            col = i % colunas
            linha = i // colunas
            x = 50 + col * (largura_btn + 20)
            y = y_inicio + linha * (altura_btn + 10)
            rect = pygame.Rect(x, y, largura_btn, altura_btn)
            self.botoes_ui.append((rect, rotulo, aid))

    def desenhar_botoes_na_tela(self, truncar=False):
        mouse = pygame.mouse.get_pos()
        for rect, rotulo, _aid in self.botoes_ui:
            cor = BOTAO_HOVER if rect.collidepoint(mouse) else BOTAO_COR
            pygame.draw.rect(self.tela, cor, rect, border_radius=6)
            pygame.draw.rect(self.tela, DOURADO, rect, 2, border_radius=6)
            texto = rotulo[:38] if truncar else rotulo
            t = self.fonte_btn.render(texto, True, BRANCO)
            self.tela.blit(
                t,
                (rect.centerx - t.get_width() // 2, rect.centery - t.get_height() // 2),
            )

    def desenhar_painel(self):
        tela = self.controle.montar_interface()

        if self.em_animacao():
            return

        if self.em_combate():
            self.montar_botoes(tela, COMBATE_BOTOES_Y)
            self.desenhar_botoes_na_tela()
            if tela["textos"]:
                self.desenhar_banner_superior(tela["textos"][-4:])
            return

        if self.cena_atual in ("bebado_esbarra", "combate_inicio"):
            self.montar_botoes(tela, ALTURA - 70)
            self.desenhar_botoes_na_tela()
            if tela["textos"]:
                self.desenhar_banner_superior(tela["textos"][-4:])
            return

        if self.cena_atual == "origem_select":
            self.desenhar_banner_superior(tela["textos"])
            return

        if self.cena_atual == "janela":
            self.montar_botoes(tela, ALTURA - 70)
            self.desenhar_botoes_na_tela()
            return

        metricas = self.calcular_metricas_painel(tela)
        if metricas is None:
            return
        painel_y, altura_painel = metricas
        linhas_txt = self.coletar_linhas_texto(tela)

        painel = pygame.Surface((LARGURA, altura_painel), pygame.SRCALPHA)
        painel.fill(PAINEL_COR)
        self.tela.blit(painel, (0, painel_y))

        y = painel_y + 16
        for sub in linhas_txt:
            self.tela.blit(self.fonte.render(sub, True, BRANCO), (50, y))
            y += 28

        y_botoes = y + 8 if linhas_txt else painel_y + 16
        self.montar_botoes(tela, y_botoes)

        if tela["pedir_texto"]:
            p = f'{tela["dica_texto"]} {self.input_buffer}_'
            self.tela.blit(self.fonte.render(p, True, DOURADO), (50, painel_y + altura_painel - 50))
        elif tela["pedir_numero"]:
            mn, mx = tela["pedir_numero"]
            p = f'{tela["dica_numero"]} ({mn}-{mx}): {self.input_buffer}_'
            self.tela.blit(self.fonte.render(p, True, DOURADO), (50, painel_y + altura_painel - 50))

        if self.erro_input:
            self.tela.blit(
                self.fonte_btn.render(self.erro_input, True, ERRO_COR),
                (50, painel_y + altura_painel - 28),
            )

        self.desenhar_botoes_na_tela(truncar=True)
        self.desenhar_botao_voltar(painel_y)

    def desenhar_tudo(self):
        self.desenhar_cena_base()
        self.desenhar_hud()
        self.desenhar_painel()

    def trocar_cena(self, nova):
        if nova == self.cena_atual:
            return True
        if not executar_fade_out(self.tela, self.relogio, self.desenhar_tudo):
            return False
        self.cena_atual = nova
        if nova == "dialogo_candidus" and self.controle.etapa in (
            "intro_name",
            "intro_origin",
            "intro_welcome",
        ):
            self.tocar("candidus")
        return executar_fade_in(self.tela, self.relogio, self.desenhar_tudo)

    def sincronizar_cena(self):
        nova = self.fase_para_cena()
        if nova != self.cena_atual:
            self.trocar_cena(nova)

    def iniciar_animacao(self, modo, etapas, ao_fim=None):
        self.animacao = {
            "modo": modo,
            "indice": 0,
            "inicio_etapa": pygame.time.get_ticks(),
            "etapas": etapas,
            "etapa": etapas[0],
            "ao_fim": ao_fim,
        }

    def iniciar_intro_combate(self):
        self.cena_atual = "combate_inicio"
        self.iniciar_animacao(
            "sprites",
            [{"sprite_key": "combate_inicio", "duracao": MS_CENA_NARRATIVA}],
            "intro_combate",
        )

    def iniciar_animacao_turno_combate(self):
        r = self.controle.resultado_turno
        if not r:
            return
        etapas = [
            {"sprite_key": "combate_atk_player", "duracao": MS_CENA_NARRATIVA},
            {"sprite_key": "combate_atk_enemy", "duracao": MS_CENA_NARRATIVA},
        ]
        if r["ended"]:
            if r["victory"]:
                etapas.append(
                    {"sprite_key": "combate_vitoria", "duracao": MS_CENA_RESULTADO_COMBATE}
                )
            else:
                etapas.append(
                    {"sprite_key": "combate_derrota", "duracao": MS_CENA_RESULTADO_COMBATE}
                )
        self.cena_atual = "combate_inicio"
        self.tocar("espada")
        if r["ended"] and r["victory"]:
            self.tocar("vitoria")
        self.iniciar_animacao("sprites", etapas, "turno_combate")

    def iniciar_animacao_dados(self):
        dr = self.controle.resultado_dados
        if not dr:
            return
        d1, d2 = dr["player"]
        d3, d4 = dr["npc"]
        etapas = [
            {"tipo": "rolling", "duracao": MS_ROLAGEM_DADOS},
            {"tipo": "result", "quem": "player", "d1": d1, "d2": d2, "duracao": MS_RESULTADO_DADOS},
            {"tipo": "rolling", "duracao": MS_ROLAGEM_DADOS},
            {"tipo": "result", "quem": "npc", "d1": d3, "d2": d4, "duracao": MS_RESULTADO_DADOS},
        ]
        self.cena_atual = "mesa_de_jogos"
        self.iniciar_animacao("dados", etapas)

    def atualizar_animacao(self):
        if not self.animacao:
            return False
        agora = pygame.time.get_ticks()
        etapas = self.animacao["etapas"]
        idx = self.animacao["indice"]
        if idx >= len(etapas):
            return False
        etapa = etapas[idx]
        self.animacao["etapa"] = etapa
        if agora - self.animacao["inicio_etapa"] < etapa["duracao"]:
            return True
        self.animacao["indice"] += 1
        self.animacao["inicio_etapa"] = agora
        if self.animacao["indice"] >= len(etapas):
            modo = self.animacao["modo"]
            ao_fim = self.animacao.get("ao_fim")
            self.animacao = None
            if modo == "dados":
                grana_antes = self.controle.jogador["grana"]
                self.controle.finalizar_animacao_dados()
                if self.controle.jogador["grana"] != grana_antes:
                    self.tocar("moeda")
            elif ao_fim == "intro_combate":
                self.controle.finalizar_intro_combate()
            elif ao_fim == "turno_combate":
                grana_antes = self.controle.jogador["grana"]
                self.controle.finalizar_animacao_combate()
                if self.controle.jogador["grana"] > grana_antes:
                    self.tocar("moeda")
                self.sincronizar_cena()
            return False
        return True

    def acao(self, escolha):
        self.erro_input = ""
        grana_antes = self.controle.jogador["grana"]
        self.controle.executar_escolha(escolha)
        self.input_buffer = ""
        tocou = False
        if escolha == "intro_door_enter":
            self.tocar("porta")
            tocou = True
        elif escolha == "cacador_combate":
            self.tocar("bandido")
            tocou = True
        elif escolha in ("bardo_alegre", "bardo_sombria"):
            if self.controle.jogador["grana"] < grana_antes:
                self.tocar("moeda")
            tocou = True
        elif "_buy_" in escolha:
            if self.controle.mensagens and "Você guarda" in self.controle.mensagens[-1]:
                self.tocar("moeda")
            tocou = True
        if self.controle.etapa == "combat_intro":
            self.iniciar_intro_combate()
            tocou = True
        elif self.controle.etapa == "combat_animacao":
            self.iniciar_animacao_turno_combate()
            tocou = True
        else:
            self.sincronizar_cena()
        if not tocou:
            self.tocar("interacao")

    def enter_texto(self):
        tela = self.controle.montar_interface()
        if tela["pedir_texto"]:
            self.controle.submit_text(self.input_buffer)
            self.input_buffer = ""
            self.sincronizar_cena()
        elif tela["pedir_numero"]:
            try:
                v = int(self.input_buffer)
            except ValueError:
                self.erro_input = "Digite um número inteiro."
                return
            err = self.controle.submit_number(v)
            if err:
                self.erro_input = err
            else:
                self.input_buffer = ""
                self.erro_input = ""
                if self.controle.etapa == "dados_animacao":
                    self.iniciar_animacao_dados()
                else:
                    self.sincronizar_cena()

    def ir_npc(self, npc):
        self.controle.enter_npc(npc)
        self.input_buffer = ""
        self.erro_input = ""
        if npc != "lobby" and npc in SOM_NPC:
            self.tocar(SOM_NPC[npc])
        self.sincronizar_cena()

    def voltar_lobby(self):
        if self.em_combate() or self.em_animacao():
            return
        self.controle.enter_npc("lobby")
        self.input_buffer = ""
        self.erro_input = ""
        self.tocar("interacao")
        self.sincronizar_cena()

    def clique_origem(self, pos):
        for i, rect in self.rects_origem.items():
            if rect.collidepoint(pos):
                self.acao(f"origin_{i}")
                return True
        return False

    def processar_clique(self, pos):
        if self.em_animacao():
            return False

        if self.cena_atual == "origem_select":
            return self.clique_origem(pos)

        if self.cena_atual == "lobby" and self.controle.etapa == "lobby":
            for npc, rect in self.hotspots.items():
                if rect.collidepoint(pos):
                    self.ir_npc(npc)
                    return True
            for rect, _rotulo, aid in self.botoes_ui:
                if rect.collidepoint(pos):
                    self.acao(aid)
                    return True
            return False

        if self.mostra_botao_voltar_lobby() and self.botao_voltar.collidepoint(pos):
            self.voltar_lobby()
            return True

        for rect, _rotulo, aid in self.botoes_ui:
            if rect.collidepoint(pos):
                self.acao(aid)
                return True
        return False

    def loop(self):
        while self.rodando:
            if self.em_animacao():
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        self.rodando = False
                self.atualizar_animacao()
                self.desenhar_tudo()
                pygame.display.flip()
                self.relogio.tick(FPS)
                continue

            tela = self.controle.montar_interface()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.rodando = False
                    break

                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN:
                        if tela["pedir_texto"] or tela["pedir_numero"]:
                            self.enter_texto()
                        elif len(tela["botoes"]) == 1:
                            self.acao(tela["botoes"][0][1])
                    elif evento.key == pygame.K_BACKSPACE:
                        self.input_buffer = self.input_buffer[:-1]
                    elif evento.unicode and (tela["pedir_texto"] or tela["pedir_numero"]):
                        if tela["pedir_numero"] and not evento.unicode.isdigit():
                            continue
                        self.input_buffer += evento.unicode

                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    self.processar_clique(evento.pos)

            if self.em_animacao():
                self.atualizar_animacao()
                self.desenhar_tudo()
                pygame.display.flip()
                self.relogio.tick(FPS)
                continue

            self.desenhar_tudo()
            pygame.display.flip()
            self.relogio.tick(FPS)

        parar_musica_fundo()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--console":
        rodar_modo_console()
    else:
        JanelaJogo().loop()
