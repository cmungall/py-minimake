import functools
import inspect

global depth
depth = 0

def action(func):
    @functools.wraps(func)
    def wrapper_action(*args, **kwargs):
        bound = inspect.signature(func).bind(*args, **kwargs)
        bound.apply_defaults()
        #print(f'{func.__name__} called with {bound} A: {bound.args} AA: {bound.kwargs}')
        global depth
        indent = '    ' * depth
        depth += 1
        #print(f'{indent}INIT: {func.__name__} ARGS: {args} KWARGS: {kwargs.items()}')
        product = func(*args, **kwargs)
        # product = func(*bound.args, **bound.kwargs)
        if isinstance(product, list):
            None
        elif isinstance(product, tuple):
            None
        else:
            if len(args) > 0:
                product.input = args[0]
            for k, v in bound.arguments.items():
                setattr(product, k, v)
                print(f'{indent}   SET: {k} = {v}')
        #print(f'{indent}Product = {product} // {product.__repr__()}')
        depth -= 1
        return product
    return wrapper_action