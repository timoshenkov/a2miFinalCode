# Copyright 2016 Shakir James. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================

"""Parser for Wikipedia data files

Parses the images_en.nt and labels_en.nt files. The images_en.nt file
associates Wikipedia categories with images, whereas the labels_en.nt file
associates Wikipedia categories with labels

Both files consist of triples <A> <B> <C> that describe various
aspects of Wikipedia categories, not just images and labels.
You can think of these triples as an association between <A> and <C>
where <B> describes the type of association. The files contain several
kinds of triples, but, for the purposes of this assignment,
only two types are relevant: the ones in images_en.nt
where B is http://xmlns.com/foaf/0.1/depiction
(in this case, A is the category and C is an image URL), and
the ones in labels_en.nt where B is http://www.w3.org/2000/01/rdf-schema#label
(in this case, A is the category and C is the label).
"""
from __future__ import print_function

from nltk import stem


IMAGE_ASSOCIATION = '<http://xmlns.com/foaf/0.1/depiction>'
LABEL_ASSOCIATION = '<http://www.w3.org/2000/01/rdf-schema#label>'


class Stemmer(object):
    """Implement stemming algorithm."""
    def __init__(self):
        self._stemmer = stem.PorterStemmer()

    def stem(self, word):
        """Return transformed word."""
        return self._stemmer.stem(word).lower().decode('latin1')


def parse_triples(text_stream, association, a_filter=''):
    """Iterate on the DBpedia file.

    This generates (key, value) pairs with the specified association in the
    DBpedia files. The file format is <A> <B> <C> where B describes the type
    of association between <A> and <C>.

    Args:
        text_stream: file-like object, text I/O stream that produces strings.
        filter: string, yield entries with A that starts with string.
        link: string, the type of association.
    Yields:
        (A, C) pairs where A and C have the specified association.
    """
    strip = lambda s: s.replace('<', '').replace('>', '')
    next(text_stream)  # skip first line
    for line in text_stream:
        line = unicode(line)
        a, b, c = line.split()[:3]
        if b != association:
            continue
        if a_filter and not a.rsplit('/', 1)[-1].startswith(a_filter):
            continue
        yield (strip(a), strip(c))
    text_stream.close()


def image_iterator(text_stream, filter=''):
    """Iterate on the DBpedia image data.

    This generates (category, url) pairs with specified relationship in the
    DBpedia images_en.nt. The file associates Wikipedia categories with images
    in the format <A> <B> <C> where A is the category, B is the type of
    association, and C is value (e.g. url or label).

    Args:
        text_stream: file-like object, text I/O stream that produces strings.
        filter: string, yield entries with categories that starts with string.
    Yields:
        (key, value) pairs, where key is category and value is url.
    """
    return parse_triples(text_stream, IMAGE_ASSOCIATION, a_filter=filter)


def label_iterator(text_stream):
    """Iterate on the DBpedia label data.

    This generates (category, label) pairs with specified relationship in the
    DBpedia labels_en.nt . The file associates Wikipedia categories with
    labels in the format <A> <B> <C> where A is the category, B is the type of
    association, and C is the label.

    Args:
        text_stream: file-like object, text I/O stream that produces strings.
    Yields:
        (key, value) pairs, where key is category and value is label.
    """
    for category, label in parse_triples(text_stream, LABEL_ASSOCIATION):
        label = label.replace('"', '').split('@')[0]
        yield (category, label)
