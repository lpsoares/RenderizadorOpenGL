#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Renderizador OpenGL.

Desenvolvido por: Luciano Soares <lpsoares@insper.edu.br>
Disciplina: Computação Gráfica
Data: 24 de Abril de 2023
"""

import glfw
import numpy as np
from renderizador.camera import *
from renderizador.utils import *
from renderizador.callbacks import *
from pyquaternion import Quaternion


class Camera:

    def __init__(self, type="examine", near=0.1, far=100, eye=[0.0, 0.0, 10.0]):
        
        # Tipos de navegação ("examine", "fly")
        self.type = type

        # Paramentros iniciais
        self.eye = np.array(eye, np.float32)
        self.at = np.array([0.0, 0.0, 0.0])
        self.up = np.array([0.0, 1.0, 0.0])
        self.fov = np.deg2rad(45.0)

        self.look_at = np.identity(4)
        
        self.near = near
        self.far = far

        # Outros
        self.front = np.array([0.0, 0.0, -1.0])
        self.right = np.array([-1.0, 0.0, 0.0])
        
        # Velocidades de manipulação
        self.mouse_speed = 0.002
        self.keyboard_speed = 0.2
        self.scroll_speed = 0.2


    def calc_look_at(self):

        # Matriz de Look At clássica
        w = normalize(self.at - self.eye)
        u = normalize(np.cross(w, self.up))
        v = normalize(np.cross(u, w))

        # Preenchendo a Matriz
        self.look_at = np.identity(4, np.float32)
        self.look_at[0,:3] = u
        self.look_at[1,:3] = v
        self.look_at[2,:3] = -w
        self.look_at[0,3] = np.dot(-u,self.eye)
        self.look_at[1,3] = np.dot(-v,self.eye)
        self.look_at[2,3] = np.dot(w,self.eye)

    
    def calc_projection(self):
        aspect = Callbacks.resolution[0]/Callbacks.resolution[1]
        fovy = 2 * np.arctan(np.tan(self.fov/2)*(1/aspect))    
        top = self.near * np.tan(fovy)
        right = top * aspect

        self.persp = np.array([[self.near/right, 0, 0, 0],
                          [0, self.near/top, 0, 0],
                          [0, 0, -(self.far+self.near)/(self.far-self.near), (-2*self.far*self.near)/(self.far-self.near)],
                          [0, 0, -1, 0]], np.float32)

        return self.persp
    

    def get_eye(self):
        return self.eye


    def get_projection_matrix(self):
        self.calc_projection()
        return self.persp


    def get_view_matrix(self):
        self.calc_look_at()
        return self.look_at


    def send_keys(self, key):
        if key == glfw.KEY_W:
            self.eye += self.front * self.keyboard_speed
        elif key == glfw.KEY_S:
            self.eye -= self.front * self.keyboard_speed
        elif key == glfw.KEY_D:
            self.eye += self.right * self.keyboard_speed
        elif key == glfw.KEY_A:
            self.eye -= self.right * self.keyboard_speed

    
    def orbit(self, offset):

        # Calculando as rotações horizontal e vertical
        qx = Quaternion(axis=np.cross(self.eye-self.at, self.up), angle=-offset[1]*self.mouse_speed)
        qy = Quaternion(axis=-self.up, angle=offset[0]*self.mouse_speed)

        # Integrando e aplicando a manipulação
        quat = qx * qy
        self.eye = quat.rotate(self.eye)
        self.up = quat.rotate(self.up)
        self.front = quat.rotate(self.front)
        self.right = quat.rotate(self.right)


    def navigate(self, offset):

        # Calculando as rotações horizontal e vertical
        #qx = Quaternion(axis=np.cross(self.eye-self.at, self.up), angle=offset[1]*self.mouse_speed)
        qx = Quaternion(axis=self.right, angle=offset[1]*self.mouse_speed)
        qy = Quaternion(axis=-self.up, angle=offset[0]*self.mouse_speed)

        # Integrando e aplicando a manipulação
        quat = qx * qy

        # m1 = np.identity(4)
        # m1[0:3,3] = self.eye[0]-self.at[0]
        m1 = np.array([[1.0, 0.0, 0.0, self.eye[0]-self.at[0]],
                       [0.0, 1.0, 0.0, self.eye[1]-self.at[1]],
                       [0.0, 0.0, 1.0, self.eye[2]-self.at[2]],
                       [0.0, 0.0, 0.0, 1.0]])

        # m2 = np.identity(4)
        # m2[0:3,3] = -(self.eye[0]-self.at[0])
        m2 = np.array([[1.0, 0.0, 0.0, -(self.eye[0]-self.at[0])],
                       [0.0, 1.0, 0.0, -(self.eye[1]-self.at[1])],
                       [0.0, 0.0, 1.0, -(self.eye[2]-self.at[2])],
                       [0.0, 0.0, 0.0, 1.0]])
        
        tmp = m1 @ quat.transformation_matrix @ m2
        self.at = (tmp @ np.append(self.at,1))[:3]
        self.up = quat.rotate(self.up)
        self.front = quat.rotate(self.front)
        self.right = quat.rotate(self.right)


    def send_mouse(self, offset):
        if self.type == "examine":
            self.orbit(offset)
        elif self.type == "fly":
            self.navigate(offset)


    def send_scroll(self, offset):
        self.fov += self.scroll_speed * offset[1]

