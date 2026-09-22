#!/usr/bin/env python3

# Allow direct execution
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import http.server
import threading

from test.helper import FakeYDL, expect_dict, expect_value, http_server_port
from yt_dlp.compat import compat_etree_fromstring
from yt_dlp.extractor import YoutubeIE, get_info_extractor
from yt_dlp.extractor.common import InfoExtractor
from yt_dlp.utils import (
    ExtractorError,
    RegexNotFoundError,
    encode_data_uri,
    strip_jsonp,
)

TEAPOT_RESPONSE_STATUS = 418
TEAPOT_RESPONSE_BODY = "<h1>418 I'm a teapot</h1>"


class InfoExtractorTestRequestHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        if self.path == '/teapot':
            self.send_response(TEAPOT_RESPONSE_STATUS)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(TEAPOT_RESPONSE_BODY.encode())
        else:
            assert False


class DummyIE(InfoExtractor):
    def _sort_formats(self, formats, field_preference=[]):
        self._downloader.sort_formats(
            {'formats': formats, '_format_sort_fields': field_preference})


class TestInfoExtractor(unittest.TestCase):
    def setUp(self):
        self.ie = DummyIE(FakeYDL())

    def test_ie_key(self):
        self.assertEqual(get_info_extractor(YoutubeIE.ie_key()), YoutubeIE)

    def test_html_search_regex(self):
        html = '<p id="foo">Watch this <a href="http://www.youtube.com/watch?v=BaW_jenozKc">video</a></p>'
        search = lambda re, *args: self.ie._html_search_regex(re, html, *args)
        self.assertEqual(search(r'<p id="foo">(.+?)</p>', 'foo'), 'Watch this video')

    def test_opengraph(self):
        ie = self.ie
        html = '''
            <meta name="og:title" content='Foo'/>
            <meta content="Some video's description " name="og:description"/>
            <meta property='og:image' content='http://domain.com/pic.jpg?key1=val1&amp;key2=val2'/>
            <meta content='application/x-shockwave-flash' property='og:video:type'>
            <meta content='Foo' property=og:foobar>
            <meta name="og:test1" content='foo > < bar'/>
            <meta name="og:test2" content="foo >//< bar"/>
            <meta property=og-test3 content='Ill-formatted opengraph'/>
            <meta property=og:test4 content=unquoted-value/>
            '''
        self.assertEqual(ie._og_search_title(html), 'Foo')
        self.assertEqual(ie._og_search_description(html), 'Some video\'s description ')
        self.assertEqual(ie._og_search_thumbnail(html), 'http://domain.com/pic.jpg?key1=val1&key2=val2')
        self.assertEqual(ie._og_search_video_url(html, default=None), None)
        self.assertEqual(ie._og_search_property('foobar', html), 'Foo')
        self.assertEqual(ie._og_search_property('test1', html), 'foo > < bar')
        self.assertEqual(ie._og_search_property('test2', html), 'foo >//< bar')
        self.assertEqual(ie._og_search_property('test3', html), 'Ill-formatted opengraph')
        self.assertEqual(ie._og_search_property(('test0', 'test1'), html), 'foo > < bar')
        self.assertRaises(RegexNotFoundError, ie._og_search_property, 'test0', html, None, fatal=True)
        self.assertRaises(RegexNotFoundError, ie._og_search_property, ('test0', 'test00'), html, None, fatal=True)
        self.assertEqual(ie._og_search_property('test4', html), 'unquoted-value')

    def test_html_search_meta(self):
        ie = self.ie
        html = '''
            <meta name="a" content="1" />
            <meta name='b' content='2'>
            <meta name="c" content='3'>
            <meta name=d content='4'>
            <meta property="e" content='5' >
            <meta content="6" name="f">
        '''

        self.assertEqual(ie._html_search_meta('a', html), '1')
        self.assertEqual(ie._html_search_meta('b', htm
# ... [truncated] ...
http://api.new.livestream.com/accounts/6115179/events/6764928/videos/144884262.f4m',
                    'ext': 'flv',
                    'format_id': '2148',
                    'protocol': 'f4m',
                    'tbr': 2148,
                    'width': 1280,
                    'height': 720,
                }]
            ),
        ]

        for f4m_file, f4m_url, expected_formats in _TEST_CASES:
            with open('./test/testdata/f4m/%s.f4m' % f4m_file, encoding='utf-8') as f:
                formats = self.ie._parse_f4m_formats(
                    compat_etree_fromstring(f.read().encode()),
                    f4m_url, None)
                self.ie._sort_formats(formats)
                expect_value(self, formats, expected_formats, None)

    def test_parse_xspf(self):
        _TEST_CASES = [
            (
                'foo_xspf',
                'https://example.org/src/foo_xspf.xspf',
                [{
                    'id': 'foo_xspf',
                    'title': 'Pandemonium',
                    'description': 'Visit http://bigbrother404.bandcamp.com',
                    'duration': 202.416,
                    'formats': [{
                        'manifest_url': 'https://example.org/src/foo_xspf.xspf',
                        'url': 'https://example.org/src/cd1/track%201.mp3',
                    }],
                }, {
                    'id': 'foo_xspf',
                    'title': 'Final Cartridge (Nichico Twelve Remix)',
                    'description': 'Visit http://bigbrother404.bandcamp.com',
                    'duration': 255.857,
                    'formats': [{
                        'manifest_url': 'https://example.org/src/foo_xspf.xspf',
                        'url': 'https://example.org/%E3%83%88%E3%83%A9%E3%83%83%E3%82%AF%E3%80%80%EF%BC%92.mp3',
                    }],
                }, {
                    'id': 'foo_xspf',
                    'title': 'Rebuilding Nightingale',
                    'description': 'Visit http://bigbrother404.bandcamp.com',
                    'duration': 287.915,
                    'formats': [{
                        'manifest_url': 'https://example.org/src/foo_xspf.xspf',
                        'url': 'https://example.org/src/track3.mp3',
                    }, {
                        'manifest_url': 'https://example.org/src/foo_xspf.xspf',
                        'url': 'https://example.com/track3.mp3',
                    }]
                }]
            ),
        ]

        for xspf_file, xspf_url, expected_entries in _TEST_CASES:
            with open('./test/testdata/xspf/%s.xspf' % xspf_file, encoding='utf-8') as f:
                entries = self.ie._parse_xspf(
                    compat_etree_fromstring(f.read().encode()),
                    xspf_file, xspf_url=xspf_url, xspf_base_url=xspf_url)
                expect_value(self, entries, expected_entries, None)
                for i in range(len(entries)):
                    expect_dict(self, entries[i], expected_entries[i])

    def test_response_with_expected_status_returns_content(self):
        # Checks for mitigations against the effects of
        # <https://bugs.python.org/issue15002> that affect Python 3.4.1+, which
        # manifest as `_download_webpage`, `_download_xml`, `_download_json`,
        # or the underlying `_download_webpage_handle` returning no content
        # when a response matches `expected_status`.

        httpd = http.server.HTTPServer(
            ('127.0.0.1', 0), InfoExtractorTestRequestHandler)
        port = http_server_port(httpd)
        server_thread = threading.Thread(target=httpd.serve_forever)
        server_thread.daemon = True
        server_thread.start()

        (content, urlh) = self.ie._download_webpage_handle(
            'http://127.0.0.1:%d/teapot' % port, None,
            expected_status=TEAPOT_RESPONSE_STATUS)
        self.assertEqual(content, TEAPOT_RESPONSE_BODY)


if __name__ == '__main__':
    unittest.main()

