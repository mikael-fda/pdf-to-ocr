
def count_n_w(name, word):
    print(name, word)
    with open(f"/data/original/{name}.txt", 'w') as f:
        f.write(name + " - " + word)
    return len(name) + len(word)


