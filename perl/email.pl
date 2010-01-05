#!/usr/bin/perl -wT

# loosely based off of http://github.com/zigdon/Zigdon/blob/master/cgi/mktmp.pl

use Data::Dumper;

use strict;
use CGI;

$ENV{"PATH"}="";

my $q = new CGI;
my $emailaddress = "stu\@sente.cc";

my $DEBUG=0;
my $D;
if ($DEBUG){
	open($D,  ">>/var/www/sente/htdocs/logs/cgi.log") or die "cannot open debug file: $!";
}
else{
	open($D,  ">>/dev/null") or die "cannot open devnull for debug: $!";
}


print $q->header;

print "<html><body>";
my $dir = "/usr/lib/cgi-bin/paste";
if ($q->param('id') and $q->param('id') =~ /(\d+)/) {
  my $id = $1;
  if (open(NOTE, "$dir/$1")) {
    print "<pre>";
    print <NOTE>;
    close NOTE;
    print "</pre><br />";
  } else {
    print "That link no longer exists. ";
    print "You can create a new one at <a href=\"/cgi-bin/email.pl\">here</a>.";
  }
} elsif ($q->param('note') and $q->param('note') =~ /(.*)/s) {
  my $note = $1;
  $note =~ s/&/&amp;/g;
  $note =~ s/</&lt;/g;
  $note =~ s/>/&gt;/g;
 
  my $id = int(rand(1e4));
  my $count = 100;
  while (open ID, "$dir/$id") {
    $id = int(rand(1e4));
    last unless --$count;
  }
 
  if ($count == 0) {
    print "Failed to save note, sorry. Try again later.";
  } else {
    if (open(ID, ">$dir/$id")) {
      print ID $note;
      close ID;
			
		my $file =  $id;
		
		$file =~ s/\s//g;


      my $subject="http://sente.cc/cgi-bin/email.pl?id=$id";
			
		if(open(MAIL, "| /usr/bin/mail -s $subject $emailaddress")) {
			print MAIL $subject;
			print MAIL "\n\n";
			print MAIL $note;
			close MAIL;
		}else{
			print "cannot send email $!";
		}

      print "<pre>\n";
      print "an email has been sent\n";
		print "<a href=\"http://sente.cc/cgi-bin/email.pl?id=$id\">http://sente.cc/cgi-bin/email.pl?id=$id</a>\n";
		print "<hr/>";
		print $note;
		print "</pre>";
    } else {
      print "Failed to save/email your note: $!. Try again later.";
    }
  }
} else {
  print <<HTML;
<html><head><title>Leave a "secure" note</title></head>
<body><form action="/cgi-bin/email.pl" method="post">
Enter text:<br />
<textarea name="note" cols="70" rows="30"></textarea><br />
<input type="submit" value="Save note" />
</form>
HTML
}
 
print "</body></html>";
