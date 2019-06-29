import pickle

def open_model():
    # save model in text file
    with open("train.pickle", "rb") as f:
        model=pickle.load(f)
    return model