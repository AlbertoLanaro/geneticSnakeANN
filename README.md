# Genetic Snake with ANN
This project applies a genetic algorithm to the popular game "snake" using Python.
Every snake is characterized by an ANN that predicts the future snake’s move: go straight, turn right, turn left.
Right now we have implemented three type of inputs, which are described in [input.py](https://github.com/AlbertoLanaro/geneticSnakeANN/blob/master/src/input.py). The input format will be described later (see section **ANN Input types**).
The algorithm is based on a simulation of many snakes playing (best results are achieved with 10.000 snakes) in parallel, each one seeking for its food.
After all the snakes are dead (end of a generation), we sort them by their fitness (which is a value that represent how well a snake has performed during the current generation) and we perform [crossover](https://en.wikipedia.org/wiki/Crossover_(genetic_algorithm)) and random [mutation](https://en.wikipedia.org/wiki/Mutation_(genetic_algorithm)) between the DNA of the best snakes.
The game can be played with or without borders (variable **BORDER_BOOL** in [conf.py](https://github.com/AlbertoLanaro/geneticSnakeANN/blob/master/src/conf.py)). As expected, best results are achieved when the borders are disabled (see section **Results**).

All the parameters of the algorithm could be tuned on the [conf.py](https://github.com/AlbertoLanaro/geneticSnakeANN/blob/master/src/conf.py) file.

Our project is built to be as modular as possible in order to allow the addition of new features or new decision algorithms in a simple and straight way.

## Getting Started

How to run the self learning game:

### Prerequisites

You will need python 3.5+ with numpy, pygame, scipy and matplotlib libraries.
If you want to install them with pip run:

```
python3 -m pip install numpy scipy matplotlib
python3 -m pip install -U pygame 
```
To see if it pygame works, run one of the included examples: 
```
python3 -m pygame.examples.aliens
```

## Running the Tests

Now you are ready to run the example we made.
1) Choose your configuration changing the parameters of the configuration file 
2) Run
```
cd src
python3 snake_train.py
```
Now you will train the snakes. For each generation, on the screen you can see the best snakes of the previous generation and the statistics of the current generation.
After the fitness of a snake overcomes a value set on the [conf.py](https://github.com/AlbertoLanaro/geneticSnakeANN/blob/master/src/conf.py) file a json with the DNA of the snake will be created and stored in the json folder. If you want to see how well a single snake plays given a certain stored DNA you can run the following
```
python3 snake_test_from_json.py json/filename.json
```

## ANN Input Types
As discussed above, we implemented different possible ANN's input types (see [input.py](https://github.com/AlbertoLanaro/geneticSnakeANN/blob/master/src/input.py)). The one that performs better is the one we called **PointOfView**. In this case, the input simply consists in what the snake sees around himself (1 if food, -1 if borders, -2 if body, 0 otherwise) and the encoded position of the food.
## Results
Here we discuss some of the results we obtaind from the simulations. We show how the evolution process leads to snake with higher fitness and we show how trained snakes behaves when tested alone.
### Evolution process
Below you can see an example of how the evolution process works. Generation by generation, it can be seen how the snakes improve and understand how to survive longer in the game. In the Figure below it can seen how the average snake fitness increases in time.

![](https://github.com/AlbertoLanaro/geneticSnakeANN/blob/lanarodev/doc/snake_evolution.gif?raw=true)

### Snake with Borders 
Here we present an example of how a trained snake performs playing with the border mode turned on.

![](https://github.com/AlbertoLanaro/geneticSnakeANN/blob/lanarodev/doc/single_border.gif?raw=true)

### Snake without Borders
Here we present an example of how a trained snake performs playing in a borderless environment.

![](https://github.com/AlbertoLanaro/geneticSnakeANN/blob/lanarodev/doc/single_no_borders.gif?raw=true)

## Authors

* **Alberto Lanaro**  - [AlbertoLanaro](https://github.com/AlbertoLanaro)
* **Mario Bonsembiante**  - [MarioBonse](https://github.com/MarioBonse)
