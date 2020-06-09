def paginate(args: dict, **kwargs):
    """
    Paginate a request
    :param args: Request args to paginate
    :param kwargs: Form: key=value where key is the arg key and value is the default value for a given key
    :return: Tuple with pagination
    """
    t = (type(y)(args.get(x, y)) if y is not None else args.get(x, y) for x, y in kwargs.items())
    return t
