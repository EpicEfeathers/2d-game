import pygame
import numpy as np

def generate_terrain():
    arr = np.loadtxt('map.txt', dtype=int)  
    return arr