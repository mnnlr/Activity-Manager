# -*- mode: python ; coding: utf-8 -*-

from kivy_deps import sdl2, glew

a = Analysis(
    ['monitor.py'],
    pathex=[r'C:\Users\Dhruv PC\Desktop\Activity-Manager\Kivy'],
    binaries=[],
    datas=[
        ('login.kv', '.'),
        ('sample.kv', '.'),
        ('icon.png', '.'),  
        ('logo.png', '.')
    ],
    hiddenimports=[
        'kivy',
        'kivy.core',
        'kivy.core.window',
        'kivy.core.text',
        'kivy.lang',
        'kivy.factory',
        'kivy.graphics',
        'kivy.uix',
        'kivymd',
        'kivymd.uix',
        'kivymd.uix.card',
        'kivymd.uix.button',
        'kivymd.uix.label',
        'kivymd.uix.dialog',
        'kivymd.uix.datatables',
        'kivymd.uix.gridlayout',
        'kivymd.uix.scrollview',
        'login_screen', 
        'success_screen',
        'logout_action',
        'action',
        'extract_cookie',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
    name='activity_monitor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='C:\\Users\\Dhruv PC\\Desktop\\Activity-Manager-responsive\\Kivy\\logo.ico', 
)
