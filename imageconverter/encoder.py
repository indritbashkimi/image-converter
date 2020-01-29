import subprocess
from pathlib import Path
from threading import Thread

import settings


class EncoderListener:
    def on_file_encode(self, path: Path, success: bool):
        pass


class EncoderManager(EncoderListener):
    def __init__(self, queue, parameters, listener=None, jobs=1):
        self._queue = queue
        self._parameters = parameters
        self._jobs = jobs
        self._listener = listener
        self._threads = []
        self._working = False
        self._threads_working = 0

    def do_job(self):
        print('encoder manager: do job')
        if not self._working:
            self._working = True
            self._threads_working = self._jobs
            encoder_class = self.get_encoder(self._parameters['output_format'])
            for n in range(self._jobs):
                thread = encoder_class(self._queue, self._parameters, self)
                self._threads.append(thread)
                thread.start()

    @staticmethod
    def get_encoder(output_format):
        if output_format == 'WebP':
            return WebpEncoder
        elif output_format == 'PNG':
            return PngEncoder
        elif output_format == 'JPEG':
            return JpegEncoder
        else:
            raise Exception('Unknown format ' + output_format)

    def on_job_done(self):
        if self._working:
            if self._threads_working == 0:
                raise Exception("WTF self._threads_working == 0")
            self._threads_working -= 1
            if self._threads_working == 0:
                self._listener.on_job_done()
        else:
            raise Exception("WTF job done but not working")

    def on_file_encode(self, path: Path, success: bool):
        if self._listener:
            self._listener.on_file_encode(path, success)

    def abort(self):
        if self._working:
            for thread in self._threads:
                thread.force_stop()
            for thread in self._threads:
                thread.join()
            self._working = False


class Encoder(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        pass

    def force_stop(self):
        pass


class WebpEncoder(Encoder):
    def __init__(self, queue, parameters, listener=None):
        super().__init__()
        self._queue = queue
        self._parameters = parameters
        self._listener = listener
        self._cwebp_options = None
        self._dwebp_options = None
        self._output_format = parameters['output_format']
        if self._output_format != 'WebP':
            raise Exception('Unknown output format: ' + self._output_format)

    def force_stop(self):
        super().force_stop()

    def run(self):
        print('encoder: run')
        input_path = self._queue.get_next()
        while input_path:
            output_path = self.get_output_path(input_path)
            if input_path.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                cmd = 'cwebp -q %d %s "%s" -o "%s"' % (self._get_quality(input_path),
                                                       self._get_cwebp_options(),
                                                       input_path,
                                                       output_path)
            elif input_path.suffix.lower() in ['.webp']:
                cmd = 'dwebp "%s" %s -o "%s"' % (input_path.absolute().__str__(),
                                                 self._get_cwebp_options(),
                                                 output_path.absolute().__str__())
            else:
                raise Exception("Unknown format")
            proc = subprocess.Popen(cmd + " > /dev/null", shell=True)
            proc.wait()
            if self._listener:
                self._listener.on_file_encode(input_path, True)
            input_path = self._queue.get_next()
        if self._listener:
            self._listener.on_job_done()

    def _get_quality(self, path: Path) -> int:
        if self._parameters['qfile']:
            # image[q89].jpg. rimuovendo l'estensione l'algoritmo lavora con dim ext generica
            img = path.name
            q = img[-3:-1]
            if len(img) > 5 and img[-5:-3] == '[q' and str.isnumeric(q) and img[-1] == ']':
                if q == '00':
                    return 100
                return int(q)
        return self._parameters['quality']

    def _get_cwebp_options(self) -> str:
        if self._cwebp_options is None:
            s = ''
            if self._parameters['size'] != 0:
                s += ' -size ' + str(self._parameters['size'])
            if self._parameters['pass'] != 0:
                s += ' -pass ' + str(self._parameters['pass'])
            if self._parameters['quiet']:
                s += ' -quiet'
            self._cwebp_options = s
        return ''

    def _get_dwebp_options(self) -> str:
        if self._dwebp_options is None:
            self._dwebp_options = ''
        return self._dwebp_options

    def get_output_path(self, path: Path):
        suffix = '.webp' if self._output_format == 'webp' else '.png'
        return path.with_suffix(suffix)


class PngEncoder(Encoder):
    def __init__(self, queue, parameters, listener=None):
        super().__init__()
        self._queue = queue
        self._parameters = parameters
        self._listener = listener
        raise Exception('Not implemented yet.')


class JpegEncoder(Encoder):
    def __init__(self, queue, parameters, listener=None):
        super().__init__()
        self._queue = queue
        self._parameters = parameters
        self._listener = listener
        raise Exception('Not implemented yet.')

