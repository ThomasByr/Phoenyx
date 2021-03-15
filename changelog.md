# Changelog

> "War... war never changes" - the Sole Survivor

1.  *v0.0.a1* lets see PyPI...
    * initial commit and packaging
    * please note that alpha version are no longer accessible for download
2.  *v0.0.a2* wow such a mess
    * some refractor
    * name changing from pygame_engine to phoenyx (because the bird...)
    * efficiency improvement because frames are parts of success
3.  *v0.0.a3* now comes the big stuff
    * wait... [Buttons](phonyx/button.py) ? (type ``help(phoenyx.button.Button)`` to learn more)
    * buttons have better click response (hold or choose the number of frames to pass while uncliked to be able to trigger the button again)
4.  *v0.0.a4* I need to port html5
    * [Sliders](phonyx/slider.py) now ? (type ``help(phoenyx.slider.Slider)`` to learn more)
    * sliders have their name on the left, minimum and maximum value on respective sides
    * added the current value on top of the cursor
5.  *v0.1.0* how do I upload images on PyPI ?
    * buttons and sliders do not rely anyore on images for greater portability but are now less customizable
    * initial release on PyPI !
6.  *v0.1.1* too much errors in console
    * buttons and sliders can now be hidden
    * changed python dependency from 3.8 to 3.9 to improve reliability trough better type checks
    * slightly better WARNING and ERROR messages (button and slider name is displayed)
7.  *v0.1.2* lets be unique !
    * saving the state of the Engine works properly and also saves rect_mode
    * file test.py now features more drawing basics
    * button and slider have alternative drawing methods
    * better overall validation tests for objects
    * class name changing from Engine to Renderer
8.  *v0.1.3* game basics right ?
    * keyboard integration (you can now use ``Renderer.keys.`` to find keys)
    * keys stored in a new unaccessible class so autocompletion works
    * added option for keys to perform actions only when released, pressed or hold
9.  *v0.1.4* rainbow 1567
    * excluded some unnecessary files from build
    * some typo fix
    * added new colors, a lot of them
10. *v0.1.5* visual code messing with import statements
    * split renderer lib into many files for readability
    * lib fix, bug from circular imports
11. *v0.1.6* big update but not really because some stuff doesn't work
    * better color check especially when passing a string as a parameter
    * trying to comply with MS VS Code docstring "support"
    * added new 2D, 3D, and 4D [Open Simplex Noise](phoenyx/opensimplexnoise.py) algorithm
    * added new n dimensionnal [Perlin Noise](phoenyx/perlinnoise.py) algorith
    * first step trough interractive drawing
    * adding exhaustive [Documentation](helpme.md) slowly
    * first try of [Menu](phoenyx/menu.py) implementation (type ``help(phoenyx.menu.Menu)`` to learn more)
    * short animation when opening and closing menus
    * better spacing and drawing, animation ends properly and on the right side
    * menus appear before buttons and sliders
    * menus somewhat protected holding mouse button
    * added aliases for some properties as callable (is it really a good idea ?)
12. *v0.1.7* fixing fixes
    * a lot of bugs from previous update have been fixed
    * Noises library are now imported correctly
    * displaying menus name when drawing them
    * removed python sys import when unnecessary
13. *v0.1.8* are performances a real thing in python ?
    * added additionnal type import when importing phoenyx
    * messed with generator type in Perlin Noise
    * Noise library now work in all said dimensions
    * adding callable was not a good idea and now it's gone
14. *v0.1.9* all tests almost performed, few bugs left
    * OpenSimplex call now does not raise stupid value errors
    * fatal error in renderer in last version, removed it
    * added a new example file to generate Perlin noise, go check that out !
    * menu now have a proper background (might be off when background is animated though)
15. *v0.1.10* slm 14 b c
    * created this file because the README was starting to look like my homework list
    * short description of the changelog was added in the previous file
    * added additionnal documentation, lots of it
    * menu bodys won't disapear anymore when closing menus
    * fixed drawing coordinates for menu background
    * menu background can either be transparent, from a specific color, or match the window background color
    * the length of menu finally does something
    * made all constants accessible so that you can choose colors more confidently and deal with some options
16. *v0.1.11* a frame is a frame
    * replaced some draw stuff with native pygame to gain little performance
    * translation does not apply on sliders, buttons and menus anymore
    * added a option to reset translation state completly when needed
    * you can now effectively quit the sketch when dynamically drawing on window (using IDLE for eg)
    * new methods for basic drawing
    * menu text size is now configurable
17. *v0.1.12* some more drawing
    * small fix in test file, another test file is available (inverse kinematics) !
    * updated docstring when creating menu with Renderer to fit init method
    * first try of rotation, you can rotate the screen, but it is not recommended...
    * note that rotation unlike Processing only affect what has been drawn and not what will be drawn (this might change in the future)
    * also rotating is relative to the center, because pygame does not allow for much native customization
    * first try of scale, you can scale the sceen
    * scale is relative to the center, should you rotate and scale, scale first and then rotate to eliminate pixels artefacts (costs a lot of computer performances)
    * drawing method fix for lines
    * added squared distance calculation (also added casting) for Vectors
    * new methods for Vectors that does not modify the current object
18. *v0.1.13* pretty print
    * new invisible class called ``ErrorHandler`` to handle errors in a more pretty way
    * Phoenyx warnings are now less spam and display the number of times they occured (like in the js console log)
    * note that the terminal is not longer usable for standart inputs and outputs
    * worked around previous line, somehow... you can now use ``error_handler_set_soft`` in setup or anywhere in the main body of the program to use standard error messaging
    * you can now know where the mouse is inside of the main window
