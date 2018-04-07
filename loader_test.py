import test
import kvs
import loader


class LoadImagesTestCase(test.TestCase):
    def setUp(self):
        self.kvs = kvs.Dict()
        self.image_iterator = [
            (
                'http://dbpedia.org/resource/Azhikode,_Thrissur',
                'http://commons.wikimedia.org/wiki/Special:FilePath/Azhikode_Munakkal_-_Estuary_(Hari_Bhagirath).jpg'
            ),
            (
                'http://dbpedia.org/resource/Azhikode,_Kannur',
                'http://commons.wikimedia.org/wiki/Special:FilePath/Gulikan_vellattam.jpg'
            ),
        ]

    def test_load_image_kvs(self):
        loader.load_images(self.kvs, self.image_iterator)
        for key, value in self.image_iterator:
            self.assertItemsEqual(self.kvs.get(key), [value])


class LoadTermsTestCase(test.TestCase):
    def setUp(self):
        self.kvs = kvs.Dict()  # label word => category
        self.images_kvs = kvs.Dict()  # category => URL
        self.label_iterator = [
            (
                "http://dbpedia.org/resource/American_National_Standards_Institute",
                "American National Standards Institute"
            )
        ]
        self.word_categories = [
            ('American', 'http://dbpedia.org/resource/American_National_Standards_Institute'),
            ('National', 'http://dbpedia.org/resource/American_National_Standards_Institute'),
            ('Standards', 'http://dbpedia.org/resource/American_National_Standards_Institute'),
            ('Institute', 'http://dbpedia.org/resource/American_National_Standards_Institute'),
        ]

    @test.mock.patch('loader.Stemmer.stem')
    def test_load_labels(self, mock):
        mock.side_effect = lambda x: x
        self.images_kvs.put(
            'http://dbpedia.org/resource/American_National_Standards_Institute',
            'http://upload.wikimedia.org/wikipedia/commons/8/8f/ANSI_logo.GIF')
        loader.load_terms(self.kvs, self.images_kvs, self.label_iterator)
        for word, category in self.word_categories:
            self.assertItemsEqual(self.kvs.get(word), [category])
        mock.assert_has_calls([
            test.mock.call('American'), test.mock.call('National'),
            test.mock.call('Standards'), test.mock.call('Institute')
        ])

    def test_load_labels_no_image(self):
        loader.load_terms(self.kvs, self.images_kvs, self.label_iterator)
        for word, category in self.word_categories:
            with self.assertRaises(KeyError):
                self.kvs.get(word)


if __name__ == '__main__':
    test.main()
