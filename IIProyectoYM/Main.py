import json 
import pygame 
import tkinter 
import random
import pygame, sys
from menu import*

def main (ventana):
    ventana.destroy()
    pygame.init()
    pantalla = pygame.display.set_mode((640, 480))
    pygame.display.set_caption ('DakarDeath')
    Fuente = pygame.font.SysFont('Arial', 20)


    while True:
        pantalla.fill ((255,255,255))
        aux = 1
        tiempo = int (pygame.time.get_ticks()/1000)
        if aux == tiempo:
            aux +=1 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        contador = Fuente.render('Tiempo: ' + str(tiempo), 0, (100,45,0))
        pantalla.blit(contador, (0,0))
        pygame.display.update()
main ()
