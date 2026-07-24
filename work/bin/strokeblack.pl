#!/usr/bin/env perl
use warnings;
use strict;
use Getopt::Long;
use XML::LibXML;
use XML::LibXML::XPathContext;

our $extension;

# Getopt::Long::Configure("gnu_getopt");
# Getopt::Long::GetOptions(
# ) or die(":-(");

local $/ = undef;
my $dom;

while (<>) {
    $dom = XML::LibXML->load_xml(no_blanks => 1, string => $_);
    my $xpc = XML::LibXML::XPathContext->new($dom);

    my @all_nodes = $xpc->findnodes("//*");
    my @nodes;

    @nodes = grep { has_stroke_color($_) } @all_nodes;
    foreach my $node (@nodes) {
        fix_stroke_color($node);
    }
} continue {
    print($dom->toString(0));
}

sub has_stroke_color {
    my ($node) = @_;
    my $style = $node->getAttribute("style");
    return if !defined $style;
    return $style =~ m{([";])stroke:#[0-9A-Fa-f]{6}([";])};
}

sub fix_stroke_color {
    my ($node) = @_;
    my $style = $node->getAttribute("style");
    return if !defined $style;
    if ($style =~ s{([";])stroke:(#[0-9A-Fa-f]{6})([";])}{
        $1 . "stroke:#000000" . $3
    }ge) {
        $node->setAttribute("style", $style);
    }
}

1;
