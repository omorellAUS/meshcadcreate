# mac_packaging.spec - For creating double-clickable MeshCADCreate.app

block_cipher = None

a = Analysis(
    ['src/meshcadcreate/cli.py'],
    pathex=['src'],
    binaries=[],
    datas=[
        ('README.md', '.'),
        ('LICENSE', '.'),
        ('installer', 'installer'),
    ],
    hiddenimports=['open3d', 'trimesh', 'PySide6', 'scipy', 'numpy', 'matplotlib'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='meshcad',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    target_arch='x86_64',
)

app = BUNDLE(
    exe,
    name='MeshCADCreate.app',
    icon='installer/meshcad_icon.icns',
    bundle_identifier='com.perthresoles.meshcad',
    info_plist={
        'CFBundleShortVersionString': '1.0',
        'CFBundleVersion': '1.0',
        'NSHighResolutionCapable': 'True',
    },
)
