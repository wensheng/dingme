block_cipher = None


a = Analysis(['dingme.py'],
             pathex=['E:\\github\\dingme'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
a.datas += [('alarm.ico', 'E:\\github\\dingme\\alarm.ico',  'DATA'),
            ('WinForeground.wav', 'E:\\github\\dingme\\WinForeground.wav', 'DATA')]
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='dingme',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='alarm.ico')
