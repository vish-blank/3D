import sys
import math

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtCore import Qt
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt


class Viewport(QOpenGLWidget):
    def __init__(self):
        super().__init__()

        self.distance = 8.0
        self.yaw = 45.0
        self.pitch = 30.0

        self.target_x = 0.0
        self.target_y = 0.0
        self.target_z = 0.0

        self.last_mouse_x = 0
        self.last_mouse_y = 0
        self.mouse_button = None

    def initializeGL(self):
        glClearColor(0.08, 0.08, 0.08, 1.0)
        glEnable(GL_DEPTH_TEST)

    def resizeGL(self, width, height):
        if height == 0:
            height = 1

        glViewport(0, 0, width, height)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, width / height, 0.1, 1000.0)

        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        yaw = math.radians(self.yaw)
        pitch = math.radians(self.pitch)

        camera_x = self.target_x + self.distance * math.cos(pitch) * math.sin(yaw)
        camera_y = self.target_y + self.distance * math.sin(pitch)
        camera_z = self.target_z + self.distance * math.cos(pitch) * math.cos(yaw)

        gluLookAt(
            camera_x,
            camera_y,
            camera_z,
            self.target_x,
            self.target_y,
            self.target_z,
            0.0,
            1.0,
            0.0
        )

        self.draw_axes()
        self.draw_cube()

    def draw_axes(self):
        glLineWidth(2.0)

        glBegin(GL_LINES)

        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(-3.0, 0.0, 0.0)
        glVertex3f(3.0, 0.0, 0.0)

        glColor3f(0.0, 1.0, 0.0)
        glVertex3f(0.0, -3.0, 0.0)
        glVertex3f(0.0, 3.0, 0.0)

        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(0.0, 0.0, -3.0)
        glVertex3f(0.0, 0.0, 3.0)

        glEnd()

    def draw_cube(self):
        vertices = [
            (-1, -1, -1),
            (1, -1, -1),
            (1, 1, -1),
            (-1, 1, -1),
            (-1, -1, 1),
            (1, -1, 1),
            (1, 1, 1),
            (-1, 1, 1)
        ]

        faces = [
            (0, 1, 2, 3),
            (4, 5, 6, 7),
            (0, 1, 5, 4),
            (2, 3, 7, 6),
            (0, 3, 7, 4),
            (1, 2, 6, 5)
        ]

        colors = [
            (1.0, 0.0, 0.0),
            (0.0, 1.0, 0.0),
            (0.0, 0.0, 1.0),
            (1.0, 1.0, 0.0),
            (1.0, 0.0, 1.0),
            (0.0, 1.0, 1.0)
        ]

        glBegin(GL_QUADS)

        for i, face in enumerate(faces):
            glColor3f(*colors[i])

            for vertex in face:
                glVertex3f(*vertices[vertex])

        glEnd()

    def mousePressEvent(self, event):
        self.mouse_button = event.button()
        self.last_mouse_x = event.position().x()
        self.last_mouse_y = event.position().y()

    def mouseReleaseEvent(self, event):
        self.mouse_button = None

    def mouseMoveEvent(self, event):
        x = event.position().x()
        y = event.position().y()

        dx = x - self.last_mouse_x
        dy = y - self.last_mouse_y

        self.last_mouse_x = x
        self.last_mouse_y = y

        if self.mouse_button == Qt.MouseButton.LeftButton:
            self.yaw += dx * 0.5
            self.pitch -= dy * 0.5
            self.pitch = max(-89.0, min(89.0, self.pitch))
            self.update()

        elif self.mouse_button == Qt.MouseButton.MiddleButton:
            pan_speed = self.distance * 0.002

            self.target_x -= dx * pan_speed
            self.target_y += dy * pan_speed

            self.update()

    def wheelEvent(self, event):
        delta = event.angleDelta().y()

        if delta > 0:
            self.distance *= 0.9
        else:
            self.distance *= 1.1

        self.distance = max(1.0, min(100.0, self.distance))

        self.update()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("3D Modeller")
        self.resize(1000, 700)

        self.viewport = Viewport()
        self.setCentralWidget(self.viewport)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())