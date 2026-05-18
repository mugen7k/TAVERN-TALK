import pygame
import sys

# ==========================================
# 1. INICIALIZAÇÃO
# ==========================================
pygame.init()

# Definindo o tamanho da tela (Largura x Altura)
LARGURA = 800
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Meu Primeiro Jogo em Pygame")

cor_balao = (255, 255, 255)  # Branco
cor_texto = (0, 0, 0)        # Preto
fonte = pygame.font.SysFont("Arial", 20)

# O Relógio controla os Quadros Por Segundo (FPS)
relogio = pygame.time.Clock()

# Definindo Cores no formato RGB (Red, Green, Blue)
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)

# Variáveis do nosso "Personagem" (um quadrado)
jogador_x = 400
jogador_y = 300
tamanho_jogador = 50
velocidade = 5

texto_superficie = fonte.render("Olá! Como posso ajudar?", True, cor_texto)
# ==========================================
# 2. O LOOP PRINCIPAL
# ==========================================
rodando = True
while rodando:

    # A. CAPTURA DE EVENTOS ----------------
    for evento in pygame.event.get():
        # Se o usuário clicar no 'X' da janela
        if evento.type == pygame.QUIT:
            rodando = False

    # B. ATUALIZAÇÃO LÓGICA ----------------
    # Pegar todas as teclas que estão sendo pressionadas no momento
    teclas = pygame.key.get_pressed()

    # Mover o jogador alterando as coordenadas (lembre-se do eixo Y invertido!)
    if teclas[pygame.K_LEFT]:
        jogador_x -= velocidade
    if teclas[pygame.K_RIGHT]:
        jogador_x += velocidade
    if teclas[pygame.K_UP]:
        jogador_y -= velocidade
    if teclas[pygame.K_DOWN]:
        jogador_y += velocidade

    # C. RENDERIZAÇÃO (DESENHO) ------------
    # 1º: Limpar a tela da imagem anterior preenchendo com PRETO
    tela.fill(PRETO)

    # 2º: Desenhar o jogador. A função rect pede (onde desenhar, cor, (x, y, largura, altura))
    pygame.draw.rect(tela, AZUL, (jogador_x, jogador_y, tamanho_jogador, tamanho_jogador))

    pygame.draw.rect(tela, cor_balao, (90, 140, 260, 40), border_radius=10)
    # Exibe o texto dentro do balão
    tela.blit(texto_superficie, (100, 150))

    # 3º: Atualizar a tela inteira para mostrar o que acabamos de desenhar
    pygame.display.flip()

    # Controlar a velocidade do jogo (60 FPS)
    relogio.tick(155)

# ==========================================
# 3. FINALIZAÇÃO
# ==========================================
pygame.quit()
sys.exit()