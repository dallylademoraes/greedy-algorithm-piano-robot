# 🎹 Piano Robótico — Método Guloso

Sistema didático que simula a execução pianística automática de um robô utilizando o **método guloso** como estratégia de decisão.

O projeto foi desenvolvido em **Python**, **Pygame** e **pyFluidSynth**, com animações que representam uma mão robótica articulada tocando a melodia *Für Elise*, demonstrando visualmente o processo de **seleção gulosa** — onde o robô escolhe, a cada nota, o dedo mais próximo para minimizar o movimento total.

💡 Este projeto faz parte do trabalho acadêmico **“Estudo e Implementação de Algoritmo Baseado na Técnica de Método Guloso”**, inspirado no artigo:  
> **Automatic Piano Performance Interaction System Based on Greedy Algorithm for Dexterous Manipulator** > *ScienceDirect, 2024* > [🔗 Acesse o artigo aqui](https://www.sciencedirect.com/science/article/pii/S2096579624000548)

---

## 🚀 Tecnologias utilizadas

- [Python 3.10+](https://www.python.org/downloads/)
- [Pygame](https://www.pygame.org/news)
- [NumPy](https://numpy.org/)
- [pyFluidSynth](https://pypi.org/project/pyFluidSynth/)
- [FluidSynth](https://github.com/FluidSynth/fluidsynth)

---

## ⚙️ Instalação e Configuração Completa (Windows)

Abaixo estão **todas as instruções detalhadas** para configurar e executar o projeto corretamente com som realista.

---

### 🧩 1️⃣ Clonar o repositório

Abra o **PowerShell** ou **Prompt de Comando** e execute:


git clone [https://github.com/dallylademoraes/greedy-algorithm-piano-robot.git](https://github.com/dallylademoraes/greedy-algorithm-piano-robot.git)
cd greedy-algorithm-piano-robot


Isso cria uma cópia do projeto na sua máquina e entra na pasta do projeto.

### 📦 2️⃣ Instalar dependências do Python

Instale as bibliotecas necessárias com:

```bash
pip install pygame numpy pyFluidSynth
```

✅ Isso instala:

  * **Pygame**: para gráficos e animações;
  * **NumPy**: para cálculos e interpolação;
  * **pyFluidSynth**: para gerar o som do piano usando o FluidSynth.

### 🎧 3️⃣ Instalar o FluidSynth no Windows

O FluidSynth é um sintetizador de áudio que o `pyFluidSynth` utiliza para tocar sons reais de instrumentos (via arquivo `.sf2`).

**Passo a passo:**

1.  Baixe o pacote de instalação do FluidSynth:

    👉 **[Download do FluidSynth para Windows](https://www.google.com/search?q=https://github.com/FluidSynth/fluidsynth/releases/download/v2.3.5/fluidsynth-2.3.5-win10-x64.zip)** (link para versão estável)

2.  Extraia o arquivo `ZIP` em qualquer lugar (por exemplo, na sua área de trabalho).

3.  Dentro do ZIP, haverá uma pasta `bin/` com arquivos como:

      * `fluidsynth.exe`
      * `libfluidsynth-3.dll`
      * `libglib-2.0-0.dll`
      * `libintl-8.dll`
      * `libgobject-2.0-0.dll`
      * `libgthread-2.0-0.dll`
      * `libgmodule-2.0-0.dll`
      * `libwinpthread-1.dll`

4.  Crie as seguintes pastas no seu computador:
    `C:\tools\fluidsynth\bin`

5.  Copie **todos** os arquivos `.dll` e `.exe` da pasta `bin` do ZIP para:
    `C:\tools\fluidsynth\bin`

6.  Verifique se o caminho final ficou assim:
    `C:\tools\fluidsynth\bin\libfluidsynth-3.dll`

⚠️ **Importante:**

  * O arquivo principal precisa se chamar `libfluidsynth-3.dll`.
  * Se o nome estiver diferente (ex: `fluidsynth.dll`), renomeie para esse.
  * 💡 O Python procura essa DLL automaticamente no caminho `C:\tools\fluidsynth\bin`.

### 🎼 4️⃣ Baixar o arquivo de som piano.sf2

O arquivo `.sf2` contém os timbres reais do piano.

**Ele não está incluído no repositório** (o GitHub não aceita arquivos acima de 100 MB).

Você pode baixar um dos seguintes *soundfonts* gratuitos:

  * 🎵 **[FluidR3 GM](https://www.google.com/search?q=https://member.keymusician.com/Member/FluidR3_GM/FluidR3_GM.sf2)** (padrão leve e estável)
  * 🎵 **[Timbres of Heaven 3.4](https://www.google.com/search?q=https://github.com/m-vi/Timbres-of-Heaven/releases/download/v3.4/Timbres.of.Heaven.GM_GS_XG_SFX.V.3.4.sf2)** (som profissional)
  * 🎵 **[Nice-Keys GM 3.0](https://www.google.com/search?q=https://github.com/KemenAran/Nice-Keys-GM/releases/download/v3.0/Nice-Keys-GM_v3.0.sf2)** (ótimo piano realista)

Após baixar:

1.  Renomeie o arquivo para:
    `piano.sf2`
2.  Coloque o arquivo na pasta principal do projeto, assim:
    ```
    greedy-algorithm-piano-robot/
    ├── piano_greedy_didatico.py
    ├── .gitignore
    ├── README.md
    └── piano.sf2  ← aqui
    ```

### ▶️ 5️⃣ Executar o projeto

Agora, execute o programa com:

```bash
python piano_greedy_didatico.py
```

Na tela principal:

  * Pressione **Barra de Espaço (SPACE)** → para tocar *Für Elise*.
  * Pressione **R** → para reiniciar a posição da mão robótica.
  * Pressione **X** → para sair.

💡 Se o som não sair, verifique se o `piano.sf2` está no mesmo diretório do script e se o caminho `C:\tools\fluidsynth\bin` existe.

### 🧠 6️⃣ Conceito — Método Guloso aplicado

O método guloso (*Greedy Algorithm*) é usado para decidir qual dedo o robô deve mover a cada nova nota.

A lógica é simples:

> Em cada passo, escolha o dedo mais próximo da tecla que deve ser tocada.

Essa decisão localmente ótima nem sempre é globalmente ideal, mas permite que o sistema opere rapidamente e com eficiência em tempo real.

Durante a execução:

1.  Cada dedo tem uma posição atual sobre o teclado.
2.  Para cada nota, o algoritmo calcula a distância até a tecla alvo.
3.  O dedo com menor distância é escolhido para tocar (decisão gulosa).
4.  A posição da mão é atualizada e o movimento é animado.

-----

## 🖥️ Visualização e recursos didáticos

A interface mostra:

  * 🎹 Um teclado com notas reais (A4–G\#5).
  * 🤖 Uma mão robótica com 5 dedos articulados.
  * 🧭 Um painel (HUD) com:
      * Nota atual tocada
      * Dedo escolhido
      * Distância percorrida
      * Dedo mais usado
      * Distância total estimada

Tudo é desenhado com Pygame e os sons são reproduzidos via `pyFluidSynth` com o `piano.sf2`.

## 🧩 Estrutura do projeto

```
greedy-algorithm-piano-robot/
├── piano_greedy_didatico.py   # Código principal (algoritmo + animação)
├── .gitignore                 # Ignora piano.sf2 e temporários
├── README.md                  # Documentação completa
└── piano.sf2                  # (coloque aqui manually)
```

## 🧰 Solução de problemas comuns

| Erro ou aviso | Solução |
| :--- | :--- |
| `FileNotFoundError: libfluidsynth-3.dll` | Confirme que existe `C:\tools\fluidsynth\bin\libfluidsynth-3.dll`. |
| `pyFluidSynth não disponível` | Reinstale com `pip install pyFluidSynth`. |
| `Soundfont não encontrado` | Coloque `piano.sf2` na pasta principal do projeto. |
| `SDL3 not initialized` | Apenas um aviso — o áudio ainda funciona no Windows. |

-----

## 👩‍💻 Autora

**Dallyla de Moraes**

Universidade Federal do Tocantins (UFT)

  * 📘 **Disciplina:** Projeto e Implementação de Algoritmos
  * 📅 **Ano:** 2025
  * 🔗 **GitHub:** [@dallylademoraes](https://www.google.com/search?q=https://github.com/dallylademoraes)

-----

## ⚠️ Observação importante

O arquivo `piano.sf2` (soundfont de piano) não é distribuído neste repositório due à limitação de tamanho do GitHub (100 MB).

Para executar o projeto corretamente, baixe um soundfont `.sf2` e coloque-o na pasta principal do projeto conforme explicado acima.

## 📜 Licença

Este projeto é de uso acadêmico e educativo, sob licença MIT.

Sinta-se livre para estudar, modificar e aprimorar o código com fins didáticos.

