import urllib.request, tempfile, bz2, os

class Downloader:
    """Retrieve and extract wikispecies dump files"""

    def __init__(self):
        """Construct a downloader"""
        pass

    def download(self, web_location):
        """Download a dump file and store it in the user's temporary folder"""

        tmp_dir = tempfile.gettempdir()
        web_filename = web_location.split('/')[-1]
        local_location = "%s/%s" % (tmp_dir, web_filename)

        urllib.request.urlretrieve(web_location, local_location)
        decompressed_location = self.extract(local_location)

        return decompressed_location

    def extract(self, local_location):
        """Extract the given compressed file"""
        
        decompressed_location = local_location[:-4]

        data = bz2.BZ2File(local_location).read()
        output = open(decompressed_location, 'w')
        output.write(data)
        output.close()
        os.remove(local_location)

        return decompressed_location
