# Genetic Snake with ANN :snake:
This project applies a genetic algorithm to the popular game "snake".
Every snake is characterized by an ANN that predicts its future move: go straight, turn right, turn left.
Right now we have implemented three type of inputs, which are described in [input.py](https://github.com/AlbertoLanaro/geneticSnakeANN/blob/master/src/input.py).
The algorithm is based on a simulation of many snakes playing (best results are achieved with ~10.000 snakes), each one seeking for its food. The DNA of each snake is composed by the weights of the ANN. Each DNA is randomly initialized.
After all the snakes died (end of a generation), we sort them by their fitness (which is a value that represent how well a snake has performed during the current generation) and perform [crossover](https://en.wikipedia.org/wiki/Crossover_(genetic_algorithm)) and random [mutation](https://en.wikipedia.org/wiki/Mutation_(genetic_algorithm)) between the DNA of the best snakes.
The game can be played with or without borders (variable **BORDER_BOOL** in [conf.py](https://github.com/AlbertoLanaro/geneticSnakeANN/blob/master/src/conf.py)). As expected, best results are achieved when the borders are disabled (see section **Results**).

All the parameters of the algorithm can changed by tuning the parameters described in the [conf.py](https://github.com/AlbertoLanaro/geneticSnakeANN/blob/master/src/conf.py) file.

The is built to be as modular as possible in order to allow the addition of new features or new decision algorithms in a simple and straight way.

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
After the fitness of a snake overcomes a certain value (see [conf.py](https://github.com/AlbertoLanaro/geneticSnakeANN/blob/master/src/conf.py)) a json file with the DNA of the snake will be created and stored in the json folder. If you want to see how well a single snake plays given a certain stored DNA you can run the following:
```
python3 snake_test_from_json.py json/filename.json
```

## ANN Input Types
As discussed above, we implemented different possible ANN's input types (see [input.py](https://github.com/AlbertoLanaro/geneticSnakeANN/blob/master/src/input.py)). The one that performs better is the one we called **PointOfViewUpgraded**. In this case, the input simply consists in what the snake sees around himself (1 if food, -1 if borders, -2 if body, 0 otherwise), the encoded position of the food and the last three change of direction that the snake did.
## Results
Here we present some of the results we obtained from the simulations. We show how the evolution process leads to snakes with higher fitness and how trained snakes behaves when tested alone.
### Evolution process
Below you can see an example of how the evolution process works. As can be seen from the figure below, generation by generation, it can be seen how the snakes improve and understand how to survive longer in the game. 

In this example, where the snakes were playing in a 8x8 field, after around 260 genereations they understood how to reach the maximum possible fitness of 64 :metal:

<div align="center">
<img src="https://github.com/AlbertoLanaro/geneticSnakeANN/blob/master/doc/fitness.png?raw=true" width="450" height="450" />
</div>
  
<div align="center">
<img src="https://github.com/AlbertoLanaro/geneticSnakeANN/blob/master/doc/snake_evolution.gif?raw=true" width="450" height="450" />
</div>



### Snake with Borders 
Here we present an example of how a trained snake performs playing with the border mode turned on.

<div align="center">
<img src="https://github.com/AlbertoLanaro/geneticSnakeANN/blob/master/doc/single_border.gif?raw=true" width="450" height="450" />
</div>


### Snake without Borders
Here we present an example of how a trained snake performs playing in a borderless environment.

single_border

<div align="center">
<img src="https://github.com/AlbertoLanaro/geneticSnakeANN/blob/master/doc/single_no_borders.gif?raw=true" width="450" height="450" />
</div>


## Future Works
In order to achieve better performance we are investigating different input types and different ANN setups. One of the possible next steps is to introduce a more complex model for the snake brain such as a LSTM network (in order to capture the sequentiality of the events) or a CNN.

## Authors

* **Alberto Lanaro** :nerd_face: - [AlbertoLanaro](https://github.com/AlbertoLanaro)
* **Mario Bonsembiante** :nerd_face: - [MarioBonse](https://github.com/MarioBonse)
