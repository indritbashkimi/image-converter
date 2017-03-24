from pathlib import Path
from threading import Lock

import settings
import utils
from encoder import Encoder, EncoderManager, EncoderListener


class ManagerListener(object):

    def on_file_add(self, path: Path, total: int):
        pass

    def on_file_remove(self, path: Path, total: int):
        pass

    def on_encoding_start(self):
        pass

    def on_file_picked(self):
        pass

    def on_file_encode(self, path: Path, success: bool, files_left: int):
        pass

    def on_progress(self, progress: float):
        pass

    def on_encoding_finish(self):
        pass

    def on_encoding_stop(self):
        pass


class Queue:
    def __init__(self):
        self._queue_lock = Lock()

    def get_next(self) -> Path:
        files = self._get_files()
        if files is None or len(files) == 0:
            return None
        with self._queue_lock:
            path = self._get_files().pop()
        return path

    def is_empty(self) -> bool:
        return self._get_files().__len__() == 0

    def _get_files(self) -> list:
        return None


mime_white_list = (
    'image/',
    'image/webp',
    'image/jpeg',
    'image/png',
)


class Manager(Queue, EncoderListener):
    def __init__(self):
        super().__init__()
        self._listeners = None
        self._files = None
        self._encoder = None
        self._mime = None
        self._parameters = settings.parameters
        self._max_cores = utils.cpu_count()
        self._encoder = None
        self._lock = Lock()
        self._working = False

    def add_file(self, path: Path):
        #print(path.absolute())
        if not self._files:
            self._files = []
        if path.is_file() and path not in self._files and self._is_supported(path):
            print('supported')
            self._files.append(path)
            for listener in self._listeners:
                listener.on_file_add(path, self._files.__len__())

    def remove_file(self, path: Path):
        if self._files is None:
            return
        index = -1
        for i, p in self._files:
            if p == path:
                index = i
                break
        if index != -1:
            self.remove_file_at(index)

    def remove_file_at(self, index: int):
        path = self._files.pop(index)
        for listener in self._listeners:
            listener.on_file_remove(path, self._files.__len__())

    def add_listener(self, listener: ManagerListener):
        if not self._listeners:
            self._listeners = set()
        self._listeners.add(listener)

    def get_encoder(self) -> Encoder:
        return self._encoder

    def set_encoder(self, encoder: Encoder):
        self._encoder = encoder

    def get_parameters(self):
        return self._parameters

    def start_job(self):
        print('start job')
        with self._lock:
            if not self._files:
                print('Nothing to convert')
                return
            if not self._working:
                if self._encoder is None:
                    self._encoder = EncoderManager(self, self._parameters, self, utils.cpu_count())
                self._encoder.do_job()
                self._working = True

    def stop_job(self):
        print('stop job')
        with self._lock:
            if self._working:
                self._encoder.abort()
                self._working = False

    def _is_supported(self, path: Path) -> bool:
        if not self._mime:
            from mimetypes import MimeTypes
            self._mime = MimeTypes()
        mime_type = self._mime.guess_type(str(path.absolute()))
        return mime_type[0] in self.supported_mime_types

    @property
    def supported_mime_types(self):
        return mime_white_list

    def _get_files(self) -> list:
        return self._files

    def on_job_done(self):
        for listener in self._listeners:
            listener.on_encoding_finish()

    def on_file_encode(self, path: Path, success: bool):
        for listener in self._listeners:
            listener.on_file_encode(path, success, len(self._files))

