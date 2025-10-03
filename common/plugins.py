
_REG = {}
def register(game, name, fn): _REG.setdefault(game, {})[name] = fn
def get(game, name): return _REG.get(game, {}).get(name)
def list_names(game): return sorted(_REG.get(game, {}).keys())
