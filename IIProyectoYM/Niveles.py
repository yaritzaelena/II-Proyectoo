import json
import pygamen
import base64
import StringIO
import gzip

def load_ima(1.png):
    return pygame.image.load(1.png).convert_alpha()

class Niveles():
    def __init__(self):
        self.imagenes = []
        self.imagenes_de_capa = []
        self.conjunto_de_capas = []
        self.tilewidth = 0
        self.tileheight = 0
    def convertir(self, lista, col):
       
        nueva = []
        for i in range(0, len(lista), col):
            nueva.append(lista[i:i+col])
        return nueva
    def traducir(self, cadena):
        # Decodifica el mapa.
        cadena = base64.decodestring(cadena)
        # Descomprime el mapa.
        copmressed_stream = StringIO.StringIO(cadena)
        gzipper = gzip.GzipFile(fileobj=copmressed_stream)
        cadena = gzipper.read()
        salida = []
        
        #es para convertir los caracteres
        for idx in xrange(0, len(cadena), 4):
            val = ord(str(cadena[idx])) | (ord(str(cadena[idx + 1])) << 8) | \
            (ord(str(cadena[idx + 2])) << 16) | (ord(str(cadena[idx + 3])) << 24)
            salida.append(val)

        return salida
        #esta funcion es para cargar el mapa
    def cargar_mapa(self, nombre): 
        Mapa_tmx = minidom.parse(""+nivel1)
        nodo_principal = Mapa_tmx.childNodes[1]
        
        #Estas modificaciones son para poder cargar imagenes directamente...
        tileset = nodo_principal.getElementsByTagName('tileset')
        self.tilewidth = int(tileset[0].attributes.get("tilewidth").value)
        self.tileheight = int(tileset[0].attributes.get("tileheight").value)
        
        
        for j in nodo_principal.getElementsByTagName('image'):
            
            temp_ima_name = j.attributes.get("source").value
            #es para cargar una imagen
            temp_ima = load_ima(temp_ima_name)
            #creo una lista con la imagen partida en tiles....
            temp_tiles = cut_by_w_h(temp_ima,self.tilewidth,self.tileheight)
            #las agrego a una lista principal
            self.imagenes = self.imagenes+temp_tiles
        
        #buscamos el tamaño del mapa
        tamano_width = int(nodo_principal.attributes.get("width").value)
        tamano_height = int(nodo_principal.attributes.get("height").value)
        
        for i in range(len(nodo_principal.childNodes)):
            nodo_actual = nodo_principal.childNodes[i]
            #revisamos si existe un nodo...
            if nodo_actual.nodeType == 1:
                #si el nodo no es de tilesets, pregunto si es de capas...
                if nodo_actual.nodeName == "layer":
                    datos = nodo_actual.childNodes[1]
                    #quitamos saltos de linea y espacios...
                    capa = datos.childNodes[0].data.replace("\n", "").replace(" ", "")
                    capa = self.traducir(capa)
                    capa = self.convertir(capa, tamano_width)
                    self.conjunto_de_capas.append(capa)

        #esto es por que me gustan los returns XD
        return self.conjunto_de_capas
        
    def get_capa(self,num):
        #no tengo que explicarlo... ¿verdad?
        return  self.conjunto_de_capas[num]
        
    def imprime_capa(self,superficie,numero, x=0,y=0):
        #imprime una capa determinada en una superficie determinada
        capa = self.conjunto_de_capas[numero]
        
        image_num = 0
        #para calcular la posición  inicial y final
        # x=0
        # y=0
        #esto es una alluda para ver como luce en modo texto el mapa....
        print "####################"
        # empezamos el recorrido
        for fila in capa:
            x=0
            print ":",
            for columna in fila:
                #si el numero es diferente a 0...
                if columna != 0:
                    # seleccionamos la imagen, recordemos que tiled
                    # comienza a contar espacio no vacio a partir de 1
                    # pero nuestra lista de imagenes comienza en el 0
                    ima = self.imagenes[columna-1]
                    #la colocamos en el mapa...
                    superficie.blit(ima, (x,y))
                    print columna,
                # esto es simplemente para poder velo en modo texto...
                else:
                    print " ",
                #aumentamos la posición en X...
                x+=self.tilewidth
            print ":"
            # y ahora aumentamos la posición en Y...
            y+=self.tileheight
    
    def trasforma_a_imagenes(self, capa_num):
        #esto resive el numero de la capa y regresa una imagen de sus dimenciones...
        capa = self.conjunto_de_capas[capa_num]
        
        filas = len(capa)
        columnas = len(capa[0])
        # primero creamos una imagen vacia de las dimenciones de la capa...
        imagen_capa = pygame.Surface((columnas*self.tileheight, filas*self.tilewidth))
        # le fijamos un color que usaremos de trasparencia a la imagen...
        imagen_capa.fill((255,0,255))
        # sobre ella dibujamos la capa...
        self.imprime_capa(imagen_capa,capa_num)
        # y borramos el color alfa...
        imagen_capa.set_colorkey((255,0,255))
        # regresamos una copia de la imagen...
        return imagen_capa.copy()
    
    def imprime_imagen_capa(self, pantalla, pos_x=0,pos_y=0, numero=0):
        # 
        pantalla.blit(self.imagenes_de_capa[numero],(pos_x,pos_y))
    
    def hacer_colisionbox_capa(self, numero):
        # esto crea una serie de cajas de colisiones de una capa determinada
        capa = self.conjunto_de_capas[numero]
        colision_rects = []
        x=0
        y=0
        w = 0
        temp_x = 0
        for fila in capa:
            x=0
            for columna in fila:
                # esto junta por columna, las cajas de colision
                # para que sean menos
                if columna != 0:
                    if temp_x == 0 and w == 0:
                        temp_x = x
                    w+=self.tilewidth
                else:
                    if w != 0:
                        colision_rects.append(pygame.Rect(temp_x,y, w, self.tileheight))
                        w=0
                        temp_x = 0
                x+=self.tilewidth
            
            #---esto es en el caso de que la columna este llena de tiles...
            # ya que si eso ocurre, nunca se cumplira la condición del "else"
            if w != 0:
                colision_rects.append(pygame.Rect(temp_x,y, w, self.tileheight))
                w=0
                temp_x = 0
            y+=self.tileheight
        
        return colision_rects

def cut_by_w_h(imagen,w,h):
    Lista_ima = [];
    ima_w = imagen.get_width()
    ima_h = imagen.get_height()
    columnas = (ima_w/w)
    filas = (ima_h/h)
    f = 0
    c = 0
    ima_temp = pygame.Surface((w, h))
    while(f<filas):
        while(c<columnas):
            ima_temp.fill((255,255,255))
            ima_temp.set_colorkey((255,255,255))
            rect = ((c * w),(f * h),w, h)
            ima_temp.blit(imagen, (0,0), rect)
            Lista_ima.append(ima_temp.copy())
            c+=1
        c=0
        f+=1
    return Lista_ima
