from django import template

from shop.models import Category


register = template.Library()


# Теги сортировки товаров
@register.simple_tag()
def get_subcategories(category):
    """
        Возвращает подкатегории указанной категории.

        Args:
            category (Category): Категория, для которой нужно получить подкатегории.

        Returns:
            QuerySet: Подкатегории указанной категории.
        """
    return Category.objects.filter(parent=category)


@register.simple_tag()
def get_sorted():
    """
    Возвращает список сортировок.

    Returns:
        list: Список сортировок.
    """
    sorters = [
        {
            'title': 'Цена',
            'sorters': [
                ('price', 'По возрастанию'),
                ('-price', 'По убыванию')
            ]
        },
        {
            'title': 'Цвет',
            'sorters': [
                ('color', 'от А до Я'),
                ('-color', 'от Я до А')
            ]
        },
        {
            'title': 'Размер',
            'sorters': [
                ('size', 'По возрастанию'),
                ('-size', 'По убыванию')
            ]
        }
    ]

    return sorters
