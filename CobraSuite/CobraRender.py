import pygame
import ctypes

# CobraRender for Pygame
# William Hostettler. 2025.

# Standardized method of raising an error in this library.
def error(obj: str, problem: str):
    eString = "ERROR! (CobraRender) "
    eString = eString + obj + ": " + problem
    print(eString)
    return eString

# Primary class of CobraRender.
# WindowManager acts as a middleman between pygame screen functions and the game surface. REPLACES the flip() function.
# The goal is to allow a game to render frames to one internal surface at a set resolution, then pass that surface to WM for scaling to desired resolution.
class WindowManager:
    # The window defaults to 1080p, with the caption "Program".
    def __init__(self):
        self.outputSurface = pygame.display.set_mode((1920, 1080))
        pygame.display.set_caption("Program")
        self.clock = pygame.time.Clock()
    # WM includes an internal pygame clock object. clockTick() acts as a passthrough to pygames tick() function.
    def clockTick(self, fps: int):
        self.clock.tick(fps)
    # Renames the window caption
    def rename(self, newName: str):
        pygame.display.set_caption(newName)
    # Returns window size as a tuple.
    def getSize(self):
        return self.outputSurface.get_size()
    # Takes a surface, scales to WM resolution, then calls pygame flip function.
    def renderFrame(self, frameSurface):
        scaledFrame = pygame.transform.scale(frameSurface, self.getSize())
        self.outputSurface.blit(scaledFrame, (0,0))
        pygame.display.flip()
    # Sets windowed resolution to a preset defined below.
    def standard(self, newRes: str):
        match newRes:
            case "SD":
                self.outputSurface = pygame.display.set_mode((854, 480))
            case "HD":
                self.outputSurface = pygame.display.set_mode((1280, 720))
            case "FHD":
                self.outputSurface = pygame.display.set_mode((1920, 1080))
            case "QHD":
                self.outputSurface = pygame.display.set_mode((2560, 1440))
            case "4K":
                self.outputSurface = pygame.display.set_mode((1280, 720))
            case _:
                error("WindowManager", "Invalid Resolution Standard")
    # Turns on the pygame FULLSCREEN flag.
    def fullscreen(self, on: bool):
        if on:
            self.outputSurface = pygame.display.set_mode(self.getSize(), pygame.FULLSCREEN)
        else:
            self.outputSurface = pygame.display.set_mode(self.getSize())
    # Sets windowed resolution to user defined parameters.
    def customRes(self, newWidth: int, newHeight: int):
        self.outputSurface = pygame.display.set_mode((newWidth, newHeight))

# On laptops, Windows is probably using a screen scale over 100%. Calling this function will make the thread DPI aware, allowing for accurate window sizes.
def windowsScaleAware():
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception as e:
        error("Windows User32 Process", "Could not activate DPI awareness for thread.")