#!/usr/bin/env perl
#
# stroke96.pl - make all stroke widths 96px in an SVG drawing.
#
use warnings;
use strict;
use Getopt::Long;
use XML::LibXML;
use XML::LibXML::XPathContext;
use Math::Trig qw(pi);
use File::Inplace;

our $STROKE_WIDTH = 96;

our $extension;

# Getopt::Long::Configure("gnu_getopt");
# Getopt::Long::GetOptions() or die(":-(");

local $/ = undef;
my $dom;

while (<>) {
    my $dom = XML::LibXML->load_xml(no_blanks => 1, string => $_);
    my $xpc = XML::LibXML::XPathContext->new($dom);

    my @all_nodes = $xpc->findnodes("//*");
    my @nodes;

    @nodes = grep { has_stroke_width($_) } @all_nodes;
    foreach my $node (@nodes) {
        fix_stroke_width($node);
    }
} continue {
    print($dom->toString(0));
}

sub has_stroke_width {
    my ($node) = @_;
    my $style = $node->getAttribute("style");
    return if !defined $style;
    return $style =~ m{([";])stroke-width:(-?\d+(?:\.\d*)?|\.\d+)([";])};
}

sub fix_stroke_width {
    my ($node) = @_;
    my $style = $node->getAttribute("style");
    return if !defined $style;
    my @transform = get_inverse_transform($node);
    if ($style =~ s{([";])stroke-width:(-?\d+(?:\.\d*)?|\.\d+)([";])}{
        $1 . "stroke-width:" . ($STROKE_WIDTH * $transform[0]) . $3
    }ge) {
        $node->setAttribute("style", $style);
    }
}

sub get_inverse_transform_from_node {
    my ($node) = @_;
    my @transform = identity();
    for (; $node; $node = $node->parentNode) {
        next unless $node->isa("XML::LibXML::Element");
        next unless $node->can("hasAttribute");
        if ($node->hasAttribute("viewBox")) {
            my $view_box = $node->getAttribute("viewBox");
            my ($view_box_x, $view_box_y, $view_box_width, $view_box_height) = split(/\s+/, $view_box);
            if ($node->hasAttribute("width") && $node->hasAttribute("height")) {
                my $width = $node->getAttribute("width");
                my $height = $node->getAttribute("height");
                @transform = compose(@transform, scale($view_box_width / $width, $view_box_height / $height));
            }
        }
        if ($node->hasAttribute("transform")) {
            my $transform_2 = $node->getAttribute("transform");
            my @transform_2 = inverse(parse_transform_string($transform_2));
            @transform = compose(@transform, @transform_2);
        }
    }
}

sub parse_transform_string {
    my ($transform) = @_;
    if ($transform =~ m{^(matrix|scale|rotate|skew|translate)\((.*)\)$}) {
        my ($oper, $params) = $1;
        my @params = split(qr{\s+|\s*,\s*}, $params);
        if ($oper eq "matrix") {
            die("matrix: not enough parameters\n") if scalar @params < 6;
            die("matrix: too many parameters\n") if scalar @params > 6;
            return @params[0..5];
        }
        if ($oper eq "scale") {
            die("scale: not enough parameters\n") if scalar @params < 1;
            die("scale: too many parameters\n") if scalar @params > 2;
            return scale(@params[0..1]);
        }
        if ($oper eq "translate") {
            die("translate: not enough parameters\n") if scalar @params < 1;
            die("translate: too many parameters\n") if scalar @params > 2;
            return translate(@params[0..1]);
        }
        if ($oper eq "rotate") {
            die("rotate: not enough parameters\n") if scalar @params < 1;
            die("rotate: too many parameters\n") if scalar @params > 1;
            return rotate($params[0]);
        }
        if ($oper eq "skew") {
            die("skew: not enough parameters\n") if scalar @params < 1;
            die("skew: too many parameters\n") if scalar @params > 1;
           return skew($params[0]);
        }
        return @params;
    }
    die(sprintf("invalid argument for parse_transform_string\n"));
}

sub transform_point {
    my ($x, $y, @transform) = @_;
    ($x, $y) = ($transform[0] * $x + $transform[2] * $y + $transform[4],
                $transform[1] * $x + $transform[3] * $y + $transform[5]);
    return ($x, $y);
}

sub identity {
    return (1, 0, 0, 1, 0, 0);
}

sub translate {
    my ($x, $y) = @_;
    $x //= 0;
    $y //= 0;
    return (1, 0, 0, 1, $x, $y);
}

sub scale {
    my ($x, $y) = @_;
    $y //= $x;
    return ($x, 0, 0, $y, 0, 0);
}

sub rotate {
    my ($deg) = @_;
    my $rad = $deg * pi / 180;
    my ($c, $s) = (cos($rad), sin($rad));
    return ($c, $s, -$s, $c, 0, 0);
}

sub skew {
    my ($deg) = @_;
    my $rad = $deg * pi / 180;
    my $t = tan($rad);
    return (1, 0, $t, 1, 0, 0);
}

sub compose {
    my @a = @_[0..5];
    my @b = @_[6..11];
    my @c;
    $c[0] = $a[0] * $b[0] + $a[1] * $b[2];
    $c[1] = $a[0] * $b[1] + $a[1] * $b[3];
    $c[2] = $a[2] * $b[0] + $a[3] * $b[2];
    $c[3] = $a[2] * $b[1] + $a[3] * $b[3];
    $c[4] = $a[4] * $b[0] + $a[5] * $b[2] + $b[4];
    $c[5] = $a[4] * $b[1] + $a[5] * $b[3] + $b[5];
    return @c;
}

sub inverse {
    my @orig = @_[0..5];
    my $det = $orig[0] * $orig[3] - $orig[1] * $orig[2];
    if (!$det) {
        die("attempt to invert a singular matrix\n");
    }
    my @into;
    $into[0] =  $orig[3] / $det;
    $into[1] = -$orig[1] / $det;
    $into[2] = -$orig[2] / $det;
    $into[3] =  $orig[0] / $det;
    $into[4] = -$orig[4] * $into[0] - $orig[5] * $into[2];
    $into[5] = -$orig[4] * $into[1] - $orig[5] * $into[3];
    return @into;
}

1;
