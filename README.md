# Project 3 for Scientific Computing: Fall 2023

![wfc_win](https://github.com/olincollege/scicomp-p3-omg-wfc/assets/95325894/42d230de-e6c2-40db-9d95-6a414e12d6d0)

## Running the Code

### Install

This project uses one external python library:

1. `pygame`

Install it via `pip`:

    ```bash
    pip install pygame
    ```

Then clone this repo:

    ```bash
    git clone git@github.com:olincollege/scicomp-p3-omg-wfc.git
    ```

### Run

This project contains one main python file, and it's fairly straightforward to use the model by running **own_attempt_wfc.py**. After being run, a pygame window should pop up on your machine, and the model will be run. It can be closed by pressing the Esc or Q keys while the model is running, or by closing out of the window. Thw window will not automatically close when the model is finished, and will instead display the finished image.

## Simulation

### Premise

In this project, I decided to take advantage of the class time and pursue a project I've been wanting to look at for a while: the Wave Function Collapse algorithm. First developed in 2016, WFC was created by Maxim Gumin as a way to "generate bitmaps that are locally similar to the input bitmap". It has use in game design and art, with these and many more examples shown on the [original repository](https://ieeexplore.ieee.org/document/9421370).

Here, I was attempting to recreate the results of [a paper on WFC](https://ieeexplore.ieee.org/document/9421370), with the result I was attempting to create being a general form of the algorithm itself. I wanted to be able to fully understand and implement the logic behind WFC. At first, I used a [tutorial on what the algorithm looks like in python/pygame](https://dev.to/kavinbharathi/the-fascinating-wave-function-collapse-algorithm-4nc3), but because I've gotten so comfortable with pygame over the course of the past few months in Scientific Computing, I eventually deviated from the form of WFC shown in that article in favor of the cleaner one outlined in the paper.

### Implementation

Most of the work this project was recreating the algorithm itself, and I found that the internal logic made a lot more sense after messing around with it for a few hours. Any of the information needed to understand what exactly is happening to generate the output image can be found through the article and repository linked above. The tileset that is currently in this repository is a fairly basic one, but with a non-negligible chance for a situation to arise wherein the algorithm gets stuck. In this implementation, this triggers a full reset of the image generation, as backtracking to a "more computable" stage in the collapse is a NP-hard problem. Here are the tiles I used:

![4](https://github.com/olincollege/scicomp-p3-omg-wfc/assets/95325894/f6528aff-d680-4a86-843e-88588d440bc8)
![3](https://github.com/olincollege/scicomp-p3-omg-wfc/assets/95325894/226dc7c3-9eaa-4791-bf3c-0ae487b54b7a)
![2](https://github.com/olincollege/scicomp-p3-omg-wfc/assets/95325894/e91f5092-5ff1-4dbc-8b76-f082733c87e6)
![1](https://github.com/olincollege/scicomp-p3-omg-wfc/assets/95325894/23cbcbc0-583a-4b36-9bdc-33079ca6a0aa)
![0](https://github.com/olincollege/scicomp-p3-omg-wfc/assets/95325894/60d835a9-64d3-4c11-9b3c-467e3182ae51)

#### Control

To adjust the size of the image created, the tile size (resulting resoltion), or the speed of the simulation, simply adjust the global variables at the top of the file to your liking.

### Results

**I was able to succesfully create an algorithm that non-deterministically generates a larger image, wherein the result is locally similar to an input bitmap, just like I wanted!**

The benchmarking for this one is fairly straightforward, as it's obvious when looking by eye that the algorithm makes an image that succeeds by its own rules. Because of the nature of this project, it is difficult to run tests to see if a rule is being violated until there was a visible error. I've run this more than a couple times at this point, and it doesn't seem like anything's amiss - It follows its own internal logic, as can be proved by print statements.

#### Limitations

- This model is slightly more simplistic than a classic WFC algorithm, and while I don't think it has any logic errors, it also doesn't do anything particularly unexpected.
- I use a time.sleep() function to slow down the collapse function, which isn't as nice for this type of application as the pygame.Clock.tick() function (and sometimes makes it a little tricky to try to close the window).

### Use

The use of my implementation is fairly straightforward: it looks cool! The more advanced applications of this, like to make game maps or randomly generated mazes/levels for deep learning application, are only slightly beyond what I've done here, depending on the complexity of the tileset. As it is, I could hardcode just about any 2d tileset of a reasonable size and generate many different kinds of bitmaps based on them.

However, I currently only have the one tileset coded in, and as it is, the primary function is mainly to show off the algorithm itself.

### In the Future

Some of the things I am the most excited about using WFC for are stretch goals for if I come back to this (which I hope to!), such as
- Reading an input bitmap rather than hardcoding one
- Having a tileset with symmetry and a function that can interpret that, rather than manually rotating the tiles and inputting them as different images
- Making my own tilesets! I would like to get this to work on a wallpaper like the one below, and I think it would go even better if I could get the symmetry part solved first

![image](https://github.com/olincollege/scicomp-p3-omg-wfc/assets/95325894/8da8dab3-d2dc-46b3-a184-b5264fc93c8c)
- Being able to export the result straight to PNG rather than taking a screenshot
- UI for changing the speed (or possibly even tilesets?? Like [this project](https://amarcolina.github.io/WFC-Explorer/?pattern=H4sIAAAAAAAAA2NgwAUYGxhxyhGSxC03KkmxJABofUQNswEAAA==), which is a little opaque tbh)
- A more accessible UI in general, maybe with user interaction, specifically with fixing certain tiles in place (There are [several](https://oskarstalberg.com/game/wave/wave.html) [examples](https://bolddunkley.itch.io/wfc-mixed) online of WFC that are done super well in this regard).
- I feel like I should at least MENTION that this can make the leap to the third dimension (because it's unbelievably cool!), even though I don't plan on doing that anytime soon
