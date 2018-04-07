import test
import parser


class ImageIteratorTestCase(test.TestCase):
    def setUp(self):
        self.image_association = parser.IMAGE_ASSOCIATION
        self.text_stream = test.StringIO()
        self.text_stream.write(
            "# started 2014-07-25T21:33:17Z\n"
            "<http://dbpedia.org/resource/Albedo> " + self.image_association + " <http://commons.wikimedia.org/wiki/Special:FilePath/Albedo-e_hg.svg> .\n"
            "<http://dbpedia.org/resource/Albedo> <http://dbpedia.org/ontology/thumbnail> <http://commons.wikimedia.org/wiki/Special:FilePath/Albedo-e_hg.svg?width=300> .\n"
            "<http://commons.wikimedia.org/wiki/Special:FilePath/Albedo-e_hg.svg> <http://xmlns.com/foaf/0.1/thumbnail> <http://commons.wikimedia.org/wiki/Special:FilePath/Albedo-e_hg.svg?width=300> .\n"
            "<http://commons.wikimedia.org/wiki/Special:FilePath/Albedo-e_hg.svg> <http://purl.org/dc/elements/1.1/rights> <http://en.wikipedia.org/wiki/File:Albedo-e_hg.svg> .\n"
            "<http://commons.wikimedia.org/wiki/Special:FilePath/Albedo-e_hg.svg?width=300> <http://purl.org/dc/elements/1.1/rights> <http://en.wikipedia.org/wiki/File:Albedo-e_hg.svg> .\n"
            "<http://dbpedia.org/resource/Azhikode,_Thrissur> " + self.image_association + " <http://commons.wikimedia.org/wiki/Special:FilePath/Azhikode_Munakkal_-_Estuary_(Hari_Bhagirath).jpg> .\n"
            "<http://dbpedia.org/resource/Azhikode,_Kannur> " + self.image_association + " <http://commons.wikimedia.org/wiki/Special:FilePath/Gulikan_vellattam.jpg> .\n"
        )
        self.text_stream.seek(0)

    @test.mock.patch('parser.parse_triples')
    def test_image_iterator_filter(self, mock):
        text_stream = test.StringIO()
        filter = 'Az'
        parser.image_iterator(text_stream, filter=filter)
        mock.assert_called_once_with(
            text_stream, parser.IMAGE_ASSOCIATION, a_filter=filter)

    def test_parse_images_triples(self):
        expected = [
            ('http://dbpedia.org/resource/Azhikode,_Thrissur', 'http://commons.wikimedia.org/wiki/Special:FilePath/Azhikode_Munakkal_-_Estuary_(Hari_Bhagirath).jpg'),
            ('http://dbpedia.org/resource/Azhikode,_Kannur', 'http://commons.wikimedia.org/wiki/Special:FilePath/Gulikan_vellattam.jpg'),
        ]
        actual = list(parser.image_iterator(self.text_stream, filter="Az"))
        self.assertItemsEqual(actual, expected)
        self.assertTrue(self.text_stream.closed)


class LabelIteratorTestCase(test.TestCase):
    def setUp(self):
        self.label_association = parser.LABEL_ASSOCIATION
        self.text_stream = test.StringIO()
        self.text_stream.write(
            "# started 2014-07-25T21:33:17Z\n"
            "<http://dbpedia.org/resource/AfghanistanHistory>  " + self.label_association + " \"AfghanistanHistory\"@en .\n"
            "<http://dbpedia.org/resource/AccessibleComputing> " + self.label_association + " \"AccessibleComputing\"@en .\n"
        )
        self.text_stream.seek(0)

    @test.mock.patch('parser.parse_triples')
    def test_label_iterator(self, mock):
        list(parser.label_iterator(self.text_stream))
        mock.assert_called_once_with(self.text_stream, parser.LABEL_ASSOCIATION)

    def test_parse_labels_triples(self):
        expected = [
            ('http://dbpedia.org/resource/AccessibleComputing', 'AccessibleComputing'),
            ('http://dbpedia.org/resource/AfghanistanHistory', 'AfghanistanHistory'),
        ]
        actual = list(parser.label_iterator(self.text_stream))
        self.assertItemsEqual(actual, expected)
        self.assertTrue(self.text_stream.closed)


class StemmerTestCase(test.TestCase):
    def setUp(self):
        self.stemmer = parser.Stemmer()

    @test.mock.patch('nltk.stem.PorterStemmer.stem')
    def test_stemmer_stem(self, mock):
        self.stemmer.stem('Abc')
        mock.assert_called_once_with('Abc')

    @test.mock.patch('nltk.stem.PorterStemmer.stem')
    def test_stemmer_lower(self, mock):
        mock.side_effect = lambda x: x
        transformed = self.stemmer.stem('Abc')
        self.assertEqual(transformed, 'abc')


if __name__ == '__main__':
    test.main()
