from django import template

from menu.models import MenuItem

register = template.Library()


@register.simple_tag
def get_menu():
    menu_items = MenuItem.objects.all()

    def tree(objects):
        depth = min([get_depth(obj) for obj in objects])
        objects_on_level = [obj for obj in objects if get_depth(obj) == depth]
        _tree = []

        for object in objects_on_level:
            children = menu_items.filter(parent=object)
            object.children.set(tree(children) if children else [])
            _tree.append(object)

        return _tree

    return tree(menu_items) if menu_items else []


def get_depth(obj):
        depth = 0
        while obj.parent:
            obj = obj.parent
            depth += 1
        return depth