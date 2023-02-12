#!/usr/bin/env python

from pdf_ripper import PDFripper as rip
import yaml


def parse_yaml(file='metadata.yaml') -> dict:
    with open(file, 'r') as fl:
        dict = yaml.load(fl, Loader=yaml.FullLoader)
    return dict


def main():
    metadata = parse_yaml()
    sites = {k: rip(metadata[k].get('url')) for k in metadata}
    for name, site in sites.items():
        site.extract('output')


if __name__ == '__main__':
    main()
