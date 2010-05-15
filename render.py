import pygame
from view_port import ViewPort2D

class Renderer2D(object):
    def __init__(self, location, screen, screenRes, grid, gridSize):
        self.screen = screen
        self.screenRes = screenRes
        self.gridWidth, self.gridHeight = gridSize
        self.grid = grid

        self.view = ViewPort2D(location, screenRes, gridSize)
        self.surface = pygame.Surface(gridSize)
        self.regenerate_surface()

    def regenerate_surface(self):
        """ Regenerates the main game surface - SLOW! """
        for x in xrange(0, self.gridWidth):
            for y in xrange(0, self.gridHeight):
                self.update_square((x, y, self.view.z))
    
    def update_square(self, location):
        """ Updates a single grid square in the display """
        x, y, z = location
        terrainNode = self.grid.get_node_at(location)
        if terrainNode is not None:
            rect = pygame.Rect(x, y, 1, 1)
            terrainNode.contents.render(rect, self.surface)

    def render_terrain(self):
        """ Renders the viewable terrain onto the screen """
        area = pygame.Rect(self.view.x, self.view.y,
            self.view.columns, self.view.rows)
        viewArea = self.surface.subsurface(area)
        pygame.transform.scale(viewArea, self.screenRes, self.screen)

    def render_objects(self, objects):
        """ Renders renderable objects (e.g. movers) """
        for obj in objects:
            loc = obj.get_location()
            if self.view.contains(loc):
                screenX, screenY = self.view.grid2screen(loc)
                rect = pygame.Rect(screenX, screenY,
                        self.view.blockSize,
                        self.view.blockSize)
                obj.render(rect, self.screen)
