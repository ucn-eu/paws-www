#!/usr/bin/perl -wT
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser); 
use DBI;
use Mail::Sender;
#use lib 'lib';
use WWW::Twilio::API;
use strict;
use DateTime;

print header;
print start_html(
	-title	=>	'PAWS User Creation',
	-style	=>	{'src'	=>	'/styles/style.css'},
);
#print img { src => "/images/pawshdrmid.png", align => "CENTER" }; 
print img { src => "/images/Paws-Logo.jpg", align => "CENTER" }; 

my $dbh = DBI->connect( "dbi:mysql:radius", "radius", "radius_Par0la") or 	
    &dienice("Can't connect to db: $DBI::errstr");
	
my $username = param('username');
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


my $account_sid = "ACc07c0a5e06a6874e320a2e7023e71fa8"; 
my $auth_token = "653e4fb633fef83e0d10c58abc7a2871";

##########
my $user_code = param( 'code' );



if( $user_code ){

  # select the user from the database with all known values instead of just first name,
  # may be better to use primary key and pass it to the url and use it as id,
  my $query = q{select * from temp_user where code = ? };
  my $sth   = $dbh->prepare( $query );
  $sth->execute( $user_code );
  my $row   = $sth->fetchrow_hashref();
  my ($dbuser, $dbcode ) = ( $row->{ 'fname' }, $row->{ 'code' } );

  # I am checking only for the user with first name, may be check for all known values
  # otherwise reuse the original table by adding  two new columns one for code and other for
  # status, once the code is confirmed change the status to yes or 1 so you can check the
  # user status at any point.
  if( ( $username == $dbuser ) and ( $user_code == $dbcode ) ){
   $sth = $dbh->prepare("DELETE FROM radcheck  WHERE username=? AND attribute = 'Auth-Type'") or &dbdie;
        $sth->execute($username) or &dbdie;
#print "Location: https://vpn.publicaccesswifi.org/secure-cgi/signup_user.cgi/";  
 print "<h3>Account Verified</h3>Thanks for registering with PAWS, your account for $lastname is verified. Using your WiFi enabled device (e.g smartphone or laptop), connect to the PAWS WiFi signal where it is available, open your proper and type vpn.publicaccesswifi.org in the address bar and press enter, then follow the instructions to 'set up PAWS on my device'." 

  }
  exit;
}
######


if (!defined $username ) {
	&print_form;
	exit(0)
}

if ($username !~ /^\w{3,32}$/) {
	&dienice("Please use an alphanumeric username between 3 and 32 letters long, with no spaces.");   
}

if ($telephone == 0) {
&dienice("Please enter a mobile number.");
}

#  perl -e '$blah=join "", map{(a..z,A..Z,0..9)[rand 62]} 0..7; print $blah'
if ($randpass eq "rp") {
	#my @ichars = (a..z, A..Z, 0..9);
	my @ichars = ("A".."Z", "a".."k", "m".."z", "0", "2".."9");
	$newpass1 .= $ichars[rand @ichars] for 1..8;
}
else {
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
		&dienice("Please use an alphanumeric value for the password reminder  between 2 and 128 letters long, with no spaces.");   
	}

# rand password
# my $rand_pass = map{(a..z,A..Z,0..9)[rand 62]} 0..7'

my $signup = "Self Signup";
my $rec;
my $sth = $dbh->prepare("select * from radcheck where username = ?") or &dbdie;
$sth->execute($username) or &dbdie;
if ( $rec = $sth->fetchrow_hashref) {
	#print "DU: $rec->{username}, DP: $rec->{value}\n";
    &dienice("Username $username already exists in PAWS database!");
}

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

$sth = $dbh->prepare("INSERT INTO radcheck  VALUES (NULL, ?, 'Auth-Type', ':=', 'Reject')") or &dbdie; 
$sth->execute($username) or &dbdie;


$sth = $dbh->prepare("INSERT INTO radcheck  VALUES (NULL, ?, 'Password', '==', ?)") or &dbdie; 
$sth->execute($username, $newpass1) or &dbdie;

$sth = $dbh->prepare("INSERT INTO radreply  VALUES (NULL, ?, 'Session-Timeout', ':=', '10800')") or &dbdie; 
$sth->execute($username) or &dbdie;

my $ts = DateTime->now->datetime;
my $notes = "Add notes here";

#$sth = $dbh->prepare("INSERT INTO radremind  VALUES (NULL, ?, ?, ?, ?)") or &dbdie; 



### Steve add: get user's IP to track for self sign up
my $q = new CGI; ## create a CGI object
my $user_ip = $q->remote_host();
#print $user_ip;
### End: Steve add

#$sth = $dbh->prepare("INSERT INTO radpawsusers  VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)") or &dbdie; 
#$sth->execute($username, $firstname, $lastname, $housenumber, $streetname, $postcode, $telephone, $email, $passwordquestion, $passwordanswer, $signup, $notes, $ts) or &dbdie;

$sth = $dbh->prepare("INSERT INTO radpawsusers  VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)") or &dbdie; 
$sth->execute($username, $firstname, $lastname, $housenumber, $streetname, $postcode, $telephone, $email, $passwordquestion, $passwordanswer, $signup, $notes, $ts, $user_ip) or &dbdie;

######

#------------------------------------------------------------------
# from here its the registration process of sending emails etc;
my $query = q{Insert into temp_user values ( ?, ?, ?, ? ) };

# unique 8 digit code
my @set = ('0' ..'9', 'A' .. 'Z');
my $code = join '' => map $set[rand @set], 1 .. 8;

# populate the database to use this value;
my $sth = $dbh->prepare( $query );

# not checking the values, have to do it to make sure all values are intact;
 $sth->execute( $username, $lastname, $postcode, $code ) || die "Cant add the rows to the database";

eval{
#  if ( $email eq "" ) {
  send_sms( $username, $lastname, $postcode, $code, $telephone );
#  } else {
  send_mail( $username, $lastname, $postcode, $code, $email ); 
# }	
};
#if( $@ ){
#  print "Your registration failed for following reasons. ".$@;
#  exit;
#}

#if ( $email eq "" ) {
print "</br>$username added for activation. <br/> $lastname, please check your mobile for our text message (SMS). Click the link in the message (or paste the link in a browser) and finish the activation." ;
#} else {
#print "</br>$username added for activation. <br/> $lastname, please check your email for our message. Clink the link in the message  and finish the activation." ;
#}
#------------------------------------------------------------------
sub send_mail{
  my ( $username, $lastname, $postcode, $code, $email ) = @_;

  my $sender = new Mail::Sender {
          smtp => 'localhost',
          from => 'DoNotReply@vpn.publicaccesswifi.org',
          on_errors => undef,
  } or die "Can't create the Mail::Sender object: $Mail::Sender::Error\n";
  $sender->Open({
          to => 'c.greiffenhagen@lboro.ac.uk',
          cc => 'Murray.Goulden@nottingham.ac.uk,Richard.Mortier@nottingham.ac.uk,David.Morton@nottingham.ac.uk,Steve.North@nottingham.ac.uk',
          subject => 'User Self-Sign-Up: New account added'
  }) or die "Can't open the message: $sender->{'error_msg'}\n";
  $sender->SendLineEnc("Username: $username, has signed up today. Check the admin page for more details\n\n");

  $sender->SendLineEnc("\n\nBest regards,\nThe PAWS Team\n");
  $sender->Close()
          or die "Failed to send the message: $sender->{'error_msg'}\n";
}

################
sub send_sms{
my ( $username, $lastname, $postcode, $code, $telephone ) = @_;
my $twilio = new WWW::Twilio::API( AccountSid => $account_sid,
                                   AuthToken  => $auth_token, );

    my $response = $twilio->POST('SMS/Messages',
                                 From => '441158241502',
                                 To   => $telephone,
                                 Body => "Click for PAWS: https://vpn.publicaccesswifi.org/secure-cgi/signup_user.cgi?username=$username&code=$code");
#    print $response->{content};

}

################


if ($randpass eq "rp") {

	print qq(
	<h2>Success:</h2>
	<p>
	Username: $username
	<br>
	Password: $newpass1
	<br>
	<br>


	</p>
	);
}
else {
	print qq(
	<h2>Success:</h2>
	<p>
	Username: $username
	<br>
	Password: NOT DISPLAYED
	</p>
	);
}

print "<br><br><br>";

print end_html;
exit 0;

###############################################

sub print_form {

# menu
my $q1 = 'Mother\'s maiden name?';
my $q2 = 'Pet\'s name?';
my $q3 = 'School name?';

my @menuvalues = ($q1, $q2, $q3);


	print qq(<h1>User Self-Sign-Up:</h1>);
	print start_form;

	print table(

	Tr(
		td('<b>Personal information</b>'),
		td(' ')
	),

	Tr(
		td('First name (mandatory):'),
		td(
			textfield(
				-name 	=>	'firstname',
				-size	=>	'64',
				-maxlength	=>	'128',
			)
		)
	),
	Tr(
		td('Last name (mandatory):'),
		td(
			textfield(
				-name 	=>	'lastname',
				-size	=>	'64',
				-maxlength	=>	'64',
				-onblur		=> "document.forms[0].username.value = document.forms[0].firstname.value + document.forms[0].lastname.value;"
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
		td('Mobile  number (mandatory):'),
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
		td('<br><b>Account information</b>'),
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
		td('<br><b>Password reminder question</b>'),
		td(' ')
	),

	Tr(
		td(
			popup_menu(
        			-name    => 'passwordquestion',
        			-values  => \@menuvalues,
        			-default => $q1
    			)
		),
		td(
			textfield(
				-name 	=>	'passwordanswer',
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



