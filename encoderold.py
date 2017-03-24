import os
import subprocess
from threading import Lock, Thread
import utils


class EncoderOld(Thread):
    def __init__(self, queue, settings, listener):
        self.filelist = queue
        self.settings = settings
        self.listener = listener
        self.stopped = False
        self.aborted = False
        self.left = len(self.filelist)
        self.size = 0
        self.totalsize = 0
        self.procs = []
        self.errors = []
        self.threads = []
        self.lock = Lock()
        Thread.__init__(self)

    def run(self):
        self.check_settings()
        self.cwebp_settings = self.get_cwebp_settings()
        self.dwebp_settings = self.get_dwebp_settings()
        for file in self.filelist:
            self.totalsize += os.path.getsize(file)
        for i in range(self.settings['jobs']):
            self.threads.append(Thread(target=self.encode))
            self.threads[i].start()
        for thread in self.threads:
            thread.join()
        if not self.aborted:
            self.listener.notify_finish(self.errors, self.stopped)

    def encode(self):
        print('New thread launched.')
        while not self.stopped:
            self.lock.acquire()
            if len(self.filelist) == 0:
                self.lock.release()
                break
            input_file = self.filelist.pop()
            self.lock.release()
            output = self.getoutput(input_file)
            print(input_file, self.get_quality(input_file))
            ext = utils.getext(input_file)
            if ext == '.webp':
                cmd = 'dwebp "%s" %s -o "%s"' % (input_file, self.dwebp_settings, output)
            elif ext == '.gif':
                cmd = 'gif2webp -q %d %s "%s" -o "%s"' % (self.get_quality(input_file), self.cwebp_settings, input_file, output)
            else: # .jpg .jpeg .png
                cmd = 'cwebp -q %d %s "%s" -o "%s"' % (self.get_quality(input_file), self.cwebp_settings, input_file, output)
            proc = subprocess.Popen(cmd, shell=True)
            self.lock.acquire()
            self.procs.append(proc)
            self.lock.release()
            proc.wait()
            if os.path.exists(output):
                if not os.path.getsize(output):
                    self.errors.append(input_file)
                    try:
                        os.system('rm "' + output + '"')
                    except:
                        pass
            else:
                self.errors.append(input_file)
            self.lock.acquire()
            self.procs.remove(proc)
            self.left -= 1
            self.update_progress(input_file)
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
        print('dir:', self.settings['dir'])        

    def get_quality(self, img):
        if self.settings['qfile']:
            # image[q89].jpg. rimuovendo l'estensione l'algoritmo lavora con dim ext generica
            img = utils.getname(img)
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
        root, ext = os.path.splitext(path) # '/home/indrit/image', '.jpg'
        print(root, ext)
        if self.settings['dir'] != '':
            root = self.settings['dir'] + utils.getname(path)
            print('nuovo root:',root)
        if ext == '.webp':
            ext = '.png'
        else:
            ext = '.webp'
        output = root + ext
        print(output)
        if not self.settings['replace']:
            i = 0
            while os.path.exists(output):
                i += 1
                output = root + '_' + str(i) + ext
        return output

    def update_progress(self, image):
        self.size += os.path.getsize(image)
        if not self.aborted:
            self.listener.update_progress(int((self.size/self.totalsize) * 100), self.left)

    def stop(self):
        self.stopped = True

    def abort(self):
        self.stopped = True
        self.aborted = True
        self.lock.acquire()
        for proc in self.procs:
            proc.terminate()
        self.lock.release()