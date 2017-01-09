# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 11:53:08 2016

@author: BE34B2EN
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
        self._client_secret = "94FqwtC5Q51jdwqnysxquhaX/VxYl7tGjmQTS7i5Vy4="
        self._client_id = "BE34B2EN"
        self._url_request = "http://api.microsofttranslator.com"
        self._grant_type = "client_credentials"
        self._proxies = {'https' : 'https://10.34.18.10:3128',
                       'http' : 'http://10.34.18.10:3128'}
        print("-"*50)
        print("{:>30s}".format("WARNING !"))
        print("-"*50)
        print("The API works with a key, and is limited to 2,000,000 characters"
        +" per month. Be careful to respect this limit.")


    def change_proxies(self):
        """
        Sometimes you need to change proxies within Enedis
        """
        if self._proxies['http'] == 'http://10.34.18.10:3128':
            self._proxies['http'] = 'http://10.121.108.7:3128'

        if self._proxies['https'] == 'https://10.34.18.10:3128':
            self._proxies['https'] = 'https://10.121.108.7:3128'

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

#    lines = [x for x in open('sacre_coeur_chinois.txt','r',encoding='utf-8' )]
#
#    f = open('sacre_coeur_chinois_traduit.txt','a',encoding='utf-8')
#    print()
#    for i, line in enumerate(lines):
#        time.sleep(1)
#        print("Translated {:.0f} comments".format(i+1))
#        try:
#            *s, l = line.split("|")
#            f.write('|'.join(s)+"|"+t.translate(l.strip(),'zh-CN','fr')+'\n')
#        except:
#            pass
#    f.close()