import pygame
import random
import os
import math
import tkinter as tk
from tkinter import messagebox
from complementos.funcoes import inicializarBancoDeDados
from complementos.funcoes import escreverDados, TextInput
import json
from complementos.sprites import carregar_imagens, SpriteOlho, SpriteOlho2, load_gif_frames, BloodSplatter
from complementos.inimigo import Inimigo, spawn_inimigo_aleatorio
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
fundoDead = pygame.image.load("Recursos/Backg/Death.png")
fonteMenu = pygame.font.Font("Recursos\Fonts\CalangoRevi.otf",18)
fonteMorte = pygame.font.SysFont("arial",120)
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
        title_name = fonteMenu.render("Digite seu nome: ", True, branco)
        prompt = fonteMenu.render("Pressione ENTER para confirmar", True, branco)

        tela.blit(title_name, (tamanho[0]//2 - title_name.get_width()//2, tamanho[1]//2 - 50))
        text_input.draw(tela, tamanho[0]//2 -100, tamanho[1]//2)
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
            "Como jogar:",
            "→ Use as setas para mover o olho",
            "→ Desvie das facas",
            "→ Ganhe pontos quando desviar das facas",
            "→ Pressione ESPAÇO para pausar o jogo",
            "",
            "Pressione ESPAÇO para começar!"
        ]

        y_offset = tamanho[1]//2 - (len(tutorial_texts) * 30)
        for text in tutorial_texts:
            text_surface = fonteMenu.render(text, True, branco)
            text_rect = text_surface.get_rect(center=(tamanho[0]//2, y_offset))
            tela.blit(text_surface, text_rect)
            y_offset += 60

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

    inimigo_index = spawn_inimigo_aleatorio(inimigo_images, tamanho[0], inimigo_group, Inimigo)

    blood_group = pygame.sprite.Group()
    
    # Intro Musica
    pygame.mixer.music.load("Recursos\SoundTracks\Death.mp3")
    pygame.mixer.music.play(-1)

    print("After")

    

    posicaoXPersona = 400
    posicaoYPersona = 300
    movimentoXPersona  = 0
    
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
                spawn_inimigo_aleatorio(inimigo_images, tamanho[0], inimigo_group, Inimigo)

            olho_grupo_sprites.update()  # Atualiza o sprite do olho
            inimigo_group.update()

            for inimigo in list(inimigo_group):
                if inimigo.rect.top >= 700 and not inimigo.collided:
                    pontos += 1
                    inimigo_group.remove(inimigo)
                elif inimigo.rect.top >= 700:
                    inimigo_group.remove(inimigo)

            olho_sprite.rect.x += movimentoXPersona

            if olho_sprite.rect.x < 0:
                olho_sprite.rect.x = 0
            elif olho_sprite.rect.x > 950:
                olho_sprite.rect.x = 950

            if olho_sprite.rect.y < 0:
                olho_sprite.rect.y = 0
            elif olho_sprite.rect.y > 650:
                olho_sprite.rect.y = 650

            if  pygame.sprite.spritecollide(olho_sprite, inimigo_group, False):
                vidas -= 1
                for inimigo in pygame.sprite.spritecollide(olho_sprite, inimigo_group, False):
                    inimigo.collided = True
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
                    dead()
        
            
        tela.fill(branco)
        tela.blit(fundoJogo, (0,0) )
        olho_grupo_sprites.draw(tela)
        inimigo_group.draw(tela)
        blood_group.draw(tela)
        #pygame.draw.circle(tela, preto, (posicaoXPersona,posicaoYPersona), 40, 0 )
        pygame.draw.rect(tela, (255, 0, 0), olho_sprite.rect, 2)

        for inimigo in inimigo_group:
            pygame.draw.rect(tela, (0, 0, 255), inimigo.rect, 2)
        
        texto_pontos = fonteMenu.render(f"Pontos: {pontos} ", True, branco)
        pontos_rect = texto_pontos.get_rect()
        pontos_rect.topright = (tamanho[0] - 15, 15)
        tela.blit(texto_pontos, pontos_rect)
        
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

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                square_rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
                if square_rect.collidepoint(mouse_pos):
                    jogar()
                
        #startPhrase = fonteMenu.render("Você não quer saber o que tem ali?", True, preto)

            
            
        tela.fill(branco)
        tela.blit(fundoStart, (0,0) )
        #tela.blit(startPhrase, (tamanho[0] // 2 - startPhrase.get_width() // 2, 300 ))
        #square_button = pygame.draw.rect(tela, (255, 0, 0), (rect_x, rect_y, rect_width, rect_height), width=2)
        olho2_group.update()
        olho2_group.draw(tela)
        
        pygame.display.update()
        relogio.tick(60)


def dead():
    pygame.mixer.music.stop()
    larguraButtonStart = 150
    alturaButtonStart  = 40
    larguraButtonQuit = 150
    alturaButtonQuit  = 40
    
    
    root = tk.Tk()
    root.title("Tela da Morte")

    # Adiciona um título na tela
    label = tk.Label(root, text="Log das Partidas", font=("Arial", 16))
    label.pack(pady=10)

    # Criação do Listbox para mostrar o log
    listbox = tk.Listbox(root, width=50, height=10, selectmode=tk.SINGLE)
    listbox.pack(pady=20)

    # Adiciona o log das partidas no Listbox
    log_partidas = open("log.dat", "r").read()
    log_partidas = json.loads(log_partidas)
    for chave in log_partidas:
        listbox.insert(tk.END, f"Pontos: {log_partidas[chave][0]} na data: {log_partidas[chave][1]} - Nickname: {chave}")  # Adiciona cada linha no Listbox
    
    root.mainloop()
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 140
                    alturaButtonStart  = 35
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 140
                    alturaButtonQuit  = 35

                
            elif evento.type == pygame.MOUSEBUTTONUP:
                # Verifica se o clique foi dentro do retângulo
                if startButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonStart = 150
                    alturaButtonStart  = 40
                    jogar()
                if quitButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonQuit = 150
                    alturaButtonQuit  = 40
                    quit()
                    
        
            
            
        tela.fill(branco)
        tela.blit(fundoDead, (0,0) )

        
        startButton = pygame.draw.rect(tela, branco, (10,10, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonteMenu.render("Iniciar Game", True, preto)
        tela.blit(startTexto, (25,12))
        
        quitButton = pygame.draw.rect(tela, branco, (10,60, larguraButtonQuit, alturaButtonQuit), border_radius=15)
        quitTexto = fonteMenu.render("Sair do Game", True, preto)
        tela.blit(quitTexto, (25,62))


        pygame.display.update()
        relogio.tick(60)


start()

