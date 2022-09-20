# -*- coding: UTF8 -*-
# Este arquivo é parte do programa SupyPlay
# Copyright 2010–2022 Carlo Oliveira <carlo@nce.ufrj.br>,
# `Labase <http://labase.activufrj.nce.ufrj.br>`__; `GPL <http://j.mp/GNU_GPL3>`__.
#
# SupyPlay é um software livre; você pode redistribuí-lo e/ou
# modificá-lo dentro dos termos da Licença Pública Geral GNU como
# publicada pela Fundação do Software Livre (FSF); na versão 2 da
# Licença.
#
# Este programa é distribuído na esperança de que possa ser útil,
# mas SEM NENHUMA GARANTIA; sem uma garantia implícita de ADEQUAÇÃO
# a qualquer MERCADO ou APLICAÇÃO EM PARTICULAR. Veja a
# Licença Pública Geral GNU para maiores detalhes.
#
# Você deve ter recebido uma cópia da Licença Pública Geral GNU
# junto com este programa, se não, veja em <http://www.gnu.org/licenses/>
"""Controller handles routes starting with /code.

.. codeauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

Changelog
---------

.. versionadded::    22.09
        Adds version from version.py file.

"""
from bottle import Bottle, get, view, post, request
from model.datasource import DS
from base64 import decodebytes as dcd
from base64 import encodebytes as ecd
from version import __version__

__author__ = 'carlo'
DEFAULT_CODE = """# default
try:
    import superpython.%s.main as main
    main.main()
except:
    from browser import document, html
    document["pydiv"].html = ""
    document["pydiv"] <= html.IMG(src="/images/site_em_construcao_.jpg")
"""
MENU = "Help,/site/help.html:About,/site/about.html:Home,/"
CSS = "solarized codemirror bulma style roboto".split()
JS = "codemirror show-hint python-hint active-line matchbrackets python".split()
# JS = "brython brython_stdlib codemirror show-hint python-hint active-line matchbrackets python".split()

appbottle = Bottle()  # create another WSGI application for this controller and resource.


# debug(True) #  uncomment for verbose error logging. Do not use in production


@post('/play/__create')
def gamer_create():
    codename, code = request.json['codename'], request.json['code']
    # codename, code = request.query['codename'], request.query['code']

    project, *moduler = codename.split('/')
    filename = "/".join(moduler)
    code = dcd(str.encode(code)).decode("utf-8")
    try:
        code_status = DS.create_file(project, filename, code)
    except Exception as err:
        code_status = "Fail creating {}: {}".format(filename, err)
    return code_status


@post('/play/__save')
def gamer_save():
    codename, code = request.json['codename'], request.json['code']
    # codename, code = request.query['codename'], request.query['code']

    project, *moduler = codename.split('/')
    filename = "/".join(moduler)
    # print(f"game_controller ->> gamer_save() codename:{codename} filename:{filename}")
    code = dcd(str.encode(code)).decode("utf-8")
    try:
        code_status = DS.save_file(project, filename, code)
    except Exception as err:
        code_status = "Fail saving {}: {}".format(filename, err)
    return code_status


@post('/play/__append_log')
def gamer_append_log():
    codename, code = request.json['codename'], request.json['code']
    # codename, code = request.query['codename'], request.query['code']

    project, *moduler = codename.split('/')
    filename = "/".join(moduler)
    code = dcd(str.encode(code)).decode("utf-8")
    try:
        code_status = DS.append_file(project, filename, code)
    except Exception as err:
        code_status = "Fail saving {} {}: {}".format(project, filename, err)
        print("gamer_append_logException", code_status)
    return code_status


@get('/play/<mod>/<name>')
@view("play")
def gamer(mod, name):
    modl, namel = mod.lower(), name.lower()
    # noinspection PyBroadException
    try:
        code_file = DS.get_file_contents(modl, namel)
        code = code_file.content
        # code = dcd(str.encode(code_file.content)).decode("utf-8")
    except Exception as _:
        code = "# " + ".".join([modl, namel, "main.py"])
        code = ecd(bytearray(code.encode("UTF8"))).decode("utf-8")
        print("gamerException", code)

    return dict(
        pagetitle='SupyPlay - {} - {}'.format(mod.capitalize(), name.capitalize()), title=name,
        modText=mod.capitalize(),
        nameText=name.capitalize(),
        image="supygirls_logo.png", mod=mod.replace(',', '_').lower(), code=code,
        brython_css=CSS, brython_js=JS,
        menu=[m.split(",") for m in MENU.split(":")],
        version=__version__
    )
