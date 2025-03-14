#!/usr/bin/env perl
use warnings;
use strict;
use XML::LibXML;
use XML::LibXML::XPathContext;
use Getopt::Long;

our $in_place = 0;

Getopt::Long::Configure('gnu_getopt');
Getopt::Long::GetOptions('i|in-place' => \$in_place) or die(":-(");

local $/ = undef;
my $doc;
while (<>) {
    printf STDERR ("Read $ARGV\n");
    $doc = XML::LibXML->load_xml(
        string => $_,
        keep_blanks => 1,
    );
    my $xpc = XML::LibXML::XPathContext->new($doc);
    $xpc->registerNs('inkscape', 'http://www.inkscape.org/namespaces/inkscape');
    $xpc->registerNs('sodipodi', 'http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd');
    $xpc->registerNs('svg', 'http://www.w3.org/2000/svg" width="1008" height="1680');
    my $svg_elt = $doc->documentElement;
    my $height = $svg_elt->getAttribute('height');
    my $width = $svg_elt->getAttribute('width');
    my @view_box = split(' ', $svg_elt->getAttribute('viewBox') // '');
    my ($view_box_x1, $view_box_y1, $view_box_x2, $view_box_y2) = @view_box;

    my $move_guide = sub {
        my ($name, $y) = @_;
        my ($guide) = $xpc->findnodes("//sodipodi:guide[\@inkscape:label='$name']");
        if (!$guide) {
            return;
        }
        my $position = $guide->getAttribute('position');
        my ($pos_x, $pos_y) = split(/\s*,\s*/, $position);
        my $orientation = $guide->getAttribute('orientation');
        my ($orientn_x, $orientn_y) = split(/\s*,\s*/, $orientation);
        my $horizontal_guide = !$orientn_x && $orientn_y;
        my $vertical_guide = $orientn_x && !$orientn_y;
        if ($horizontal_guide) {
            print STDERR ("$pos_x,$pos_y");
            my $guideline_x = convert($pos_x, $view_box_x1, $view_box_x2, 0, $height);
            my $guideline_y = $y;
            $pos_y = convert($guideline_y, 0, $height, $view_box_y1, $view_box_y2);
            print STDERR (" => $pos_x,$pos_y\n");
            $guide->setAttribute('position', "${pos_x},${pos_y}");
        }
    };

    &$move_guide('accentcenter', 1536);
    &$move_guide('accentbelowcenter', 192);

} continue {
    if (eof && $in_place && $ARGV ne '-') {
        my $fh;
        my $ARGVTMP = $ARGV . ".tmp";
        open($fh, '>', $ARGVTMP) or die("$ARGVTMP: $!\n");
        print $fh $doc->toString(1) or die("$ARGVTMP: $!\n");
        close($fh) or die("$ARGVTMP: $!\n");
        rename($ARGVTMP, $ARGV) or die("$ARGV => $ARGVTMP: $!\n");
        print STDERR ("Wrote $ARGV\n");
    } else {
        print $doc->toString(1);
    }
}

sub move_guide {
}

sub convert {
    my ($coord, $from_1, $from_2, $to_1, $to_2) = @_;
    my $a = ($coord - $from_1) / ($from_2 - $from_1);
    my $b = $to_1 + $a * ($to_2 - $to_1);
    return $b;
}
