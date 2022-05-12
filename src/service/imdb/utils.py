def memory_cache(func):
    """ Кешырования данных """
    memo = {}

    def wrapper(*arg):
        if memo.get(f'{arg[2]}'):
            return func(*arg)
        else:
            memo[f'{arg[2]}'] = arg[1]
            return True
    return wrapper
