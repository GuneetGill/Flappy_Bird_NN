import numpy as np
import scipy.special
import random
from defs import *


class Nnet:
    #num of input nodes, hidden nodes and output nodes 
    def __init__(self, num_input, num_hidden, num_output):
        #save as property of class
        self.num_input = num_input
        self.num_hidden = num_hidden
        self.num_output = num_output
        #generate weights randomly between input nodes and hidden nodes and between hidden nodes and output nodes
        #between range of -0.5 and 0.5 and size is based on hidden and input nodes
        self.weight_input_hidden = np.random.uniform(-0.5, 0.5, size=(self.num_hidden, self.num_input))
        self.weight_hidden_output = np.random.uniform(-0.5, 0.5, size=(self.num_output, self.num_hidden))
        #activation function to use the sigmoid function 
        self.activation_function = lambda x: scipy.special.expit(x)

    #output of 1 value sending neural net 1 dimestional array
    def get_outputs(self, inputs_list):
        #transpose list into 2 dimenional list since right now it is 1dimensional
        #[[1,2,3]] to [[1],[2],[3]]
        inputs = np.array(inputs_list, ndmin=2).T
        
        #multiple input matrix with weights by doing dot product
        hidden_inputs = np.dot(self.weight_input_hidden, inputs)
        #apply the sigmoid function to the output from above 
        hidden_outputs = self.activation_function(hidden_inputs)

        #do matrix multiplcation again with next layer which is matrix from avobe with hidden layer
        final_inputs = np.dot(self.weight_hidden_output, hidden_outputs)
        #apply sigmoid function to result from above
        final_outputs = self.activation_function(final_inputs)
        
        return final_outputs

    def get_max_value(self, inputs_list):
        #get the max valeu from the final output since it is a list of values we only want max
        outputs = self.get_outputs(inputs_list)
        return np.max(outputs)
    
    def modify_weights(self):
        #modify some of the bad birds weights 
        Nnet.modify_array(self.weight_input_hidden)
        Nnet.modify_array(self.weight_hidden_output)

    def create_mixed_weights(self, net1, net2):
        #takes two neural nets and create hidden inputs and outputs based on their values
        self.weight_input_hidden = Nnet.get_mix_from_arrays(net1.weight_input_hidden,  net2.weight_input_hidden)
        self.weight_hidden_output = Nnet.get_mix_from_arrays(net1.weight_hidden_output,  net2.weight_hidden_output)       

    def modify_array(a):
        #loop through array and modify array readwrite func
        for x in np.nditer(a, op_flags=['readwrite']):
            #if random floar between 0 and 1 is less than our weight then
            #generate new random number
            if random.random() < MUTATION_WEIGHT_MODIFY_CHANCE:
                x[...] = np.random.random_sample() - 0.5

    #when we create a child create a mix of weights input two arrays and create 1 even mix array 
    def get_mix_from_arrays(ar1, ar2):

        #assume size of array is both same
        total_entries = ar1.size
        num_rows = ar1.shape[0]
        num_cols = ar1.shape[1]

        #only want to take half if we have total size was 12 we take 6
        num_to_take = total_entries - int(total_entries * MUTATION_ARRAY_MIX_PERC)
        #pick random selection of index's from array based on half^^ and do not replace the index we take
        idx = np.random.choice(np.arange(total_entries),  num_to_take, replace=False)

        #array is same number of rows and cols as one we inputted
        res = np.random.rand(num_rows, num_cols)

        #itterate through array and replace random values we got from res with either array 1 or 2 values
        for row in range(0, num_rows):
            for col in range(0, num_cols):
                index = row * num_cols + col
                #create even mix from arrays
                if index in idx:
                    res[row][col] = ar1[row][col]
                else:
                    res[row][col] = ar2[row][col]

        return res
























































