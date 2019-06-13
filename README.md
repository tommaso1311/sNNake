# sNNake

Evolving **neural networks** using **genetic algorithm**.

<table>
<th colspan="2" style="text-align:center">
Build status
</th>
<tr>
<td style="text-align:center"><b>master</td>
<td><img src="https://circleci.com/gh/tommaso1311/sNNake.svg?style=svg"/></td>
</tr>
<tr>
<td style="text-align:center"><b>dev</td>
<td><img src="https://circleci.com/gh/tommaso1311/sNNake/tree/dev.svg?style=svg"/></td>
</tr>
</table>

## Description

**sNNake** is the final exam project I wrote for the course of Data Analysis for Applied Physics and corrected and improved for the course Software and Computing for Applied Physics.

The project consists in creating the popular game snake and adding a neural network to play it. This network is then evolved using a genetic algorithm to play better at each iteration.

## Installation
Since the project is not a package, the only way to install it is by download or cloning it, via the proper button or the command line (if **git** is installed):

	git clone https://github.com/tommaso1311/sNNake
	
## Usage

I had a lot of fun writing and testing the base game, so I thought the possibility to play it without caring about the model should be included. Apart from this there is the option to simply train a new model or to load an existing one (to both retrain or assess its performance).

There are a lot of options with which to run the program to better customize the model, to see a complete list of them run:

	python main.py --help

#### Playing the base game

To play a normal game simply run:

	python main.py --play
	
#### Training a new model

To train a new model run the command:

	python main.py --train
	
but if you think this may be too simple, run:

	python main.py --train -g 100 -k 80 -n 25 10 -e 1000 -m "name_of_the_model"
	
as this would create a model of 100 generations of 80 snakes each, with a maximum game duration of 1000 steps and a neural network with two hidden layers on 25 and 10 perceptrons respectively and saves it with a specified name.

#### Loading an existing model

To load an existing model run the command:

	python main.py --load

and simply follow the instructions.
If you want to load a specific model, simply use the flag -m as in the previous example:

	python main.py --load -m "name_of_the_model"