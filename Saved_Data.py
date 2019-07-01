import pickle

def open_model_linear_regression():
    # save model in text file
    with open("model_linear_regression.pickle", "rb") as f:
        model=pickle.load(f)
    return model

def save_model_linear_regression(model_linear_regression):
    with open("model_linear_regression.pickle", "wb") as f:
        pickle.dump(model_linear_regression, f)

def open_model_neural_network():
    # save model in text file
    with open("model_neural_network.pickle", "rb") as f:
        model=pickle.load(f)
    return model

def save_model_neural_network(model_neural_network):
    with open("model_neural_network.pickle", "wb") as f:
        pickle.dump(model_neural_network, f)

def open_datasets():
    with open("datasets.pickle", "rb") as f:
        match_train,match_test=pickle.load(f)
    return match_train,match_test

def save_datasets(match_train,match_test):
    with open("datasets.pickle", "wb") as f:
        pickle.dump([match_train,match_test], f)