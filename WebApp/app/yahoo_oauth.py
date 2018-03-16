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
        self.access_token = None
        self.refresh_token = None
        self.expiration_time = time.time()

        # session
        self.session = None


    def authorize(self):
        '''
          Redirect to the yahoo authorize page.
          Please call this method when user request route('/authorize')
        '''
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

        self._update_token(request.args['code'])

        # update basic info
        # return current user 


    def request(self, request_str, params={'format': 'json'}):
        ''' Response to a user request '''

        # refresh access token 60 seconds before it expires
        if self.expiration_time - time.time() < 60:
            self._update_token()

        if self.session is None:
            self.session = self.service.get_session(self.access_token)

        return self.session.get(url=request_str, params=params)


    def _get_callback_url(self):
        '''
          The callback url should be something like "http://www.yourdomain.com/callback"
        '''
        return url_for('oauth_callback', _external=True)


    def _update_token(self, code=None):

        callback_url = self._get_callback_url()

        if self.refresh_token:
            data = {
                "refresh_token": self.refresh_token,
                "redirect_uri": callback_url,
                "grant_type": "refresh_token",
            }
        else:
            data = {
                "code": code,
                "redirect_uri": callback_url,
                "grant_type": "authorization_code",
            }

        raw_token = self.service.get_raw_access_token(data=data)
        parsed_token = raw_token.json()
        # print('parsed_token=', parsed_token)
        self.access_token = parsed_token["access_token"]
        self.refresh_token = parsed_token["refresh_token"]
        self.expiration_time = time.time() + parsed_token["expires_in"]

        # get session
        self.session = self.service.get_session(self.access_token)


# Initialize a YahooOAuth object
credentials_file = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'credentials.txt'))
yahoo_oauth = YahooOAuth(credentials_file)
