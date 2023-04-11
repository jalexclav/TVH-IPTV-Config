#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from backend.epgs import read_config_all_epgs, add_new_epg, read_config_one_epg, update_epg, delete_epg, import_epg_data
from lib.epg import read_channels_from_all_epgs, read_channels_from_epg_cache
from backend.api import blueprint
from flask import request, jsonify, current_app


@blueprint.route('/tic-api/epgs/get', methods=['GET'])
def api_get_epgs_list():
    all_epg_configs = read_config_all_epgs()
    return jsonify(
        {
            "success": True,
            "data":    all_epg_configs
        }
    )


@blueprint.route('/tic-api/epgs/settings/new', methods=['POST'])
def api_add_new_epg():
    add_new_epg(request.json)
    return jsonify(
        {
            "success": True
        }
    )


@blueprint.route('/tic-api/epgs/settings/<epg_id>', methods=['GET'])
def api_get_epg_config(epg_id):
    epg_config = read_config_one_epg(epg_id)
    return jsonify(
        {
            "success": True,
            "data":    epg_config
        }
    )


@blueprint.route('/tic-api/epgs/settings/<epg_id>/save', methods=['POST'])
def api_set_epg_config(epg_id):
    update_epg(epg_id, request.json)
    # TODO: Trigger an update of the cached EPG config
    return jsonify(
        {
            "success": True
        }
    )


@blueprint.route('/tic-api/epgs/settings/<epg_id>/delete', methods=['DELETE'])
def api_delete_epg(epg_id):
    config = current_app.config['APP_CONFIG']
    delete_epg(config, epg_id)
    # TODO: Trigger an update of the cached EPG config
    return jsonify(
        {
            "success": True
        }
    )


@blueprint.route('/tic-api/epgs/update/<epg_id>', methods=['POST'])
def api_update_epg(epg_id):
    config = current_app.config['APP_CONFIG']
    import_epg_data(config, epg_id)
    return jsonify(
        {
            "success": True,
        }
    )


##### TODO: Migrate to SQLite

@blueprint.route('/tic-api/epgs/channels', methods=['GET'])
def api_get_all_epg_channels():
    config = current_app.config['APP_CONFIG']
    epgs_channels = read_channels_from_all_epgs(config)
    return jsonify(
        {
            "success": True,
            "data":    epgs_channels
        }
    )


@blueprint.route('/tic-api/epgs/channels/<epg_id>', methods=['GET'])
def api_get_channels_from_epg(epg_id):
    config = current_app.config['APP_CONFIG']
    epgs_channels = read_channels_from_epg_cache(config, epg_id)
    return jsonify(
        {
            "success": True,
            "data":    epgs_channels
        }
    )
