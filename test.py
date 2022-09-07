import pickle

with open('links.pkl', 'rb') as f:
    links = pickle.load(f)

print(links[0])