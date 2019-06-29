import pickle

def open_model():
    # save model in text file
    with open("model.pickle", "rb") as f:
        model=pickle.load(f)
    return model

def save_model(model):
    with open("model.pickle", "wb") as f:
        pickle.dump(model, f)

def open_datasets():
    with open("datasets.pickle", "rb") as f:
        match_train,match_test=pickle.load(f)
    return match_train,match_test

def save_datasets(match_train,match_test):
    with open("datasets.pickle", "wb") as f:
        pickle.dump([match_train,match_test], f)