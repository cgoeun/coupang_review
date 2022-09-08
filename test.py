import pickle

with open('links_8cate.pkl', 'rb') as f:
    links = pickle.load(f)
del links[0]
with open('links_8cate.pkl', 'wb') as f2:
    pickle.dump(links, f2)

