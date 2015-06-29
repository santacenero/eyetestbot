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
for i in range(1,200):

    #Area de la matriz de colores
    #Deber ser configurada según la resolución del ordenador
    rango_x = range(922,1258)
    rango_y = range(286,621)
    bbox=(922,286,1258,621)

    mapa = []

    #Captura la imagen
    image = ImageGrab.grab(bbox)
    ImageGrab.grab(bbox).save("screen_capture_" + str(i) + "_.bmp", "BMP")
    image_full = ImageGrab.grab()
    data = image.getcolors()

    #Elimina el color blanco
    data2 = []
    for d in data:
        if d[1] not in [(255,255,255), (254,254,254)]:
            data2.append(d)

    #Ordena por colores
    sorted_by_color = sorted(data2, key=lambda tup: tup[0])

    if i <= 69: a = 2
    if i > 69 and a < 85 : a = 3
    if i >= 85 : a = 4

    #Selecciona el color objetivo (normalmente el segundo con más pixels)
    color_target = sorted_by_color[len(sorted_by_color)-a][1]

    #Busca un pixels del color objetivo
    for y in rango_y:
        find = False
        for x in rango_x:
            color = image_full.getpixel((x, y))
            if color == color_target:
                #Y hace click
                click(x+5,y+5)
                find = True
                break
        if find:
            break

