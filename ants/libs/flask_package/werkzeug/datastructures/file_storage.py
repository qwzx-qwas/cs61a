from __future__ import annotations

import mimetypes
from io import BytesIO
from os import fsdecode
from os import fspath

from .._internal import _plain_int
from .structures import MultiDict


class FileStorage:
    """The :class:`FileStorage` class is a thin wrapper over incoming files.
    It is used by the request object to represent uploaded files.  All the
    attributes of the wrapper stream are proxied by the file storage so
    it's possible to do ``storage.read()`` instead of the long form
    ``storage.stream.read()``.
    """

    def __init__(
        self,
        stream=None,
        filename=None,
        name=None,
        content_type=None,
        content_length=None,
        headers=None,
    ):
        self.name = name
        self.stream = stream or BytesIO()

        # If no filename is provided, attempt to get the filename from
        # the stream object. Python names special streams like
        # ``<stderr>`` with angular brackets, skip these streams.
        if filename is None:
            filename = getattr(stream, "name", None)

            if filename is not None:
                filename = fsdecode(filename)

            if filename and filename[0] == "<" and filename[-1] == ">":
                filename = None
        else:
            filename = fsdecode(filename)

        self.filename = filename

        if headers is None:
            from .headers import Headers

            headers = Headers()
        self.headers = headers
        if content_type is not None:
            headers["Content-Type"] = content_type
        if content_length is not None:
            headers["Content-Length"] = str(content_length)

    def _parse_content_type(self):
        if not hasattr(self, "_parsed_content_type"):
            self._parsed_content_type = http.parse_options_header(self.content_type)

    @property
    def content_type(self):
        """The content-type sent in the header.  Usually not available"""
        return self.headers.get("content-type")

    @property
    def content_length(self):
        """The content-length sent in the header.  Usually not available"""
        if "content-length" in self.headers:
            try:
                return _plain_int(self.headers["content-length"])
            except ValueError:
                pass

        return 0

    @property
    def mimetype(self):
        """Like :attr:`content_type`, but without parameters (eg, without
        charset, type etc.) and always lowercase.  For example if the content
        type is ``text/HTML; charset=utf-8`` the mimetype would be
        ``'text/html'``.

        .. versionadded:: 0.7
        """
        self._parse_content_type()
        return self._parsed_content_type[0].lower()

    @property
    def mimetype_params(self):
        """The mimetype parameters as dict.  For example if the content
        type is ``text/html; charset=utf-8`` the params would be
        ``{'charset': 'utf-8'}``.

        .. versionadded:: 0.7
        """
        self._parse_content_type()
        return self._parsed_content_type[1]

    def save(self, dst, buffer_size=16384):
        """Save the file to a destination path or file object.  If the
        destination is a file object you have to close it yourself after the
        call.  The buffer size is the number of bytes held in memory during
        the copy process.  It defaults to 16KB.

        For secure file saving also have a look at :func:`secure_filename`.

        :param dst: a filename, :class:`os.PathLike`, or open file
            object to write to.
        :param buffer_size: Passed as the ``length`` parameter of
            :func:`shutil.copyfileobj`.

        .. versionchanged:: 1.0
            Supports :mod:`pathlib`.
        """
        from shutil import copyfileobj

        close_dst = False

        if hasattr(dst, "__fspath__"):
            dst = fspath(dst)

        if isinstance(dst, str):
            dst = open(dst, "wb")
            close_dst = True

        try:
            copyfileobj(self.stream, dst, buffer_size)
        finally:
            if close_dst:
                dst.close()

    def close(self):
        """Close the underlying file if possible."""
        try:
            self.stream.close()
        except Exception:
            pass

    def __bool__(self):
        return bool(self.filename)

    def __getattr__(self, name):
        try:
            return getattr(self.stream, name)
        except AttributeError:
            # SpooledTemporaryFile doesn't implement IOBase, get the
            # attribute from its backing file instead.
            # https://github.com/python/cpython/pull/3249
            if hasattr(self.stream, "_file"):
                return getattr(self.stream._file, name)
            raise

    def __iter__(self):
        return iter(self.stream)

    def __repr__(self):
        return f"<{type(self).__name__}: {self.filename!r} ({self.content_type!r})>"


class FileMultiDict(MultiDict):
    """A special :class:`MultiDict` that has convenience methods to add
    files to it.  This is used for :class:`EnvironBuilder` and generally
    useful for unittesting.

    .. versionadded:: 0.5
    """

    def add_file(self, name, file, filename=None, content_type=None):
        """Adds a new file to the dict.  `file` can be a file name or
        a :class:`file`-like or a :class:`FileStorage` object.

        :param name: the name of the field.
        :param file: a filename or :class:`file`-like object
        :param filename: an optional filename
        :param content_type: an optional content type
        """
        if isinstance(file, FileStorage):
            value = file
        else:
            if isinstance(file, str):
                if filename is None:
                    filename = file
                file = open(file, "rb")
            if filename and content_type is None:
                content_type = (
                    mimetypes.guess_type(filename)[0] or "application/octet-stream"
                )
            value = FileStorage(file, filename, name, content_type)

        self.add(name, value)


# circular dependencies
from .. import http