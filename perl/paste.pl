#!/usr/bin/perl -wT
 
# The idea is to present a CGI over https, allowing you to leave a note with a
# link that will work exactly once.
#
# The design attempts to be secure, both from non-root attackers on the server,
# or from remote attacks.
#
# Let's assume brute force attacks will be blocked on the IP level (say, any IP
# hitting the CGI 50 times in an hour will be blocked for a day). This won't
# stop brute force attacks local to the server, so suggestions would be welcome
# there too.
#
# The onetime directory has odd permissions - root owned, 0733, meaning you can
# read a file if you know it's name, but you can't list it.
 
use strict;
use CGI;
 
my $q = new CGI;
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
    print "This link is no longer valid. ";
    print "You can enter a new one <a href=\"/cgi-bin/paste.pl\">here</a>.";
  }
} elsif ($q->param('note') and $q->param('note') =~ /(.*)/s) {
  my $note = $1;
  $note =~ s/&/&amp;/g;
  $note =~ s/</&lt;/g;
  $note =~ s/>/&gt;/g;
 
  my $id = int(rand(1e3));
  my $count = 100;
  while (open ID, "$dir/$id") {
    $id = int(rand(1e3));
    last unless --$count;
  }
 
  if ($count == 0) {
    print "Failed to save note, sorry. Try again later.";
  } else {
    if (open(ID, ">$dir/$id")) {
      print ID $note;
      close ID;
 
		print "<code>";
      print "Your note has been saved. Please send this link to the recipient:<br />\n";
      print "http://sente.cc/cgi-bin/paste.pl?id=$id";
		print "\n<br />";
      print "This link will work one time only - it will automatically be deleted after it's visited.";
    } else {
      print "Failed to save your note: $!. Try again later.";
    }
  }
} else {
  print <<HTML;
<html><head><title>Leave a "secure" note</title></head>
<body><form name="paste" action="/cgi-bin/paste.pl" method="post" >
Enter text:<br />
<textarea name="note" cols="60" rows="20"></textarea><br />
<input type="submit" value="Save note" />
</form>
HTML
}
 
print "</body></html>";
