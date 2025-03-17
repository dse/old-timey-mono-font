#!/usr/bin/env perl
use warnings;
use strict;
use XML::LibXML;
use XML::LibXML::XPathContext;
use Getopt::Long;
use Carp::Always;

our %NS;
our $GREEN;
our $BLUE;
our $BLACK;
our $BROWN;
BEGIN {
    %NS = (
        inkscape => 'http://www.inkscape.org/namespaces/inkscape',
        sodipodi => 'http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd',
        svg      => 'http://www.w3.org/2000/svg',
    );
    $GREEN = "rgb(143,240,164)";
    $BLUE = "rgb(0,134,229)";
    $BLACK = "rgb(0,0,0)";
    $BROWN = "rgb(152,106,68)";
}

our $in_place = 0;

Getopt::Long::Configure('gnu_getopt');
Getopt::Long::GetOptions('i|in-place' => \$in_place) or die(":-(");

local $/ = undef;
my $thingy;
while (<>) {
    printf STDERR ("Read $ARGV\n");
    $thingy = My::Thingy->new();
    $thingy->load_xml($_);
    $thingy->move_or_create_horizontal_guide('accentcenter', 1536);
    $thingy->move_or_create_horizontal_guide('accentbelowcenter', 192);

    $thingy->move_or_create_horizontal_guide('descender', 36);
    $thingy->move_or_create_horizontal_guide(undef, 84);
    $thingy->move_or_create_horizontal_guide(undef, 64, $GREEN);
    $thingy->move_or_create_horizontal_guide(undef, 132);
} continue {
    if (eof && $in_place && $ARGV ne '-') {
        my $fh;
        my $ARGVTMP = $ARGV . ".tmp";
        open($fh, '>', $ARGVTMP) or die("$ARGVTMP: $!\n");
        print $fh $thingy->to_string() or die("$ARGVTMP: $!\n");
        close($fh) or die("$ARGVTMP: $!\n");
        rename($ARGVTMP, $ARGV) or die("$ARGV => $ARGVTMP: $!\n");
        print STDERR ("Wrote $ARGV\n");
    } else {
        print $thingy->to_string();
    }
}

package My::Thingy {
    sub new {
        my ($class) = @_;
        my $self = bless({}, $class);
        return $self;
    }
    sub load_xml {
        my ($self, $str) = @_;
        my $doc = XML::LibXML->load_xml(
            string => $str,
            keep_blanks => 1,
        );
        my $xpc = XML::LibXML::XPathContext->new($doc);
        $xpc->registerNs(inkscape => $NS{inkscape});
        $xpc->registerNs(sodipodi => $NS{sodipodi});
        $xpc->registerNs(svg      => $NS{svg});
        my $svg = $doc->documentElement;
        my $height = $svg->getAttribute('height');
        my $width = $svg->getAttribute('width');
        my @view_box = split(' ', $svg->getAttribute('viewBox') // '');
        my ($view_box_xmin, $view_box_ymin, $view_box_xmax, $view_box_ymax) = @view_box;
        $self->{doc} = $doc;
        $self->{xpc} = $xpc;
        $self->{svg} = $svg;
        $self->{height} = $height;
        $self->{width} = $width;
        $self->{view_box_xmin} = $view_box_xmin;
        $self->{view_box_xmax} = $view_box_xmax;
        $self->{view_box_ymin} = $view_box_ymin;
        $self->{view_box_ymax} = $view_box_ymax;
    }
    sub move_or_create_horizontal_guide {
        my ($self, $guide_name, $new_pos_y, $color) = @_;
        $self->move_horizontal_guide($guide_name, $new_pos_y, $color) or
          $self->create_horizontal_guide($guide_name, $new_pos_y, $color);
    }
    sub list_horizontal_guides {
        my ($self) = @_;
        foreach my $guide ($self->{xpc}->findnodes("//sodipodi:guide")) {
            my $pos = $guide->getAttribute("position");
            my ($pos_x, $pos_y) = split(/\s*,\s*/, $pos);
            my $pos_y_svg = $self->y_view_box_to_svg($pos_y);
            my $pos_x_svg = $self->x_view_box_to_svg($pos_x);
            print("$pos_x, $pos_y => $pos_x_svg, $pos_y_svg\n");
        }
    }
    sub move_horizontal_guide {
        my ($self, $guide_name, $new_pos_y_svg, $color) = @_;
        my $new_pos_y_vbox = $self->y_svg_to_view_box($new_pos_y_svg);
        my $guide;
        if (defined $guide_name) {
            ($guide) = $self->{xpc}->findnodes("//sodipodi:guide[\@inkscape:label='$guide_name']");
        } else {
            my @guides = $self->{xpc}->findnodes("//sodipodi:guide");
            foreach my $g (@guides) {
                my $pos = $g->getAttribute("position");
                my ($pos_x_vbox, $pos_y_vbox) = split(/\s*,\s*/, $pos);
                if (abs($pos_x_vbox - 0) < 0.001 && abs($pos_y_vbox - $new_pos_y_vbox) < 0.001) {
                    $guide = $g;
                    last;
                }
            }
        }
        if (!$guide) {
            return;
        }
        my $position = $guide->getAttribute('position');
        my ($pos_x_vbox, $pos_y_vbox) = split(/\s*,\s*/, $position);
        my $orientation = $guide->getAttribute('orientation');
        my ($orientn_x, $orientn_y) = split(/\s*,\s*/, $orientation);
        my $is_horizontal_guide = !$orientn_x && $orientn_y; # 0,1
        my $is_vertical_guide = $orientn_x && !$orientn_y;   # 1,0
        my $height = $self->{height};
        my $width = $self->{width};
        if ($is_horizontal_guide) {
            $guide->setAttribute('position', "${pos_x_vbox},${new_pos_y_vbox}");
            if (defined $color) {
                $guide->setAttribute("inkscape:color", $color);
            }
        }
        return 1;
    }
    sub create_horizontal_guide {
        my ($self, $guide_name, $new_pos_y_svg, $color) = @_;
        $color //= $BLUE;
        my $new_pos_y_vbox = $self->y_svg_to_view_box($new_pos_y_svg);
        my $guide = $self->{doc}->createElement("sodipodi:guide");
        $guide->setAttribute('position', sprintf("%f,%f", 0, $new_pos_y_vbox));
        $guide->setAttribute("inkscape:locked", "false");
        if (defined $guide_name) {
            $guide->setAttribute("inkscape:label", $guide_name);
        }
        $guide->setAttribute("inkscape:color", $color);
        $guide->setAttribute("orientation", "0,1");
        my ($namedview) = $self->{xpc}->findnodes("//sodipodi:namedview");
        if (!$namedview) {
            die("no namedview element\n");
        }
        $namedview->appendChild($guide);
    }
    sub to_string {
        my ($self) = @_;
        return $self->{doc}->toString(1);
    }
    sub y_svg_to_view_box {
        my ($self, $coord) = @_;
        return $self->convert($coord, 0, $self->{height}, $self->{view_box_ymin}, $self->{view_box_ymax});
    }
    sub y_view_box_to_svg {
        my ($self, $coord) = @_;
        return $self->convert($coord, $self->{view_box_ymin}, $self->{view_box_ymax}, 0, $self->{height});
    }
    sub x_svg_to_view_box {
        my ($self, $coord) = @_;
        return $self->convert($coord, 0, $self->{width}, $self->{view_box_xmin}, $self->{view_box_xmax});
    }
    sub x_view_box_to_svg {
        my ($self, $coord) = @_;
        return $self->convert($coord, $self->{view_box_xmin}, $self->{view_box_xmax}, 0, $self->{width});
    }
    sub convert {
        my ($self, $coord, $from_1, $from_2, $to_1, $to_2) = @_;
        my $a = ($coord - $from_1) / ($from_2 - $from_1);
        my $b = $to_1 + $a * ($to_2 - $to_1);
        return $b;
    }
}
