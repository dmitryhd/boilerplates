#!/usr/bin/env python3

"""
Simple web config editor
"""

# pylint: disable=import-error

import os
import argparse
import logging
import json
import flask as fl

from crm_mini import config as cfg
from crm_mini.file_context import Context

config = cfg.Config
context = Context(config)

EXE_PATH = 'crm_mini.py'

log = logging.getLogger('werkzeug')
log.setLevel(logging.WARN)


def get_application(given_config=None) -> fl.Flask:
    """ Configure application from settings. """
    if given_config:
        global context
        context = Context(given_config)
    app = fl.Flask(__name__)
    app.debug = True
    set_routing(app)
    print(context.working_dir)
    return app


def set_routing(app):
    """
    Set url routes to given application.
    """
    # Views
    app.add_url_rule('/', 'edit_config_view', edit_config_view)
    # REST api
    app.add_url_rule('/api/save_config/', 'save_config',
                     save_config, methods=['POST'])
    app.add_url_rule('/api/command/', 'command',
                     execute_command, methods=['POST'])
    app.add_url_rule('/api/get_log/', 'get_log', get_log)


REST_SUCCESS = json.dumps({'success': True}), 200, \
               {'ContentType': 'application/json'}
REST_FAIL = json.dumps({'success': False}), 400, \
               {'ContentType': 'application/json'}

# -------------------------
# Views


def edit_config_view():
    """ Main view """
    log.info('config: {}'.format(context.working_dir))
    first_sheet = config['Attachment']['Sheets'][0]['name']
    return fl.render_template(
        'edit_config.html',
        recipients=context.get_recipients(),
        html_template=context.get_html_template(),
        sheet_sql=context.get_sheet_sql(first_sheet),
        log=get_log()
    )

# -------------------------
# Rest API


def save_config():
    """ REST get config """
    post_data = fl.request.get_json()
    if not post_data:
        return REST_FAIL
    log.info('save to: {}'.format(context.working_dir))
    if 'recipients' in post_data:
        log.warn('Write recipients to {}'.format(context.recipients))
        context.set_recipients(post_data['recipients'])
    if 'html_template' in post_data:
        log.warn('Write html_template to {}'.format(context.html_template))
        context.set_html_template(post_data['html_template'])
    if 'sheets_sql' in post_data:
        name = config['Attachment']['Sheets'][0]['name']
        file_location = context.sheet[name]
        log.warn('Write sheets_sql to {}'.format(file_location))
        # TODO: write only to first now
        context.set_sheet_sql(name, post_data['sheets_sql'])
    return REST_SUCCESS


def execute_command():
    post_data = fl.request.get_json()
    if not post_data:
        return REST_FAIL
    if 'command' in post_data:
        # TODO refactor it, system is bad approach to this
        command = post_data['command']
        log.info('Get command: {}'.format(command))
        os.system('{} {}'.format(EXE_PATH, command))
    return REST_SUCCESS


def get_log():
    try:
        with open(context.log_file, 'r') as fd:
            lines = fd.readlines()
            lines.reverse()
            return ''.join(lines)
    except FileNotFoundError:
        return 'no log file'


def parse_args():  # pragma: no cover
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=cfg.DEFAULT_PORT)
    return parser.parse_args()


def run_server(port=cfg.DEFAULT_PORT):  # pragma: no cover
    app = get_application()
    log.info('config: {}'.format(context.working_dir))
    app.run(port=port)


def main():  # pragma: no cover
    args = parse_args()
    run_server(args.port)

if __name__ == '__main__':  # pragma: no cover
    main()
