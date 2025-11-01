# a nix-shell env with all dependancies (nixOS)
{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python3
    figlet
  ];

  shellHook = ''
    echo "entered shellklok.py nix-shell environment..."
    ecgi "exit with ctrl+d"
  '';
}
