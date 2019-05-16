from tkinter import *
import json 
import pygame
from network import Network
pygame.init()
pygame.mixer.music.load ('FondoMenu.wav') #Musica de fondo 
pygame.mixer.music.play(2)

class Player(pygame.sprite.Sprite): #Clase de los jugadores
    
    def __init__ (self):
        #Funcion para la imagen y la posicion inicial de los carros jugadores 
        pygame.sprite.Sprite. __init__ (self)
        self.IPlayer1 = pygame.image.load ('carro1.png') #Imagen del primer carro jugador 
        self.IPlayer2 = pygame.image.load ('carro2.png')# Imagen del segundo carro jugador
        self.ImgagenExplosion = pygame.image.load('.png') #Imagen para cuando le disparan a la nave
        self.rect = self.IPlayer1.get_rect ()
        self.rect = self.IPlayer2.get_rect ()
        self.rect.centerx = (450) #Posicion en x de la nave
        self.rect.centery = (410) #Posicion en y de la nave
        self.rect.centera = (460)
        self.rect.centerb = (420)
        self.listaDisparo1 = [] #Lista para que el carro1 pueda disparar
        self.listaDisparo2 = [] # Lista para que el carro2 pueda disparar 
        self.Vida1 = True
        self.Vida2 = True
        self.velocidad1 = 20 #Movimiento del carro1
        self.velocidad2 = 20 #Movimiento del carro2 
        
        self.sonidodisparo = pygame.mixer.Sound ('Sonido/disparar.wav') #Sonido del disparo

    def movimientoDerecha (self):
        self.rect.right += self.velocidad
        self.__movimiento ()
    def movimientoIzquierda (self):
        self.rect.left -= self.velocidad
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
    def destruccion(self): #Funcion cuando la nave 'muere'
        self.Vida1 = False
        self.Vida2 = False 
        self.velocidad = 0
        self.ImagenNave = self.ImgagenExplosion


    
   
def Guardar():
    usuarios = []
    guardar = entradaU.get()
    usuarios.append(guardar)
    usuario.append (guardar)
    datos = json.dumps(usuario)
    fill = open('nicks.txt','w')
    fill.write(datos)
    fill.close()
    
ventana = Tk()
usuario = []

ventana.title ('Menu')
ventana.geometry ('400x450-500-150')
ventana.config(bg = 'black')
    
imagen = PhotoImage( file= "carros.png")
foto = Label (ventana, image = imagen).place(x= 0, y=0)

nombreJuego=Label(ventana,text="DakarDeath",font=('Times New Roman',20)).place(x=125,y=5)

nickname=Label(ventana,text="Ingrese su Nickname",font=('Times New Roman',15)).place(x=100,y=200)
entradaU = StringVar()
user = Entry (ventana, textvariable=entradaU). place(x= 125, y=260)
botonJugar = Button(ventana, text= 'Iniciar partida',command = lambda: main(ventana), font = ('Times New Roman',14)).place(x= 130, y=300)

continuar = Button (ventana, text= 'Guardar',command=Guardar, font = ('Times New Romn', 14), width = 6).place(x= 280, y= 250)


def main (ventana):
    pygame.init()
    ventana.destroy()
    pantalla = pygame.display.set_mode((640, 480))
    pygame.display.set_caption ('DakarDeath')
    Fuente = pygame.font.SysFont('Arial', 20)
    #Objetos

    jugadores = Player ()
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
                
        contador = Fuente.render('Tiempo: ' + str(tiempo), 0, (100,45,0))
        jugador.dibujar(pantalla)
        pantalla.blit(contador, (0,0))
        pygame.display.update()

