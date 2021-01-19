import os

from VwPipeline import Loggers


class VwCache:
    def __init__(self, path: str):
        self.Path = path
        os.makedirs(self.Path, exist_ok=True)

    @staticmethod
    def _file_name(string_hash: str) -> str:
        import hashlib
        return hashlib.md5(string_hash.encode('utf-8')).hexdigest()

    def _get_path(self, context: str, args_hash: str) -> str:
        folder_name = os.path.join(self.Path, context)
        os.makedirs(folder_name, exist_ok=True)
        return os.path.join(context, VwCache._file_name(args_hash))

    def get_rel_path(self, opts_in: dict, opt_out: str = None, salt: str = None, logger = Loggers.ConsoleLogger()) -> str:
        from VwPipeline import VwOpts
        opts = VwOpts.to_string(opts_in)
        if salt:
            opts = opts + f' -# {salt}'
        args_hash = VwOpts.string_hash(opts)
        result = self._get_path(f'cache{opt_out}', args_hash)
        logger.debug(f'Generating path for opts_in: {VwOpts.to_string(opts_in)}, opt_out: {opt_out}. Result: {result}')
        return result

    def get_path(self, opts_in: dict, opt_out: str = None, salt: str = None, logger = Loggers.ConsoleLogger()) -> str:
        return os.path.join(self.Path, self.get_rel_path(opts_in, opt_out, salt, logger))
