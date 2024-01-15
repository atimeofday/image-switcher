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

    # Initializes UI elements defined in window.ui XML
    # To support more options, add line items to the window.ui XML definitions for the corresponding drop-down menus
    rebase, spin, desktop, driver, hardware = [Gtk.Template.Child() for i in range(5)]


    # Main application logic
    # Translates UI element selections to rebase commands, runs them, and handles errors
    def run_rebase(widget, operation, self):

        # Dictionary for refactoring spin + desktop selections to named spins
        # Substitutes "error" in the rebase command for invalid spin + desktop combinations
        # This avoids null/None handling issues, and indicates that certain combinations are known to not exist
        spin_desktop_lookup = {
            "main-gnome":    "silverblue",
            "main-kde":      "kinoite",
            "main-sway":     "sericea",
            "bazzite-kde":   "bazzite",
            "bluefin-gnome": "bluefin",
            "bluefin-kde":   "error",
            # To support or exclude new combinations, add key: value string pairs to this dictionary
        }

        # TODO replace placeholder with rpm-ostree status check to determine which registry to use
        command_signing = "ostree-image-signed:docker://ghcr.io/ublue-os/" if True else "ostree-unverified-registry:ghcr.io/ublue-os/"

        spin     =                     self.spin.get_selected_item().get_string().lower()
        desktop  = "-"               + self.desktop.get_selected_item().get_string().lower()
        hardware = ""  if (hardware := self.hardware.get_selected_item().get_string().lower()) == "general"     else "-" + hardware
        driver   = ""  if (driver   := self.driver.get_selected_item().get_string().lower())   == "open source" else "-" + driver

        # Composes rebase command from selected GUI options and handles -main image edge case
        # This may be adjusted or refined to reduce code complexity
        rebase = spin_desktop_lookup.get(spin + desktop, spin + desktop) + hardware + driver
        if "-" not in rebase:
            rebase = rebase + "-main"


        # Main error handling - "error" can be added at any stage of building the rebase command string, by any necessary logic
        # This may be extended with if clauses, or replaced with more formal exception handling
        if "error" in rebase:
            #TODO replace print with GUI message, popup, or other notification for end users
            print("Image does not exist, please try other options.")

        else:
            #TODO perform subprocess.run([command]) asynchronously so the GUI continues responding
            #TODO indicate or show rebase process status for end users
            #TODO replace shell=True (security hole) with list-based subprocess.run command; see PR #3 for example
            rebase_command = f"rpm-ostree rebase {command_signing}{rebase}:latest"
            subprocess.run(f"flatpak-spawn --host {rebase_command}", shell=True)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Connects main logic function to the rebase button in the window title bar, as defined in window.ui XML
        self.rebase.connect("clicked", self.run_rebase, self)

