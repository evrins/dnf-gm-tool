# -*- mode: python ; coding: utf-8 -*-
import sys
import os

block_cipher = None

# --- Custom Logic: Select Icon based on Platform ---
# Default to None
icon_path = None

if sys.platform.startswith('win'):
    # Windows requires .ico
    icon_path = 'resources/icon.ico'
elif sys.platform.startswith('darwin'):
    # macOS requires .icns
    icon_path = 'resources/icon.icns'
else:
    # Linux (often uses .png, though PyInstaller exe icon support is limited on Linux)
    icon_path = 'resources/icon.ico'

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('zhconv', 'zhconv')
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'PySide6.Qtpdf',
        'PySide6.QtNetwork',
        'PySide6.QtQml',
        'PySide6.QtQuick'
    ],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='seria',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=[icon_path],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='seria',
)
app = BUNDLE(
    coll,
    name='seria.app',
    icon=icon_path,
    bundle_identifier='hu.evrins.seria',
)
