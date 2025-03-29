#!/usr/bin/env perl
use warnings;
use strict;
use XML::LibXML;
use XML::LibXML::XPathContext;
use Getopt::Long;

our %NS;
BEGIN {
    %NS = (
        inkscape => 'http://www.inkscape.org/namespaces/inkscape',
        sodipodi => 'http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd',
        svg      => 'http://www.w3.org/2000/svg',
    );
}

our $in_place = 0;

Getopt::Long::Configure('gnu_getopt');
Getopt::Long::GetOptions('i|in-place' => \$in_place) or die(":-(");

local $/ = undef;
my $doc;
my $dirty;
while (<>) {
    $dirty = 0;
    $doc = XML::LibXML->load_xml(
        string => $_,
        keep_blanks => 1,
    );
    my $xpc = XML::LibXML::XPathContext->new($doc);
    $xpc->registerNs(inkscape => $NS{inkscape});
    $xpc->registerNs(sodipodi => $NS{sodipodi});
    $xpc->registerNs(svg      => $NS{svg});
    my $svg = $doc->documentElement;
    foreach my $grid ($xpc->findnodes("//inkscape:grid")) {
        my $attr = $grid->getAttribute("visible");
        if (!defined $attr || $attr ne "true") {
            $dirty = 1;
            $grid->setAttribute("visible", "true");
        }
    }
} continue {
    if (eof && $in_place && $ARGV ne '-') {
        if ($dirty) {
            my $fh;
            my $ARGVTMP = $ARGV . ".tmp";
            open($fh, '>', $ARGVTMP) or die("$ARGVTMP: $!\n");
            print $fh $doc->toString(1) or die("$ARGVTMP: $!\n");
            close($fh) or die("$ARGVTMP: $!\n");
            rename($ARGVTMP, $ARGV) or die("$ARGV => $ARGVTMP: $!\n");
            print STDERR ("Wrote $ARGV\n");
        } else {
            print STDERR ("No change to $ARGV\n");
        }
    } else {
        print $doc->toString(1);
    }
}
