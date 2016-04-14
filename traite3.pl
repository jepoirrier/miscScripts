#!/usr/bin/perl
# traite3 : test internet connection; now gnuplot is piped from script itself

use Time::HiRes;
use Net::Ping;

# Variables
$host = "www.jabber.org"; # hostname to check
$maxtimetowait = 5; # maximum time to wait between ping, in seconds
$maxiteration = 500; # maximum number of iterations/pings
$i = 0; # simple iterator

# builds the filename for the data, the graph and the string for the graph title
($s, $m, $h, $day, $month, $yearoffset, $dow, $doy, $dsl) = localtime();
$month++;
$year = 1900 + $yearoffset;
$datafilename = "traite-" . $year . $month . $day . $h . $m . $s;
$graphfilename = $datafilename . ".png";
$datafilename = $datafilename . ".dat";
$chainetitre = $year . "/" . $month . "/" . $day;

# Simple information on time
$maxminutes = $maxtimetowait * $maxiteration / 60;
printf("It's now $h:$m:$s. Processing will take a maximum of %.2f minute(s).\n", $maxminutes);

open(OUTPUT, ">$datafilename")
	or die "impossible to create the data file";

print "Data will be stored in file $datafilename\n";

# builds the ping object
$p = Net::Ping->new("tcp");
$p->hires();

while($i < $maxiteration)
{
	# build timestamp
	($s, $m, $h, $day, $month, $yearoffset, $dow, $doy, $dsl) = localtime();
	$month++;
	$year = 1900 + $yearoffset;
	
	# do ping
	($ret, $duration, $ip) = $p->ping($host);

	# write part of the result
	$chaine = "$day/$month/$year $h:$m:$s $host $ip ";

	# check results
	if($ret==1)
	{
		$duration *= 1000;
		$chaine = $chaine . $duration;
	}
	else
	{
		printf("NaN");
	}
	
	# write end of the result string
	$chaine = $chaine . " ms";

	# print the result, both on screen (with a % indication) ...
	$percentage = $i * 100 / $maxiteration;
	printf("$chaine %.1f %% done\n", $percentage);
	
	# ...	and in the datafile
	print OUTPUT $chaine . "\n";

	$timetowait = rand($maxtimetowait) + 1;
	sleep($timetowait);

	$i++;
}

# ensure we are on a new line
print "\n";

# close ping object and the output file
$p->close();
close(OUTPUT)
	or die "Impossible to close the data file ($datafilename). Results should however be all right\n";

# open pipe for Gnuplot
open(PLOT, "| gnuplot")
	or die "Impossible to launch gnuplot\n";

print PLOT qq{set term png small\n};
print PLOT qq{set xdata time\n};
print PLOT qq{set timefmt "\%H:\%M:\%S"\n};
print PLOT qq{set format x "\%H:\%M:\%S"\n};
print PLOT qq{set missing 'NaN'\n};
print PLOT qq{set out "$graphfilename"\n};
print PLOT qq{set title "Internet connection test\\nTarget: $host\\n$chainetitre"\n};
print PLOT qq{set xlabel "Hours:Minutes:Seconds"\n};
print PLOT qq{set ylabel "Ping response time (ms)"\n};
print PLOT qq{set autoscale y\n};
print PLOT qq{set autoscale x\n};
print PLOT qq{plot '$datafilename' using 2:5 notitle with lines\n};
print PLOT qq{reset\n};

# close the pipe to Gnuplot
close(PLOT)
	or die "Impossible to close the pipe -> gnuplot";

# Inform the graph filename
print "Graph is stored in file $graphfilename\n";

# Now, it's finished!
