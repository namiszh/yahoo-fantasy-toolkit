# -*- coding: utf-8 -*-
"""
    Yahoo OAuth

    :copyright: (c) 2018 by Marvin Huang
"""

from flask import url_for, request, redirect
from rauth import OAuth2Service
import json
import os
import time


class YahooOAuth(object):
    '''
        This class hands yahoo oauth things
    '''
    def __init__(self, credentials_file, base_url="http://fantasysports.yahooapis.com/fantasy/v2/"):
        # load credentials
        with open(credentials_file, "r") as f:
            credentials = f.read().splitlines()
        if len(credentials) != 2:
            raise RuntimeError("Incorrect number of credentials found.")

        # Initialize OAuth2 Service
        self.service = OAuth2Service(
            client_id=credentials[0],
            client_secret=credentials[1],
            name="yahoo",
            authorize_url="https://api.login.yahoo.com/oauth2/request_auth",
            access_token_url="https://api.login.yahoo.com/oauth2/get_token",
            base_url=base_url
        )

        # tokens
        self.code = None
        self.access_token = None
        self.refresh_token = None
        self.expiration_time = time.time()

        # session
        self.session = None

        # there are many case that we need to authorize,
        # the filed indicates the source info 
        self.oauth_source = None

    def is_authorized(self):
        # print('acess token', self, self.access_token)
        return self.access_token is not None

    def authorize(self, source):
        '''
          Redirect to the yahoo authorize page.
          Please call this method when user request route('/authorize')
        '''
        self.oauth_source = source

        return redirect(self.service.get_authorize_url(
            response_type='code',
            redirect_uri=self._get_callback_url())
        )


    def callback(self):
        '''
          Get user info after login in
          Please call this method when request route('/callback')
        '''
        if 'code' not in request.args:
            return None, None, None

        self.code = request.args['code']
        self._update_token()


    def request(self, request_str, params={'format': 'json'}):
        ''' Response to a user request '''

        if self.expiration_time - time.time() < 60:
            # refresh access token 60 seconds before it expires
            self._update_token()

        if self.session is None:
            self.session = self.service.get_session(self.access_token)

        return self.session.get(url=request_str, params=params)


    def _get_callback_url(self):
        '''
          The callback url should be something like "http://www.yourdomain.com/callback"
        '''
        return url_for('oauth_callback', oauth_source=self.oauth_source, _external=True)


    def _update_token(self):

        callback_url = self._get_callback_url()

        if self.refresh_token:
            data =  {
                        "refresh_token": self.refresh_token,
                        "redirect_uri": callback_url,
                        "grant_type": "refresh_token",
                    }
        else:
            data =  {
                        "code": self.code,
                        "redirect_uri": callback_url,
                        "grant_type": "authorization_code",
                    }

        raw_token = self.service.get_raw_access_token(data=data)
        parsed_token = raw_token.json()
        self.access_token = parsed_token["access_token"]
        # print('acess token', self, self.access_token)
        self.refresh_token = parsed_token["refresh_token"]
        self.expiration_time = time.time() + parsed_token["expires_in"]

        # get session
        self.session = self.service.get_session(self.access_token)



