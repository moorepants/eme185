import os

from pelican import signals
from pelican import contents

from jinja2 import Environment, ChoiceLoader, FileSystemLoader


def execjinja2(instance):
    if type(instance) in (contents.Article, contents.Page):
        base_path = os.path.dirname(os.path.abspath(__file__))
        jinja2_env = Environment(
            loader=ChoiceLoader([
                FileSystemLoader(
                    os.path.join(base_path, instance.settings['THEME'],
                                 'templates')
                ),
            ]),
            **instance.settings['JINJA_ENVIRONMENT']
        )
        jinja2_template = jinja2_env.from_string(instance._content)

        kwargs = instance._context
        if type(instance) is contents.Article:
            kwargs['article'] = instance
        elif type(instance) is contents.Page:
            kwargs['page'] = instance

        instance._content = jinja2_template.render(**kwargs)


def register():
    signals.content_object_init.connect(execjinja2)
