from flask import get_flashed_messages, Markup, json, current_app, g, request

from belka.models.apis import FIELD_TYPES, FIELD_CONTENT_TYPES


def init_jinja(app):
    app.jinja_env.policies['json.dumps_kwargs'] = {'sort_keys': True, 'ensure_ascii': False}

    @app.context_processor
    def context_processors():
        """
        Возвращает flash-сообщения в виде [('error', [msg1, msg2, msg3]), ('success', [msg1, msg2]), ...]
        :return:
        """
        def make_flashes():
            result = {}
            for cat, msg in get_flashed_messages(with_categories=True):
                result.setdefault(cat, []).append(msg)
            return result

        return {
            'flashes': make_flashes,
            'FIELD_TYPES': FIELD_TYPES,
            'FIELD_CONTENT_TYPES': FIELD_CONTENT_TYPES
        }

    @app.template_filter('pizda')
    def promise_type(text):
        return 'pizda'
