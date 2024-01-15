pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'ublue_image_switcher'
gnome = import('gnome')

gnome.compile_resources('ublue-image-switcher',
  'ublue-image-switcher.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', get_option('prefix') / get_option('localedir'))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'ublue-image-switcher.in',
  output: 'ublue-image-switcher',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr--r--'
)

ublue_image_switcher_sources = [
  '__init__.py',
  'main.py',
  'window.py',
]

install_data(ublue_image_switcher_sources, install_dir: moduledir)
