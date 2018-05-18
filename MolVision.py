import pygame
from pygame.locals import *
import pybel
import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


def get_atoms(smile):
    molecule = pybel.readstring('smi', smile)
    molecule.make3D()
    return molecule.atoms


if __name__=="__main__":
    smile = input("Введите молекулу в формате SMILE (например, пропилен -> C=CC):")
    atoms = get_atoms(smile)
    
    atoms_base = [[None]*4 for i in range(len(atoms))]

    for i in range(len(atoms)):
        atoms_base[i][0] = atoms[i].type
        atoms_base[i][1] = list(map(str, atoms[i].coords))[0]
        atoms_base[i][2] = list(map(str, atoms[i].coords))[1]
        atoms_base[i][3] = list(map(str, atoms[i].coords))[2]

    for atom in atoms:
        print(atom.type, ' '.join(map(str, atom.coords)))


class Molecule(object):
    def __init__(self, atoms):
        self.atoms = atoms


    def load_from_file(self, fn):
        atoms = []
        with open(fn) as f:
            for l in f:
                el, x, y, z = l.split()
                self.atoms.append(
                    (el, float(x), float(y), float(z)))
        return cls(atoms)


def quadric():
    quad = gluNewQuadric()
    return quad


def sphere(quad, dx, dy, dz, r, g, b, radius):
    longitude = 10
    lat = 10

    glPushMatrix()
    glColor3f(r, g, b)
    glTranslatef(dx, dy, dz)
    gluSphere(quad, radius, longitude, lat)
    glPopMatrix()


def main():
    pygame.init()
    display = (800, 700)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    lightpos = (1.0, 1.0, 1.0)
    pygame.display.set_caption('Молекула')
    glLightfv(GL_LIGHT0, GL_POSITION, lightpos)
    gluPerspective(110, (display[0]/display[1]), 0.01, 10.0)
    

    glTranslatef(0.0,0.0, -5)

    quad = quadric()

    while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            glRotatef(0.4, 0, 0.5, 0)
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            glClearColor(0, 0, 0, 1)

            for i in range(len(atoms_base)):
                dx = float(atoms_base[i][1])
                dy = float(atoms_base[i][2])
                dz = float(atoms_base[i][3])
                if atoms_base[i][0] == 'C3' or atoms_base[i][0] == 'C2' or atoms_base[i][0] == 'Car':
                    sphere(quad, dx, dy, dz, 255, 255, 0, 0.7)
                elif atoms_base[i][0] == 'H':
                    sphere(quad, dx, dy, dz, 0, 255, 0, 0.5)
                elif atoms_base[i][0] == 'HO':
                    sphere(quad, dx, dy, dz, 0, 255, 255, 0.62)
                elif atoms_base[i][0] == '02' or atoms_base[i][0] == '03':
                    sphere(quad, dx, dy, dz, 255, 0, 0, 0.6)
                elif atoms_base[i][0] == 'N3':
                    sphere(quad, dx, dy, dz, 128, 0, 128, 0.52)    
                else:
                    sphere(quad, dx, dy, dz, 55, 0, 255, 0.6)


            pygame.display.flip()
            pygame.time.wait(10)



main()
