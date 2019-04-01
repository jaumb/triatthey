import csv

# Override DictReader fieldnames to strip leading/trailing whitespace from field names
class DictReaderStrip(csv.DictReader):
    @property
    def fieldnames(self):
        if self._fieldnames is None:
            csv.DictReader.fieldnames.fget(self)
            if self._fieldnames is not None:
                self._fieldnames = [name.strip() for name in self._fieldnames]
                self._fieldnames = [name.lower() for name in self._fieldnames]
        return self._fieldnames
