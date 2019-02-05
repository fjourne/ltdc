#!/usr/bin/perl
use open ':encoding(UTF-8)';
use utf8;
binmode STDOUT, ":utf8";

open DRAGONS, "/tmp/derniersDragons.gv";
print "Content-type: text/html; charset=UTF-8\r\n\r\n";
print '<html>';
print '<head>';
print '<meta charset="UTF-8">';
print '<style type="text/css">';
print '.leftside {';
print 'position: absolute;';
print 'margin-left: 18%;';
print '}';
print '.centerside {';
print 'position: absolute;';
print 'margin-left: 40%;';
print '}';
print '.rightside {';
print 'position: absolute;';
print 'margin-left: 62%;';
print '}';
print '</style>';
print '<title>Affichage des trames</title>';
print '</head>';
print '<body>';
while (<DRAGONS>) {
	sub AddNoeudLabel {
	   my ($first,$second,%NoeudLabel) = @_;
	   $noeud=$first;
	   $label=$second;
		$label =~ s/"//g;
		$NoeudLabel{$label} = $noeud;
		return %NoeudLabel;
	}

	if (/(\w+) \[label=("[^"]*"|\w+)[^\]]* peripheries=2 shape=octagon\]/) {
		%trames=AddNoeudLabel($1,$2,%trames);
	}
	if (/(\w+) \[label=("[^"]*"|\w+)[^\]]* peripheries=1 shape=ellipse\]/) {
		%pnjs=AddNoeudLabel($1,$2,%pnjs);
	}
	if (/(\w+) \[label=("[^"]*"|\w+)[^\]]* peripheries=1 shape=invhouse\]/) {
		%objets=AddNoeudLabel($1,$2,%objets);
	}
	if (/(\w+) \[label=("[^"]*"|\w+)[^\]]* shape=box\]/) {
		%places=AddNoeudLabel($1,$2,%places);
	}
	if (/(\w+) \[label=("[^"]*"|\w+)[^\]]* peripheries=1 shape=octagon\]/) {
		%events=AddNoeudLabel($1,$2,%events);
	}
	if (/(\w+) \[label=("[^"]*"|\w+)[^\]]* peripheries=1 shape=pentagon\]/) {
		%assets=AddNoeudLabel($1,$2,%assets);
	}
	if (/(\w+) \[label=("[^"]*"|\w+)[^\]]* peripheries=2 shape=ellipse\]/) {
		%groups=AddNoeudLabel($1,$2,%groups);
	}
}
@trameslist = keys(%trames);
@trameslist = sort @trameslist;
@pnjslist = keys(%pnjs);
@pnjslist = sort @pnjslist;
@placeslist = keys(%places);
@placeslist = sort @placeslist;
@eventslist = keys(%events);
@eventslist = sort @eventslist;
@groupslist = keys(%groups);
@groupslist = sort @groupslist;
@objetslist = keys(%objets);
@objetslist = sort @objetslist;
@assetslist = keys(%assets);
@assetslist = sort @assetslist;

sub PrintSelectBox {
   my ($name,@list,%hashList) = @_;
    print "<form action=\"image.pl\" method=\"GET\" target=img>";
	print "<label for=\"im\">$name </label>";
	print "<select name=\"im\">";
	print "<option value=\"\">All</option>\n";
	foreach (@list) {
		print "<option value=\"$hashList{$_}\">$_</option>\n";
	}
	print "</select>";
	print "<input type=\"submit\" value=\"Show !\">";
	print "</form>";
}

print '<div class=leftside>';
print "<form action=\"image.pl\" method=\"GET\" target=img>";
print "<label for=\"im\">Objets </label>";
print "<select name=\"im\">";
print "<option value=\"\">All</option>\n";
foreach (@objetslist) {
	print "<option value=\"$objets{$_}\">$_</option>\n";
}
print "</select>";
print "<input type=\"submit\" value=\"Show !\">";
print "</form>";

# PrintSelectBox('Events', @eventslist, %events);
print "<form action=\"image.pl\" method=\"GET\" target=img>";
print "<label for=\"im\">Events </label>";
print "<select name=\"im\">";
print "<option value=\"\">All</option>\n";
foreach (@eventslist) {
	print "<option value=\"$events{$_}\">$_</option>\n";
}
print "</select>";
print "<input type=\"submit\" value=\"Show !\">";
print "</form>";
print '</div>';


print '<div class=centerside>';
print "<form action=\"image.pl\" method=\"GET\" target=img>";
print "<label for=\"im\">PNJs </label>";
print "<select name=\"im\">";
print "<option value=\"\">All</option>\n";
foreach (@pnjslist) {
	print "<option value=\"$pnjs{$_}\">$_</option>\n";
}
print "</select>";
print "<input type=\"submit\" value=\"Show !\">";
print "</form>";

print "<form action=\"image.pl\" method=\"GET\" target=img>";
print "<label for=\"im\">Trames </label>";
print "<select name=\"im\">";
print "<option value=\"\">All</option>\n";
foreach (@trameslist) {
	print "<option value=\"$trames{$_}\">$_</option>\n";
}
print "</select>";
print "<input type=\"submit\" value=\"Show !\">";
print "</form>";

print "<form action=\"image.pl\" method=\"GET\" target=img>";
print "<label for=\"im\">Groupes </label>";
print "<select name=\"im\">";
print "<option value=\"\">All</option>\n";
foreach (@groupslist) {
	print "<option value=\"$groups{$_}\">$_</option>\n";
}
print "</select>";
print "<input type=\"submit\" value=\"Show !\">";
print "</form>";
print '</div>';


print '<div class=rightside>';
print "<form action=\"image.pl\" method=\"GET\" target=img>";
print "<label for=\"im\">Roles </label>";
print "<select name=\"im\">";
print "<option value=\"\">All</option>\n";
foreach (@assetslist) {
	print "<option value=\"$assets{$_}\">$_</option>\n";
}
print "</select>";
print "<input type=\"submit\" value=\"Show !\">";
print "</form>";

# PrintSelectBox('Lieux', @placeslist, %places);
print "<form action=\"image.pl\" method=\"GET\" target=img>";
print "<label for=\"im\">Lieux </label>";
print "<select name=\"im\">";
print "<option value=\"\">All</option>\n";
foreach (@placeslist) {
	print "<option value=\"$places{$_}\">$_</option>\n";
}
print "</select>";
print "<input type=\"submit\" value=\"Show !\">";
print "</form>";
print '</div>';
print '</body>';
print '</html>';
