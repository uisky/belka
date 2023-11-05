from flask import redirect, render_template, request, flash, url_for, abort, jsonify

from . import bp
from belka.models import db, Api, Field, Data


@bp.get('/<api_name>')
def items(api_name):
    """
    ?search.{field}
    ?page
    ?pagesize
    """
    q = db.select(Api).filter_by(active=True, name=api_name)
    api = db.one_or_404(q, description='API не найден. Удалили, может?')

    q = db.select(Data).filter_by(api_id=api.id).order_by(Data.sort)
    data = db.session.execute(q).scalars().all()

    result = []
    for obj in data:
        item = {
            'id': obj.id
        }
        ok = True
        for field in api.fields:
            val = obj.content.get(field.name)
            search_param = f'search.{field.name}'
            if search_param in request.args:
                if field.type != 'string':
                    abort(400, 'Нельзя искать по не-текстовым полям.')
                if request.args[search_param].lower() not in val.lower():
                    ok = False
                    break

            item[field.name] = val

        if ok:
            result.append(item)

    page = request.args.get('page', 0, type=int)
    pagesize = request.args.get('page_size', 20, type=int)

    total = len(result)
    result = result[page * pagesize : (page + 1) * pagesize]

    resp = jsonify({'total': total, 'results': result})
    resp.headers['X-Total'] = str(total)
    return resp


@bp.get('/<api_name>/<int:obj_id>')
def item(api_name, obj_id):
    """
    ?search.{field}
    ?page
    ?pagesize
    """
    q = db.select(Api).filter_by(active=True, name=api_name)
    api = db.one_or_404(q, description='API не найден. Удалили, может?')

    q = db.select(Data).filter_by(api_id=api.id, id=obj_id).order_by(Data.sort)
    obj = db.session.execute(q).scalar_one_or_none()
    if not obj:
        abort(404, 'Записи с таким ID не существует.')

    item = {
        'id': obj.id
    }
    for field in api.fields:
        val = obj.content.get(field.name)
        item[field.name] = val

    return jsonify(item)
