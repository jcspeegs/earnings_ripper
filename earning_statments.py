#!/usr/bin/env python

import logging
from pdf_ripper import PDFripper as Rip
import yaml
import os


def parse_yaml(file='metadata.yaml') -> dict:
    with open(file, 'r') as fl:
        dict = yaml.load(fl, Loader=yaml.FullLoader)
    return dict


def main():
    logging.basicConfig(level=logging.INFO)
    DRY_RUN = True
    OUT = os.path.join(os.getenv('HOME'), 'Downloads')

    metadata = parse_yaml()
    sites = {k: Rip(metadata[k].get('url'), dry_run=DRY_RUN) for k in metadata}
    for name, site in sites.items():
        path = os.path.join(OUT, name)
        site.extract(path)


if __name__ == '__main__':
    main()
