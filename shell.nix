# Small nix-shell environment for python 3.10 + poetry
#
# See https://nixos.wiki/wiki/Python
# launch with nix-shell (and not 'nix shell' !)
#
# nix-shell --run 'python --version; poetry --version'
# Python 3.10.13
# Poetry (version 1.7.1)
#
let
  pkgs = import <nixpkgs> { };
in
pkgs.mkShell {
  packages = with pkgs; [
    (python310.withPackages (python-pkgs: with python-pkgs; [
      pip
      psycopg
      virtualenv
    ]))
    poetry
  ];
}
