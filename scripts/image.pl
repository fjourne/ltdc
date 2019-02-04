#!"D:\Tools\Strawberry\perl\bin\perl.exe"

#use CGI::Debug;
use utf8;
use warnings;
use warnings  qw(FATAL utf8);    # Fatalize encoding glitches.
use open ':encoding(UTF-8)';
use File::Spec;
use File::Copy;
use GraphViz2;
open DRAGONS, "derniersDragons.gv";
# print "Content-type: image/png\r\n\r\n"; # Affichage png
print "Content-type: text/html\r\n\r\n";

$ENV{'REQUEST_METHOD'} =~ tr/a-z/A-Z/;
if ($ENV{'REQUEST_METHOD'} eq "GET")
{
	$buffer = $ENV{'QUERY_STRING'};
}
my $graph = GraphViz2->new(strict => 1);
# Récupérer la liste des nodes concernés si sélection

$SEP = '\b|\b';

#Récupérer la liste des lieux existants
while (<DRAGONS>) {
	if (/(\w+)( \[[^\]]* shape=box\])/) {
		push @places, $1;
	}
}
close DRAGONS;
open DRAGONS, "derniersDragons.gv";

#Lorsque lié à un lieu, ne pas aller chercher les noeuds derrière celui-ci sauf lieu sélectionné dans le menu déroulant
if ($buffer =~ /im=(\w+)/) {
	(@src) = <DRAGONS>;
	push @names, $1;
	for($j=0; $j<2; $j++){
		@anames = @names;
		@dnames = @names;
		$i = -1;
		while ($#dnames != $i) {
			$i = $#dnames;
			$reg = '(\b'.join ($SEP, @names);
			$reg .='\b) ?-- ?(\w+)';
			foreach $tmp (@src) {
				if ($tmp !~ /color/ and $tmp =~ /$reg/i and (';'.(join ";", @dnames).';') !~ /;$2;/) {
					$foundname = grep { $_ eq $2 } @names;
					if( grep { $_ eq $2 } @places){
						$found = grep { $_ eq $2 } @selectedplaces;
						if($found == 0){
							push @selectedplaces, $2;
						}
					} elsif($foundname == 0) {
						push @dnames, $2;
					}
				}
			}
		}
		$i = -1;
		while ($#anames != $i) {
			$i = $#anames;
			$reg = '(\w+) ?-- ?(\b'.join ($SEP, @names);
			$reg .='\b)';
			foreach $tmp (@src) {
				if ($tmp !~ /color/ and $tmp =~ /$reg/i and (';'.(join ";", @anames).';') !~ /;$1;/) {
					$foundname = grep { $_ eq $1 } @names;
					if( grep { $_ eq $1 } @places){
						$found = grep { $_ eq $1 } @selectedplaces;
						if($found == 0){
							push @selectedplaces, $1;
						}
					} elsif($foundname == 0) {
						push @anames, $1;
					}
				}
			}
		}
		@names = (@anames, @dnames);
	}
	@names = (@names, @selectedplaces);
	close DRAGONS;
	open DRAGONS, "derniersDragons.gv";
}

while (<DRAGONS>) {
	# Ajout des nodes
	if(/(\w+) \[label=("[^\"]*"|[^ ]*) fillcolor=("[^\"]*"|[^ ]*) link="([^\"]*)" peripheries=([1-2]) shape=([^ ]*)\]/) {
		$noeud = $1;
		$label = $2;
		$color=$3;
		$url=$4;
		$periph=$5;
		$shape=$6;
		if($#names == -1 or ((';'.(join ";", @names).';') =~ /;$noeud;/i)or ($noeud =~/\d+/)){
			$url =~ s/ /_/g;
			$url =~ s/'/.27/g;
			$url =~ s/,/.2C/g;
			$url =~ s/à/.C3.A0/g;
			$url =~ s/â/.C3.A2/g;
			$url =~ s/ä/.C3.A4/g;
			$url =~ s/å/.C3.A5/g;
			$url =~ s/ç/.C3.A7/g;
			$url =~ s/è/.C3.A8/g;
			$url =~ s/é/.C3.A9/g;
			$url =~ s/ê/.C3.AA/g;
			$url =~ s/ë/.C3.AB/g;
			$url =~ s/î/.C3.AE/g;
			$url =~ s/ï/.C3.AF/g;
			$url =~ s/ô/.C3.B4/g;
			$url =~ s/ù/.C3.B9/g;
			$url =~ s/û/.C3.BB/g;
			$url =~ s/ü/.C3.BC/g;
			$url =~ s/Â/.C3.82/g;
			$url =~ s/Ä/.C3.84/g;
			$url =~ s/É/.C3.89/g;
			$url =~ s/Î/.C3.8E/g;
			$url =~ s/Ï/.C3.8F/g;
			$url =~ s/Ô/.C3.94/g;
			$url =~ s/Û/.C3.9B/g;
			$url =~ s/Ü/.C3.9C/g;
			$color =~ s/"//g;
			$label =~ s/"//g;
			$graph->add_node(name => $noeud, label => $label, shape => $shape, URL => $url, peripheries => $periph, fillcolor => $color, style => 'filled');
		}
	}

	$color = "black";

	# Ajout des edges avec label
	if (/(\w+) ?-- ?(\w+) ?\[ ?(label) ?= ?\"([^\"]+)\"/) {
		$tmp = $_;
		$noeud1 = $1;
		$noeud2 = $2;
		$label = $3;
		$labelname = $4;
		if ($#names == -1 or ((';'.(join ";", @names).';') =~ /;$noeud1;/i and (';'.(join ";", @names).';') =~ /;$noeud2;/i)
		or ($noeud1 =~/\d+/ and $noeud2 =~/\d+/)) {
		
			if ($noeud1 =~ /\d+/ and $noeud2 =~ /\d+/) {
				$graph->add_edge(from => $noeud1, to => $noeud2, color => $color, $label => $labelname);
			}
			else {
				$graph->add_edge(from => $noeud1, to => $noeud2, color => $color, $label => $labelname);
			}
		}
	}
	# Ajout des edges sans label
	elsif(/(\w+) ?-- ?(\w+)/) {
		$tmp = $_;
		$noeud1 = $1;
		$noeud2 = $2;
		if ($#names == -1 or ((';'.(join ";", @names).';') =~ /;$noeud1;/i and (';'.(join ";", @names).';') =~ /;$noeud2;/i)
		or ($noeud1 =~/\d+/ and $noeud2 =~/\d+/)) {
			if ($noeud1 =~ /\d+/ and $noeud2 =~ /\d+/) {
				$graph->add_edge(from => $noeud1, to => $noeud2, color => $color);
			}
			else {
				$graph->add_edge(from => $noeud1, to => $noeud2, color => $color);
			}
		}
	}
}

# Génération du fichier SVG
my($format)      = shift || 'svg';
my($output_file) = shift || File::Spec -> catfile('.', "dragonstmp.$format");
$graph -> run(format => $format, output_file => $output_file);

# Affichage du SVG
open SVG, "dragonstmp.$format";
# $dragonstmp, $buff;
while(read SVG, $buff, 1024) {
    $dragonstmp .= $buff;
}
close SVG;
print $dragonstmp;
# copy "dragonstmp.$format", \*STDOUT; # Affichage png

