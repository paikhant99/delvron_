# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('views', 'views'), ('customs.py','.'), ('business', 'business'), ('persistence', 'persistence'), ('constants.py', '.'), ('images', 'images'), ('PDFViewer.py', '.')],
    hiddenimports=['tkinter.filedialog', 'tkcalendar', 'sqlite3', 'reactivex', 'win32api', 'win32con', 'win32gui', 'win32print', 'win32ui', 'PIL','reportlab.pdfgen', 'reportlab.lib', 'reportlab.platypus', 'customtkinter', 'babel.numbers', 'fitz'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
splash = Splash(
    'images/main_banner.png',
    binaries=a.binaries,
    datas=a.datas,
    text_pos=None,
    text_size=12,
    minify_script=True,
    always_on_top=True,
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    splash,
    splash.binaries,
    [],
    name='Delvron',
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
    icon=['images\\logo_color.png'],
)

