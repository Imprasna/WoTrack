from hamcrest import assert_that, not_none, none, has_entries

from spotify.utils.cache import Cache


class TestCache(object):
    def test_can_connect_to_server_successfully(self):
        memcached = Cache.memcached_handle()
        assert_that(memcached, not_none())

    def test_get_object_not_in_cache_returns_nothing(self):
        assert_that(Cache.get('i-do-not-exist'), none())

    def test_set_object_can_be_retrieved_later(self):
        fake_data = {
            'fake_property1': 'fake-property1-value',
            'fake_property2': 'fake-property2=value',
        }
        Cache.set('fake-object-key', fake_data)
        assert_that(Cache.get('fake-object-key'), has_entries({
            'fake_property1': 'fake-property1-value',
            'fake_property2': 'fake-property2=value',
        }))

    def test_can_clear_cache(self):
        fake_data = {
            'some-key': 'some value'
        }

        Cache.clear()
        assert_that(Cache.get('some-key'), none())

        Cache.set('some-key', fake_data)
        cached_data = Cache.get('some-key')
        assert_that(cached_data, not_none())
        assert_that(cached_data, has_entries(fake_data))

        Cache.clear()
        assert_that(Cache.get('some-key'), none())
