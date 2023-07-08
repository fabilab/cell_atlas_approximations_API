import h5py


class ApproximationFile():
    """Abstraction for accessing atlas approximation files."""
    def __init__(self, file_name, mode: str = 'r'):
        """Access atlas approximation files.

        This class should be used via the `with` statement.

        Args:
            file_name: The file name or path.
            mode: Whether to access the file as read ('r', default) or write ('w').

        NOTE: Compressing the h5 file (e.g. gz, zip) slows down access too much. Data sparsity
        is around 1/3 nonzeros for both gene expression and chromatin accessibility, but the
        latter has a lot more features (~50k GE vs ~1M CA), ballooning the file size. It would
        be great to think of a file compression approach that does not compromise on speed too
        much or, alternatively, to a lossy feature selection approach to achieve the same.
        """
        self.file_name = file_name
        self.mode = mode

    def __enter__(self):
        self.handles = [self.file_name]

        # NOTE: gzip (or zip) slows down access *considerably*
        if str(self.handles[-1]).endswith('.gz'):
            import gzip
            self.handles.append(gzip.open(self.handles[-1], self.mode+'b'))

        self.handles.append(h5py.File(self.handles[-1], self.mode))
        self.handles = self.handles[1:]
        return self.handles[-1]


    def __exit__(self, *args):
        for handle in self.handles[::-1]:
            handle.close()
        self.handles = []
