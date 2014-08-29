#!/usr/bin/perl -wT
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser); 
use DBI;
use strict;

print header;
print start_html(
	-title	=>	'PAWS Users',
	-style	=>	{'src'	=>	'/styles/style.css'},
);
#print img { src => "/images/pawshdrmid.png", align => "CENTER" }; 
print img { src => "/images/Paws-Logo.jpg", align => "CENTER" }; 

print qq(<h1>PAWS Users List</h1>);

my $dbh = DBI->connect( "dbi:mysql:radius", "radius", "radius_Par0la") or 	
    &dienice("Can't connect to db: $DBI::errstr");
	

my $rec;
my $sth = $dbh->prepare("select * from radcheck where id>11 order by username,attribute") or &dbdie;
$sth->execute() or &dbdie;

print start_form;

print "<table>\n";

my $activate_me = "";
while( $rec = $sth->fetchrow_hashref) {
	#print Tr( td($rec->{username}), td($rec->{value}));
	if ($rec->{value} eq "Reject") {
		$activate_me = $rec->{username};
		next;
	}
	if ($activate_me eq $rec->{username}) {
		$activate_me = "to activate!";
	}
	
	print Tr( 
		td($rec->{username}), 
		td(' '),
		td("<a href=\'/secure-cgi/adm/eu.cgi?un=$rec->{username}\'>Edit $activate_me</a>"),
		td(' '),
		td(' '),
		td("<a href=\'/secure-cgi/adm/du.cgi?username=$rec->{username}&delete=yes\'>Delete Account</a>"),
	);

	$activate_me = "";

}

	#print "DU: $rec->{username}, DP: $rec->{value}\n";
print "</table>\n";
print end_form;
#my $rec = $sth->fetchrow_hashref; 

#my $uinfo = $sth->fetchrow_hashref;

#if (! defined $rec ) {
#	print "NOT DEFINEd\n";
#}


#if ($rec->{value} ne $oldpass) {
#   &dienice(qq(Your old password is incorrect. If you can't remember it, please use the <a href="../forgotpass.html">reset password</a> form instead.));
#}

# now store it in the database...

# temp comment
#$sth = $dbh->prepare("INSERT INTO radcheck  VALUES (NULL, ?, 'Password', '==', ?)") or &dbdie; 
#$sth->execute($username, $newpass1) or &dbdie;

#$sth = $dbh->prepare("INSERT INTO radreply  VALUES (NULL, ?, 'Session-Timeout', ':=', '10800')") or &dbdie; 
#$sth->execute($username) or &dbdie;

#$sth = $dbh->prepare("INSERT INTO radremind  VALUES (NULL, ?, ?, ?, ?)") or &dbdie; 
#$sth = $dbh->prepare("INSERT INTO radpawsusers  VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)") or &dbdie; 
#$sth->execute($username, $firstname, $lastname, $housenumber, $streetname, $postcode, $telephone, $email,  $a1, $a2, $a3) or &dbdie;

#print qq(
#<h2>Success:</h2>
#<p>
#Username: $username
#<br>
#Password: $newpass1
#</p>
#);

print end_html;
exit 0;

###############################################

sub print_form {


	print qq(<h1>User Creation:</h1>);
	print start_form;

	print table(
	Tr(
		td('<b>Account information</b>'),
		td(' ')
	),

	Tr(
		td('Username:'),
		td(
			textfield(
				-name 	=>	'username',
				-size	=>	'16',
				-maxlength	=>	'16',
				)
		)
	),

	Tr(
		td('New password:'),
		td(
			 password_field(
				-name 	=>	'newpass1',
				-size	=>	'16',
				-maxlength	=>	'16',
			)
		)
	),

	Tr(
		td('New password again:'),
		td(
			password_field(
				-name 	=>	'newpass2',
				-size	=>	'16',
				-maxlength	=>	'16',
			)
		)
	),


	Tr(
		td('Tick for random password:'),
		td(
			checkbox(
				-name    => 'randpass',
				-checked => 0,
				-value   => 'rp',
				-label   => '',
    			)
		)
	),




	Tr(
		td('<br><b>Personal information</b>'),
		td(' ')
	),

	Tr(
		td('First name:'),
		td(
			textfield(
				-name 	=>	'firstname',
				-size	=>	'64',
				-maxlength	=>	'128',
			)
		)
	),
	Tr(
		td('Last name:'),
		td(
			textfield(
				-name 	=>	'lastname',
				-size	=>	'64',
				-maxlength	=>	'128',
			)
		)
	),



	Tr(
		td('House number:'),
		td(
			textfield(
				-name 	=>	'housenumber',
				-size	=>	'4',
				-maxlength	=>	'7',
			)
		)
	),
	Tr(
		td('Street name:'),
		td(
			textfield(
				-name 	=>	'streetname',
				-size	=>	'64',
				-maxlength	=>	'128',
			)
		)
	),

	Tr(
		td('Postal code:'),
		td(
			textfield(
				-name 	=>	'postcode',
				-size	=>	'16',
				-maxlength	=>	'16',
			)
		)
	),

	Tr(
		td('Telephone number:'),
		td(
			textfield(
				-name 	=>	'telephone',
				-size	=>	'16',
				-maxlength	=>	'16',
			)
		)
	),

	Tr(
		td('Email:'),
		td(
			textfield(
				-name 	=>	'email',
				-size	=>	'64',
				-maxlength	=>	'128',
			)
		)
	),








	Tr(
		td('<br><b>Password reminder questions</b>'),
		td(' ')
	),

	Tr(
		td('Mother\'s maiden name:'),
		td(
			textfield(
				-name 	=>	'a1',
				-size	=>	'64',
				-maxlength	=>	'128',
			)
		)
	),

	Tr(
		td('Pet\'s name:'),
		td(
			textfield(
				-name 	=>	'a2',
				-size	=>	'64',
				-maxlength	=>	'128',
			)
		)
	),

	Tr(
		td('School name:'),
		td(
			textfield(
				-name 	=>	'a3',
				-size	=>	'64',
				-maxlength	=>	'128',
			)
		)
	),

	Tr(
		td('<br>'),
		td(' ')
	),


	Tr(
		td(''),
		td(
			submit(
				-name	=>	'submit_form',
				-value	=>	'Create User!',
			)
		)
	),

	);


##########
##########

	print end_form;
	print end_html;
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



