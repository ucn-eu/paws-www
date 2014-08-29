#!/usr/bin/perl -wT
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser); 
use DBI;
use Mail::Sender;

use strict;


print header;
print start_html(
	-title	=>	'PAWS User Edit',
	-style	=>	{'src'	=>	'/styles/style.css'},
);
#print img { src => "/images/pawshdrmid.png", align => "CENTER" }; 
print img { src => "/images/Paws-Logo.jpg", align => "CENTER" }; 

my $dbh = DBI->connect( "dbi:mysql:radius", "radius", "radius_Par0la") or 	
    &dienice("Can't connect to db: $DBI::errstr");
	
my $username = param('username');
my $delete = param('delete');

if ( defined $username ) {

if ($delete eq "yes") {
        my $sth = $dbh->prepare("DELETE FROM radpawsusers WHERE username=?") or &dbdie;
        $sth->execute($username) or &dbdie;
        my $sth = $dbh->prepare("DELETE FROM radcheck WHERE username=?") or &dbdie;
        $sth->execute($username) or &dbdie;
	print "User deleted";

} else {
	print "User not deleted";
}
print "<br><br><br>";
print "<a href='lu.cgi'>List users</a>";

print end_html;
exit 0;

} else {
  &dienice("Username doesnt exist.");
}

sub dienice {
    my($msg) = @_;
    #print img { src => "/images/pawshdrmid.png", align => "CENTER" }; 
    print "<h2>Error</h2>\n";
    print $msg;
    exit;
}

sub dbdie {
    my($package, $filename, $line) = caller;
    my($errmsg) = "Database error: $DBI::errstr<br>
                called from $package $filename line $line";
    &dienice($errmsg);
}



