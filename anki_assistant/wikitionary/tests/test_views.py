class WordViewTest:
    endpoint = '/api/word/5703'

    def test_get_single_word(self, api_client):
        res = api_client().get(self.endpoint)
        assert res.status_code == 200
        assert res.data['title'] == 'dictionary'

    def test_only_GET_HEAD_and_OPTIONS_methods_are_accepted(self, api_client):
        res = api_client().get(self.endpoint)
        assert res.headers['Allow'] == 'GET, HEAD, OPTIONS'

    def test_ipa_contains_only_one_element(self, api_client):
        res = api_client().get(self.endpoint)
        ipa = res.data['ipa'].split('|')
        assert len(ipa) == 1

    def test_giving_mode_annotated_query_param_retrives_annotated_json(
        self, api_client
    ):
        res = api_client().get(self.endpoint + '?mode=annotated')
        assert res.status_code == 200
        assert res.data['audio']['include']


class WordListViewTest:
    def test_get_multiple_words(self, api_client):
        res = api_client().get("/api/words?from=10&to=20")
        assert res.status_code == 200
