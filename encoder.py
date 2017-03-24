import os
from settings import cpu_count
from threading import Lock, Thread
import utils


class Encoder(Thread):
    def __init__(self, filelist, settings, listener):
        self.filelist = filelist
        self.settings = settings
        self.listener = listener
        self.converted = 0
        self.stop = False
        self.size = 0
        self.totalsize = 0
        self.errors = []
        self.threads = []
        self.nthreads = cpu_count()
        self.index = 0
        self.lock = Lock()
        self.cwebp_settings = None
        self.dwebp_settings = None
        Thread.__init__(self)

    def run(self):
        self.check_settings()
        self.cwebp_settings = self.get_cwebp_settings()
        self.dwebp_settings = self.get_dwebp_settings()
        for file in self.filelist:
            self.totalsize += os.path.getsize(file)
        for i in range(self.nthreads):
            self.threads.append(Thread(target=self.encode))
            self.threads[i].start()
        for thread in self.threads:
            thread.join()
        new_filelist = []
        for file in self.filelist:
            if file:
                new_filelist.append(file)
        self.listener.notify_finish(self.errors, new_filelist)

    def encode(self):
        while self.stop == False and self.index < len(self.filelist):
            self.lock.acquire()
            my_index = self.index
            self.index += 1
            self.lock.release()
            image = self.filelist[my_index]
            self.filelist[my_index] = None
            output = self.getoutput(image)
            if utils.getextension(os.path.split(image)[1]) == '.webp':
                command = 'dwebp "%s" %s -o "%s"' % (image, self.dwebp_settings, output)
            else:
                command = 'cwebp -q %d %s "%s" -o "%s"' % (self.get_quality(image), self.cwebp_settings, image, output)
            os.system(command)
            if os.path.exists(output):
                if not os.path.getsize(output):
                    self.errors.append(image)
                    try:
                        os.system('rm "' + output + '"')
                    except:
                        pass
            else:
                self.errors.append(image)
            self.lock.acquire()
            self.converted += 1
            self.update_progress(image)
            self.lock.release()

    def check_settings(self):
        dest = self.settings['dir']
        if dest != '':
            if not os.path.isdir(dest):
                try:
                    os.mkdir(dest)
                except:
                    dest=''
        self.settings['dir'] = dest      

    def get_quality(self, img):
        if self.settings['qfile']:
            # image[q89].jpg. rimuovendo l'estensione l'algoritmo lavora con dim ext generica
            img = utils.getname(os.path.split(img)[1])
            q = img[-3:-1]
            if len(img) > 5 and img[-5:-3] == '[q' and str.isnumeric(q) and img[-1] == ']':
                if q == '00':
                    return 100
                return int(q)
        return self.settings['quality']

    def get_cwebp_settings(self):
        s = ''
        if self.settings['size'] != 0:
            s += ' -size ' + str(self.settings['size'])
            if self.settings['pass'] != 0:
                s += ' -pass ' + str(self.settings['pass'])
        if self.settings['quiet']:
            s += ' -quiet'
        return s

    def get_dwebp_settings(self):
        return ''

    def getoutput(self, path):
        root, ext = os.path.splitext(path)
        if self.settings['dir'] != '':
            root = self.settings['dir'] + os.path.split(root)[1]
        if ext == '.webp':
            return root + '.png'
        return root + '.webp'

    def update_progress(self, image):
        self.size += os.path.getsize(image)
        self.listener.update_progress(int((self.size / self.totalsize) * 100), self.converted)

    def abort(self):
        self.stop = True
