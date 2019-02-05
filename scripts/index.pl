#!/usr/bin/perl

print "Content-type: text/html\r\n\r\n";

print '<HTML>
  <HEAD>
    <TITLE>Derniers Dragons</TITLE>
  </HEAD>
  <FRAMESET rows="120,*">
    <FRAME src=menu.pl name=menu>
    <FRAME name=img>
  </FRAMESET>
</HTML>';
