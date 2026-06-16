# mac_packaging.spec - Simplified for First Working .app (no Open3D GUI for now)

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
    hiddenimports=[
        'numpy', 'scipy', 'trimesh', 'PySide6', 'matplotlib'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['open3d'],   # Temporarily exclude Open3D to get a working .app
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
    icon='installer/meshcad_icon.png',
    bundle_identifier='com.perthresoles.meshcadcreate',
    info_plist={
        'CFBundleShortVersionString': '1.0',
        'CFBundleVersion': '1.0',
        'NSHighResolutionCapable': 'True',
    },
)
