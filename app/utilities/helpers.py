import inspect
import re
def get_function_string_repr(func):
    """Get the function string representation"""
    func_str_repr = str(func)
    result = re.findall(r"\w+[.]\w+", func_str_repr)
    return result[-1]
    