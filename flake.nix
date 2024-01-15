{
  description = "Image Switcher for Universal Blue systems";

  inputs = {
    nixpkgs.url = "nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
  }:
    flake-utils.lib.eachDefaultSystem (
      system: let
        pkgs = import nixpkgs {inherit system;};
        native-build-inputs = with pkgs; [
              (python3.withPackages (p: with p; [
                pygobject3
                pygobject-stubs
              ]))
              gtk4
              vala
              meson
              ninja
              wrapGAppsHook4
              desktop-file-utils
              gobject-introspection
            ];
          build-inputs =  with pkgs; [
              gtk4
              glib
              gsettings-desktop-schemas
              gdk-pixbuf
              libadwaita
            ];
      in {
        packages = {
          default = self.packages.${system}.imageswitcher;
          imageswitcher = pkgs.stdenv.mkDerivation {
            pname = "ublue-image-switcher";
            version = "0.0.1-testing";
            src = ./.;
            nativeBuildInputs = native-build-inputs; 
            buildInputs = build-inputs;
            meta = with pkgs.lib; {
              homepage = "https://github.com/atimeofday/image-switcher";
              description = "Image Switcher for Universal Blue systems";
              maintainers = [null];
              license = licenses.asl20;
              platforms = platforms.unix;
            };
          };
        };

        devShells.default = pkgs.mkShell { packages = build-inputs ++ native-build-inputs; };

        formatter = pkgs.alejandra;
      }
    );
}
