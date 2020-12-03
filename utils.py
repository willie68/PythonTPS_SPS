def constrain(x, a, b):
    if x < a: 
        return a
    if x > b:
        return b
    return x
