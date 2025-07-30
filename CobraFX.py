import pygame
from io import BytesIO

# Will Hostettler
# Version 1
# Features: Static and Dynamic animations. SVG images.

# Easy way to create animations at any FPS independent of the main game's FPS
# Folder Format: META.txt, each frame labeled starting at zero.
# META.txt: Line 1, main game FPS (probably 60). Line 2, animation FPS. Line 3, frame count of the animation.
class StaticAnimation():
    def __init__(self, fp: str, type: str):
        self.folderPath = fp
        self.currentFrame = 0
        self.selfFrame = 0
        # SubFile function.
        def sf(fileName: str):
            return self.folderPath + "/" + fileName
        
        with open(sf("META.txt"), "r") as file:
            lines = file.readlines()
            self.logicFPS = int(lines[0])
            self.thisFPS = int(lines[1])
            self.frameCount = int(lines[2])

        self.images = []
        for i in range(self.frameCount):
            imageLocation = sf(str(i) + type)
            self.images.append(pygame.image.load(imageLocation).convert_alpha())

        totalTime = self.frameCount / self.thisFPS
        self.frameLimit = totalTime * self.logicFPS
        self.frameDelay = self.logicFPS / self.thisFPS
        self.frameMap = []
        for i in range(self.frameCount):
            self.frameMap.append(i * self.frameDelay)


    # Pushes the logic forward in the animation, should be called every frame
    # Will return the correct image according to its internal FPS
    def pulse(self):
        if self.currentFrame == self.frameLimit:
            self.currentFrame = 0
        if self.currentFrame in self.frameMap:
            self.selfFrame = self.frameMap.index(self.currentFrame)
        self.currentFrame = self.currentFrame + 1
        #print(str(self.currentFrame) + " " + str(self.selfFrame))
        return self.images[self.selfFrame]
    
    def scale(self, scale: float):
        index = 0
        for frame in self.images:
            self.images[index] = pygame.transform.scale_by(frame, scale)
            index = index + 1

    def freeScale(self, scaleX: float, scaleY: float):
        index = 0
        for frame in self.images:
            self.images[index] = pygame.transform.scale_by(frame, (scaleX, scaleY))
            index = index + 1


    

# A container for static animations. Useful for character animation.
# A DynamicAnimation folder should just contain StaticAnimation subfolders
class DynamicAnimation():
    def __init__(self, path: str, type: str, main: str, scale: float):
        self.folderPath = path
        self.mainName = main
        self.type = type
        self.activeAnimation = StaticAnimation((path + "/" + main), type)
        self.scale = scale
        self.activeAnimation.scale(self.scale)
    def pulse(self):
        return self.activeAnimation.pulse()
    
    # Takes the name of a new subfolder as a parameter. The animation will now load from that folder.
    def shift(self, newName: str):
        self.mainName = newName
        self.activeAnimation = StaticAnimation((self.folderPath + "/" + newName), self.type)
        self.activeAnimation.scale(self.scale)
    
    def rescale(self, newScale: float):
        self.scale = newScale
        self.activeAnimation.scale(self.scale)


# SVG Image translates an svg file into a scalable (rasterized scale only) pygame image.
# Any element that uses color #ff0000 can be overridden. Great for customizable assets. Edits a stored copy of the svg data.
# Pygame image is retrieved by simply using the objects "image" variable
# The object has no usable image by default. Rasterize generates one from the data directly. setSize generates one at scale.
class svgImage:
    def __init__(self, path: str):
        self.filePath = path
        with open(path, "r") as file:
            self.plaintext = file.read()
        self.color = "#ff0000"
        self.baseScale = 1.0
        self.xStretch = 0.0
        self.yStretch = 0.0
    # Standard render without scaling
    def rasterize(self):
        svgBytes = self.plaintext.encode("utf-8")
        svg_stream = BytesIO(svgBytes)
        self.image = pygame.image.load(svg_stream).convert_alpha()
    def replaceColor(self, hex: str):
        self.plaintext = self.plaintext.replace(self.color, hex)
        self.color = hex
    def setSize(self, base: float, xstr: int, ystr:int):
        self.baseScale = base
        # Stretch ranges from levels -5 to 5
        def convertToMult(level: int):
            start = 1.0
            convert = float(level) * 0.1
            return start + convert
        self.xStretch = self.baseScale * convertToMult(xstr)
        self.yStretch = self.baseScale * convertToMult(ystr)
        self.rasterize()
        self.image = pygame.transform.scale_by(self.image, (self.xStretch, self.yStretch))

# A simple progress bar.
class ProgressBar:
    # Takes pygame surface, x-y coords, width and height of the bar, progress (0 - 100), and colors for back and front
    def __init__(self, screen, x: int, y: int, width: int, height: int, progress: int, colorBG: str, colorFR: str):
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.prog = progress
        self.colorBG = colorBG
        self.colorFR = colorFR
        self.screenRef = screen
    def update(self, new: int):
        self.prog = new
    def render(self):
        # Background Bar
        pygame.draw.rect(self.screenRef, self.colorBG, (self.x, self.y, self.w, self.h))
        # Foreground Bar
        # Progress is given as a percentage from 0 to 100
        percent = float(self.prog) / 100.0
        calcWidth = int(float(self.w) * percent)
        pygame.draw.rect(self.screenRef, self.colorFR, (self.x, self.y, calcWidth, self.h))