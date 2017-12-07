#!/usr/bin/env python
# encoding: utf-8

from flask import abort
from flask_restful import Resource
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from .parsers import user_post_parser

from ...models import User


class AuthApi(Resource):
    def post(self):
        args = user_post_parser.parse_args()
        user = User.query.filter_by(
            username=args['username']
        ).one()

        if user.check_password(args['password']):
            #  s = Serializer(
                #  current_app.config['SECRET_KEY'],
                #  expirse_in=600
            #  )
            #  return {'token': s.dumps({'id': user.id})}
            return user.generate_auth_token(600)
        else:
            abort(401)
