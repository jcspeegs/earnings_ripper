{ pkgs ? import <nixpkgs> {} }:
let
  pyPacks = p: with p; [
    yfinance
    pyyaml
    requests
    pandas
    flake8
    beautifulsoup4
    ipykernel
    pytest
  ];
  py = pkgs.python311.withPackages pyPacks;
in py.env
