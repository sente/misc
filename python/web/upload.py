import web
import os


urls = ('/upload', 'Upload',
	'/', 'Upload')

web.config.debug = False

app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'filename': 'gote'})


#TODO check to see if the file already exists
#TODO make sure the file is not ".htaccess" or any other troublesome files
#TODO remove the sessions dependency


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
		filedir = '/var/www/sente/htdocs/uploaded'
		#TODO check to see if the file already exists
		#TODO make sure myfile is not ".htaccess" or any other troublesome files
		#	currently the .htaccess file cannot be overwritten because thx to file perms
		if 'myfile' in x: # to check if the file-object is created
			filepath=x.myfile.filename.replace('\\','/') # replaces the windows-style slashes with linux ones.
			filename=filepath.split('/')[-1] # splits the and chooses the last part (the filename with extension)
			ffff=filedir + '/' + filename
			fout = open(ffff,'w')
			fout.write(x.myfile.file.read())
			fout.close()
			os.lchown(ffff, -1, 33) #33 is the www-data group id

		session.filename='http://sente.cc/uploaded/' + filename
		web.sendmail('stu@sente.cc', 'stu@sente.cc' , session.filename, session.filename)
	#	raise web.seeother('/')



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

if __name__ == "__main__":
	app.run()

#;vim sts:4
