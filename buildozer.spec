[app]

title = BazaarYar
package.name = bazaryar
package.domain = org.bazaryar

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf

requirements = python3==3.11.9,hostpython3==3.11.9,kivy==2.3.1

orientation = portrait
version = 1.0

android.api = 35
android.minapi = 24
android.ndk = 27c
android.ndk_api = 24
android.archs = arm64-v8a

android.accept_sdk_license = True
android.enable_androidx = True

p4a.branch = master

log_level = 2
