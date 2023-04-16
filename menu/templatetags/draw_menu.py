from django import template

from menu.models import MenuItem

register = template.Library()


@register.inclusion_tag('menu/menu_list.html', takes_context=True)
def draw_menu(context, menu):
    selected_item_slug = context['request'].GET.get(menu)
    if selected_item_slug:
        items = MenuItem.objects.filter(menu__name=menu)

        selected_item = items.get(slug=selected_item_slug)
        selected_items_id = get_selected_items_id(selected_item)

        primary_items = items.values().filter(parent=None)
        for item in primary_items:
            if item['id'] in selected_items_id:
                item['child_items'] = get_child_items(
                    items, item['id'], selected_items_id)

        result_dict = {
            'items': primary_items,
            'selected_item': selected_item
        }
    else:
        items = MenuItem.objects.filter(menu__name=menu, parent=None)
        result_dict = {'items': [item for item in items]}

    result_dict['menu'] = menu
    return result_dict


def get_selected_items_id(item: MenuItem) -> list[int]:
    selected_items_id = []
    while item:
        selected_items_id.append(item.pk)
        item = item.parent
    return selected_items_id


def get_child_items(items, current_item_id, selected_items_id):
    child_items = items.values().filter(parent_id=current_item_id)
    for item in child_items:
        if item['id'] in selected_items_id:
            item['child_items'] = get_child_items(
                items, item['id'], selected_items_id)
    return child_items
