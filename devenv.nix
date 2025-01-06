{ pkgs, lib, config, inputs, ... }:

{
  packages = with pkgs; [
    dbus
    dbus-glib
  ];
  languages.python = {
    enable = true;
    venv.enable = true;
  };
}
