# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['C:\\Users\\lishu\\PycharmProjects\\untitled\\UI\\mainCode.py','C:\\Users\\lishu\\PycharmProjects\\untitled\\UI\\False_Lable.py','C:\\Users\\lishu\\PycharmProjects\\untitled\\UI\\MainDis.py','C:\\Users\\lishu\\PycharmProjects\\untitled\\UI\\EmptyUI.py','C:\\Users\\lishu\\PycharmProjects\\untitled\\Animal\\RuleBase.py'],
             pathex=['C:\\Users\\lishu\\PycharmProjects\\untitled\\UI'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
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
          [],
          exclude_binaries=True,
          name='mainCode',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='mainCode')
