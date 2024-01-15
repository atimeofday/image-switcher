# window.py
#
# Copyright 2023 Ian Off
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# 	http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0

from gi.repository import Adw, Gio, Gtk
import subprocess

@Gtk.Template(resource_path='/org/ublue/ImageSwitcher/window.ui')
class UblueImageSwitcherWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'UblueImageSwitcherWindow'

    rebase, spin, desktop, driver, hardware = [Gtk.Template.Child() for i in range(5)]


    def run_rebase(widget, operation, self):

        spin_desktop_lookup = {
            "main-gnome":    "silverblue",
            "main-kde":      "kinoite",
            "main-sway":     "sericea",
            "bazzite-kde":   "bazzite",
            "bluefin-gnome": "bluefin",
            "bluefin-kde":   "error",
        }

        command_signing = "ostree-image-signed:docker://ghcr.io/ublue-os/" if True else "ostree-unverified-registry:ghcr.io/ublue-os/"

        spin     =                     self.spin.get_selected_item().get_string().lower()
        desktop  = "-"               + self.desktop.get_selected_item().get_string().lower()
        hardware = ""  if (hardware := self.hardware.get_selected_item().get_string().lower()) == "general"     else "-" + hardware
        driver   = ""  if (driver   := self.driver.get_selected_item().get_string().lower())   == "open source" else "-" + driver

        rebase = spin_desktop_lookup.get(spin + desktop, spin + desktop) + hardware + driver
        if "-" not in rebase:
            rebase = rebase + "-main"

        if "error" in rebase:
            print("Image does not exist, please try other options.")
        else:
            rebase_command = f"rpm-ostree rebase {command_signing}{rebase}:latest"
            subprocess.run(f"flatpak-spawn --host {rebase_command}", shell=True)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.rebase.connect("clicked", self.run_rebase, self)

