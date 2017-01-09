# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 11:53:08 2016

@author: betienne
"""

import requests
import re
import urllib
import time


class Translator(object):

    def __init__(self):
        """
        Change client_id and client_secret api key if needed
        Register at datamarket.azure.com
        """
        self._client_secret = "XXX"
        self._client_id = "ZZZ"
        self._url_request = "http://api.microsofttranslator.com"
        self._grant_type = "client_credentials"
 #       self._proxies = {'https' : 'https://00.00.00.00:0000',
 #                      'http' : 'http://00.00.00.00:0000'}
        print("-"*50)
        print("{:>30s}".format("WARNING !"))
        print("-"*50)
        print("The API works with a key, and is limited to 2,000,000 characters"
        +" per month. Be careful to respect this limit.")


    def change_proxies(self):
        """
        Sometimes you need to change proxies 
        """
        if self._proxies['http'] == 'http://00.00.00.00:0000':
            self._proxies['http'] = 'http://00.00.00.00:0000'

        if self._proxies['https'] == 'https://00.00.00.00:0000':
            self._proxies['https'] = 'https://00.00.00.00:0000'

    def _get_token(self):
        """
        Get token for API request. The data obtained herein are used
        in the variable header.
        Returns:
            token['access_token'] : access token key of returned token
                                    dictionary, string
        """
        args = {'client_id': self._client_id,
                'client_secret': self._client_secret,
                'scope': self._url_request,
                'grant_type': self._grant_type}

        formatted_args = urllib.parse.urlencode(args).encode("utf-8")

        oauth_url = "https://datamarket.accesscontrol.windows.net/v2/OAuth2-13"
        token = requests.post(oauth_url,
                              data=formatted_args,
                              proxies=self._proxies).json()
        return(token['access_token'])


    def translate(self, text, src, dst):
        """
        Translate a given text from a source language to a target language
        Args:
            text : text to translate, string
            src : source language, string
            dst : target language, string
        Returns:
            r : translated text, string
        """
        uri = "http://api.microsofttranslator.com/v2/Http.svc/Translate?"
        args = "text=" + text + "&from=" + src + "&to=" + dst
        headers = {"Authorization" : "Bearer " + self._get_token()}

        message = """
        ERROR : Failed to send the request. Make sure :
        1) the languages you gave are correct.
        Visit https://msdn.microsoft.com/en-us/library/hh456380.aspx
        2) you might want to change proxies by calling the change_proxies()
        method
        """

        try:
            r = requests.get(uri+args,
                             headers=headers,
                             proxies=self._proxies)

            return(re.findall(r'>(.+)<', r.text)[0])
        except Exception:
            self.change_proxies()
            print("Proxies have been changed. Please retry")


    def test(self):
        """
        To test if service works correctly with Chinese
        The result must be "Bonjour"
        """
        print(self.translate('你好', 'zh-CN', 'fr'))


if __name__=='__main__':

    t = Translator()
    t.test()

