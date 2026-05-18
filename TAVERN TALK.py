import random
from random import randint


def monta_save_zuado():
    return {
        "grana": 77,
        "mochila": [],
        "nome_mano": "",
    }


def chuta_numero_ai(prompt, minimo, maximo):
    while True:
        raw = input(prompt)
        try:
            valor = int(raw)
        except ValueError:
            print("Digite um número válido.")
            print()
            continue
        if minimo <= valor <= maximo:
            return valor
        print(f"Escolha um número entre {minimo} e {maximo}.")
        print()


def mostra_grana(state):
    c = state["grana"]
    if c == 0:
        print("Não sobrou nada...")
        print()
    elif c == 1:
        print("Você só tem mais uma moeda.")
        print()
    else:
        print(f"Você tem {c} moedas.")
        print()


def lista_as_parada(state):
    inv = state["mochila"]
    if not inv:
        print("Seu inventário está vazio.")
        print()
        return
    print("Itens no seu inventário:")
    for item in inv:
        print(f"  - {item}")
    print()


def bate_na_porta():
    while True:
        print(
            """
Você chega à porta da taverna."""
        )
        print(
            """
1 = Entrar
2 = Olhar a janela
"""
        )
        entrar_na_taverna = input("O que você faz?: ")
        if entrar_na_taverna == "1":
            break
        elif entrar_na_taverna == "2":
            print(
                """
Você olha lá dentro e vê vários homens rindo e brindando. Parece um lugar muito aconchegante."""
            )


def papo_inicial_velho(state):
    print(
        '''Em seguida um homem bêbado esbarra em você, ele nem se preocupa em pedir desculpas.

Você vai até o balcão.

Um homem careca, barbudo e ranzinza se aproxima para te atender:
"Qual o seu nome jovem?" Indaga o velho careca e barbudo.
'''
    )

    player_name = str(input("Me chamo... "))
    player_name = player_name.strip()
    player_name = player_name.title()
    state["nome_mano"] = player_name
    print()


def de_onde_ce_vem(state):
    player_name = state["nome_mano"]
    print(f'"De que bandas você vem {player_name}?"')
    print(
        """1 = Montanhas Milenares
2 = Litoral Lamuriante
3 = Vale Venerável
4 = Cidade Cinzenta
5 = Lugar nenhum!
"""
    )

    player_history = chuta_numero_ai("Responda: ", 1, 5)
    print()

    match player_history:
        case 1 | 3:
            print('"Ha, já imaginava. Essa cara de bebê não engana ninguém! Haha!"')
        case 2 | 4:
            print(
                '"Hmm, já ouvi muitos relatos sombrios dessas bandas. Você parece muito conservado para ter vindo de lá. "'
            )
        case 5:
            print('"Ahh vai ser assim então. Ok."')


COISAS_DO_BAR = [
    ("Hidromel do Vale", 5),
    ("Ensopado de raiz", 8),
    ("Pão de centeio", 2),
]


def bagunca_do_baldao(state):
    while True:
        print("Você permanece no balcão.")
        print(
            '''Candidus limpa um copo com um pano surrado.
"Quer gastar suas moedas com algo decente?"

1 = Ver cardápio e comprar
2 = Ver moedas
3 = Ver inventário
4 = Voltar ao salão
'''
        )
        esc = input("O que faz?: ")
        print()

        match esc:
            case "1":
                print('"Eis o que temos hoje:"')
                for i, (nome, preco) in enumerate(COISAS_DO_BAR, start=1):
                    print(f"{i} = {nome} — {preco} moedas")
                print("0 = Cancelar")
                print()
                escolha = chuta_numero_ai("Comprar qual item? (número): ", 0, len(COISAS_DO_BAR))
                if escolha == 0:
                    print('"Mudou de ideia? Tudo bem."')
                    print()
                    continue
                nome, preco = COISAS_DO_BAR[escolha - 1]
                if state["grana"] < preco:
                    print('"Moedas não bastam, volte quando tiver o que é justo."')
                    print()
                else:
                    state["grana"] -= preco
                    state["mochila"].append(nome)
                    print(f'Candidus empurra o pedido até você. "{nome} é seu."')
                    print()
            case "2":
                mostra_grana(state)
            case "3":
                lista_as_parada(state)
            case "4":
                print("Você afasta-se do balcão e volta ao burburinho do salão.")
                print()
                break
            case _:
                print("Candidus ergue uma sobrancelha. " '"Não entendi o que quis dizer."')
                print()


MAPINHA_DO_MOLEQUE = [
    ("Mapa das Ruínas de Ferro", 12),
    ("Mapa das Rotas do Sal", 6),
    ("Mapa rabiscado de uma caverna", 4),
]


def mesa_do_cara_capuz(state):
    while True:
        print(
            """Você vai até o viajante.

O estranho ajusta o capuz e sorri com cautela.
"Mapas confiáveis — ou quase. O que procura, forasteiro?"

1 = Ver mapas à venda
2 = Pedir um boato (de graça)
3 = Voltar ao salão
"""
        )
        esc = input("O que faz?: ")
        print()

        match esc:
            case "1":
                for i, (nome, preco) in enumerate(MAPINHA_DO_MOLEQUE, start=1):
                    print(f"{i} = {nome} — {preco} moedas")
                print("0 = Cancelar")
                print()
                escolha = chuta_numero_ai("Qual mapa? (número): ", 0, len(MAPINHA_DO_MOLEQUE))
                if escolha == 0:
                    print('"Hmm. Outra hora então."')
                    print()
                    continue
                nome, preco = MAPINHA_DO_MOLEQUE[escolha - 1]
                if state["grana"] < preco:
                    print('"Sem moedas, sem mapa. Regra simples."')
                    print()
                else:
                    state["grana"] -= preco
                    state["mochila"].append(nome)
                    print(f"Ele desliza o pergaminho na mesa. Você guarda: {nome}.")
                    print()
            case "2":
                print(
                    '"Ouvi dizer que patrulhas reais dobraram na estrada leste. Cuidado ao amanhecer."'
                )
                print()
            case "3":
                print("Você se afasta da mesa do viajante.")
                print()
                break
            case _:
                print("O viajante inclina a cabeça, confuso.")
                print()


def cantoria_do_malandro(state):
    while True:
        print(
            """Você vai até o direção ao bardo.

O bardo afina uma corda e pisca para você.
"Uma canção aquece a alma — ou esvazia a bolsa, se for generoso."

1 = Pedir uma canção alegre (gorjeta 3 moedas)
2 = Pedir uma balada sombria (gorjeta 2 moedas)
3 = Apenas ouvir de longe (de graça)
4 = Voltar ao salão
"""
        )
        esc = input("O que faz?: ")
        print()

        match esc:
            case "1":
                if state["grana"] < 3:
                    print('"Moedas faltando... volte quando puder pagar a alegria."')
                    print()
                else:
                    state["grana"] -= 3
                    print(
                        "O salão ri com uma melodia saltitante. Por um instante, o mundo parece mais leve."
                    )
                    print()
            case "2":
                if state["grana"] < 2:
                    print('"Sem gorjeta, sem sombras cantadas."')
                    print()
                else:
                    state["grana"] -= 2
                    print(
                        "A voz dele desce como névoa; alguns clientes baixam o tom das conversas."
                    )
                    print()
            case "3":
                print(
                    "Você escuta um refrão distante. O bardo acena em agradecimento silencioso."
                )
                print()
            case "4":
                print("Você volta ao centro do salão.")
                print()
                break
            case _:
                print("O bardo coça a nuca. " '"Não captei o pedido."')
                print()


def jogo_zuado_dos_dado(state):
    while True:
        print(
            """Você senta à mesa de jogos
                
"Eai forasteiro, quer tentar a sorte? É só jogar os dados, o maior número leva o ouro!"

1 = Apostar
2 = Verificar o número de moedas
3 = Voltar ao balcão
"""
        )
        escolha_zoada = input("O que irá fazer?: ")
        print()

        match escolha_zoada:
            case "1":
                if state["grana"] >= 1:
                    grana_apostada = 0

                    while not (1 <= grana_apostada <= state["grana"]):
                        print('"Quanto dinheiro vai apostar mané?"')
                        print()
                        while True:
                            raw = input("Vou apostar: ")
                            print()
                            try:
                                grana_apostada = int(raw)
                            except ValueError:
                                print("Digite um número inteiro.")
                                print()
                                continue
                            break
                        if not (1 <= grana_apostada <= state["grana"]):
                            print(
                                f'"Aposta inválida. Você tem {state["grana"]} moedas — aposte entre 1 e isso."'
                            )
                            print()

                    if grana_apostada == state["grana"]:
                        print('"Tudo isso?!"')

                    print('"Hua hua, vamos lá. Você primeiro..."')
                    print()
                    print("Você joga os dados...")
                    print()
                    dado_player_1 = random.randint(1, 6)
                    dado_player_2 = random.randint(1, 6)
                    soma_dados_player = dado_player_1 + dado_player_2
                    print(
                        f"Você tirou {dado_player_1} e {dado_player_2}. A soma é {soma_dados_player}"
                    )
                    dado_npc_1 = random.randint(1, 6)
                    dado_npc_2 = random.randint(3, 6)
                    soma_dados_npc = dado_npc_1 + dado_npc_2
                    print(
                        f"O estranho tirou {dado_npc_1} e {dado_npc_2}. A soma é {soma_dados_npc}"
                    )
                    print()

                    if soma_dados_npc > soma_dados_player:
                        print('"Hahaha, talvez você tenha mais sorte da próxima vez"')
                        state["grana"] = state["grana"] - grana_apostada
                        print()
                        print(f"Você perdeu {grana_apostada} moedas")
                        print()
                    elif soma_dados_npc < soma_dados_player:
                        print('"Você está com sorte jovem"')
                        state["grana"] = state["grana"] + grana_apostada
                        print()
                        print(f"Você ganhou {grana_apostada} moedas")
                        print()
                    else:
                        print('"Olha! Parece que empatamos"')
                        print()
                else:
                    print('"Parece que você está sem dinheiro seu zé ruela hahaha!"')

            case "2":
                mostra_grana(state)

            case "3":
                print('"Chega de apostar!"')
                print()
                print("Você volta ao balcão")
                break


TRALHA_DO_BRABO = [
    ("Dica: esconderijo na doca", 7),
    ("Faca de caça (usada)", 10),
]


def soco_no_badernador(state):
    print(
        """
Um sujeito largo cutuca sua cadeira.
"Esse lugar é apertado demais pra dois heróis", rosna ele.

O caçador suspira. "Resolve isso rápido — não quero sangue no meu contrato."
"""
    )
    player_hp = 16
    inimigo_hp = 12
    print(f"Seu vigor: {player_hp} | Bandido: {inimigo_hp}")
    print()

    while player_hp > 0 and inimigo_hp > 0:
        print(
            "1 = Atacar (1 a 6 de dano; o bandido revida com 1 a 6)\n"
            "2 = Postura defensiva (1 a 3 de dano; recebe 0 a 3 de volta)"
        )
        acao = input("Sua ação: ").strip()
        print()

        if acao == "1":
            dano_player = random.randint(1, 6)
            inimigo_hp -= dano_player
            print(f"Você acerta um golpe por {dano_player} de dano.")
        elif acao == "2":
            dano_player = random.randint(1, 3)
            inimigo_hp -= dano_player
            print(f"Você avança com cautela, causando {dano_player} de dano.")
        else:
            print("Hesitação custa cara: você tropeça e erra o timing.")
            print()
            dano_player = 0

        if inimigo_hp <= 0:
            break

        if acao == "1":
            dano_inimigo = random.randint(1, 6)
        elif acao == "2":
            dano_inimigo = random.randint(0, 3)
        else:
            dano_inimigo = random.randint(2, 5)

        player_hp -= dano_inimigo
        print(
            f"O bandido revida com {dano_inimigo} de dano. Seu vigor: {max(player_hp, 0)} | "
            f"Bandido: {max(inimigo_hp, 0)}"
        )
        print()

    if player_hp > 0:
        premio = 15
        state["grana"] += premio
        print(
            f"O bandido cai. O caçador acena com aprovação. Você encontra {premio} moedas na bolsa dele."
        )
        print()
    else:
        multa = min(8, state["grana"])
        state["grana"] -= multa
        print(
            "Você apaga no chão da taverna. O caçador puxa você pelo colarinho a tempo — mas sua bolsa fica mais leve."
        )
        print(f"Você perde {multa} moedas (ou o que tinha).")
        print()


def rola_com_o_cacador(state):
    while True:
        print(
            """Você senta na mesma mesa que o caçador de recompensas.

Ele examina um cartaz manchado de tinta.
"Negócios são negócios. Posso vender informação... ou te arrumar problema, se for do tipo que gosta."

1 = Ver ofertas do caçador
2 = Duelo rápido com um bandido na taverna (combate)
3 = Voltar ao salão
"""
        )
        esc = input("O que faz?: ")
        print()

        match esc:
            case "1":
                for i, (nome, preco) in enumerate(TRALHA_DO_BRABO, start=1):
                    print(f"{i} = {nome} — {preco} moedas")
                print("0 = Cancelar")
                print()
                escolha = chuta_numero_ai("Comprar o quê? (número): ", 0, len(TRALHA_DO_BRABO))
                if escolha == 0:
                    print('"Decisão sensata às vezes é não comprar nada."')
                    print()
                    continue
                nome, preco = TRALHA_DO_BRABO[escolha - 1]
                if state["grana"] < preco:
                    print('"Moedas curtas — volte quando pagar."')
                    print()
                else:
                    state["grana"] -= preco
                    state["mochila"].append(nome)
                    print(f"Você guarda: {nome}.")
                    print()
            case "2":
                soco_no_badernador(state)
            case "3":
                print("Você levanta da mesa do caçador.")
                print()
                break
            case _:
                print("O caçador franze a testa. " '"Fale de novo, com clareza."')
                print()

def dialogo_com_o_bebado(state):
    player_name = state["nome_mano"]
    print("Você vai em direção ao bêbado")
    print()
    print('E antes que você possa dizer qualquer coisa, ele se vira para você e diz:')
    while True:
        frase_do_bebado = random.randint(1, 10)
        print()
        match frase_do_bebado:
            case 1:
                print('"Escuta aqui, meu chapa... o meu cavalo lá fora tem um motor 1.5 VTEC manual, tá duvidando? Hic... ele bebe bem menos que eu!"')
            case 2:
                print('"O problema do mundo é que os elfos roubaram todo o nosso queijo... e o rei não faz nada a respeito..."')
            case 3:
                print('"Eu levanto peso três vezes na semana inteirinha só pra ter força de conseguir... hic... levantar essa caneca de novo. Enche aí, chefia!"')
            case 4:
                print('"Eu juro por todos os deuses, aquela cadeira ali no canto olhou pra mim torto. Ela sabe muito bem o que fez."')
            case 5:
                print('"Se eu fechar os olhos e der um soco giratório agora mesmo, o vento da minha mão me leva voando direto pra minha cama."')
            case 6:
                print('"Sabe qual é a grande verdade do universo? Hic... Se você plantar uma moeda de ouro num barril de cerveja, no mês que vem nasce uma árvore de canecas! Eu juro, um gnomo me contou..."')
            case 7:
                print('"Garçom, traz mais uma rodada! E faz um brinde praquela parede ali no fundo... ela é a única nessa sala inteira que tá conseguindo ficar em pé sem se apoiar em nada hoje."')
            case 8:
                print(f'"Ouça aqui {player_name}, aquele que tem um "porquê" para viver pode suportar quase qualquer "como".')
            case 9:
                print(f'"Ouça aqui {player_name}, não é o que acontece com você, mas como você reage a isso que importa.')
            case 10:
                print(f'"Ouça aqui {player_name}, age apenas segundo uma máxima tal que possas ao mesmo tempo querer que ela se torne lei universal.')

        print('''
    Você olha para a cara dele sem entender nada.
    1 = "O quê?"
    2 = Ignora e volta para o balcão
    ''')
        decisao_com_o_bebado = str(input('O que você faz? '))
        if decisao_com_o_bebado == '2':
            print('Você ignora e volta ao balcão confuso.')
            break


def menu_grande_taverna(state):
    player_name = state["nome_mano"]
    print(
        f'''"Me chamo Candidus, sou dono deste estabelecimento. Não me arrume confusão aqui {player_name}, senão irá conhecer meu lado não tão receptivo."
'''
    )
    while True:
        print(
            '''"Fique à vontade jovem. Aliás, vai querer algo para animar essa cara feia?"

1 = Pedir uma bebida ou comida no balcão
2 = Ir até o viajante
3 = Enfrentar o bêbado
4 = Ir até o bardo
5 = Ir a mesa de jogos
6 = Falar com o caçador de recompensas
7 = Ir embora e seguir sua jornada
'''

        )
        o_que_o_mano_quer = str(input('"E aí, o que vai querer?:" '))
        print()

        match o_que_o_mano_quer:
            case "1":
                bagunca_do_baldao(state)
            case "2":
                mesa_do_cara_capuz(state)
            case "3":
                dialogo_com_o_bebado(state)
            case "4":
                cantoria_do_malandro(state)
            case "5":
                jogo_zuado_dos_dado(state)
            case "6":
                rola_com_o_cacador(state)
            case "7":
                print("Você vai embora")
                break
            case _:
                print("Candidus resmunga. " '"Não entendi o que você quer."')
                print()


def comeca_a_zueira():
    state = monta_save_zuado()
    print(
        "Você avista a fumaça da taverna de longe. Realmente um hidromel não iria mal, seria ótimo para esquentar em meio àquela noite fria."
    )

    bate_na_porta()

    print(
        """
Você empurra aquela porta pesada, a atravessa, e logo uma onda de calor atinge seu corpo.
"""
    )

    papo_inicial_velho(state)
    de_onde_ce_vem(state)
    menu_grande_taverna(state)

    print("Você atravessa a porta pesada, e enfrenta novamente o frio da noite.")


if __name__ == "__main__":
    comeca_a_zueira()
