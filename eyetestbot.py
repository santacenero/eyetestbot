#!/usr/bin/env python
# encoding: utf8
#-------------------------------------------------------------------------------
# Nombre:      eyetestbot.py
# Proposito:   Simulacion de una partida al juego https://www.igame.com/eye-test/
#
# Autor:       santacenero
#
# Creado:      28/06/2015
# Copyright:   (c) santacenero 2015
#-------------------------------------------------------------------------------

#Librerias
import ImageGrab, Image
import collections
import time
import win32api, win32con


#Simular click
def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)


#Programa principal
for i in range(1,600):

    #Area de la matriz de colores
    #Deber ser configurada según la resolución del ordenador
    x1, x2 = 646,982
    y1, y2 = 263,597

    rango_x = range(x1,x2)
    rango_y = range(y1,y2)

    bbox=(x1,y1,x2,y2)

    mapa = []


    #Captura la imagen
    image = ImageGrab.grab(bbox)
    ImageGrab.grab(bbox).save("screen_capture_" + str(i) + "_.bmp", "BMP")

    #Obtengo el borde
    image_borde = image.filter(ImageFilter.CONTOUR)
    image_borde.save('borde_' + str(i) + '.png')

    #Me quedo solo con las coordenadas de color blanco de la imagen filtrada
    #pero con el color del original
    image_filtrada = Image.new("RGB", image.size, "white")
    for x in range(0,image.size[0]):
        for y in range(0,image.size[1]):
            color = image_borde.getpixel((x, y))
            if color == (255,255,255):
                image_filtrada.putpixel((x,y),image.getpixel((x, y)))
    image_filtrada.save('filtrada_' + str(i) + '.png')

    #Blanqueo pixeles aislados que hayan quedado
    image_filtrada2 = Image.new("RGB", image.size, "white")
    for x in range(0,image.size[0]):
        for y in range(0,image.size[1]):
            color = image_filtrada.getpixel((x, y))
            if color <> (255,255,255):
                try:
                    color_arr = image_filtrada.getpixel((x, y-1))
                    color_aba = image_filtrada.getpixel((x, y+1))
                    color_der = image_filtrada.getpixel((x+1, y))
                    color_izq = image_filtrada.getpixel((x-1, y))

                    if color_arr == (255,255,255) and color_aba == (255,255,255) and color_der == (255,255,255) and color_izq == (255,255,255):
                        image_filtrada2.putpixel((x,y),(255,255,255))
                    else:
                        image_filtrada2.putpixel((x,y),image_filtrada.getpixel((x, y)))

                except:
                    print "Error"
                    err = 1


    image_filtrada2.save('filtrada2_' + str(i) + '.png')
    image_full = ImageGrab.grab()
    data = image_filtrada2.getcolors()

    data2 = []
    for d in data:
        if d[1] not in [(255,255,255), (254,254,254)]:
            data2.append(d)

    sorted_by_color = sorted(data2, key=lambda tup: tup[0])
    color_target = sorted_by_color[len(sorted_by_color)-2][1]

    for y in rango_y:
        find = False
        for x in rango_x:
            color = image_full.getpixel((x, y))
            if color == color_target:
                click(x,y)
                find = True
                break

        if find:
            break
