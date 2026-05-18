import pygame
import sys
import random
import ctypes
import os

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

pygame.init()
tela = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Tavern Talk")
relogio = pygame.time.Clock()

# CORES
PRETO = (0, 0, 0)

# SPRITES
sprite_lobby = pygame.image.load("assets/lobby.png").convert_alpha()
sprite_dialogo_com_candidus = pygame.image.load("assets/DIALOGO COM CANDIDUS.png").convert_alpha()
sprite_dialogo_com_bebado = pygame.image.load("assets/DIALOGO COM O BEBADO.png").convert_alpha()

botao_ir_ao_candidus = pygame.Rect(760,215,360,380)
botao_voltar_universal = pygame.Rect(1800,950,100,100)

def cena_lobby():
    tela.blit(sprite_lobby, (0, 0))

def cena_candidus():
    tela.blit(sprite_dialogo_com_candidus, (0, 0))

cena_atual = "lobby"

rodando = True
while rodando:

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:

            if cena_atual == "lobby":
                if botao_ir_ao_candidus.collidepoint(evento.pos):
                    cena_atual = "dialogo_candidus"

            elif cena_atual == "dialogo_candidus":
                if botao_voltar_universal.collidepoint(evento.pos):
                    cena_atual = "lobby"

    tela.fill(PRETO)

    match cena_atual:
        case "lobby":
            cena_lobby()
        case "dialogo_candidus":
            cena_candidus()


    pygame.display.flip()
    relogio.tick(30) # Trava o jogo em 60 FPS

pygame.quit()
sys.exit()