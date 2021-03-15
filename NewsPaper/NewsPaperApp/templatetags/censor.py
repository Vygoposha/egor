from django import template

register = template.Library()


@register.filter(name='censor')
def censor(value):
    censored_words = ['слово1', 'слово2']
    if isinstance(value, str):
        censored_list = value.split(' ')
        for cl_index, cl_value in enumerate(censored_list):
            for c_word in censored_words:
                if c_word in cl_value.lower():
                    len_dif = len(c_word) - len(cl_value) - 1
                    censored_list[cl_index] = cl_value[0] + '.' * (len(c_word) - 2) + cl_value[len_dif:]
        return ' '.join(censored_list)
    else:
        raise ValueError(f'Фильтр <censor> можно применить только к объекту типа <str>')

