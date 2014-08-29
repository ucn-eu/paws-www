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
	
my $un = param('un');
my $activation = param('activation');
my $username = param('username');
my $password = param('password');
my $newpass1 = param('newpass1');
my $newpass2 = param('newpass2');
my $randpass = param('randpass');

my $firstname = param('firstname');
my $lastname = param('lastname');

my $housenumber = param('housenumber');
my $streetname = param('streetname');
my $postcode = param('postcode');
my $telephone = param('telephone');
my $email = param('email');


my $passwordquestion = param('passwordquestion');
my $passwordanswer = param('passwordanswer');



if ( defined $username ) {

if ($username !~ /^\w{3,32}$/) {
	&dienice("Please use an alphanumeric username between 3 and 32 letters long, with no spaces.");   
}

#  perl -e '$blah=join "", map{(a..z,A..Z,0..9)[rand 62]} 0..7; print $blah'
if ($randpass eq "rp") {
	#my @ichars = (a..z, A..Z, 0..9);
	my @ichars = ("A".."Z", "a".."k", "m".."z", "0", "2".."9");
	$newpass1 .= $ichars[rand @ichars] for 1..8;
}
elsif ($newpass1 ne "" && $newpass2 ne "") {
	if ($newpass1 !~ /^\w{8,24}$/) {
		&dienice("Please use an alphanumeric value for new password  between 8 and 24 letters long, with no spaces.");   
	}
	if ($newpass2 !~ /^\w{8,24}$/) {
		&dienice("Please use an alphanumeric value for new password confirmation  between 8 and 24 letters long, with no spaces.");   
	}

	if ($newpass1 ne $newpass2) {
   		&dienice("You didn't type the same thing for both new password fields. Please check it and try again.");
	}
}

if ($passwordanswer !~ /^.{2,128}$/) {
	&dienice("Please use an alphanumeric value for Answer 1  between 2 and 128 letters long.");   
}

# rand password
# my $rand_pass = map{(a..z,A..Z,0..9)[rand 62]} 0..7'

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
my $sth = $dbh->prepare("UPDATE radpawsusers SET firstname=?, lastname=?, housenumber=?, streetname=?, postcode=?, telephone=?, email=?, passwordquestion=?, passwordanswer=? WHERE username=?") or &dbdie; 
$sth->execute($firstname, $lastname, $housenumber, $streetname, $postcode, $telephone, $email,  $passwordquestion, $passwordanswer, $username) or &dbdie;


if ($newpass1 ne "" ) {
	$sth = $dbh->prepare("UPDATE radcheck  SET value=? WHERE username=?") or &dbdie; 
	$sth->execute($newpass1, $username) or &dbdie;

}


################


if ($randpass eq "rp") {
	print "<h2>User $username updated with password $newpass1.</h2>\n";
}
else {
	print "<h2>User $username updated.</h2>\n";
}


print "<br><br><br>";
print "<a href='/'>Back to homepage</a>";
print end_html;
exit 0;
}
###############################################
if (defined $un) {

my $sth = $dbh->prepare("select * from radcheck where username = ? and value = ?") or &dbdie;
$sth->execute($un,$password) or &dbdie;
my $rec;
unless ( $rec = $sth->fetchrow_hashref) {
&dienice("Either Username $un could not be found PAWS database or password is wrong");
}

my $sth = $dbh->prepare("select * from radpawsusers where username = ?") or &dbdie;
        $sth->execute($un) or &dbdie;
        my $rec;
        unless ( $rec = $sth->fetchrow_hashref) {
        &dienice("Username $un could not be found PAWS database!");
	 }

	$sth = $dbh->prepare("select * from radcheck where username = ? and attribute = 'Auth-Type' and value = 'Reject'") or &dbdie;
	$sth->execute($un) or &dbdie;
	my $ua = "ACTIVATED";
	my $ua_status = 1;
	my $ua_action = "deactivate";
	my $ua_tick = "Untick";
	my $rec1;
	if ( $rec1 = $sth->fetchrow_hashref) {
		$ua = "NOT ACTIVATED";
		$ua_status = 0;
		$ua_action = "activate";
		$ua_tick = "Tick";
	}

	# menu
	my $q1 = 'Mother\'s maiden name?';
	my $q2 = 'Pet\'s name?';
	my $q3 = 'School name?';
	
	my @menuvalues = ($q1, $q2, $q3);



	print "<h1>Hello $rec->{firstname} $rec->{lastname}. Welcome to the PAWS account update page.</h1>";
	print start_form(
		-action => '/secure-cgi/edit_details.cgi'
		);


 	print hidden(
        	-name      => 'username',
        	-default   =>  $rec->{username}
    	);

	print table(
	Tr(
		td('<br><b>Account information</b>'),
		td('<br><font color="red">Please leave the password fields and tickbox empty if you do NOT wish to reset the user password.</font>')
	),

	Tr(
		td('Username:'),
		td("<b> $rec->{username} </b>")
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
		td('First name: (mandatory)'),
		td(
			textfield(
				-name 	=>	'firstname',
				-size	=>	'64',
				-maxlength	=>	'64',
				-value		=> $rec->{firstname}	
			)
		)
	),
	Tr(
		td('Last name: (mandatory)'),
		td(
			textfield(
				-name 	=>	'lastname',
				-size	=>	'64',
				-maxlength	=>	'128',
				-value		=> $rec->{lastname}	
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
				-value		=> $rec->{housenumber}	
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
				-value		=> $rec->{streetname}	
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
				-value		=> $rec->{postcode}	
			)
		)
	),

	Tr(
		td('Mobile Number (mandatory):'),
		td(
			textfield(
				-name 	=>	'telephone',
				-size	=>	'16',
				-maxlength	=>	'16',
				-value		=> $rec->{telephone}	
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
				-value		=> $rec->{email}	
			)
		)
	),








	Tr(
		td('<br><b>Password reminder questions</b>'),
		td(' ')
	),




        Tr(
                td(
                        popup_menu(
                                -name    => 'passwordquestion',
                                -values  => \@menuvalues,
                                -default => $rec->{passwordquestion}
                        )
                ),
                td(
                        textfield(
                                -name   =>      'passwordanswer',
                                -size   =>      '64',
                                -maxlength      =>      '128',
                                -default => $rec->{passwordanswer}
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
				-value	=>	'Update User!',
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



