#!/usr/bin/python

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

"""Loader for Wikipedia image search

Load two key/value stores: images and terms. The images KVS maps
the DBpedia/Wikipedia category (key) to the image URLs (value),
and the terms KVS maps the a label (key) to a DBpedia categories.

To run:
$ python loader.py -d --filter=Al
"""
from __future__ import absolute_import, print_function, unicode_literals

import logging

from argparse import ArgumentParser, FileType
from .kvs import Dict, DynamoDB, Shelf
from .parser_nt import image_iterator, label_iterator, Stemmer

IMAGES_KVS_NAME = 'images'
TERMS_KVS_NAME = 'terms'
STORAGE_CHOICES = {
    'disk': Shelf,
    'mem': Dict,
    'cloud': DynamoDB
}


def parse_args(prog='loader', description='Wiki loader.'):
    parser = ArgumentParser(prog=prog, description=description)
    parser.add_argument('-d', dest='debug', action='store_true', help="debug")
    parser.add_argument(
        '--filter', default='', help="index only terms that start with FILTER")
    parser.add_argument(
        '--kvs', choices=STORAGE_CHOICES.keys(), default='disk',
        help="store data in KVS")
    parser.add_argument(
        '--images', type=FileType('r'), default='data/images_en.nt',
        help="path to images data file")
    parser.add_argument(
        '--labels', type=FileType('r'), default='data/labels_en.nt',
        help="path to labels data file")
    return parser.parse_args()


def load_images(kvs, image_iterator):
    """Build index from image data.

    Store images in KVS where the key is the Wikipedia category and the value
    is the image URL.

    For example, store the entry:
    key: http://dbpedia.org/resource/American_National_Standards_Institute
    value: http://upload.wikimedia.org/wikipedia/commons/8/8f/ANSI_logo.GIF

    Args:
        kvs: object, key-value store to store image category, URL pairs
        image_iterator: generator, yields (category, URL) pairs
    """
    
    for image in image_iterator:
        #kvs[image[0]] = image[1]
        print(image[0], '-', image[1])
        kvs.put(image[0], image[1])



def load_terms(kvs, images_kvs, label_iterator):
    """Build "inverted index" from labels data.

    Store labels in KVS where the key is a word from the label and the value
    is the Wikipedia category. The label is broken into separate words and
    stemmed.

    For example, given the label "American National Standards Institute",
    store the following entries:
    key: american
    value: http://dbpedia.org/resource/American_National_Standards_Institute

    key: nate
    value: http://dbpedia.org/resource/American_National_Standards_Institute

    key: standard
    value: http://dbpedia.org/resource/American_National_Standards_Institute

    key: institut
    value: http://dbpedia.org/resource/American_National_Standards_Institute

    Args:
        kvs: object, key-value store (modified label, category) pairs
        label_iterator: generator, yields (category, label) pairs
    """
    
    for label in label_iterator:
        category = label[0]
        words = label[1]
        #print(words)
        for word in words.split(" "):
            #kvs[word.lower()] = category
            #print("99999",word)
            #print("99999",category)
            kvs.put(word,category)
            #print("999",kvs.get(word))


def main():
    args = parse_args()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    logging.debug('debug {}'.format(args.debug))
    logging.debug('images {}'.format(args.images))
    logging.debug('labels {}'.format(args.labels))
    logging.debug('filter {}'.format(args.filter))
    logging.debug('kvs {}'.format(args.kvs))

    images = image_iterator(args.images, filter=args.filter)
    images_kvs = STORAGE_CHOICES[args.kvs](IMAGES_KVS_NAME)
    load_images(images_kvs, images)

    terms_kvs = STORAGE_CHOICES[args.kvs](TERMS_KVS_NAME)
    labels = label_iterator(args.labels)
    load_terms(terms_kvs, images_kvs, labels)

    terms_kvs.close()
    images_kvs.close()

if __name__ == '__main__':
    main()