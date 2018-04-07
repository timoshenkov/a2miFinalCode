import test
import kvs
import querier


@test.mock.patch('querier.Stemmer.stem', side_effect=lambda x: x)
class QueryTestCase(test.TestCase):
    def setUp(self):
        self.labels_kvs = kvs.Dict()
        self.labels = {  # keyword => wiki category
            'azhar': set([
                'http://dbpedia.org/resource/Azhar_Levi_Sianturi',
                'http://dbpedia.org/resource/Azhar_College',
                'http://dbpedia.org/resource/Azhar_al-Dulaimi',
                'http://dbpedia.org/resource/Azhar_Usman'
            ]),
            'azharuddin': set([
                'http://dbpedia.org/resource/Azhikodan_Raghavan'
            ])
        }
        self.images = {  # wiki category => URL
            'http://dbpedia.org/resource/Azhar_Levi_Sianturi': set([
                'http://en.wikipedia.org/wiki/Special:FilePath/'
                'Azhar_-_Live_in_Holland_2004.jpg'
            ]),
            'http://dbpedia.org/resource/Azhar_College': set([
                'http://commons.wikimedia.org/wiki/Special:FilePath/The_Crest_'
                'of_Azhar_College_Akurana_Kandy.png'
            ]),
            'http://dbpedia.org/resource/Azhar_al-Dulaimi': set([
                'http://commons.wikimedia.org/wiki/Special:FilePath/Azhar_'
                'Dulaymi_\\u2013_Killed_19_May.jpg'
            ]),
            'http://dbpedia.org/resource/Azhar_Usman': set([
                'http://en.wikipedia.org/wiki/Special:FilePath/AzharUsman.jpg'
            ]),
            'http://dbpedia.org/resource/Azhikodan_Raghavan': set([
                'http://commons.wikimedia.org/wiki/Special:'
                'FilePath/Com_azhikodan.jpg'
            ])
        }
        self.labels_kvs = kvs.Dict()
        for label, categories in self.labels.iteritems():
            for category in categories:
                self.labels_kvs.put(label, category)

        self.images_kvs = kvs.Dict()
        for category, urls in self.images.iteritems():
            for url in urls:
                self.images_kvs.put(category, url)

    def _get_urls(self, words):
        return set([
            u for w in words for c in self.labels[w] for u in self.images[c]
        ])

    def test_query_keyword(self, mock):
        words = ['azhar']
        urls = self._get_urls(words)
        matches = querier.query(words, self.images_kvs, self.labels_kvs)
        self.assertItemsEqual(urls, matches)
        self.assertIsInstance(matches, list)

    def test_query_keywords_two(self, mock):
        words = ['azhar', 'azharuddin']
        urls = self._get_urls(words)
        matches = querier.query(words, self.images_kvs, self.labels_kvs)
        self.assertItemsEqual(urls, matches)

    def test_query_no_keyword_match(self, mock):
        try:
            querier.query(['noop'], self.images_kvs, self.labels_kvs)
        except KeyError:
            self.fail('Unexpected KeyError.')

if __name__ == '__main__':
    test.main()
