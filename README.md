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

Imagens em [`assets/`](assets/). Áudio no modo gráfico:

- **Trilha:** primeiro arquivo de áudio na raiz de `assets/` (ex.: `.mpeg`, `.mp3`) em loop.
- **Efeitos:** arquivos `.wav` em [`assets/sons/`](assets/sons/) (ver tabela abaixo).

### Efeitos sonoros (`assets/sons/`)

| Arquivo | Quando toca |
|---------|-------------|
| `PORTA ABRINDO.wav` | Entrar na taverna |
| `FALA CANDIDUS.wav` | Intro com Candidus / clicar no dono |
| `FALA VIAJANTE.wav` | Clicar no viajante |
| `FALA BARDO.wav` | Clicar no bardo |
| `FALA BEBADO.wav` | Clicar no bêbado |
| `FALA MESA DE JOGOS.wav` | Clicar na mesa de dados |
| `FALA BANDIDO.wav` | Caçador / iniciar duelo |
| `MOEDA.wav` | Compra, gorjeta, aposta (ganho/perda), recompensa do combate |
| `INTERAÇÃO.wav` | Botões gerais e voltar ao salão |
| `BARULHO ESPADA BATENDO.wav` | Turno de combate |
| `BANDIDO DERROTADO.wav` | Vitória no duelo |

---

## Estrutura do projeto

| Arquivo / pasta | Função |
|-----------------|--------|
| [`teste.py`](teste.py) | Jogo completo: lógica + interface gráfica + modo console |
| [`assets/`](assets/) | Sprites, trilha de fundo e pasta `sons/` |
| [`assets/sons/`](assets/sons/) | Efeitos sonoros (`.wav`) |
| [`requirements.txt`](requirements.txt) | Dependência: `pygame` |
| [`EXPLICACAO_DO_CODIGO.md`](EXPLICACAO_DO_CODIGO.md) | Documentação: resumo do jogo + explicação técnica do código |

O código foi organizado em **um arquivo** de propósito: facilita entrega e leitura em disciplina introdutória, com `ControleJogo` (regras) e `JanelaJogo` (tela) bem separados por classe.

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
