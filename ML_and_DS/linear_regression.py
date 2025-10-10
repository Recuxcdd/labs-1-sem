import matplotlib.pyplot as plt
import numpy as np


X = np.random.normal(50, 70, 200)
X -= np.min(X) - np.random.randint(0, 250)
Y = X / 4 + np.random.normal(X, 50) + np.random.rand() % 200
Y -= np.min(Y) - np.random.randint(0, 250)
X = np.expand_dims(X, axis=1)
Y = np.expand_dims(Y, axis=1)
data_set = np.concatenate((X, Y), axis=1)
np.random.shuffle(data_set)
splt = int(len(X) * 0.8)
X_training = data_set[:splt, 0]
Y_training = data_set[:splt, 1]
X_testing = data_set[splt:, 0]
Y_testing = data_set[splt:, 1]


def get_k_b(X, Y):
    k = ((X - np.mean(X)) * (Y - np.mean(Y))).sum() / ((X - np.mean(X))**2).sum()
    b = np.mean(Y) - k * np.mean(X)
    return k, b


k, b = 0, 0
k, b = get_k_b(X_training, Y_training)


fig, ax = plt.subplots(1, 2, figsize=(8, 4))
ax[0].scatter(X_training, Y_training)
line1, = ax[0].plot(X_training, k * X_training + b, "r")
ax[0].set_title("Training data")
ax[1].scatter(X_testing, Y_testing)
line2, = ax[1].plot(X_testing, k * X_testing + b, "r")
ax[1].set_title("Testing data")
plt.ion()
plt.show()
plt.pause(5)


def mse_loss(X, Y, k, b):
    return np.sum((Y - (k * X + b))**2) / np.size(X)


def learn(X, Y, k, b):
    learn_rate = 0.000001
    k_deriv = -2 / np.size(X) * np.sum(X * (Y - k * X - b))
    b_deriv = -2 / np.size(X) * np.sum(Y - k * X - b)
    k -= k_deriv * learn_rate
    b -= b_deriv * learn_rate * 1000
    return k, b


def predict(x):
    return k * x + b

 
def predict_from_test():
    rand_ind = np.random.randint(0, np.size(X_testing) - 1)
    y_pred = predict(X_testing[rand_ind])
    temp = [y_pred, Y_testing[rand_ind]]
    ax[1].scatter(X_testing[rand_ind], Y_testing[rand_ind], color="orange", s=60)
    plt.pause(0.001)
    print("*" * 60)
    print(f"x = {X_testing[rand_ind]}")
    print(f"y_pred = {y_pred}; y = {Y_testing[rand_ind]}")   
    print()
    print(f"accuracy = {round(min(temp) / max(temp), 2)}")
    print("*" * 60)
    

def MSE_test_metrik():
    L = mse_loss(X_testing, Y_testing, k, b)
    print("*" * 38)
    print(f"MSE Loss for Testing_data = {L}")
    print("*" * 38)


# epochs = 100

# print("-" * 38)
# for epoch in range(epochs):
#     print(f"k = {k}; b = {b}")
#     print(f"В {epoch} эпоху MSE_loss = {mse_loss(X_testing, Y_testing, k, b)}")
#     print("-" * 38)
#     k, b = learn(X_training, Y_training, k, b)
#     line1.set_ydata(k * X_training + b)
#     line2.set_ydata(k * X_testing + b)
#     plt.pause(0.001)


# MSE_test_metrik()


# plt.pause(999999)
    




