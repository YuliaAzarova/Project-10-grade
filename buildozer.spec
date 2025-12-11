[app]

title = Sort Visualizer
package.name = sortvisualizer
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,txt
requirements = python3,kivy,kivy_garden,kivy_garden.graph
presplash.filename = assets/presplash.png
icon.filename = assets/icon.png

orientation = portrait

fullscreen = 0

android.api = 33
android.ndk = 25b
android.minapi = 21

android.permissions = INTERNET

p4a.local_recipes =
p4a.branch = master

[buildozer]

log_level = 2
warn_on_root = 1
version = 1.0
