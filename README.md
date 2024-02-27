<div align="center">
   
# Optics
Optics is a Python-based simulator of optic phenomenons. It uses the Pygame library for app development.
</div>

## Status
| Feature              | Status |
|----------------------|--------|
| Flashlight           | ✅      |
| Mirror               | ✅      |
| Lens                 | ✅      |
| Prism                | ✅      |
| Transmittance factor | ✅      |
| Reflection factor    | ✅      |
| color                | ✅      |
| refractive index     | ✅      |

## Installation
There are two ways to install the project: download exe file, or run the project from source.

> [!NOTE]
> If you don't want to modify the project, we recommend using the first method.

### Method 1
1. Go to the ***Releases*** page on our project's GitHub
2. Download ***1.0 - zip***
3. Extract all the files
4. Run ***optyka.exe***

### Method 2
1. Clone the repository: `git clone https://github.com/Hohenzoler/optyka.git`
2. Navigate to the project directory: `optyka`
3. Install the required packages: `pip install -r requirements.txt`
4. Run the main script: `python main.py`


## Usage
* Click Start.
* You can choose:
   - new save (nothing is placed)
   - load preset (a premade project made by the developers)
   - one of your saves (if you have any)
* Now you can place objects and see how they interact with each other.
* `Right click` an object to pick it up or release it.
* When holding an object, click `P` to open its parameters window.
* Parameters include:
   - position
   - angle relative to horizontal position
   - size relative to original size
   - reflection factor (how much of the light gets reflected)
   - transmittance (how much of the light passes through the object)
   - laser (only for flashlights, if on, they only emit one beam)
   - color 
   - texture (only for mirrors)
* When holding an object you can also press `R` to enter _resizing mode_
* While in _resizing mode_ you can click one of the points visible on the object and place said point elsewhere, thus resizing the object.


* You can enter _drawing mode_ by clicking the icon that looks like this <p align="center"><img width="60" height="60" border = 10 src="https://github.com/Hohenzoler/optyka/blob/main/images/bad_pen.png"></p>


   - While in _drawing mode_ you can draw a new object by clicking different places on screen.
   - You can also delete the last point placed by pressing `Backspace` or move a point by `right clicking`.
   - Then, when `Enter` is pressed, a mirror in the desired shape is added to the environment.
* Press `up` to randomize colors of all flashlights



## Objects and Features:
### The app includes various objects:
* **Flashlight** - produces light that other objects can interact with.
* **Mirror** - a rectangular object that reflects light.
* **Colored glass** - if a beam of light passes through it, the light changes color accordingly to the color of the glass.
* **Prism** - a triangular object that disperses and redirects light that enters it.
* **Custom-shaped mirror** - it's a regular mirror, but you can draw it so it assumes the desired shape.
* **Lens** - magnifies or demagnifies light that enters it.
* **Corridor** - Light can enter and exit it from the sides but the two other sides work like mirrors.

### The app also includes the following features:
* **Parameters** - Every object has parameters that change the way they interact with the environment.
* **Saving and loading** - you can save your loadout when quitting and come back to it later. You can also delete your saves.
* **Presets** - you can load a premade project (preset) as if you had made it yourself.
* **Picking up objects** - you can `right click` an object to pick it up or put it down.
* **Reshaping objects** - you can press `R` to begin reshaping held object
* **Rotating objects** - you can rotate held objects using scroll.
* **Intersection prevention** - objects cannot intersect with each other (just like in real life).
* **Adjustable resolution** - you can change the resolution of the window.
* **Togglable fullscreen** - you can toggle fullscreen on and off.
* **Adjustable hotbar location** - you can change the location of the hotbar.
* **Pretty flashlight toggle** - you can turn pretty flashlight on and off (Works best on high-end machines).
* **Bin** - you can delete objects you don't need anymore.
* **Achievements** - you can measure how much of the application you have discovered.
* **FPS meter** - measures frames per second.
* **Clock** - Lets you know what time it is.
* **Sound effects** - helps to immerse in the world of optics.
* **Calm music** - makes the experience much more pleasant
* **Color randomizer** - activated by pressing `up`, there isn't any particular reason for its existence

## Opinions
> "I think it's a great app. It's very educational and fun to play with. I would recommend it to anyone who wants to learn about optics." - *Jeff*

Picture of Jeff:

![Jeff](images/Jeff.png)

## Credits
This project is developed by [Hohenzoler](https://github.com/Hohenzoler), [MalyszekTobias](https://github.com/MalyszekTobias), [rutra8002](https://github.com/rutra8002), [lolekszcz](https://github.com/lolekszcz) and [V8Enthusiast](https://github.com/V8Enthusiast).

Large majority of the assets used in the app were made by our team.
We have permission to use the font as stated [here](https://www.dafont.com/junegull.font).

We also have permission to use the background music, made by [C418](https://www.youtube.com/watch?v=XuZDeT8zI5c&ab_channel=C418-Topic)
