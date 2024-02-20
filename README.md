# Optyka

## Description
Optyka is a Python-based game project. It uses the Pygame library for app development and includes various sound effects and GUI elements.

> [!TIP]
> Don't use this.

## Status
| Feature              | Status |
|----------------------|--------|
| Flashlight           | ✅      |
| Mirror               | ✅      |
| Lens                 | ✅❌     |
| Prism                | ✅      |
| Zwierciadlo          | ❌      |
| Transmittance factor | ✅      |
| Reflection factor    | ✅      |
| color                | ✅      |
| refractive index     | ❌      |

## Installation
There are two ways to install the project: download exe file, or run the project from source.
### Method 1
1. Clone the repository: `git clone https://github.com/Hohenzoler/optyka.git`
2. Navigate to the project directory: `cd optyka`
3. Install the required packages: `pip install -r requirements.txt`
4. Run the main script: `python main.py`

### Method 2
1. Go to the ***Releases*** page on GitHub
2. Download ***1.0 - zip***
3. Extract all the files
4. Run ***optyka.exe***


## Usage
1. Click Start.
2. You can choose:
   - new game (nothing is placed)
   - load preset (a premade project made by the developers)
   - one of your saves (if you have any)
3. Now you can place objects and see how they interact with each other.
4. `Right click` an object to pick it up and later to release it.
5. When an object is picked up, click `P` to open its parameters window.
6. Parameters include:
   - position
   - angle relative to horizontal position
   - size relative to original size
   - reflection factor (how much of the light gets reflected)
   - transmittance (how much of the light passes through the object)
   - laser (only for flashlights, if on, they only emit one beam)
   - color 
   - texture (only for mirrors)
7. Click the fifth button from the left to enter _drawing mode_
8. While in the _drawing mode_ you can draw a new object by clicking in different places on screen.
9. Then, when `Enter` is pressed, a mirror in the desired shape is added to the environment.


## Objects and Features:
### The app includes various objects:
1. **Flashlight** - produces light that other objects interact with.
2. **Mirror** - a rectangular object that reflects light.
3. **Colored glass** - if a beam of light passes through it, the light changes color accordingly to the color of the glass.
4. **Prism** - a triangular object that disperses and redirects light that enters it.
5. **Custom-shaped mirror** - it's a regular mirror, but you can draw it so it has the desired shape.
6. **Lens** - magnifies or demagnifies light that enters it.

### The app also includes the following features:
1. **Parameters** - Every object has parameters that change the way they interact with the environment.
2. **Saving and loading** - you can save your loadout when quitting and come back to it later. You can also delete your saves.
3. **Presets** - you can load a premade project(preset) as if you had made it yourself.
4. **Intersection prevention** - objects cannot intersect with each other(just like in real life).
5. **Adjustable resolution** - you can change the resolution of the window.
6. **Togglable fullscreen** - you can toggle fullscreen on and off.
7. **Adjustable hotbar location** - you can change the location of the hotbar.
8. **Pretty flashlight toggle** - you can turn pretty flashlight on and off(Works best on high-end machines).
9. **Bin** - you can delete objects you don't need anymore.
10. **Achievements** - you can measure how much of the application you have discovered.
11. **FPS meter** - measures frames per second.
12. **Clock** - Lets you know what time it is.
13. **Sound effects** - helps to immerse in the world of optics.
14. **Calm music** - makes the experience much more pleasant

## Credits
This project is developed by Hohenzoler, V8Enthusiast, rutra8002, lolekszcz and MalyszekTobias.

All images used in the app were made by our team.
We have permission to use the font as stated here: https://www.dafont.com/junegull.font