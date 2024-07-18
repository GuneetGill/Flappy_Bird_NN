# Flappy Bird with AI: A Neural Network Approach

Recreation of the Flappy Bird game with an AI component that uses a neural network to learn how to play the game by itself. Over time, the AI improves its performance through training and learns to navigate the bird more effectively.

## Technologies Used
- **Python**: The primary programming language used for this project.
- **Pygame**: A set of Python modules designed for writing video games.
- **Neural Networks**: Implemented using Python to train the AI.

## Libraries Used
- **NumPy**: Used for performing various calculations, matrix operations, vectorized computations, random number generation, and statistical analysis for evaluating neural network performance.

## Neural Network Model

The neural network model for this project has the following structure:
- **Input Layer**: 2 nodes, representing the distance from the top of the pipe to the middle of the gap within the pipe.
- **Hidden Layer**: 5 nodes with a sigmoid activation function.
- **Output Layer**: 1 node.

### Training Process

The AI training follows an evolutionary approach:
1. **Evaluation**: Birds are assessed based on how long they stay alive and their proximity to the gaps in the pipes when they die.
2. **Selection**: The best-performing birds are retained and labeled as good birds, while the poorly performing ones are either entirely eliminated or have their weights changed randomly based on the good bird weights.
3. **Generation**: New "children" birds are created based on the traits of the best-performing birds.

The goal is to continuously improve the AI’s ability to navigate through the pipes by evolving its performance over multiple generations.
