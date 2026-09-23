"""教学用缺陷版本：请依据 README 契约修复，不用于生产。"""


def paginate(items, page=1, page_size=2):
    start = page * page_size
    return items[start:start + page_size]
