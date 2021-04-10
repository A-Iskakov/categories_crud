"""
после регистрации роутов мы выгружаем описание к тэгам из докстрингов классов
"""
from categories_crud.urls import router


def postprocess_schema(result, generator, **kwargs):
    TAGS = []
    for global_tag, view_class, url_name in router.registry:
        TAGS.append({'name': global_tag, 'description': view_class.__doc__.strip()})
    result['tags'] = TAGS
    return result

