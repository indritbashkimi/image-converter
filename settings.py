import multiprocessing

def cpu_count():
    try:
        NPROCS = multiprocessing.cpu_count()
    except:
        NPROCS = 1
    return NPROCS

mime_whitelist = (
    'audio/',
    'video/',
    'application/ogg',
    'application/x-id3',
    'application/x-ape',
    'application/vnd.rn-realmedia',
    'application/x-pn-realaudio',
    'application/x-shockwave-flash',
    'application/x-3gp',
)

filepattern = (
			   (('All files'),'*.*'),
               ('JPEG','*.jpg;*.jpeg'),
               ('PNG','*.png'),
               ('WEBP','*.webp')
              )

settings = {
            'q':        85,     # default quality
            'dir':      '',     # output dir
            'qfile':    True,   # use the quality specified on the file name
            'replace':  True,   # replace existing files
            'pass':     0,      # <int> analysis pass number (1..10)
            'size':     0,      # target size (in bytes)
            'quiet':    True,   #
            'mt':       True    # use multithreading, only for dwebp (non usarlo)
           }