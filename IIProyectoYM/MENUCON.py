"""
######################################################
| Instituto Tecnológico de Costa Rica                |
| Ingenieria en Computadores                         |
| Taller de Programación                             |
|                                                    | 
| DAKAR DEATH                                        |
|                                                    |
| Yaritza Elena Lopez Bustos                         |
| Maria Fernanda Alvarez Martinez                    |
| Python 3.7                                         |
| Fecha Mayo 22 2019                                 |
######################################################
"""
from tkinter import *
import json 
import pygame
from random import randint
from pygame.locals import *
from network import Network
pygame.init()
pygame.mixer.music.load ('FondoMenu.wav') #Musica de fondo 
pygame.mixer.music.play(2)
listaEnemigo = []

class Player(pygame.sprite.Sprite): #Clase de los jugadores
    
    def __init__ (self):
        #Funcion para la imagen y la posicion inicial de los carros jugadores 
        pygame.sprite.Sprite. __init__ (self)

        self.net = Network()

        self.IPlayer1 = pygame.image.load ('carro1.png') #Imagen del primer carro jugador 
        self.IPlayer2 = pygame.image.load ('carro2.png')# Imagen del segundo carro jugador
    
        self.rect = self.IPlayer1.get_rect ()
        self.rect1 = self.IPlayer2.get_rect ()
        self.rect.centerx = (300) #Posicion en x del jugador1
        self.rect.centery = (410) #Posicion en y del jugador1
        self.rect1.centerx = (380)#Posicion en x del jugador2
        self.rect1.centery = (400)#Posicion en y del jugador2
        self.listaDisparo1 = [] #Lista para que el carro1 pueda disparar
        self.listaDisparo2 = [] #Lista para que el carro2 pueda disparar 
        self.Vida1 = True #Vida para el jugador 1
        self.Vida2 = True #Vida para el jugador 2
        self.velocidad1 = 1 #Movimiento del carro1
        self.velocidad2 = 1 #Movimiento del carro2

        self.hitbox = (self.rect.centerx + 17, self.rect.centery +2, 31, 57) #Barra de vida
        self.hitbox1 = (self.rect1.centerx + 17, self.rect1.centery + 2, 31, 57)#Barra de vida
        self.health = 10 #Vida para jugador 1
        self.health1 = 10 #Vida para el jugador 2
        self.visible = True 
        
        self.sonidodisparo = pygame.mixer.Sound ('disparar.wav') #Sonido del disparo
    
    def send_data(self):
        """
        Send position to server
        :return: None
        """       
        data = str(self.net.id) + ":" + str(self.rect.centerx) + "," + str(self.rect1.centery)
        reply = self.net.send(data)
        return reply

    @staticmethod
    def parse_data(data):
        try:
            d = data.split(":")[1].split(",")
            return int(d[0]), int(d[1])
        except:
            return 0,0

    def movimientoDerecha (self): #Movimiento de derecha (Jugador1)
        self.rect.right += self.velocidad1
        self.__movimiento ()
    def movimientoIzquierda (self): #Movimiento de izquierda (Jugador1)
        self.rect.left -= self.velocidad1
        self.__movimiento ()
    def movimientoderecha (self): #Movimiento de derecha (Jugador2)
        self.rect1.right += self.velocidad2
        self.__movimiento ()
    def movimientoizquierda (self): #Movimiento de izquierda (Jugador2)
        self.rect1.left -= self.velocidad2
        self.__movimiento ()

        
    def __movimiento (self): # Instrucciones de movimiento para carro1 y carro2

        if self.Vida1 == True and self.Vida2 == True:
            if self.rect.left <=0:
                self.rect.left = 0
            elif self.rect.right >870:
                self.rect.right = 840
            if self.rect.top > 400:
               self.rect.top = 1
            elif self.rect.bottom > 900:
               self.rect.bottom = 2
               
    def destruccion(self): #Funcion cuando los carror 'muere'
        self.Vida1 = False
        self.Vida2 = False 
        self.velocidad1 = 0
        self.velocidad2 = 0
        
        
    def disparar1 (self, x,y): #Funcion para el disparo del Jugador1
        miBala = Bala (x,y, 'bala.png', True) #Imagen del disparo del Jugador1
        self.listaDisparo1.append(miBala)#Agrega la imagen a la lista de disparo
        self.sonidodisparo.play () # Inicia el sonido de disparo
    def disparar2 (self, x,y): #Funcion para el disparo del Jugador2
        miBala = Bala (x,y, 'bala.png', True) #Imagen del disparo del Jugador2
        self.listaDisparo2.append(miBala)#Agrega la imagen a la lista de disparo
        self.sonidodisparo.play () # Inicia el sonido de disparo
        
    def hit(self):#Barra para la vida del Jugador1
        if self.health > 0:
            self.health -= 1

    def hit1(self): #Barra para la vida del Jugador2
        if self.health1 > 0:
            self.health1 -= 1


    def dibujar (self, superficie): #Dibuejar todos los elementos de los jugadores
        if self.visible:
            pygame.draw.rect(superficie, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10)) 
            pygame.draw.rect(superficie, (0,128,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
            
            pygame.draw.rect(superficie, (255,0,0), (self.hitbox1[0], self.hitbox1[1] - 20, 50, 10)) 
            pygame.draw.rect(superficie, (0,128,0), (self.hitbox1[0], self.hitbox1[1] - 20, 50 - (5 * (10 - self.health1)), 10))
            
            self.hitbox = (self.rect.left +17, self.rect.top +2, 31, 57)
            self.hitbox1 = (self.rect1.left +17, self.rect1.top +2, 31, 57)
            
        superficie.blit (self.IPlayer1, self.rect)
        superficie.blit (self.IPlayer2, self.rect1)#Dibujar elo jugador1
        
class Enemigo (pygame.sprite.Sprite):  #Clase para los carros enemigos
    
    def __init__ (self, x, y, distancia, imagenA, imagenB):
        pygame.sprite.Sprite. __init__ (self)
        
        self.imagenenemigo1 = pygame.image.load (imagenA) #Imagen 1, del enemigo
        self.imagenenemigo2 = pygame.image.load (imagenB) #Imagen 2, del enemigo

        self.listaImages = [self.imagenenemigo1, self.imagenenemigo2] #Lista de las imagenes de los enemigos
        self.posImagen = 0 #Posicion en que inicia las imagenes de los enemigos

        self.imagenEnemigo = self.listaImages [self.posImagen] #Posicion en que inicia las imagenes de los enemigos
        self.rect = self.imagenEnemigo.get_rect()
        
        self.listaDisparo = [] #Lista para los disparos de los enemigos
        self.velocidad = 1 #Velocidad de enemigos
        self.rect.top = y #Posicion en y
        self.rect.left = x #Posicion en x
        self.rangoDisparo = (1)
        self.tiempoCambio = 5
        self.conquista = False 
        self. derecha = True
        self.contador = 0
        self.Maxdescenso = self.rect.top + 100
        self.limiteDerecha= x + distancia
        self.limiteIzquierda= x - distancia
        self.hitbox = (self.rect.left + 17, self.rect.top + 2, 31, 57)
        self.health = 10 # NEW
        self.visible = True # NEW
        
    def dibujar (self, superficie): #Dibujar elementos de los enemigos
        if self.visible:                
            pygame.draw.rect(superficie,  (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10)) 
            pygame.draw.rect(superficie,   (0,128,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
            self.hitbox = (self.rect.left +17, self.rect.top +2, 31, 57)
        self.imagenEnemigo = self.listaImages[self.posImagen]                    
        superficie.blit(self.imagenEnemigo, self.rect)                         
        
    def comportamientoImages (self, tiempo): # Funcion para el cambio de imagenes de los enemigos
        if self.conquista == False:
            self.__movimientos()

            self.__ataque()
            if self.tiempoCambio == tiempo:
                self.posImagen += 1
                self.tiempoCambio += 1
            
                if self.posImagen > (len (self.listaImages)-1):
                    self.posImagen = 0
                    
    def __movimientos (self): #Movimiento enemigo
        if self.contador < 2:
            self.__movimientolateral()
        else:
             self.__descenso()
        
    def __descenso (self):
        if self.Maxdescenso == (self.rect.top-20):
            self.contador =0
            
        else:
            self.rect.top -= 1
            
    def __movimientolateral(self): #Movimiento lateral
        if self.derecha == True:
            self.rect.left = self.rect.left + self.velocidad
            if self.rect.left > self.limiteDerecha:
                self.derecha = False
                self.contador += 1
        else:
            self.rect.left = self.rect.left - self.velocidad
            if self.rect.left < self.limiteIzquierda:
                self.derecha = True
                self.contador += 1
                
    def __ataque(self): #Ataque de los enemigos
        if (randint(0,1000)<self.rangoDisparo):
            self.__disparo()
            
    def __disparo(self): #Disparo de los enemigos
        x,y = self.rect.center
        miBala = Bala (x,y, 'bala.png',False)
        self.listaDisparo.append(miBala)
        
    def hit(self): #Vida de los enemigos
        if self.health > 0:
            self.health -= 1

            
                
class Bala (pygame.sprite.Sprite): #Clase para los disparos de la nave jugador y para los enemigos
    
    def __init__ (self, x, y, ruta, personaje):
        pygame.sprite.Sprite. __init__ (self)
        self.imagenproyectil = pygame.image.load (ruta)
        self.rect = self.imagenproyectil.get_rect ()
        self.velocidadDisparo = 4
        self.rect.top = y
        self.rect.left = x

        self.disparoPersonaje = personaje
        
    def trayectoria (self): #Trayectoria de la bala
        if self. disparoPersonaje == True:
            self.rect.top = (self.rect.top - self.velocidadDisparo)
        else: self.rect.top = self.rect.top + self.velocidadDisparo
        
    def dibujar (self, superficie): #Dibuja elementos de la bala
        superficie.blit(self.imagenproyectil, self.rect)
        
def cargarEnemigos(): #Funcion para la posicion de los enemigos

        enemigo = Enemigo(100,400,90, 'E1.png', 'E1.png')
        listaEnemigo.append (enemigo)

        enemigo = Enemigo(200,400,150, 'E1.png', 'E1.png')
        listaEnemigo.append (enemigo)

        enemigo = Enemigo(300,400,100, 'E1.png', 'E1.png')
        listaEnemigo.append (enemigo)

        enemigo = Enemigo(400,400,250, 'E1.png', 'E1.png')
        listaEnemigo.append (enemigo)
        
def detenerJuego(): #Funcion para cuando se pierde 
    for enemigo in listaEnemigo:
        for disparo in enemigo.listaDisparo:
            enemigo.listaDisparo.remove(disparo) #Para que el disparo desaparezca
            enemigo.conquista = True # Para que se detenga todo


    
   
def Guardar(): #Guardar datos de los usuarios
    usuarios = []
    guardar = entradaU.get()
    usuarios.append(guardar)
    usuario.append (guardar)
    datos = json.dumps(usuario)
    fill = open('nicks.txt','w')
    fill.write(datos)
    fill.close()
    
ventana = Tk() #Ventana para el menu
usuario = []

ventana.title ('Menu') #Titulo
ventana.geometry ('400x450-500-150') #Medidas
ventana.config(bg = 'black')
    
imagen = PhotoImage( file= "carros.png") #Fondo
foto = Label (ventana, image = imagen).place(x= 0, y=0)

nombreJuego=Label(ventana,text="DakarDeath",font=('Times New Roman',20)).place(x=125,y=5)

nickname=Label(ventana,text="Ingrese su Nickname",font=('Times New Roman',15)).place(x=100,y=200)
entradaU = StringVar()
user = Entry (ventana, textvariable=entradaU). place(x= 125, y=260)
botonJugar = Button(ventana, text= 'Iniciar partida',command = lambda: main(ventana), font = ('Times New Roman',14)).place(x= 130, y=300)

continuar = Button (ventana, text= 'Guardar',command=Guardar, font = ('Times New Romn', 14), width = 6).place(x= 280, y= 250)


def main (ventana):
    pygame.init()
    ventana.destroy() #Destruir ventana menu
    pygame.mixer.music.stop() #Detener musica
    pantalla = pygame.display.set_mode((900, 500)) #Medidas
    pygame.display.set_caption ('DakarDeath') #Titulo
    Fuente = pygame.font.SysFont('Arial', 20)
    Texto1 = Fuente.render('WINNER: PLAYER 1',0,(100,45,0))
    Texto2 = Fuente.render('WINNER: PLAYER 2',0,(100,45,0))
    pygame.mixer.music.load ('aceleracion_1.wav') #Musica de fondo 
    pygame.mixer.music.play(2)
    score1 = 0 #Puntaje 1
    score2 = 0 #Puntaje 2
    #Objetos

    jugadores = Player ()
    cargarEnemigos()
    enJuego = True
    while True:

        pantalla.fill ((255,255,255))
        aux = 0
        tiempo = int (pygame.time.get_ticks()/1000)
        if aux == tiempo:
            aux +=1 
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN: #Teclas para di
                if event.key == K_q:
                    x,y = jugadores.rect1.center
                    jugadores.disparar1(x,y)
                    
                if event.key == K_SPACE:
                    x,y = jugadores.rect.center
                    jugadores.disparar2(x,y)
       ###### MOVIMIENTO DEL JUGADOR 1 #####             
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            jugadores.rect.top -= jugadores.velocidad1
        if keys[pygame.K_DOWN]:
            jugadores.rect.bottom += jugadores.velocidad1
        if keys[pygame.K_LEFT]:
            jugadores.movimientoIzquierda()
        if keys[pygame.K_RIGHT]:
            jugadores.movimientoDerecha()
        ##### MOVIMIENTO DEL JUGADOR 2 #####    
        if keys[pygame.K_a]:
            jugadores.movimientoizquierda()
        if keys[pygame.K_s]:
            jugadores.rect1.bottom += jugadores.velocidad2
        if keys[pygame.K_d]:
            jugadores.movimientoderecha()            
        if keys[pygame.K_w]:
            jugadores.rect1.bottom -= jugadores.velocidad2

        jugadores.rect.centerx, jugadores.rect.centery = jugadores.parse_data(jugadores.send_data())

        if len (jugadores.listaDisparo1)>0: #Cuando el jugador dispara
            for x in jugadores.listaDisparo1:
                x.dibujar (pantalla)
                x.trayectoria()
                
                if x.rect.top <-10:
                    jugadores.listaDisparo1.remove (x)
                else:
                    for enemigo in listaEnemigo:
                        if x.rect.colliderect(enemigo.rect):
                            score1 += 1
                            
                            
                            
        if len (jugadores.listaDisparo2)>0: #Cuando el jugador dispara
            for x in jugadores.listaDisparo2:
                x.dibujar (pantalla)
                x.trayectoria() 
                if x.rect.top <-10:
                    jugadores.listaDisparo2.remove (x)
                else:
                    for enemigo in listaEnemigo:
                        if x.rect.colliderect(enemigo.rect):
                            score2 += 1
                            
        if jugadores.rect.colliderect(jugadores.rect1): #Cuando chocan ambos carros
            jugadores.hit()
            jugadores.hit1()
            
        if jugadores.health == 0:
            jugadores.destruccion()
            enJuego=False
            detenerJuego()
            
        if jugadores.health1 == 0:
            jugadores.destruccion()
            enJuego=False
            detenerJuego()
            
        if len (listaEnemigo)>0: #Cuando el invasor dispara 
                    for enemigo in listaEnemigo:
                        enemigo.comportamientoImages(tiempo)
                        enemigo.dibujar(pantalla)
                        
                            
                        if len (enemigo.listaDisparo)>0:
                            for x in enemigo.listaDisparo:
                                x.dibujar (pantalla) #Dibujar disparo del enemigo
                                x.trayectoria()
                                
                                if x.rect.colliderect(jugadores.rect): #Cuando le disparan al jugador1
                                    jugadores.hit()                                                                    
                                if x.rect.colliderect(jugadores.rect1): #Cuando le disparan al jugador2
                                    jugadores.hit1()
                                    
                                if x.rect.top >100:
                                    enemigo.listaDisparo.remove (x)
                                else: 
                                    for disparo in jugadores.listaDisparo1: 
                                        if x.rect.colliderect (disparo.rect):
                                            jugadores.listaDisparo1.remove(disparo)
                                            enemigo.listaDisparo.remove(x)
                                            
                                    for disparo in jugadores.listaDisparo2:
                                        if x.rect.colliderect (disparo.rect):
                                            jugadores.listaDisparo2.remove(disparo)
                                            enemigo.listaDisparo.remove(x)
        #Dibujar objetos en la pantalla
        
        puntuacion1 = Fuente.render ('Score 1: ' + str (score1),0,(100,45,0))
        puntuacion2 = Fuente.render ('Score 2: ' + str (score2),0,(100,40,0))
        contador = Fuente.render('Tiempo: ' + str(tiempo), 0, (100,45,0))
        jugadores.dibujar(pantalla)
        pantalla.blit(contador, (0,0))
        pantalla.blit(puntuacion1, (0, 15))
        pantalla.blit(puntuacion2, (0, 30))
        
        if enJuego == False:
            tiempo = 0
            
            if score1 > score2:
                pantalla.blit(Texto1,(300,300))
            else:
                pantalla.blit(Texto2, (300,300))#Mostrar texto cuando se pierde

            pygame.mixer.music.stop() #Detener musica de fondo
             
        pygame.display.update()

