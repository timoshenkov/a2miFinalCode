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

"""Querier for Image search"""
from __future__ import absolute_import, print_function, unicode_literals

import argparse
import logging

from .loader import (
    IMAGES_KVS_NAME, TERMS_KVS_NAME, STORAGE_CHOICES, Stemmer)


def parse_args(prog='querier', description='Image querier.'):
    parser = argparse.ArgumentParser(prog=prog, description=description)
    parser.add_argument('-d', dest='debug', action='store_true', help="debug")
    parser.add_argument(
        'keywords', nargs='*', help="find image URLs that match KEYWORDS")
    parser.add_argument(
        '--kvs', choices=STORAGE_CHOICES.keys(), default='disk',
        help="store data in KVS")
    return parser.parse_args()


def query(keywords, images_kvs, terms_kvs):
    """Find images that match keywords.

    This function open connections to both the terms and images key/value
    stores. For each keyword, it retrieves the matching Wikipedia category
    from the terms store, then retrieve all URL matches for those
    categories from the images key/value store.

    Args:
        keywords: string, keywords separated by whitespace.
        terms_kvs: object, key-value store with (term, category) pairs
        image_kvs: object, key-value store with (category, url) pairs

    Returns:
        list of image urls matching keywords
    """
    return [] 


def main():
    args = parse_args()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    logging.debug('debug {}'.format(args.debug))
    logging.debug('kvs {}'.format(args.kvs))

    images_kvs = STORAGE_CHOICES[args.kvs](IMAGES_KVS_NAME)
    terms_kvs = STORAGE_CHOICES[args.kvs](TERMS_KVS_NAME)
    matches = query(args.keywords, images_kvs, terms_kvs)

    print("keywords {}".format(' '.join(args.keywords)))
    print("matches \n{}".format('\n'.join(matches)))

if __name__ == '__main__':
    main()