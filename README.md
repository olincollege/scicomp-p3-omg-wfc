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

This project contains two main python files, and the one that should be run in order to view the simulation that I worked on is **own_attempt_wfc.py**. After being run, a pygame window should pop up on your machine, and the model will be run. It can be closed by pressing the Esc or Q keys while the model is running, or by closing out of the window. Thw window will not automatically close when the model is finished, and will instead display the finished image.

## Simulation

### Premise

This simulation is intended to represent the modeling of cold traps on Mercury, and the movement of H2O molecules across its surface, specifically with reference to how those molecules either:

- Get photodissociated by the sun or atmospheric conditions
- Become trapped in the polar regions at the north and south poles (cold traps) of the planet, where the temperature is not sufficient to provoke jumping

This simulation is primarily based on the '93 paper by Bryan J. Butler and Duane O. Muhleman called "Mercury: Full-Disk Radar Images and the Detection and Stability of Ice at the North Pole". Their work on this particular topic can be seen in their paper under the heading "Migration". I also incorporated some work from the follow-up '97 paper by Butler, "“The migration of volatiles on the surfaces of Mercury and the Moon.”

My model uses the sunlight and temperature components of the '93 paper, but the random angle and height-based gravity components of the '97 paper.

### Implementation

#### View

Upon being run, this code creates a window with the visualization for my model, with three different colors of molecule:

- Green molecules are active, and change size depending on how high off of the surface of the planet they are during their hop
- Blue molecules are caught, specifically in the cold traps at the north and south poles of the planet
- Orange molecules are lost, most commonly dissociated by the sun, but occasionally are lost because their initial launch led to their escaping the atmosphere of the planet.

![Screenshot from 2023-10-27 02-07-21](https://github.com/olincollege/scicomp-p2-water-you-up-to/assets/95325894/a40d30fe-2aca-41fa-9d26-4eea1fb3dc2f)

The yellow area on the visualization (here wrapping from one side of our flattened planet to the other) represents the current area of the planet that is facing the sun and so is enabled to hop by the temperature of the surface.

#### Model

As mentioned, my model uses some components of both the '93 and '97 Butler papers on this subject. However, my implementation differs from theirs in a few notable ways that were necessary in order to have the visualization that I wanted.

##### Temperature and Sunlight

In order to animate the paths of individual molecules, as mentioned in the '97 paper, I needed to implement the day/night cycle of the '93 paper, which meant forgoing the temperature and stability binning by latitude of the '97 paper (not NECESSARILY, but it would have made it a lot more complicated). The way I did this was by assuming that there would always be half of the planet that faced the sun, and half that did not. I was then able to incementally move an area representing this half across the surface, letting it affect the particles that it covered.

##### States

Each molecule is its own agent that falls into one of three categories: active, captured, and lost. On any given step of the simulation, captured and lost particles don't do anything, but active particles follow the follow (simplified) steps:

1. Check if in the middle of a hop
   1a. If true, continue the hop
2. If not hopping & in sunlight, hop!
3. Check if landing from a hop
   3a. If true, check if this hop resulted in a loss
   3aa. If true, mark as lost
4. Check if in a polar region
   4a. If true, mark as caught

Being marked as either lost or caught removes a particle from the "active" list, making sure it doesn't move any more.

##### Movement

Each particle stores its location as a set of spherical coordinates, with the form (Distance from center of planet in m, Angle from north pole in deg, Azimuthal angle in deg).

Crucially, this is where my model differs the most from either of Butler's. Instead of generating the distance that the particle WOULD move, I instead took the parameters for each hop and actually moved the particle, doing projectile-motion calculations for each. This made a lot more intuitive sense to me than some of the complex trigonometry used in the papers, and it enabled me to create a visualization that would show the actual position of each molecule at each timestep, including its height and general position during the jump.

In order to do this, I had to make some of the decisions that Butler did. From the '93 paper, I took the idea of a constant launch velocity, because it lightened the computational load significantly. From the '97 paper, I took the idea of generating a random launch direction and angle. The direction was taken from a uniform distribution between 0 and 359 degrees, while the angle was taken from a isotropic distribution given by the ordinary Maxwellian distribution of a gas at rest. Using these and some trig, the simulation is able to generate a spherical coordinate vector that represents the initial velocity of any given jump.

Using the initial coordinates, velocity, and (the gravity of mercury as) acceleration for each hop, the simulation uses calculus principles to move each particle. It's important to note here that gravity, the acceleration, changes as the particle gets further from the surface. This is taken from the '97 paper and is implemented in full here, according to physics principles.

#### Controller

The controller is the main file that is run. It initializes and calls both the view and model files, and when the simulation is done running, closes the view window + prints a message to the terminal about the proportion of molecules that were captured rather than lost during the run.

### Results

The '97 paper found that the percentage of molecules that wound up trapped in in the polar cold traps, under the (nearest approximation of the) conditions in my model hovers at around 9%, which would suggest the presence of polar ice caps, as it's not an insignificant percentage in this case.

**_My model returns proportions between 10 and 12%_**, which is remarkably close, and is in fact VERY close to the results of the '93 paper, which derived an expected value of 12%, and found a simulated value of 10%.

#### Possible Reasons for Any Discrepancy

- This model abstracts away the idea that the velocities of the molecules would be distributed according to the ordinary or modified Maxwellian, and instead assumes constant initial velocity.
- This is partly due to the temperature of sunlit surface being abstracted to a flat 500 K, which is very oversimplified, and doesn't account for gradual heating and cooling.
- Speeding the sun up in relation to the rest of the model so significantly (40x!!!) in order to make sure the model runs in a reasonable time may affect the path of individual molecules, because they would spend much longer _at a time_ in the sun, and so hopping.

### Use

This model is primarily useful in understanding the paths of individual molecules on their journeys across the surface. This would be very useful in an education sense, and as a tool to aid further understanding of the system by modification of discrete factors like gravity to account for different planets, and to see how that changes our working model.

Particularly as more data gets collected, and as scientists want to know how the system and the individual agents inside it are affected, my code is adaptable enough to encourage playing around, although not robust enough to run anything like a gradient descent to work backwards from desired behaviors to obtain data (yet!)

The computational load (what with the visualization and projectile motion) mean that this model shouldn't be used for any heavy-duty computations - I don't have a ton of trust in how many particles it could realistically render at 60 FPS, and if the framerate were to dip, it would affect the behavior of the particles and possibly skew the results.
