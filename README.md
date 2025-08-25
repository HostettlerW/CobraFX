# CobraSuite
A collection of python libaries to aid in development with Pygame. 

## Modules

### CobraFX
Graphics library. Handles animations, svg images with on-the-fly color reprogramming, and simple progress bars.

### CobraRender
Provides resolution management tools to pygame. Since pygame x/y coordinates are determined by the resolution of the window, programming for multiple resolutions presents a challenge when trying to place game objects. With CobraRender, a frame can be drawn on a pygame surface at a set size (1080p recomended), and then the WindowManager object will scale that frame to your windows true resolution. This takes the place of your standard pygame flip() function. WindowManager also takes on the role of providing a pygame fps clock and window renaming.