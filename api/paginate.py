def paginate(req: dict, **kwargs):
    """
    Paginate a request
    :param req: Request to paginate
    :param kwargs: Form: key=value where key is the arg key and value is the default value for a given key
    :return: Tuple with pagination
    """
    t = (req.get(x, y), for x, y in kwargs.items())
    return t
