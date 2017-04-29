import types
import terrain_modifiers


def get_modifiers():
    """
    Obtains a reference to all the modifier functions.
    
    :return: 
    """
    return [terrain_modifiers.__dict__.get(a) for a in dir(terrain_modifiers) if isinstance(getattr(terrain_modifiers, a, None), types.FunctionType)]
