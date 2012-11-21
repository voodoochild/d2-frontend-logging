import json
from datetime import datetime
from flask import request, make_response
from application import app
# from models import ExampleModel


@app.route('/')
def home():
    return 'Hello'


@app.route('/log')
def log():
    # example = ExampleModel(
    #     example_name = form.example_name.data,
    #     example_description = form.example_description.data,
    #     added_by = users.get_current_user()
    # )
    # try:
    #     example.put()
    #     example_id = example.key().id()
    #     flash(u'Example %s successfully saved.' % example_id, 'success')
    #     return redirect(url_for('list_examples'))
    # except CapabilityDisabledError:
    #     flash(u'App Engine Datastore is currently in read-only mode.', 'info')
    #     return redirect(url_for('list_examples'))

    log_data = {
        'user-agent': request.args.get('user-agent'),
        'error': request.args.get('error'),
        'url': request.args.get('where'),
        'time': request.args.get('when')
    }

    if log_data.get('time'):
        date = int(int(log_data['time']) / 1000)
        date = datetime.fromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S')
        log_data['time'] = date

    response = make_response('{callback}({data})'.format(
        callback=str(request.args.get('callback')),
        data=json.dumps(log_data)))
    response.mimetype = 'application/json'
    return response
