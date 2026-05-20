# Explicação do código — áudio

Documentação complementar ao [README.md](README.md). O jogo está em [`teste.py`](teste.py), com `ControleJogo` (regras) e `JanelaJogo` (tela).

## Dois canais no Pygame

| Canal | API | Uso no jogo |
|-------|-----|-------------|
| Música de fundo | `pygame.mixer.music` | Arquivo na raiz de `assets/`, em loop |
| Efeitos (SFX) | `pygame.mixer.Sound` | Arquivos em `assets/sons/` |

`preparar_audio()` inicializa o mixer; `tocar_musica_fundo()` e `carregar_efeitos()` usam essa função.

Volumes: `VOLUME_MUSICA = 0.9`, `VOLUME_SFX = 1.0` (teto do Pygame).

## Carregamento dos efeitos

- `ARQUIVOS_SOM` e `SOM_NPC` mapeiam chaves para nomes de arquivo.
- `JanelaJogo.tocar(chave)` reproduz o efeito.

## Onde os sons tocam

- `ir_npc` — fala do personagem
- `executar_escolha` / `acao` — porta, moeda, duelo, interação
- `trocar_cena` — Candidus na intro
- combate e fim dos dados — espada, vitória, moeda

O modo `python teste.py --console` não usa áudio.
