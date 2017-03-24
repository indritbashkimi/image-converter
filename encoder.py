import os
import utility
from threading import Thread, Lock


class Encode(Thread):

    def __init__(self, filelist, settings, listener):
        self.filelist = filelist
        self.settings = settings
        self.listener = listener
        self.stop = False
        self.totalsize = 0
        self.size = 0
        self.errors = []
        self.threads = []
        self.lock = Lock()
        self.cwebp_settings = None
        self.dwebp_settings = None
        Thread.__init__(self)

    def run(self):
        self.cwebp_settings = self.__get_cwebp_settings()
        self.dwebp_settings = self.__get_dwebp_settings()
        for e in self.filelist:
            self.totalsize += os.path.getsize(e)
        for i in range(utility.cpu_count()-1):
            self.threads.append(Thread(target=self.encode))
            self.threads[i].start()
        self.encode()
        for thread in self.threads:
            thread.join()
        self.listener.notify_finish(self.errors)

    def encode(self):
        print('New thread launched.')
        while self.stop == False:
            self.lock.acquire()
            image = self.filelist.get()
            self.lock.release()
            if not image:
                break
            output = self.getoutput(image)
            if utility.getextension(os.path.split(image)[1]) == '.webp':
                command = 'dwebp "%s" %s -o %s > /dev/null' % (image, self.dwebp_settings, output)
            else:
                command = 'cwebp -q %d %s "%s" -o "%s" > /dev/null' % (self.get_quality(image), self.cwebp_settings, image, output)
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

            self.update_progress(image)

    def get_quality(self, img):
        # image[q89].jpg. rimuovendo l'estensione l'algoritmo lavora con dim ext generica
        img = utility.getname(img)
        if len(img) > 5 and img[-5:-3] == 'q[' and str.isnumeri(img[-3:-1]) and img[-1] == ']':
            if q == '00':
                return 100
            return int(q)
        return self.settings['q']

    def __get_cwebp_settings(self):
        s = ''
        if self.settings['pass'] != 0:
            s += ' -pass ' + str(self.settings['pass'])
        if self.settings['size'] != 0:
            s += ' -size ' + str(self.settings['size'])
        if self.settings['quiet']:
            s += ' -quiet'
        return s

    def __get_dwebp_settings(self):
        s = ''
        return s

    def getoutput(self, path):
        root, ext = os.path.splitext(path) # '/home/indrit/image', '.jpg'
        if self.settings['dir'] != '':
            root = self.settings['dir'] + os.path.split(root)[1]
        if ext == '.webp':
            return root + '.png'
        return root + '.webp'

    def update_progress(self, img):
        self.lock.acquire()
        self.filelist.done()
        self.size += os.path.getsize(img)
        self.listener.update_progress(int((self.size / self.totalsize) * 100))
        self.lock.release()

    def force_stop(self):
        self.stop = True
