import multiprocessing

def cpu_count():
    try:
        NPROCS = multiprocessing.cpu_count()
    except:
        NPROCS = 1
    return NPROCS

filepattern = (
			   (('All files'),'*.*'),
               ('JPEG','*.jpg;*.jpeg'),
               ('PNG','*.png'),
               ('WEBP','*.webp')
              )

settings = {
            'quality':      85,     # default quality
            'dir':          '',     # output dir
            'qfile':        True,   # use the quality specified on the file name
            'size':         0,      # target size (in bytes)
            'pass':         0,      # <int> analysis pass number (1..10)
            'quiet':        True,   #
           }