import datapackage
import posixpath
from nose.tools import raises
from mock import Mock, patch


class TestDatapackage(object):

    def setup(self):
        self.dpkg = datapackage.DataPackage("tests/test.dpkg")
        self.resource = datapackage.Resource(
            self.dpkg.uri,
            self.dpkg.descriptor['resources'][0])

    def teardown(self):
        pass

    def test_get_data(self):
        """Try reading the resource data"""
        data = self.resource.data
        assert data == {"foo": "bar"}

    def test_get_missing_data(self):
        """Try reading missing resource data"""
        del self.resource.descriptor['data']
        data = self.resource.data
        assert data is None

    def test_clear_data(self):
        """Check that setting data to none removes it from the descriptor"""
        self.resource.data = None
        assert 'data' not in self.resource.descriptor

    def test_set_data(self):
        """Check that setting the data works"""
        # 1 will get converted to "1" because it gets translated into
        # a json object, and json keys are always strings
        self.resource.data = {"foo": "bar", 1: 2}
        assert self.resource.data == {"foo": "bar", "1": 2}

    def test_get_path(self):
        """Try reading the resource path"""
        path = self.resource.path
        assert path == "foobar.json"

    def test_get_fullpath(self):
        """Try reading the full resource path"""
        path = self.resource.fullpath
        assert path == posixpath.join(self.dpkg.uri, "foobar.json")
        assert posixpath.exists(path)

    def test_get_missing_path(self):
        """Try reading the path when it is missing"""
        del self.resource.descriptor['path']
        path = self.resource.path
        assert path is None

    def test_get_missing_fullpath(self):
        """Try reading the full path when it is missing"""
        del self.resource.descriptor['path']
        path = self.resource.fullpath
        assert path is None

    def test_clear_path(self):
        """Check that setting path to none removes it from the descriptor"""
        self.resource.path = None
        assert 'path' not in self.resource.descriptor

    def test_clear_fullpath(self):
        """Check that setting the full path to none removes it from the
        descriptor

        """
        self.resource.fullpath = None
        assert 'path' not in self.resource.descriptor

    def test_set_path(self):
        """Check that setting the path works"""
        self.resource.path = "barfoo.json"
        assert self.resource.path == "barfoo.json"
        assert self.resource.fullpath == posixpath.join(self.dpkg.uri, "barfoo.json")

    def test_set_fullpath(self):
        """Check that setting the full path works"""
        self.resource.fullpath = posixpath.join(self.dpkg.uri, "barfoo.json")
        assert self.resource.path == "barfoo.json"
        assert self.resource.fullpath == posixpath.join(self.dpkg.uri, "barfoo.json")

    def test_get_url(self):
        """Try reading the resource url"""
        url = self.resource.url
        assert url == "http://foobar.com/"

    def test_get_missing_url(self):
        """Try reading the resource url when it is missing"""
        del self.resource.descriptor['url']
        url = self.resource.url
        assert url is None

    def test_clear_url(self):
        """Check that setting the url to none removes it from the descriptor"""
        self.resource.url = None
        assert 'url' not in self.resource.descriptor

    def test_set_url(self):
        """Try setting the resource url"""
        self.resource.url = "https://www.google.com"
        assert self.resource.url == "https://www.google.com"

    @raises(ValueError)
    def test_set_bad_url(self):
        """Try setting the resource url to an invalid url"""
        self.resource.url = "google"

    def test_get_name(self):
        """Try reading the resource name"""
        assert self.resource.name == "foobar"

    def test_get_default_name(self):
        """Try reading the default resource name"""
        del self.resource.descriptor['name']
        assert self.resource.name == ''

    def test_set_name(self):
        """Try setting the resource name"""
        self.resource.name = "barfoo"
        assert self.resource.name == "barfoo"

    def test_set_name_to_none(self):
        """Try setting the resource name to none"""
        self.resource.name = None
        assert self.resource.name == ''

    @raises(ValueError)
    def test_set_invalid_name(self):
        """Try setting the resource name to an invalid name"""
        self.resource.name = "foo bar"

    def test_get_format(self):
        """Try reading the resource format"""
        assert self.resource.format == "json"

    def test_get_default_format(self):
        """Try reading the default resource format"""
        del self.resource.descriptor['format']
        assert self.resource.format == ''

    def test_set_format(self):
        """Try setting the resource format"""
        self.resource.format = 'csv'
        assert self.resource.format == 'csv'

    def test_set_format_to_none(self):
        """Try setting the resource format to none"""
        self.resource.format = None
        assert self.resource.format == ''

    def test_get_mediatype(self):
        """Try reading the resource mediatype"""
        assert self.resource.mediatype == "application/json"

    def test_get_default_mediatype(self):
        """Try reading the default mediatype"""
        del self.resource.descriptor['mediatype']
        assert self.resource.mediatype == ''

    def test_set_mediatype(self):
        """Try setting the resource mediatype"""
        self.resource.mediatype = 'text/csv'
        assert self.resource.mediatype == 'text/csv'

    def test_set_mediatype_to_none(self):
        """Try setting the resource mediatype to none"""
        self.resource.mediatype = None
        assert self.resource.mediatype == ''

    @raises(ValueError)
    def test_set_invalid_mediatype(self):
        """Try setting the resource mediatype to an invalid mimetype"""
        self.resource.mediatype = "foo"
