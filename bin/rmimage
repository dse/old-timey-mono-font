#!/usr/bin/env perl
use warnings;
use strict;
use XML::LibXML;
use Getopt::Long;
use Data::Dumper qw(Dumper);
use File::Basename qw(dirname basename);

our $in_place;
our $in_place_ext;

Getopt::Long::Configure(qw(gnu_getopt));
Getopt::Long::GetOptions(
    'i|in-place' => \$in_place,
    'I|in-place-backup=s' => \$in_place_ext,
) or exit(1);

$in_place ||= defined $in_place_ext; # -I implies -i

local $/ = undef;
my $new = 1;
while (<>) {
    if ($new) {
        if ($in_place) {
            if (defined $in_place_ext) {
                my $backup = $ARGV;
                if (index($in_place_ext, "*") < 0) {
                    $backup = $ARGV . $in_place_ext;
                } else {
                    my ($filename, $dirs, $suffix) = fileparse($ARGV);
                    $filename =~ s{\*}{$ARGV}g;
                    $backup = $dirs . $filename . $suffix;
                }
                rename($ARGV, $backup);
            }
            open(\*ARGVOUT, ">", $ARGV);
            select(\*ARGVOUT);
        }
    }
    my $doc = XML::LibXML->load_xml(string => $_, no_blanks => 0);
    my @image = $doc->findnodes("/descendant-or-self::svg:image");
    foreach my $image (@image) {
        $image->parentNode->removeChild($image);
    }
    print($doc->toString(2));
} continue {
    $new = 1 if eof;
}
select(\*STDOUT);
