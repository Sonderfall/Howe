# import qiskit as qk
# import torch

import pennylane as qml
from pennylane import numpy as np
from pennylane.optimize import GradientDescentOptimizer, AdamOptimizer

num_qubits = 8
# num_layers = 3
dev = qml.device("default.qubit", wires=num_qubits)

def blockMPS_1(weight_x, weight_y, weight_z, wires):
    qml.Rot(weight_x[0], weight_y[0], weight_z[0], wires=wires[0])
    qml.Rot(weight_x[1], weight_y[1], weight_z[1], wires=wires[1])
    qml.CNOT(wires=wires)

def blockTTN(weight_x, weight_y, weight_z, wires):
    qml.Rot(weight_x[0], weight_y[0], weight_z[0], wires=wires[0])
    qml.Rot(weight_x[1], weight_y[1], weight_z[1], wires=wires[1])
    qml.CNOT(wires=wires)

def statepreparation(x):
    qml.BasisState(x, wires=[0, 1, 2, 3,4,5,6,7])

@qml.qnode(dev, interface="autograd")
def circuit_MPS(weights, x):

    statepreparation(x)

    # for w in weights:
    #     layer(w)

    blockMPS_1(weights[0, 0], weights[0, 1], weights[0, 2], [0, 1])
    blockMPS_1(weights[1, 0], weights[1, 1], weights[1, 2], [2, 3])
    blockMPS_1(weights[2, 0], weights[2, 1], weights[2, 2], [4, 5])
    blockMPS_1(weights[3, 0], weights[3, 1], weights[3, 2], [6, 7])

    blockMPS_1(weights[4, 0], weights[4, 1], weights[4, 2], [1, 2])
    blockMPS_1(weights[5, 0], weights[5, 1], weights[5, 2], [2, 3])
    blockMPS_1(weights[6, 0], weights[6, 1], weights[6, 2], [3, 4])
    blockMPS_1(weights[7, 0], weights[7, 1], weights[7, 2], [5, 6])
    # blockMPS_1(weights[8, 0], weights[8, 1], weights[8, 2], [6, 7])

    return qml.expval(qml.PauliZ(7))

@qml.qnode(dev, interface="autograd")
def circuit_TTN(weights, x):

    statepreparation(x)

    # for w in weights:
    #     layer(w)

    blockTTN(weights[0, 0], weights[0, 1], weights[0, 2], [0, 1])
    blockTTN(weights[1, 0], weights[1, 1], weights[1, 2], [2, 3])
    blockTTN(weights[2, 0], weights[2, 1], weights[2, 2], [4, 5])
    blockTTN(weights[3, 0], weights[3, 1], weights[3, 2], [6, 7])
    blockTTN(weights[4, 0], weights[4, 1], weights[4, 2], [1, 3])
    blockTTN(weights[5, 0], weights[5, 1], weights[5, 2], [5, 7])
    blockTTN(weights[6, 0], weights[6, 1], weights[6, 2], [3, 7])

    return qml.expval(qml.PauliZ(7))

def variational_classifier(weights, bias, x):
    return circuit_MPS(weights, x) + bias

def square_loss(labels, predictions):
    loss = 0
    for l, p in zip(labels, predictions):
        loss = loss + (l - p) ** 2

    loss = loss / len(labels)
    return loss

def accuracy(labels, predictions):
    loss = 0

    for l, p in zip(labels, predictions):
        if abs(l - p) < 1e-5:
            loss = loss + 1
    loss = loss / len(labels)

    return loss

def cost(weights, bias, X, Y):
    predictions = [variational_classifier(weights, bias, x) for x in X]

    return square_loss(Y, predictions)


data = np.loadtxt("parity_8.txt")
X = np.array(data[:, :-1], requires_grad=False)
Y = np.array(data[:, -1], requires_grad=False)
Y = Y * 2 - np.ones(len(Y))  # shift label from {0, 1} to {-1, 1}

np.random.seed(0)
# weights_init_TTN = 0.01 * np.random.randn(7, 3, 3, requires_grad=True)
weights_init_MPS = 0.01 * np.random.randn(8, 3, 3, requires_grad=True)
bias_init = np.array(0.0, requires_grad=True)

opt = AdamOptimizer(0.35)
batch_size = 5

weights = weights_init_MPS
bias = bias_init

for it in range(100):
    # Update the weights by one optimizer step
    batch_index = np.random.randint(0, len(X), (batch_size,))
    X_batch = X[batch_index]
    Y_batch = Y[batch_index]
    weights, bias, _, _ = opt.step(cost, weights, bias, X_batch, Y_batch)

    # Compute accuracy
    predictions = [np.sign(variational_classifier(weights, bias, x)) for x in X]
    acc = accuracy(Y, predictions)

    print(
        "Iter: {:5d} | Cost: {:0.7f} | Accuracy: {:0.7f} ".format(
            it + 1, cost(weights, bias, X, Y), acc
        )
    )