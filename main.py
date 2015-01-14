#!/usr/bin/env python
import webapp2
import urllib

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

class MainHand(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.write(*a, **kw)

	def render_str(self, template, **params):
		t = JINJA_ENV.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class FrontHand(MainHand):
	def get(self):
		self.write('Herro world! :)')

class LevelULHand(blobstore_handlers.BlobstoreUploadHandler, MainHand):
	def post(self):
		output = self.request.get("filestr")
		self.write(output)
		"""upload_files = self.get_uploads('file') #'file' is file upload field in the form
		if len(upload_files) <= 0:
			self.write('No file was attached.')
		else:
			blob_info = upload_files[0]
			self.redirect('/api/levels/%s' % blob_info.key())"""

class LevelDLHand(blobstore_handlers.BlobstoreDownloadHandler):
	def get(self, resource):
		resource = str(urllib.unquote(resource))
		blob_info = blobstore.BlobInfo.get(resource)
		self.send_blob(blob_info)

class UploadPageTestHand(MainHand):
	def get(self):
		upload_url = blobstore.create_upload_url('/api/levels')
		self.write('<html><head><title>Upload Test</title></head><body>')
		self.write('<form action="%s" method="POST" enctype="multipart/form-data">' % upload_url)
		self.write('Upload File: <input type="file" name="file"><br> <input type="submit name="submit" value="Submit"> </form></body></html>')

app = webapp2.WSGIApplication([
    ('/?', FrontHand),
    ('/api/levels/?', LevelULHand),
    ('/api/levels/([^/]+)?', LevelDLHand),
    ('/upload-page-test', UploadPageTestHand)
], debug=True)
