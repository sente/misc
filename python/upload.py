import web


# a primitive upload script
# to run it: python ./upload.pl #PORT
# requires web.py

urls = ('/upload', 'Upload',
	'/', 'Upload')

web.config.debug = False

app = web.application(urls, globals()) 
session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'filename': 'gote'})

class Upload:
    def GET(self):

	session.kill()
	web.header("Content-Type","text/html; charset=utf-8")
	toreturn = """<html><head><title>A slightly less annoying solution</title></head><body><center><font size="+1"/>
<br/><br/><br/>
REPLACE
<br/><br/><form method="POST" enctype="multipart/form-data" action="">
<input type="file" name="myfile" />
<input type="submit" value="Upload it"/> </form> </body></center></html>"""

	fn = str(session.filename)

	link="Upload a file"

	if fn != "gote":
		link="<a href=\"" + str(session.filename) + "\">" + str(session.filename) + "</a>"

	newstring = toreturn.replace("REPLACE", link)
	return newstring



    def POST(self):
	x = web.input(myfile={})
	filedir = '/var/www/sente/htdocs/uploaded/'
	if 'myfile' in x: # to check if the file-object is created
	    filepath=x.myfile.filename.replace('\\','/') # replaces the windows-style slashes with linux ones.
	    filename=filepath.split('/')[-1] # splits the and chooses the last part (the filename with extension)
	    fout = open(filedir +'/'+ filename,'w') # creates the file where the uploaded file should be stored
	    fout.write(x.myfile.file.read()) # writes the uploaded file to the newly created file.
	    fout.close() # closes the file, upload complete.

	session.filename='http://sente.cc/uploaded/' + filename
	web.sendmail('stu@sente.cc', 'stu@lispclub.com' , session.filename, session.filename)
	raise web.seeother('/')

if __name__ == "__main__":
   app.run()