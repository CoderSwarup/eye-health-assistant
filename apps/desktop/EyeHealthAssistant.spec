# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Eye Health Assistant.

This spec bundles:
- Application source code
- Content files (exercises, eye care articles)
- PySide6 runtime libraries
- Platform-specific dependencies
"""

import os
import sys

# Path setup
SPEC_DIR = os.path.dirname(os.path.abspath(SPEC))
SRC_DIR = os.path.join(SPEC_DIR, 'src')
CONTENT_DIR = os.path.join(SRC_DIR, 'eye_health_assistant', 'content')

# Collect data files
datas = [
    # Exercise content
    (os.path.join(CONTENT_DIR, 'exercises', 'exercises.json'),
     os.path.join('eye_health_assistant', 'content', 'exercises')),
    # Eye care content
    (os.path.join(CONTENT_DIR, 'eye_care', 'eye_care.json'),
     os.path.join('eye_health_assistant', 'content', 'eye_care')),
]

# Hidden imports for PySide6 and dependencies
hiddenimports = [
    'PySide6.QtCore',
    'PySide6.QtGui',
    'PySide6.QtWidgets',
    'PySide6.QtNetwork',
    'PySide6.QtSvg',
    'PySide6.QtOpenGL',
    'PySide6.QtMultimedia',
    'PySide6.QtWebChannel',
    'PySide6.QtWebEngineWidgets',
    'sqlalchemy.dialects.sqlite',
    'sqlalchemy.ext.baked',
    'numpy',
    'numpy.core',
    'numpy.core._methods',
    'numpy.lib',
    'numpy.lib.format',
    'numpy.random',
    # Application modules
    'eye_health_assistant.core.config',
    'eye_health_assistant.core.constants',
    'eye_health_assistant.core.logging',
    'eye_health_assistant.core.exceptions',
    'eye_health_assistant.domain.models',
    'eye_health_assistant.domain.enums',
    'eye_health_assistant.application.services',
    'eye_health_assistant.infrastructure.database',
    'eye_health_assistant.infrastructure.camera',
    'eye_health_assistant.infrastructure.notifications',
    'eye_health_assistant.monitoring',
    'eye_health_assistant.blink',
    'eye_health_assistant.timer',
    'eye_health_assistant.analytics',
    'eye_health_assistant.exercises',
    'eye_health_assistant.content',
    'eye_health_assistant.settings',
    'eye_health_assistant.notifications',
]

a = Analysis(
    [os.path.join(SRC_DIR, 'eye_health_assistant', 'main.py')],
    pathex=[SRC_DIR],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib',
        'PIL',
        'scipy',
        'pandas',
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
    name='EyeHealthAssistant',
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
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='EyeHealthAssistant',
)

# macOS .app bundle
app = BUNDLE(
    coll,
    name='Eye Health Assistant.app',
    icon=None,
    bundle_identifier='com.eyehealthassistant.desktop',
    info_plist={
        'CFBundleDisplayName': 'Eye Health Assistant',
        'CFBundleShortVersionString': '0.1.0',
        'CFBundleVersion': '0.1.0',
        'NSHumanReadableCopyright': 'Copyright (c) 2026 Eye Health Assistant Contributors. MIT License.',
        'NSCameraUsageDescription': 'Eye Health Assistant uses the camera to estimate blink rate for eye wellness monitoring. Camera data is processed locally and never stored or uploaded.',
        'NSHighResolutionCapable': True,
    },
)
