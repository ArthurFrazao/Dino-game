import pygame
from pygame.locals import * 
from sys import exit 
from config import *
import os 
from random import randrange, choice

pygame.init()
pygame.mixer.init()

dir = os.path.dirname(__file__)
dir_image = os.path.join(dir, 'imagens')
dir_audio = os.path.join(dir, 'sons')

tela= pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Dino Game')

sprite_sheet = pygame.image.load(os.path.join(dir_image, 'dinoSpritesheet.png')).convert_alpha()

som_colisao = pygame.mixer.Sound(os.path.join(dir_audio, 'sons_death_sound.wav'))
som_colisao.set_volume(1)

som_pontuacao = pygame.mixer.Sound(os.path.join(dir_audio, 'sons_score_sound.wav'))
som_pontuacao.set_volume(1)

colidiu = False

escolha_obstaculo = choice([0,1])
pontos = 0
velocidade = 10

def exibe_mensagem(mensagem, tamanho, cor):
    fonte = pygame.font.SysFont('emulogic', tamanho, True, False)
    mensagem = f'{mensagem}'
    texto = fonte.render(mensagem, True, cor)
    return texto
    
def reiniciar_jogo():
    global pontos, velocidade, colidiu, escolha_obstaculo
    pontos = 0
    velocidade = 10
    colidiu = False
    dino.rect.y = ALTURA - 64 - 96//2
    dino.pulo = False
    dinoVoador.rect.x = LARGURA
    cacto.rect.x = LARGURA
    escolha_obstaculo = choice([0,1])
    
class Dino(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.som_pulo = pygame.mixer.Sound(os.path.join(dir_audio, 'sons_jump_sound.wav'))
        self.som_pulo.set_volume(1)
        self.image_dino = []
        for i in range(3):
            img = sprite_sheet.subsurface((i * 32,0),(32,32))
            img = pygame.transform.scale(img, (32*3, 32*3))
            self.image_dino.append(img)
        self.index_lista = 0
        self.image = self.image_dino[self.index_lista]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (100,416)
        self.pulo = False
        self.pos_y_inicial = 416 - 96//2
        
    def update(self):
        if self.pulo == True:
            if self.rect.y <= 240:
                self.pulo = False
            self.rect.y -= 18
        else:
            if self.rect.y < self.pos_y_inicial:
                self.rect.y += 18
            else:
                self.rect.y = self.pos_y_inicial
                
        if self.index_lista > 2:
            self.index_lista = 0
        self.index_lista += 0.25
        self.image = self.image_dino[int(self.index_lista)]
        
    def pular(self):
        self.pulo = True
        self.som_pulo.play()
    
class Nuvem(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((7*32, 0), (32,32))
        self.image = pygame.transform.scale(self.image, (32*3, 32*3))
        self.rect = self.image.get_rect()
        self.rect.y = randrange(15, 100, 35)
        self.rect.x = LARGURA - randrange(30, 300, 90)
        
    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.y = randrange(15, 100, 35)
            self.rect.x = LARGURA
        self.rect.x -= velocidade
    
class Chao(pygame.sprite.Sprite):
    def __init__(self, posx):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((6*32, 0), (32,32))
        self.image = pygame.transform.scale(self.image, (32*2, 32*2))
        self.rect = self.image.get_rect()
        self.rect.y = ALTURA - 64
        self.rect.x = posx * 64        
           
    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = LARGURA
        self.rect.x -= 8   
        
class Cacto(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((5*32, 0), (32,32))
        self.image = pygame.transform.scale(self.image, (32*2, 32*2))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.escolha = escolha_obstaculo
        self.rect.center = (LARGURA, ALTURA - 64)
        self.rect.x = LARGURA
        
    def update(self):
        if self.escolha == 0:
            if self.rect.topright[0] < 0:
                self.rect.x = LARGURA
            self.rect.x -= velocidade
        
class DinoVoador(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_dino_voador = []
        for i in range(3,5):
            img = sprite_sheet.subsurface((i * 32, 0), (32,32))
            img = pygame.transform.scale(img, (32*3, 32*3))
            self.image_dino_voador.append(img)
            
        self.index_lista = 0
        self.image = self.image_dino_voador[self.index_lista]
        self.mask = pygame.mask.from_surface(self.image)
        self.escolha = escolha_obstaculo
        self.rect = self.image.get_rect()
        self.rect.center = (LARGURA, 300)
        self.rect.x = LARGURA
        
    def update(self):
        if self.escolha == 1:
            if self.rect.topright[0] < 0:
                self.rect.x = LARGURA
            self.rect.x -= velocidade
        
            if self.index_lista > 1:
                self.index_lista = 0
            self.index_lista += 0.25
            self.image = self.image_dino_voador[int(self.index_lista)]

todas_as_sprites = pygame.sprite.Group()
grupo_obstaculos = pygame.sprite.Group()

dino = Dino()
cacto = Cacto()
dinoVoador = DinoVoador()

todas_as_sprites.add(cacto)
todas_as_sprites.add(dino)
todas_as_sprites.add(dinoVoador)

grupo_obstaculos.add(cacto, dinoVoador)

for i in range(LARGURA*2//64):
    chao = Chao(i)
    todas_as_sprites.add(chao)    

for i in range(4):
    nuvem = Nuvem()
    todas_as_sprites.add(nuvem)

relogio = pygame.time.Clock()

while True:
    relogio.tick(30)
    tela.fill(BRANCO)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                if colidiu == False:
                    if dino.rect.y != dino.pos_y_inicial:
                        pass
                    else:
                        dino.pular()
                else:
                    reiniciar_jogo()
        
    colisoes = pygame.sprite.spritecollide(dino, grupo_obstaculos, False, pygame.sprite.collide_mask)   
    todas_as_sprites.draw(tela)
    
    if cacto.rect.topright[0] <= 0 or dinoVoador.rect.topright[0] <= 0:
        escolha_obstaculo = choice([0, 1])
        cacto.rect.x = LARGURA
        dinoVoador.rect.x = LARGURA
        cacto.escolha = escolha_obstaculo
        dinoVoador.escolha = escolha_obstaculo
        
    if colisoes and colidiu == False:
        som_colisao.play()
        colidiu = True
        
    if colidiu == True:
        if pontos % 100 == 0:
            pontos += 1
            
        game_over = exibe_mensagem('GAME OVER', 40, PRETO)
        tela.blit(game_over, (130, (ALTURA//2)))
        restart = exibe_mensagem('Pressione espaco para reiniciar', 17, PRETO)
        tela.blit(restart, (35, (ALTURA//2) - 60))
    else:
        pontos += 1
        todas_as_sprites.update()   
        texto_pontos = exibe_mensagem(pontos, 20, PRETO)
    
    if pontos % 100 == 0:
        som_pontuacao.play()
        if velocidade >= 30:
            velocidade += 0
        else:
            velocidade += 3
    
    tela.blit(texto_pontos, (550, 15))
    pygame.display.flip()