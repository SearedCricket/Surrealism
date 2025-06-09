import pygame
import random
import os
import math
import tkinter as tk
from tkinter import messagebox
from complementos.funcoes import inicializarBancoDeDados
from complementos.funcoes import escreverDados
import json
from complementos.sprites import carregar_imagens, SpriteOlho, SpriteOlho2, load_gif_frames
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
    invulneravel = False
    invuln_timer = 0
    invuln_duration = 1500
    loop2_started = False
    heart_pulse_timer = 0
    heart_base_size = 45
    heart_pulse_speed = 0.08
    heart_rotation = 0

    def obter_nome():
        global nome
        nome = entry_nome.get()  # Obtém o texto digitado
        if not nome:  # Se o campo estiver vazio
            messagebox.showwarning("Aviso", "Por favor, digite seu nome!")  # Exibe uma mensagem de aviso
        else:
            #print(f'Nome digitado: {nome}')  # Exibe o nome no console
            root.destroy()  # Fecha a janela após a entrada válida

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

    # Criação da janela principal
    root = tk.Tk()
    # Obter as dimensões da tela
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    pos_x = (largura_tela - largura_janela) // 2
    pos_y = (altura_tela - altura_janela) // 2
    root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
    root.title("Informe seu nickname")
    root.protocol("WM_DELETE_WINDOW", obter_nome)

    # Entry (campo de texto)
    entry_nome = tk.Entry(root)
    entry_nome.pack()

    # Botão para pegar o nome
    botao = tk.Button(root, text="Enviar", command=obter_nome)
    botao.pack()

    print("Before")
    # Inicia o loop da interface gráfica
    root.mainloop()
    
    # Intro Musica
    pygame.mixer.music.load("Recursos\SoundTracks\Death.mp3")
    pygame.mixer.music.play(-1)

    print("After")

    

    posicaoXPersona = 400
    posicaoYPersona = 300
    movimentoXPersona  = 0
    movimentoYPersona  = 0

    
    dificuldade  = 30
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RIGHT:
                movimentoXPersona = 15
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_LEFT:
                movimentoXPersona = -15
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_RIGHT:
                movimentoXPersona = 0
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_LEFT:
                movimentoXPersona = 0
                
        

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

        if invulneravel:
            if pygame.time.get_ticks() - invuln_timer > invuln_duration:
                invulneravel = False

        if not invulneravel and pygame.sprite.spritecollide(olho_sprite, inimigo_group, False):
            vidas -= 1
            invulneravel = True
            invuln_timer = pygame.time.get_ticks()
            for inimigo in pygame.sprite.spritecollide(olho_sprite, inimigo_group, False):
                inimigo.collided = True
            if vidas <=0:
                pygame.mixer.music.stop()
                escreverDados(nome, pontos)
                dead()
        
            
        tela.fill(branco)
        tela.blit(fundoJogo, (0,0) )
        olho_grupo_sprites.draw(tela)
        inimigo_group.draw(tela)
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

