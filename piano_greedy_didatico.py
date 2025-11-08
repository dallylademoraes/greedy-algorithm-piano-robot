"""
Piano Robótico - Demonstração didática do Método Guloso
- Visual: teclado + mão robótica articulada (didática)
- Áudio: usa pyFluidSynth + arquivo 'piano.sf2' se disponível (melhor qualidade)
         caso contrário, fallback para síntese (harmônicos)
- Algoritmo guloso: para cada nota, escolhe o dedo mais próximo (menor distância)
- Exibe HUD com nota, dedo escolhido, distância, distância total e dedo mais usado.

Requisitos:
pip install pygame numpy pyFluidSynth
Coloque opcionalmente 'piano.sf2' na mesma pasta para som de piano real.
"""

import os
import math
import time
import collections

import pygame
import numpy as np
import os
os.add_dll_directory(r"C:\tools\fluidsynth\bin")

# Tente importar fluidsynth (pyFluidSynth). Se não conseguir, usaremos fallback.
# Usamos importlib.import_module para que linters/checadores estáticos não apontem
# import não resolvido quando a biblioteca é opcional.
try:
    import importlib
    fluidsynth = importlib.import_module('fluidsynth')
    HAS_FLUIDSYNTH = True
except Exception:
    fluidsynth = None
    HAS_FLUIDSYNTH = False

# -------------------------
# Configurações gerais
# -------------------------
pygame.init()
SAMPLE_RATE = 44100
pygame.mixer.init(frequency=SAMPLE_RATE, size=-16, channels=2)  # stereo for nicer sound

WIDTH, HEIGHT = 1000, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Piano Robótico - Método Guloso (didático)")

FONT = pygame.font.SysFont(None, 20)
BIGFONT = pygame.font.SysFont(None, 28)

# Cores
WHITE = (255, 255, 255)
BLACK = (10, 10, 10)
GRAY = (220, 220, 220)
DARK = (40, 40, 40)
BLUE = (30, 144, 255)
GREEN = (0, 200, 0)
RED = (220, 50, 50)
METAL = (180, 180, 200)

# -------------------------
# Teclado: notas e layout
# -------------------------
# Vamos usar uma faixa pequena didática com 12 notas (uma oitava cromática),
# mas mapear apenas as notas que usaremos da melodia simplificada de Für Elise.
# Cada tecla é branca apenas para estilo didático (simplificamos).
NOTES_ORDER = [
    'A4','A#4','B4','C5','C#5','D5','D#5','E5','F5','F#5','G5','G#5'
]
NUM_KEYS = len(NOTES_ORDER)
KEY_W = WIDTH // NUM_KEYS
KEY_H = 220
KEY_Y = HEIGHT - KEY_H - 20

# Criar retângulos de teclas
keys = [pygame.Rect(i*KEY_W, KEY_Y, KEY_W-2, KEY_H) for i in range(NUM_KEYS)]

# -------------------------
# Áudio: FluidSynth ou síntese
# -------------------------
SOUNDFONT_FILE = "piano.sf2"  # nome esperado; se colocado, terá som melhor

fs = None
SF_LOADED = False

if HAS_FLUIDSYNTH and os.path.exists(SOUNDFONT_FILE):
    try:
        fs = fluidsynth.Synth(samplerate=SAMPLE_RATE)
        fs.start(driver="alsa" if os.name != 'nt' else None)  # None lets pyFluidSynth choose
        sfid = fs.sfload(SOUNDFONT_FILE)
        fs.program_select(0, sfid, 0, 0)
        SF_LOADED = True
        print("Soundfont carregado:", SOUNDFONT_FILE)
    except Exception as e:
        print("Falha ao iniciar FluidSynth:", e)
        SF_LOADED = False
else:
    if HAS_FLUIDSYNTH:
        print("Soundfont não encontrado. Coloque 'piano.sf2' na pasta para som melhor.")
    else:
        print("pyFluidSynth não disponível; usando síntese interna.")

# Mapa MIDI note numbers para as labels acima (A4 = 69)
NOTE_TO_MIDI = {
    'A4':69,'A#4':70,'B4':71,'C5':72,'C#5':73,'D5':74,'D#5':75,'E5':76,'F5':77,'F#5':78,'G5':79,'G#5':80
}

# Fallback: sintetizador simples (cria sons com harmônicos)
SYN_SOUNDS = {}
def synth_make_sound(midi_note, dur=0.5, volume=0.4):
    freq = 440.0 * 2 ** ((midi_note - 69)/12.0)
    t = np.linspace(0, dur, int(SAMPLE_RATE * dur), False)
    # soma de harmônicos com envelope para parecer mais 'piano-like'
    wave = (0.9*np.sin(2*np.pi*freq*t) +
            0.5*np.sin(2*np.pi*2*freq*t) * 0.5 +
            0.2*np.sin(2*np.pi*3*freq*t) * 0.2)
    # ataque e decaimento simples
    env = np.minimum(1, 5*t) * np.exp(-3*t)
    wave *= env
    wave = (wave * (2**15 -1) * volume).astype(np.int16)
    stereo = np.column_stack([wave,wave])
    sound = pygame.sndarray.make_sound(stereo.copy())
    return sound

# Pré-gerar sons de fallback para notas que vamos usar
for name, midi in NOTE_TO_MIDI.items():
    SYN_SOUNDS[name] = synth_make_sound(midi, dur=0.7, volume=0.45)

def play_note(name, vel=100, dur=0.6):
    """Toca uma nota usando FluidSynth (se disponível) ou fallback sintetizado."""
    if SF_LOADED and fs is not None:
        # channel 0, note on, wait a bit, note off (velocity 0..127)
        fs.noteon(0, NOTE_TO_MIDI[name], vel)
        # schedule noteoff after dur (non-blocking: we can call noteoff after sleep)
        # but we'll just sleep in the caller to keep sync; here we just return
    else:
        SYN_SOUNDS[name].play()

# -------------------------
# Mão robótica (didática)
# -------------------------
# Representamos a mão por um "braço" fixo e 5 dedos articulados.
HAND_BASE_X = WIDTH//2
HAND_BASE_Y = KEY_Y - 70
FINGER_LENGTHS = [50, 40]  # base segment + tip

# Posições iniciais dos dedos (índice de tecla)
fingers_pos = [i for i in range(5)]  # começar próximos 0..4
# Para uma visualização didática, mapeamos dedos para posições na região esquerda do teclado
for i in range(5):
    fingers_pos[i] = i  # toque inicial

# Estatísticas
total_distance = 0.0
finger_usage = collections.Counter()

# -------------------------
# Melodia: Für Elise (trechinho inicial simplificado)
# -------------------------
# Usamos os nomes presentes em NOTES_ORDER
melody = ['E5','D#5','E5','D#5','E5','B4','D5','C5','A4']
durations = [0.35,0.35,0.35,0.35,0.35,0.45,0.35,0.35,0.7]

# Index helper
def note_index_in_keys(note_name):
    return NOTES_ORDER.index(note_name)

# -------------------------
# Algoritmo guloso (didático)
# -------------------------
def greedy_choose(fingers, target_idx):
    """Escolhe dedo com menor distância absoluta (greedy). Retorna dedo escolhido."""
    dists = [abs(pos - target_idx) for pos in fingers]
    choice = int(np.argmin(dists))
    return choice, dists[choice]

# -------------------------
# Desenho/Animação utilitárias
# -------------------------
def draw_keyboard(active_idx=None):
    # teclado grande em baixo
    for i, rect in enumerate(keys):
        col = WHITE if i != active_idx else (200,255,200)
        pygame.draw.rect(screen, col, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        # label nota
        txt = FONT.render(NOTES_ORDER[i], True, BLACK)
        screen.blit(txt, (rect.x + 6, rect.y + 6))

def draw_hand(fingers, active_finger=None, target_x=None):
    # desenha base metálica
    pygame.draw.rect(screen, METAL, (HAND_BASE_X-50, HAND_BASE_Y-10, 100, 20), border_radius=6)
    # para cada dedo, desenhar dois segmentos e ponta
    for idx, pos in enumerate(fingers):
        # posição horizontal alvo (real x)
        x = pos * KEY_W + KEY_W//2
        base_x = HAND_BASE_X - 200 + idx*80  # espalha as bases para desenho didático
        base_y = HAND_BASE_Y
        # interpolar base->x para aparência de articulação (um braço que alcança)
        mid_x = (base_x + x) / 2
        mid_y = base_y - 30
        tip_x = x
        tip_y = base_y - 10
        # cor
        color = RED if idx == active_finger else DARK
        # desenha "braço"
        pygame.draw.line(screen, color, (base_x, base_y), (mid_x, mid_y), 10)
        pygame.draw.line(screen, color, (mid_x, mid_y), (tip_x, tip_y), 8)
        # ponta do dedo
        pygame.draw.circle(screen, color, (int(tip_x), int(tip_y)), 10)
        # rótulo do dedo
        label = FONT.render(str(idx+1), True, WHITE)
        screen.blit(label, (base_x-6, base_y-36))

    # Opcional: desenhar linha para o target (mostra a decisão)
    if target_x is not None:
        pygame.draw.line(screen, BLUE, (target_x, KEY_Y + 10), (HAND_BASE_X, HAND_BASE_Y), 2)

def draw_hud(current_note=None, chosen=None, dist=None):
    # painel superior com informações
    pygame.draw.rect(screen, (240,240,240), (10, 10, WIDTH-20, 90), border_radius=6)
    title = BIGFONT.render("Demonstração: Método Guloso - Escolha de Dedos (didática)", True, BLACK)
    screen.blit(title, (20, 14))
    y = 48
    if current_note is not None:
        txt = f"Nota: {current_note}    Dedo escolhido: {chosen+1 if chosen is not None else '-'}    Distância: {dist if dist is not None else '-'}"
        screen.blit(FONT.render(txt, True, BLACK), (20, y))
    # estatísticas
    stats = f"Distância total percorrida (estim.): {total_distance:.2f} teclas   Dedo mais usado: {finger_usage.most_common(1)[0][0]+1 if finger_usage else '-'}"
    screen.blit(FONT.render(stats, True, BLACK), (20, y+26))

# -------------------------
# Função principal: toca melodia com animação
# -------------------------
def animate_move(finger_idx, start_pos, end_pos, note_idx, dur):
    """Move o dedo suavemente (interpolação) e toca a nota no meio do movimento."""
    global fingers_pos, total_distance
    steps = max(12, int(40 * dur))  # mais passos para movimentos maiores
    for s in range(steps+1):
        t = s / steps
        # ease-in-out para movimento mais natural
        t_eased = (-0.5 * (math.cos(math.pi * t) - 1))
        current = start_pos + (end_pos - start_pos) * t_eased
        temp_positions = fingers_pos.copy()
        temp_positions[finger_idx] = current
        # redesenhar
        screen.fill(GRAY)
        active_key_idx = note_idx if t > 0.6 else None
        draw_keyboard(active_key_idx)
        draw_hand(temp_positions, active_finger=finger_idx, target_x= note_idx * KEY_W + KEY_W//2)
        draw_hud(current_note=NOTES_ORDER[note_idx], chosen=finger_idx, dist=abs(current-end_pos))
        pygame.display.flip()
        pygame.time.delay(int(dur*1000/steps))
    # atualizar posição final concreta
    move_distance = abs(start_pos - end_pos)
    total_distance += move_distance
    fingers_pos[finger_idx] = end_pos
    finger_usage[finger_idx] += 1

def play_melody():
    # toca cada nota da melodia aplicando a regra gulosa
    for note, dur in zip(melody, durations):
        idx = note_index_in_keys(note)
        chosen, dist = greedy_choose(fingers_pos, idx)
        # animar e tocar: aqui tocamos no início do movimento para sincronizar com HW real
        animate_move(chosen, fingers_pos[chosen], idx, idx, dur)
        # tocar via fluidsynth ou fallback
        if SF_LOADED and fs is not None:
            fs.noteon(0, NOTE_TO_MIDI[note], 100)
            # toque breve
            time.sleep(dur * 0.8)
            fs.noteoff(0, NOTE_TO_MIDI[note])
        else:
            play_note(note, dur=dur)
            time.sleep(dur)
        # após tocar, pequena pausa para visualização
        time.sleep(0.08)

# -------------------------
# Loop principal (interação)
# -------------------------
running = True
clock = pygame.time.Clock()

# desenho inicial
screen.fill(GRAY)
draw_keyboard()
draw_hand(fingers_pos)
draw_hud()
pygame.display.flip()

print("Pressione ESPAÇO para tocar a melodia (Für Elise simplificada).")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # reset stats for clarity a cada execução
                total_distance = 0.0
                finger_usage.clear()
                play_melody()
                # redesenhar após execução
                screen.fill(GRAY)
                draw_keyboard()
                draw_hand(fingers_pos)
                draw_hud()
                pygame.display.flip()
            elif event.key == pygame.K_r:
                # reset positions (opcional)
                for i in range(5):
                    fingers_pos[i] = i
                total_distance = 0.0
                finger_usage.clear()
                screen.fill(GRAY)
                draw_keyboard()
                draw_hand(fingers_pos)
                draw_hud()
                pygame.display.flip()

    clock.tick(30)

# limpar fluid synth
if SF_LOADED and fs is not None:
    try:
        fs.delete()
    except Exception:
        pass

pygame.quit()
