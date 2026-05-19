# Tavern Talk

**Seja bem-vindo à taverna!**

Tavern Talk é um jogo de menu interativo com temática de RPG medieval. Você entra na taverna, escolhe sua origem, conversa com NPCs, compra itens, aposta nos dados e pode duelar com um bandido — tudo com economia de moedas e inventário.

---

## Como jogar

| Modo | Comando |
|------|---------|
| **Gráfico** (Pygame) | `python teste.py` |
| **Console** (texto) | `python teste.py --console` |

### Instalação

```bash
pip install -r requirements.txt
```

Requisito: Python 3 com [Pygame](https://www.pygame.org/) (versão em `requirements.txt`).

### Dicas rápidas (modo gráfico)

1. Complete a introdução (porta, nome, origem nos cinco cartões).
2. No **salão**, clique nos personagens na imagem.
3. Use o **painel inferior** para escolhas e textos.
4. Use o **botão Voltar** (canto superior direito) para retornar ao salão nos diálogos.
5. Você começa com **77 moedas**. Para encerrar: **Sair da taverna** no salão.

Imagens estão em [`assets/`](assets/). No modo gráfico, o primeiro arquivo de áudio encontrado nessa pasta (`.mp3`, `.ogg`, `.wav`, `.mpeg`, etc.) toca em loop como trilha de fundo.

---

## Estrutura do projeto

| Arquivo / pasta | Função |
|-----------------|--------|
| [`teste.py`](teste.py) | Jogo completo (~1.340 linhas): lógica + interface gráfica + modo console |
| [`assets/`](assets/) | Sprites (salão, NPCs, combate, janela, origens, dados em `DICES/`) |
| [`requirements.txt`](requirements.txt) | Dependência: `pygame` |
| [`EXPLICACAO_DO_CODIGO.md`](EXPLICACAO_DO_CODIGO.md) | Documentação: resumo do jogo + explicação técnica do código |

O código foi organizado em **um arquivo** de propósito: facilita entrega e leitura em disciplina introdutória, com `GameController` (regras) e `TavernTalkGUI` (tela) bem separados por classe.

---

## Documentação do código

Para entender **o que o jogo faz** e **como o Python está organizado** (fases, `view`, animações, combate, dados), leia:

**[EXPLICACAO_DO_CODIGO.md](EXPLICACAO_DO_CODIGO.md)**

Inclui resumo para o jogador/apresentação e seção técnica (máquina de estados, dicionário `view`, loop Pygame, pasta `assets`).

---

## Integrantes

- Felipe Peres
- Thiago Silva
- Julia da Silva
- Fabricio Mendoza

*Projeto desenvolvido como requisito de avaliação acadêmica (FIAP).*
