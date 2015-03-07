from spotify.utils.cache import Cache


class IntegrationTestCase(object):
    def setUp(self):
        Cache.clear()

    def tearDown(self):
        Cache.clear()