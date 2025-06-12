import pygame
import random
import os
import math
import sys
import tkinter as tk
from tkinter import messagebox
from complementos.funcoes import inicializarBancoDeDados
from complementos.funcoes import escreverDados, TextInput
import json
from complementos.sprites import carregar_imagens, SpriteOlho, SpriteOlho2, load_gif_frames, BloodSplatter, FloatingObject
from complementos.inimigo import Inimigo, spawn_inimigo_aleatorio
import pyttsx3
import speech_recognition as sr
def quit():
    pygame.quit()
    sys.exit()
pygame.init()
inicializarBancoDeDados()
tamanho = (1000,700)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode( tamanho ) 
pygame.display.set_caption("Surrealismo")
icone  = pygame.image.load("Recursos\Icone\Icone.png") #trocar o diretorio do icone
pygame.display.set_icon(icone)
branco = (255,255,255)
preto = (0, 0 ,0 )
fundoStart = pygame.image.load("Recursos/Backg/Weird.png")
fundoJogo = pygame.image.load("Recursos/Backg/space.jpg")
fundoDead = pygame.image.load("Recursos/Backg/Field.png")
fonteMenu = pygame.font.Font("Recursos\Fonts\CalangoRevi.otf",18)
fonteMorte = pygame.font.SysFont("arial",120)
fonteGlitch = pygame.font.Font("Recursos\Fonts\BlueScreen.ttf")
fonteEye = pygame.font.Font("Recursos\Fonts\PixelOperatorMono8-Bold.ttf")
fonteBox = pygame.font.Font("Recursos\Fonts\mercy.otf")
coracao = pygame.image.load("Recursos/heart/Heart.png")
pontos = 0
vidas = 3

def jogar():
    
    largura_janela = 300
    altura_janela = 50
    global pontos, vidas
    pontos = 0
    vidas = 3
    loop2_started = False
    heart_pulse_timer = 0
    heart_base_size = 45
    heart_pulse_speed = 0.08
    heart_rotation = 0

    text_input = TextInput(fonteMenu)
    getting_name = True

    gif_frames = load_gif_frames("Recursos/Eye/Olho2/Olho2.gif", largura_desejada=50)
    olho2_sprite = SpriteOlho2((tamanho[0] // 2, 440), gif_frames)
    olho2_group = pygame.sprite.Group(olho2_sprite)

    while getting_name:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if text_input.handle_event(event):
                nome = text_input.text
                getting_name = False
        tela.fill((0,0,0))
        input_box_width = 220
        input_box_height = 40
        input_box_x = tamanho[0]//2 - input_box_width//2
        input_box_y = tamanho[1]//2 - input_box_height//2
        pygame.draw.rect(tela, branco, (input_box_x, input_box_y, input_box_width, input_box_height), 2)

        title_name = fonteMenu.render("Give me your name: ", True, branco)
        prompt = fonteMenu.render("Press ENTER to continue", True, branco)

        tela.blit(title_name, (tamanho[0]//2 - title_name.get_width()//2, tamanho[1]//2 - 50))
        text_input.draw(tela, input_box_x + 10, input_box_y + 9)
        tela.blit(prompt, (tamanho[0]//2 - prompt.get_width()//2, tamanho[1]//2 + 50))

        pygame.display.flip()
        relogio.tick(60)

    showing_tutorial = True
    while showing_tutorial:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                showing_tutorial = False
        tela.fill((0,0,0))

        olho2_group.update()
        olho2_group.draw(tela)

        tutorial_texts = [
            "How to play:",
            "→ Use the arrows to move the eye",
            "→ Dodge the knives",
            "→ You earn points when you dodge the knives",
            "→ Press SPACE to pause the game",
            "",
            "Press SPACE to START!"
        ]

        y_offset = tamanho[1]//2 - (len(tutorial_texts) * 30)
        for text in tutorial_texts:
            text_surface = fonteMenu.render(text, True, branco)
            text_rect = text_surface.get_rect(center=(tamanho[0]//2, y_offset))
            tela.blit(text_surface, text_rect)
            y_offset += 60

        good_luck = fonteMenu.render("Good Luck!", True, branco)
        good_luck = pygame.transform.scale(good_luck, (200,50))
        good_luck_rect = good_luck.get_rect(center=(tamanho[0]//2, y_offset + 20))
        tela.blit(good_luck, good_luck_rect)

        pygame.display.flip()
        relogio.tick(60)
    # Carregar frames do olho
    caminho_olho = "Recursos/Eye"
    largura_desejada_olho = 90
    quadros_olho = carregar_imagens(caminho_olho, largura_desejada_olho)

    # Criar sprites do olho
    olho_sprite = SpriteOlho((450, 500), quadros_olho)
    olho_grupo_sprites = pygame.sprite.Group(olho_sprite)

    # Carregar imagem inimigo
    enemy_scales = [0.4, 0.50, 0.70, 0.35]

    enemy_paths = [
        "Recursos/Knife/faca1.png",
        "Recursos/Knife/faca2.png",
        "Recursos/Knife/faca3.png",
        "Recursos/Knife/faca4.png"
    ]

    inimigo_images = []
    for path, scale in zip(enemy_paths, enemy_scales):
        img = pygame.image.load(path)
        original_size = img.get_size()
        new_size = (int(original_size[0] * scale), int(original_size[1] * scale))
        img_scaled = pygame.transform.scale(img, new_size)
        inimigo_images.append(img_scaled)

    # Grupo inimigo
    inimigo_group = pygame.sprite.Group()
    inimigo_index = 0

    inimigo_index = spawn_inimigo_aleatorio(inimigo_images, tamanho[0], inimigo_group, Inimigo, olho_sprite.rect.centerx, pontos)

    blood_group = pygame.sprite.Group()
    
    # Intro Musica
    pygame.mixer.music.load("Recursos\SoundTracks\Death.mp3")
    pygame.mixer.music.play(-1)

    hit_sound = pygame.mixer.Sound("Recursos\SoundTracks\Hit.mp3")

    movimentoXPersona  = 0
    
    floating_path = "Recursos\Cassete\Cassete.png"

    floating_object = FloatingObject((random.randint(0, tamanho[0]), random.randint(0, tamanho[1])), floating_path)
    floating_group = pygame.sprite.Group(floating_object)

    paused = False
    overlay = pygame.Surface(tamanho)
    overlay.fill((0, 0, 0))
    overlay.set_alpha(128)
    pause_text = fonteMenu.render("Pausado", True, branco)
    pause_rect = pause_text.get_rect(center=(tamanho[0]//2, tamanho[1]//2))

    keys_pressed = {
        pygame.K_LEFT: False,
        pygame.K_RIGHT: False
    }
    
    dificuldade  = 30
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                paused = not paused
                if paused:
                    movimentoXPersona = 0
                    keys_pressed[pygame.K_LEFT] = False
                    keys_pressed[pygame.K_RIGHT] = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key in keys_pressed:
                    keys_pressed[evento.key] = True
            elif evento.type == pygame.KEYUP:
                if evento.key in keys_pressed:
                    keys_pressed[evento.key] = False
                
        if not paused:
            movimentoXPersona = 0
            if keys_pressed[pygame.K_RIGHT] and not keys_pressed[pygame.K_LEFT]:
                movimentoXPersona = 15
            elif keys_pressed[pygame.K_LEFT] and not keys_pressed[pygame.K_RIGHT]:
                movimentoXPersona = -15
            blood_group.update()

                
        if not paused:

            if len(inimigo_group) == 0:
                spawn_inimigo_aleatorio(inimigo_images, tamanho[0], inimigo_group, Inimigo, olho_sprite.rect.centerx, pontos)

            olho_grupo_sprites.update()  # Atualiza o sprite do olho
            inimigo_group.update()
            floating_group.update()

            for inimigo in list(inimigo_group):
                if inimigo.rect.top >= 700 and not inimigo.collided:
                    pontos += 1
                    inimigo_group.remove(inimigo)
                elif inimigo.rect.top >= 700:
                    inimigo_group.remove(inimigo)

            olho_sprite.rect.x += movimentoXPersona

            if olho_sprite.rect.x < 0:
                olho_sprite.rect.x = 0
            elif olho_sprite.rect.x > tamanho[0] - olho_sprite.rect.width:
                olho_sprite.rect.x = tamanho[0] - olho_sprite.rect.width

            if  pygame.sprite.spritecollide(olho_sprite, inimigo_group, False):
                vidas -= 1
                for inimigo in pygame.sprite.spritecollide(olho_sprite, inimigo_group, False):
                    inimigo.collided = True
                    if vidas > 0:
                        hit_sound.play()
                        blood_pos = (olho_sprite.rect.centerx, olho_sprite.rect.top - 50)
                        blood = BloodSplatter(blood_pos, "Recursos\BloodSplatter\Blood.gif")
                        blood_group.add(blood)
                    inimigo_group.remove(inimigo)
                if vidas <=0:
                    explosion_sound = pygame.mixer.Sound("Recursos\SoundTracks\explosion_old.mp3")
                    explosion_sound.play()

                    explosion = BloodSplatter(olho_sprite.rect.center, "Recursos\BloodSplatter\explosion (2).gif")
                    blood_group.add(explosion)
                    inimigo_group.empty()
                    olho_grupo_sprites.remove(olho_sprite)

                    waiting_explosion = True
                    while waiting_explosion and any(sprite.alive() for sprite in blood_group):
                        blood_group.update()
                        tela.fill(branco)
                        tela.blit(fundoJogo, (0,0))
                        blood_group.draw(tela)
                        pygame.display.update()
                        relogio.tick(60)
                    pygame.mixer.music.stop()
                    escreverDados(nome, pontos)
                    
                    showing_leaderboard = True
                    while showing_leaderboard:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                quit()
                            if event.type == pygame.KEYDOWN:
                                showing_leaderboard = False
                        tela.fill(branco)
                        tela.blit(fundoJogo, (0,0))

                        log_partidas = json.loads(open("log.dat", "r").read())
                        sorted_scores = sorted(log_partidas.items(), key=lambda x: x[1][0], reverse=True)[:5]

                        box_width = 400
                        box_height = 350
                        box_x = (tamanho[0] - box_width) // 2 
                        box_y = (tamanho[1] - box_height) // 2

                        score_box = pygame.Surface((box_width, box_height))
                        score_box.fill((0,0,0))
                        tela.blit(score_box, (box_x, box_y))
                        pygame.draw.rect(tela, branco, (box_x, box_y, box_width, box_height), 2)

                        title = fonteMenu.render("Top 5:", True, branco)
                        title_rect = title.get_rect(centerx=tamanho[0]//2, top=box_y + 20)
                        tela.blit(title, title_rect)

                        y_offset = box_y + 70
                        for nickname, (points, date) in sorted_scores:
                            score_text = fonteMenu.render(f"{nickname}: {points} pts - {date}", True, branco)
                            score_rect = score_text.get_rect(centerx=tamanho[0]//2, top=y_offset)
                            tela.blit(score_text, score_rect)
                            y_offset += 40
                        
                        press_key = fonteMenu.render("Press any key to continue", True, branco)
                        press_rect = press_key.get_rect(centerx=tamanho[0]//2, bottom=box_y + box_height - 20)
                        tela.blit(press_key, press_rect)

                        pygame.display.update()
                        relogio.tick(60)
                    dead()
        tela.fill(branco)
        tela.blit(fundoJogo, (0,0) )
        floating_group.draw(tela)
        inimigo_group.draw(tela)
        olho_grupo_sprites.draw(tela)
        blood_group.draw(tela)
        

        texto_pontos = fonteMenu.render(f"Pontos: {pontos} ", True, branco)
        pontos_rect = texto_pontos.get_rect()
        pontos_rect.topright = (tamanho[0] - 15, 15)
        tela.blit(texto_pontos, pontos_rect)
        
        texto_pause = fonteMenu.render("press space to pause", True, branco)
        pause_txt_rect = texto_pause.get_rect()
        pause_txt_rect.topright = (tamanho[0] - 15, 35)
        tela.blit(texto_pause, pause_txt_rect)

        heart_pulse_timer += heart_pulse_speed
        pulse_scale = abs(math.sin(heart_pulse_timer)) *0.2 + 0.9
        heart_rotation = math.sin(heart_pulse_timer) * 15

        coracao_spacing = 60
        coracao_width = int(heart_base_size * pulse_scale)
        
        original_ratio = coracao.get_width() / coracao.get_height()
        coracao_height = int(coracao_width / original_ratio)

        coracao_base = pygame.transform.scale(coracao, (coracao_width, coracao_height))
        coracao_scaled = pygame.transform.rotate(coracao_base, heart_rotation)

        base_x = 20
        base_y = 30

        for i in range(vidas):
            coracao_pos = (20 + (i * coracao_spacing), 15)
            width_diff = coracao_scaled.get_width() - heart_base_size
            height_diff = coracao_scaled.get_height() - int(heart_base_size * original_ratio)
            center_offset_x = width_diff // 2
            center_offset_y = height_diff // 2
            heart_x = base_x + (i * coracao_spacing) - center_offset_x
            heart_y = base_y - center_offset_y
            tela.blit(coracao_scaled, (heart_x, heart_y))

        

        if paused:
            tela.blit(overlay, (0, 0))
            tela.blit(pause_text, pause_rect)
        
        pygame.display.update()
        relogio.tick(60)


def start():

    pygame.mixer.music.load("Recursos\SoundTracks\Sorrow.mp3")
    pygame.mixer.music.play(-1)

    gif_frames = load_gif_frames("Recursos/Eye/Olho2/Olho2.gif", largura_desejada=50)
    olho2_sprite = SpriteOlho2((tamanho[0] // 2, 389), gif_frames)
    olho2_group = pygame.sprite.Group(olho2_sprite)

    rect_width = 62
    rect_height = 70
    rect_x = (tamanho[0] - rect_width) // 2
    rect_y = 356

    texto_quit = fonteGlitch.render("Leave", True, (255,0,0))
    texto_quit = pygame.transform.scale(texto_quit, (100, 50))
    texto_quit_rect = texto_quit.get_rect()
    texto_quit_rect.bottomleft = (20, tamanho[1] - 20)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                if texto_quit_rect.collidepoint(mouse_pos):
                    quit()
                square_rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
                if square_rect.collidepoint(mouse_pos):
                    jogar()
                
        #startPhrase = fonteMenu.render("Você não quer saber o que tem ali?", True, preto)

            
            
        tela.fill(branco)
        tela.blit(fundoStart, (0,0) )
        tela.blit(texto_quit, texto_quit_rect)
        #tela.blit(startPhrase, (tamanho[0] // 2 - startPhrase.get_width() // 2, 300 ))
        #square_button = pygame.draw.rect(tela, (255, 0, 0), (rect_x, rect_y, rect_width, rect_height), width=2)
        olho2_group.update()
        olho2_group.draw(tela)
        
        pygame.display.update()
        relogio.tick(60)


def dead():
    pygame.mixer.music.stop()
    
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)

    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    olho3 = pygame.image.load("Recursos\Eye\Olho3\Olho3.png")
    olho3_target_width = 300
    olho3_original_ratio = olho3.get_height() / olho3.get_width()
    olho3_scaled_height = int(olho3_target_width * olho3_original_ratio)
    olho3 = pygame.transform.scale(olho3, (olho3_target_width, olho3_scaled_height))

    olho3_y = 150
    olho3_x = (tamanho[0] - olho3_target_width) // 2

    txt_box_width = 300
    txt_box_height = 100
    txt_box_y = 400
    txt_box_x = (tamanho[0] - txt_box_width) // 2

    txt_box_text = "Do you wish to go back?"
    txt_text_color = branco
    txt_text = fonteEye.render(txt_box_text, True, txt_text_color)
    txt_text_rect = txt_text.get_rect(center=(tamanho[0]//2, txt_box_y + txt_box_height//2))
    

    listening = False
    voice_result = None

    yes_normal = pygame.image.load("Recursos/Buttons/Yes.png")
    yes_hover = pygame.image.load("Recursos/Buttons/Yes-P.png")
    no_normal = pygame.image.load("Recursos/Buttons/No.png")
    no_hover = pygame.image.load("Recursos/Buttons/No-P.png")
    button_sound = pygame.mixer.Sound("Recursos/Buttons/Button_sound.mp3")

    button_width, button_height = 100, 50
    yes_normal = pygame.transform.scale(yes_normal, (button_width, button_height))
    yes_hover = pygame.transform.scale(yes_hover, (button_width, button_height))
    no_normal = pygame.transform.scale(no_normal, (button_width, button_height))
    no_hover = pygame.transform.scale(no_hover, (button_width, button_height))

    button_spacing = 50
    button_box_y_position = tamanho[1] - 100
    button_start_x = (tamanho[0] - (button_width * 2 + button_spacing)) // 2

    yes_rect = yes_normal.get_rect(topleft=(button_start_x, button_box_y_position))
    no_rect = no_normal.get_rect(topleft=(button_start_x + button_width + button_spacing, button_box_y_position))

    

    yes_visible = True
    no_visible = True
    button_pressed = None
    scale_factor = 1.0
    mouse_pos = pygame.mouse.get_pos()
    first_frame = True
    while True:
        mouse_pos = pygame.mouse.get_pos()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if yes_rect.collidepoint(mouse_pos) and yes_visible:
                    scale_factor = 0.9
                    button_pressed = "yes"
                elif no_rect.collidepoint(mouse_pos) and no_visible:
                    scale_factor = 0.9
                    button_pressed = "no"
            elif evento.type == pygame.MOUSEBUTTONUP:
                if button_pressed:
                    button_sound.play()
                    if button_pressed == "yes":
                        yes_visible = False
                        pygame.time.wait(200)
                        jogar()
                    else:
                        no_visible = False
                        pygame.time.wait(200)
                        quit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_v:
                    listening = True
                    listening_text = fonteEye.render("I hear you...", True, (255,205,20))
                    listening_rect = listening_text.get_rect(center=(tamanho[0]//2, txt_box_y + txt_box_height + 30))

                    tela.blit(listening_text, listening_rect)
                    pygame.display.update()

                    try:
                        with microphone as source:
                            recognizer.adjust_for_ambient_noise(source)
                            audio = recognizer.listen(source, timeout=3)
                            text = recognizer.recognize_google(audio).lower()

                            if "yes" in text or "yeah" in text:
                                button_pressed = "yes"
                                yes_visible = False
                                button_sound.play()
                                pygame.time.wait(200)
                                jogar()
                            elif "no" in text or "nope" in text:
                                button_pressed = "no"
                                no_visible = False
                                button_sound.play()
                                pygame.time.wait(200)
                                quit()
                    except sr.UnknownValueError:
                        error_text = fonteMenu.render("Couldn't understand audio", True, branco)
                        error_rect = error_text.get_rect(center=(tamanho[0]//2, txt_box_y + txt_box_height + 50))
                        tela.blit(error_text, error_rect)
                        pygame.display.update()
                        pygame.time.wait(1000)
                    except sr.RequestError:
                        error_text = fonteMenu.render("Couldn't connect to a speech service", True, branco)
                        error_rect = error_text.get_rect(center=(tamanho[0]//2, txt_box_y + txt_box_height + 50))
                        tela.blit(error_text, error_rect)
                        pygame.display.update()
                        pygame.time.wait(1000)
                    except sr.WaitTimeoutError:
                        timeout_text = fonteMenu.render("No speech detected", True, branco)
                        timeout_rect = timeout_text.get_rect(center=(tamanho[0]//2, txt_box_y + txt_box_height + 50))
                        tela.blit(timeout_text, timeout_rect)
                        pygame.display.update()
                        pygame.time.wait(1000)
                    finally:
                        listening = False
        

        tela.fill(branco)
        tela.blit(fundoDead, (0,0) )

        tela.blit(olho3, (olho3_x, olho3_y))

        txt_box_box = pygame.Surface((txt_box_width, txt_box_height))
        txt_box_box.fill((0,0,0))
        tela.blit(txt_box_box, (txt_box_x, txt_box_y))
        pygame.draw.rect(tela, branco, (txt_box_x, txt_box_y, txt_box_width, txt_box_height), 2)

        tela.blit(txt_text, txt_text_rect)
        voice_hint = fonteEye.render("Press V to use your voice", True, (255,0,0))
        voice_rect = voice_hint.get_rect(center=(tamanho[0]//2, txt_box_y + 180))
        tela.blit(voice_hint, voice_rect)
        if yes_visible:
            current_yes = yes_hover if yes_rect.collidepoint(mouse_pos) else yes_normal
            if button_pressed == "yes":
                scaled_size = (int(button_width * scale_factor), int(button_height * scale_factor))
                current_yes = pygame.transform.scale(current_yes, scaled_size)
                scaled_rect = current_yes.get_rect(center=yes_rect.center)
                tela.blit(current_yes, scaled_rect)
            else:
                tela.blit(current_yes, yes_rect)

        if no_visible:
            current_no = no_hover if no_rect.collidepoint(mouse_pos) else no_normal
            if button_pressed == "no":
                scaled_size = (int(button_width * scale_factor), int(button_height * scale_factor))
                current_no = pygame.transform.scale(current_no, scaled_size)
                scaled_rect = current_no.get_rect(center=no_rect.center)
                tela.blit(current_no, scaled_rect)
            else:
                tela.blit(current_no, no_rect)

        pygame.display.update()

        if first_frame:
            engine.say(txt_box_text)
            engine.runAndWait()
            first_frame = False

        relogio.tick(60)


start()

