# Genetic snake with ANN
This project applies a genetic algorithm to the popular game "snake". 
All moves are predicted by an ANN and it has three output: streight, right, left.
Right now we have implemented three type of inputs, which are on 
[input.py](https://github.com/AlbertoLanaro/geneticSnakeANN/blob/master/src/input.py). The one that
performs better right now is the PointOfView. We will explain later the input format. 
The algorith idea is to simulate many snakes playing (good results with 10.000) in parallel and after all die sort them
by fitness, which is a value that represent how well a snake performed, and how musch it should reproduce himself. 
At the beginning (generation 0) all the wights are chosen randomly. 
After each generation we substitue the worst snake's weight, alias DNA, (usually around the 50%) with the wheghts of the better ones.
All these parameters and many others could be turning on the che [conf.py](https://github.com/AlbertoLanaro/geneticSnakeANN/blob/master/src/conf.py) 
file. 
Our project very modular in order order to allow easly new features or new decision algorithm

## Getting Started

How to run the self learning game:

### Prerequisites

You will need python 3.6+ with numpy, pygame, scipy and matplotlib.
If you want to install them with pip run:

```
python3 -m pip install numpy scipy matplotlib
python3 -m pip install -U pygame 
```
To see if it pygame works, run one of the included examples: 

```
python3 -m pygame.examples.aliens

```

## Running the tests

Now you are ready to run the example we made.
1) Choose your configuration. 
2) Run
```
cd src
python3 snake_train.py

```
Now you will train the snakes. You can see the snakes which had the better fitness on the previus generation (they will be still alive)
and the statistics of the generation. 
After the fitnes of a snake overcomes a value choosen on the [conf.py] file a json with the DNA of the snake will be saved.
You could run a test with the DNA saved with

```
python3 snake_test_from_json.py json/filename.json
```

## Authors

* **Alberto Lanaro**  - [AlbertoLanaro](https://github.com/AlbertoLanaro)
* **Mario Bonsembiante**  - [MarioBonse](https://github.com/MarioBonse)


