# -*- mode: python ; coding: utf-8 -*-
# can run `pipenv run pyinstaller FGfGwK.spec` to generate exe.

from PyInstaller.building.api import PYZ, EXE
from PyInstaller.building.build_main import Analysis

block_cipher = None

# from https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile
added_files = [
    ('FGfGwKoptions.jsonc', './'),
    ('pelleds.jpg', './'),
    ('LICENSE', './'),
    ('README.md', './'),
]

a = Analysis(['FGfGwK.py'],
             pathex=[],
             binaries=[],
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
          cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='FGfGwK',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None)
