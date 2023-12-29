import pygame
import math

pygame.init()

width, height = 800, 800

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Solar System Simulation")

black = (0, 0, 0)
yellow = (255, 255, 0)
blue = (100, 149, 237)
red = (188, 39, 50)
white = (255, 255, 255)
green = (0, 255, 0)

window_color = black


class AstralBody:
    astronomical_unit = 149.6e9
    G = 6.67428e-11
    SCALE = 250 / astronomical_unit
    TIMESTEP = 60 * 60 * 24

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_from_sun = 0

        self.vx = 0
        self.vy = 0

    def draw(self, win):
        x = self.x * self.SCALE + width / 2
        y = self.y * self.SCALE + height / 2

        if len(self.orbit) > 2:
            updated_coordinates = []

            for coordinate in self.orbit:
                x, y = coordinate
                x = x * self.SCALE + width / 2
                y = y * self.SCALE + height / 2
                updated_coordinates.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_coordinates, 2)

        pygame.draw.circle(win, self.color, (x, y), self.radius)

    def gravity(self, other):
        other_x, other_y = other.x, other.y
        dist_x = other_x - self.x
        dist_y = other_y - self.y
        distance = math.sqrt(dist_x ** 2 + dist_y ** 2)

        if other.sun:
            self.distance_from_sun = distance

        force = self.G * (self.mass * other.mass) / distance ** 2
        theta = math.atan2(dist_y, dist_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, bodies):
        totalForce_x = totalForce_y = 0
        for body in bodies:
            if self == body:
                continue

            fx, fy = self.gravity(body)
            totalForce_x += fx
            totalForce_y += fy

        self.vx += totalForce_x / self.mass * self.TIMESTEP
        self.vy += totalForce_y / self.mass * self.TIMESTEP

        self.x += self.vx * self.TIMESTEP
        self.y += self.vy * self.TIMESTEP
        self.orbit.append((self.x, self.y))


def main():
    run = True
    clock = pygame.time.Clock()

    sun = AstralBody(0, 0, 15, yellow, 1.98892e30)
    sun.sun = True
    
    mercury = AstralBody(0.387 * AstralBody.astronomical_unit, 0, 8, white, 3.30e23)
    mercury.vy = -47400

    venus = AstralBody(0.723 * AstralBody.astronomical_unit, 0, 14, green, 4.8685e24)
    venus.vy = -35020

    earth = AstralBody(-1 * AstralBody.astronomical_unit, 0, 16, blue, 5.9742e24)
    earth.vy = 29783

    mars = AstralBody(-1.524 * AstralBody.astronomical_unit, 0, 12, red, 6.39e23)
    mars.vy = 24077

    bodies = [sun, mercury, venus, earth, mars]

    while run:
        clock.tick(60)

        window.fill(window_color)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for body in bodies:
            body.update_position(bodies)
            body.draw(window)

        pygame.display.update()

    pygame.quit()


main()
