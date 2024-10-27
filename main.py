import pygame
import random

# Inicializa o pygame
pygame.init()

# Configurações de tela
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo de Nave - Arcade")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (0, 255, 0)  # Cor do tiro

# Fonte do menu
fonte_titulo = pygame.font.Font(None, 74)
fonte_opcao = pygame.font.Font(None, 36)
fonte_vidas = pygame.font.Font(None, 36)
fonte_pontuacao = pygame.font.Font(None, 36)

# Carregar e redimensionar imagens
nave_img = pygame.image.load("nave.png")
nave_img = pygame.transform.scale(nave_img, (nave_img.get_width() // 6, nave_img.get_height() // 6))
alien_img = pygame.image.load("alien.png")
alien_img = pygame.transform.scale(alien_img, (alien_img.get_width() // 6, alien_img.get_height() // 6))

# Configurações da nave
nave_vel = 5
nave_rect = nave_img.get_rect(center=(LARGURA // 2, ALTURA - 50))

# Configurações dos tiros
tiro_vel = -10
tiros = []
TIRO_RAIO = 5  # Tamanho do tiro

# Configurações dos aliens
alien_vel = 3
aliens = []

# Função para gerar aliens aleatórios
def gerar_aliens(num_aliens):
    for _ in range(num_aliens):
        alien_x = random.randint(0, LARGURA - alien_img.get_width())
        alien_y = random.randint(-100, -40)
        alien_rect = alien_img.get_rect(topleft=(alien_x, alien_y))
        aliens.append(alien_rect)

# Inicializa com um número aleatório de aliens
gerar_aliens(random.randint(2, 5))

# Configurações de vidas e spawnprotect
vidas = 3
spawn_protect = False
ultima_colisao = 0  # Armazena o tempo da última colisão

# Configurações de pontuação
pontuacao = 0

# Função de exibição do menu
def mostrar_menu():
    menu_ativo = True
    while menu_ativo:
        tela.fill(PRETO)
        
        # Exibir título e opções
        titulo = fonte_titulo.render("Jogo de Nave - Arcade", True, BRANCO)
        tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, ALTURA // 4))

        opcao_iniciar = fonte_opcao.render("Pressione Enter para Iniciar", True, BRANCO)
        tela.blit(opcao_iniciar, (LARGURA // 2 - opcao_iniciar.get_width() // 2, ALTURA // 2))
        
        opcao_sair = fonte_opcao.render("Pressione Esc para Sair", True, BRANCO)
        tela.blit(opcao_sair, (LARGURA // 2 - opcao_sair.get_width() // 2, ALTURA // 2 + 40))
        
        pygame.display.flip()

        # Verificar eventos no menu
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:  # Enter para iniciar
                    menu_ativo = False
                elif evento.key == pygame.K_ESCAPE:  # Esc para sair
                    pygame.quit()
                    quit()

# Função para exibir o menu de fim de jogo
def mostrar_menu_fim(pontuacao):
    menu_ativo = True
    while menu_ativo:
        tela.fill(PRETO)
        
        # Exibir título e pontuação
        titulo = fonte_titulo.render("Fim de Jogo!", True, BRANCO)
        tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, ALTURA // 4))

        texto_pontuacao = fonte_pontuacao.render(f"Sua Pontuação: {pontuacao}", True, BRANCO)
        tela.blit(texto_pontuacao, (LARGURA // 2 - texto_pontuacao.get_width() // 2, ALTURA // 2))

        opcao_reiniciar = fonte_opcao.render("Pressione Enter para Reiniciar", True, BRANCO)
        tela.blit(opcao_reiniciar, (LARGURA // 2 - opcao_reiniciar.get_width() // 2, ALTURA // 2 + 40))
        
        opcao_sair = fonte_opcao.render("Pressione Esc para Sair", True, BRANCO)
        tela.blit(opcao_sair, (LARGURA // 2 - opcao_sair.get_width() // 2, ALTURA // 2 + 80))
        
        pygame.display.flip()

        # Verificar eventos no menu de fim de jogo
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:  # Enter para reiniciar
                    menu_ativo = False
                elif evento.key == pygame.K_ESCAPE:  # Esc para sair
                    pygame.quit()
                    quit()

# Função principal do jogo
def main():
    global vidas, spawn_protect, ultima_colisao, pontuacao
    relogio = pygame.time.Clock()
    executando = True

    # Loop principal do jogo
    while executando:
        tela.fill(PRETO)  # Limpar a tela

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:  # Dispara tiro
                    tiro_x = nave_rect.centerx
                    tiro_y = nave_rect.top
                    tiros.append(pygame.Rect(tiro_x, tiro_y, TIRO_RAIO * 2, TIRO_RAIO * 2))

        # Movimentação da nave
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and nave_rect.left > 0:
            nave_rect.x -= nave_vel
        if teclas[pygame.K_RIGHT] and nave_rect.right < LARGURA:
            nave_rect.x += nave_vel
        if teclas[pygame.K_UP] and nave_rect.top > 0:
            nave_rect.y -= nave_vel
        if teclas[pygame.K_DOWN] and nave_rect.bottom < ALTURA:
            nave_rect.y += nave_vel

        # Atualizar tiros
        for tiro in tiros[:]:
            tiro.y += tiro_vel
            if tiro.bottom < 0:
                tiros.remove(tiro)

        # Atualizar aliens
        for alien in aliens[:]:
            alien.y += alien_vel
            if alien.top > ALTURA:
                aliens.remove(alien)
        
        # Adiciona novos aliens aleatórios se a lista estiver vazia
        if len(aliens) < 5:  # Limita a um máximo de 5 aliens na tela
            num_aliens = random.randint(1, 3)  # Gera entre 1 a 3 novos aliens
            gerar_aliens(num_aliens)

        # Detectar colisões entre tiros e aliens
        for tiro in tiros[:]:
            for alien in aliens[:]:
                if tiro.colliderect(alien):
                    tiros.remove(tiro)
                    aliens.remove(alien)
                    pontuacao += 100  # Aumenta a pontuação em 100 pontos ao atingir um alien
                    break  # Sai do loop para evitar erros de iteração

        # Colisão entre nave e alien
        tempo_atual = pygame.time.get_ticks()
        if not spawn_protect:
            for alien in aliens:
                if nave_rect.colliderect(alien):
                    vidas -= 1
                    spawn_protect = True
                    ultima_colisao = tempo_atual
                    break
        else:
            # Desativa o spawnprotect após 2 segundos
            if tempo_atual - ultima_colisao > 2000:
                spawn_protect = False

        # Desenhar nave (fica mais escura durante o spawn_protect)
        if spawn_protect:
            nave_img_tons = nave_img.copy()
            nave_img_tons.fill((100, 100, 100), special_flags=pygame.BLEND_MULT)
            tela.blit(nave_img_tons, nave_rect)
        else:
            tela.blit(nave_img, nave_rect)

        # Desenhar tiros e aliens
        for tiro in tiros:
            pygame.draw.circle(tela, VERDE, (tiro.centerx, tiro.centery), TIRO_RAIO)
        for alien in aliens:
            tela.blit(alien_img, alien.topleft)

        # Exibir vidas e pontuação
        vidas_texto = fonte_vidas.render(f"Vidas: {vidas}", True, BRANCO)
        tela.blit(vidas_texto, (10, 10))
        pontuacao_texto = fonte_pontuacao.render(f"Pontos: {pontuacao}", True, BRANCO)
        tela.blit(pontuacao_texto, (LARGURA - 150, 10))

        # Atualiza a tela
        pygame.display.flip()
        relogio.tick(60)  # Limita a 60 FPS

        # Verifica se o jogador perdeu todas as vidas
        if vidas <= 0:
            executando = False

    # Exibir menu de fim de jogo
    mostrar_menu_fim(pontuacao)

# Inicia o jogo
mostrar_menu()
main()
pygame.quit()