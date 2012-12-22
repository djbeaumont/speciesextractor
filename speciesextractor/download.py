import urllib, tempfile, bz2, os

def download():
	"""
	Download a dump file and store it in the user's temporary folder
	"""
	tmp_dir = tempfile.gettempdir()
	web_location = "http://dumps.wikimedia.org/specieswiki/20121213/specieswiki-20121213-pages-meta-current.xml.bz2"
	web_filename = web_location.split('/')[-1]
	local_location = "%s/%s" % (tmp_dir, web_filename)

	urllib.urlretrieve(web_location, local_location)
	decompressed_location = extract(local_location)

	return decompressed_location

def extract(local_location):
	"""
	Extract the given compressed file
	"""
	decompressed_location = local_location[:-4]

	data = bz2.BZ2File(local_location).read()
	output = open(decompressed_location, 'w')
	output.write(data)
	output.close()
	os.remove(local_location)

	return decompressed_location