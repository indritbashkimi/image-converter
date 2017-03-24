
supported_files = ('.gif', '.jpg', 'jpeg', '.png', '.webp')
supported_formats = ('JPEG', 'PNG', 'WebP')

file_pattern = (
    ('All files', '*.*'),
    ('JPEG', '*.jpg;*.jpeg'),
    ('PNG', '*.png'),
    ('WebP', '*.webp')
)

parameters = {
            'output_format': 'webp',
            'quality':  85,     # default quality
            'dir':      '',     # output dir
            'qfile':    True,   # use the quality specified on the file name
            'replace':  True,   # replace existing files
            'size':     0,      # target size (in bytes)
            'pass':     1,      # <int> analysis pass number (1..10)
            'quiet':    True,   # debug
            'mt':       True    # use multithreading, only for dwebp (non usarlo)
           }