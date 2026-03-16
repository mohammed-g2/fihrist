from flask import current_app


def paginate(items, table, page):
  pagination = items.order_by(table.created_at.desc()).paginate(
    page=page, per_page=current_app.config['ITEMS_PER_PAGE'], error_out=False)
  items = pagination.items
  
  return dict(pagination=pagination, items=items)
