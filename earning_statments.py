#!/usr/bin/env python

import logging
from pdf_ripper import PDFripper as Rip
import yaml


def parse_yaml(file='metadata.yaml') -> dict:
    with open(file, 'r') as fl:
        dict = yaml.load(fl, Loader=yaml.FullLoader)
    return dict


def main():
    logging.basicConfig(level=logging.INFO)
    dry_run = False

    metadata = parse_yaml()
    sites = {k: Rip(metadata[k].get('url'), dry_run=dry_run) for k in metadata}
    for name, site in sites.items():
        site.extract('output')


if __name__ == '__main__':
    main()
