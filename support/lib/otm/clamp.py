def normalize_clamp_args(a, b):
    if a is None and b is None:
        return (0, 1)
    if a is None:              # someone's trying to clamp(x, None, b)
        raise Exception("invalid clamp arguments")
    if b is None:               # clamp(x, a, None)
        if a < 0:
            return (a, 0)
        return (0, a)
    if a > b:
        (a, b) = (b, a)
    return (a, b)

def clamp(x, a=None, b=None):
    (a, b) = normalize_clamp_args(a, b)
    if x < a:
        return a
    if x > b:
        return b
    return x
