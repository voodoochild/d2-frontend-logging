import re
import json
from flask import request, make_response, render_template, url_for, redirect
from application import app
from models import Error


@app.route('/')
@app.route('/<environment>')
def errors(environment=None):
    environments = {
        'code':    'http://discussion-app-code-env.elasticbeanstalk.com',
        'qa':      'http://discussion-app-qa-env.elasticbeanstalk.com',
        'release': 'http://discussion-app-rel-env.elasticbeanstalk.com',
        'prod':    'http://discussion.guardian.co.uk'
    }

    if environment is not None and environment not in environments.keys():
        return redirect(url_for('errors', environment=None))

    errors = Error.all().order('-time')

    if environment in environments.keys():
        errors.filter('host =', environments[environment])

    response = make_response(render_template('log.html', errors=errors))
    response.headers['Cache-Control'] = 'no-cache, max-age=0'
    return response


@app.route('/log')
def log():
    log = {
        'url': request.args.get('url'),
        'error': request.args.get('error'),
        'filename': request.args.get('filename'),
        'line': request.args.get('line'),
        'useragent': request.args.get('useragent')
    }

    if log['url'] is not None:
        match = re.findall('^http:\/\/[\w.:-]+', log['url'])
        if match:
            log['host'] = match[0]
    else:
        log['host'] = None

    if log['filename'] is not None:
        log['filename'] = log['filename'][:500]

    if log['line'] is not None:
        log['line'] = int(log['line'])

    error = Error(
        url=log['url'],
        host=log['host'],
        error=log['error'],
        filename=log['filename'],
        line=log['line'],
        useragent=log['useragent']
    )
    error.put()

    response = make_response('{callback}({data})'.format(
        callback=str(request.args.get('callback')), data=json.dumps(log)))
    response.mimetype = 'application/json'
    return response
