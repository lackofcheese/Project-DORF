import sys
import pygame
import time
import cPickle

from render import Renderer2D
from grid import Grid
from mover import RandomMover
from terrain import TerrainData
from terrain.generators import MeteorTerrainGenerator, Smoother
from terrain.generators import PlasmaFractalGenerator


class Game:
    def __init__(self):
        #Our main variables used within the game
        self.resolution = self.width, self.height = 800, 600
        self.gridSize = self.xGrid, self.yGrid = 320, 240
        self.movers = []
        self._fontFile = pygame.font.match_font('freemono')
        self._fontSize = 14

        #Build our main grid
        self.gameGrid = Grid()
        self.make_grid(self.gridSize)
       
        #initialize and blank the screen
        pygame.init()
        self.screen = pygame.display.set_mode(self.resolution)
        pygame.display.set_caption('Project D.O.R.F.')
        pygame.key.set_repeat(500, 33) # Key repeating
        self.font = pygame.font.Font(self._fontFile, self._fontSize)
        self.font.set_bold(True)

        self.generate_terrain()

        # Set up the renderer
        self.renderer = Renderer2D((0, 0, 0), self.screen, self.resolution,
                self.gameGrid, self.gridSize)

    def make_grid(self, gridSize):
        for x in range(0, gridSize[0]):
            for y in range(0 ,gridSize[1]):
                terrain = TerrainData()
                self.gameGrid.add_node((x, y, 0), terrain)

    def generate_terrain(self):
        generator = PlasmaFractalGenerator(200)
        generator.apply(self.gameGrid)
        self.gameGrid.connect_grid()

        generator = MeteorTerrainGenerator()
        smoother = Smoother(0.5)
        generator.apply(self.gameGrid)
        smoother.apply(self.gameGrid)

    def update_display(self):
        """ Updates the screen to show the appropriate visible nodes """
        self.renderer.render_terrain()
        self.renderer.render_objects(self.movers)

        self.frame += 1
        if time.time() - self.time > 1:
            self.time = time.time()
            self.fps = self.frame
            self.frame = 0

        text = self.font.render(str(self.renderer.view) +
                " FPS:{0}".format(self.fps), 1, (0, 255, 0))
        rect = text.get_rect()
        rect.x, rect.y = (0,0)
        self.screen.blit(text, rect)

        pygame.display.update()

    def move_movers(self):
        for mover in self.movers:
            mover.move()

    def save_grid(self):
        print "saving"
        save = file('world.pkl', 'wb')
        cPickle.dump(self.gameGrid, save)
        save.close()
        print "done saving"

    def load_grid(self):
        print "loading"
        load = file('world.pkl', 'rb')
        self.gameGrid = cPickle.load(load)
        load.close()
        self.update_terrain_surf()
        print "done loading"

    def execute(self):
        self.time = time.time()
        self.frame = 0
        self.fps = 0
        self.update_display()
        self.autoMovers = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    loc = self.renderer.view.screen2grid(event.pos)
                    if event.button == 1: # Add mover
                        rm = RandomMover(self.gameGrid, loc)
                        self.movers.append(rm)
                    if event.button == 3: # Remove mover  
                        for mover in self.movers:
                            if mover.get_location() == loc:
                                self.movers.remove(mover)
                                break

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.renderer.view.scroll((0, 1))
                    if event.key == pygame.K_UP:
                        self.renderer.view.scroll((0, -1))
                    if event.key == pygame.K_LEFT:
                        self.renderer.view.scroll((-1, 0))
                    if event.key == pygame.K_RIGHT:
                        self.renderer.view.scroll((1, 0))
                    if event.key == pygame.K_PAGEUP:
                        self.renderer.view.z += 1
                    if event.key == pygame.K_PAGEDOWN:
                        self.renderer.view.z -= 1
                    if event.key == pygame.K_z:
                        self.renderer.view.zoom_in()
                    if event.key == pygame.K_x:
                        self.renderer.view.zoom_out()
                    if event.key == pygame.K_SPACE:
                        if not self.autoMovers:
                            self.move_movers()
                    if event.key == pygame.K_t:
                        self.autoMovers = not self.autoMovers
                    if event.key == pygame.K_s:
                        self.save_grid()
                    if event.key == pygame.K_l:
                        self.load_grid()

            if self.autoMovers: self.move_movers()
            self.update_display()

if __name__ == "__main__":
    dorf = Game()
    dorf.execute()
