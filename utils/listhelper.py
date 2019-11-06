""" list helper

to get a list from database
"""

from utils.constants import SIZE_PER_PAGE

# pylint:disable-msg=too-many-arguments
def get_list(model, selector, convertor, page, hide_list=None, order_list=None):
    """get list
    """
    if hide_list is None:
        hide_list = []

    qs = model.objects.filter(**selector)
    count = qs.count()
    if order_list is not None:
        qs = qs.order_by(**order_list)
    rets = []
    qs = qs[(page - 1) * SIZE_PER_PAGE : page * SIZE_PER_PAGE]
    for obj in qs:
        value = convertor(obj)
        for key in hide_list:
            if key in value:
                del value[key]
        rets.append(value)
    return count, rets
