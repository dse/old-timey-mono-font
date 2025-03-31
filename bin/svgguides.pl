#!/usr/bin/env perl
use warnings;
use strict;
use XML::LibXML;
use XML::LibXML::XPathContext;
use Getopt::Long;
# use Carp::Always;

use constant COLOR_GREEN    => '#009900';
use constant COLOR_GREEN_20 => '#ff9900';
use constant COLOR_BLACK    => '#000000';
use constant COLOR_BLUE     => '#0000ff';
use constant COLOR_RED      => '#ff0000';

use constant COLOR_IS_BROWN => '#986a44';
use constant COLOR_IS_BLUE  => '#0099e5'; # 26, 4d
use constant COLOR_IS_RED   => '#ff0000'; # 7f

use constant COLOR_GRID_BLUE           => '#b3b3ff';
use constant COLOR_GRID_GREEN          => '#5aff5a';
use constant COLOR_GRID_RED            => '#ff9e9e';
use constant COLOR_GRID_GRAY           => '#bbbbbb';
use constant COLOR_GRID_ORANGE         => '#ffab57';
use constant COLOR_GRID_MAGENTA        => '#ff8cff';
use constant COLOR_GRID_CYAN           => '#1cffff';
use constant COLOR_GRID_YELLOW         => '#ffff00'; # higher luminance
use constant COLOR_GRID_BLACK          => '#000000';
use constant COLOR_GRID_WHITE          => '#ffffff';
use constant COLOR_GRID_NON_REPRO_BLUE => '#95c9d7';

use constant COLOR_OVERSHOOT_GREEN => '#8ff0a4';
use constant COLOR_EXCENTER_RED => '#bf4040';
use constant COLOR_CAPCENTER_BLACK => '#000000';

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
my $thingy;
while (<>) {
    printf STDERR ("Read $ARGV\n");
    $thingy = My::Thingy->new();
    $thingy->load_xml($_);
    $thingy->delete_guides();

    $thingy->create_guide(16, color => COLOR_OVERSHOOT_GREEN);
    $thingy->create_guide(64, color => COLOR_OVERSHOOT_GREEN);
    $thingy->create_guide(112, color => COLOR_OVERSHOOT_GREEN);
    $thingy->create_guide(36, name => 'descender');
    $thingy->create_guide(84);
    $thingy->create_guide(132);

    $thingy->create_guide(316, color => COLOR_OVERSHOOT_GREEN);
    $thingy->create_guide(364, color => COLOR_OVERSHOOT_GREEN);
    $thingy->create_guide(412, color => COLOR_OVERSHOOT_GREEN);
    $thingy->create_guide(336, name => 'baseline');
    $thingy->create_guide(384);
    $thingy->create_guide(432);

    $thingy->create_guide(864, color => COLOR_CAPCENTER_BLACK, name => 'cap-center');

    $thingy->create_guide(1092, name => 'ex-height');
    $thingy->create_guide(1044);
    $thingy->create_guide(996);
    $thingy->create_guide(1112, color => COLOR_OVERSHOOT_GREEN);
    $thingy->create_guide(1064, color => COLOR_OVERSHOOT_GREEN);
    $thingy->create_guide(1016, color => COLOR_OVERSHOOT_GREEN);

    $thingy->create_guide(1392, name => 'ascender');
    $thingy->create_guide(1344);
    $thingy->create_guide(1296);
    $thingy->create_guide(1412, color => COLOR_OVERSHOOT_GREEN);
    $thingy->create_guide(1364, color => COLOR_OVERSHOOT_GREEN);
    $thingy->create_guide(1316, color => COLOR_OVERSHOOT_GREEN);

    $thingy->create_guide(714, color => COLOR_EXCENTER_RED, name => 'ex-center/oper-center');

    $thingy->create_guide(504, orientation => 'vertical');

    $thingy->create_guide(1536, name => 'accent-center');
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
    sub list_guides {
        my ($self) = @_;
        foreach my $guide ($self->{xpc}->findnodes("//sodipodi:guide")) {
            my $pos = $guide->getAttribute("position");
            my ($pos_x, $pos_y) = split(/\s*,\s*/, $pos);
            my $pos_y_svg = $self->y_view_box_to_svg($pos_y);
            my $pos_x_svg = $self->x_view_box_to_svg($pos_x);
            print("$pos_x, $pos_y => $pos_x_svg, $pos_y_svg\n");
        }
    }
    sub delete_guides {
        my ($self) = @_;
        foreach my $guide ($self->{xpc}->findnodes("//sodipodi:guide")) {
            $guide->parentNode->removeChild($guide);
        }
    }
    sub create_guide {
        my ($self, $new_pos_svg, %args) = @_;
        my $color       = $args{color};
        my $guide_name  = $args{name};
        my $orientation = $args{orientation} // "horizontal";
        $orientation = "horizontal" if lc(substr($orientation, 0, 1)) eq 'h';
        $orientation = "vertical" if lc(substr($orientation, 0, 1)) eq 'v';
        my $is_horizontal = $orientation eq 'horizontal';
        my $guide = $self->{doc}->createElement("sodipodi:guide");
        if ($is_horizontal) {
            my $new_pos_vbox = $self->y_svg_to_view_box($new_pos_svg);
            $guide->setAttribute('position', sprintf("%f,%f", 0, $new_pos_vbox));
        } else {
            my $new_pos_vbox = $self->x_svg_to_view_box($new_pos_svg);
            $guide->setAttribute('position', sprintf("%f,%f", $new_pos_vbox, 0));
        }
        if ($args{locked}) {
            $guide->setAttribute("inkscape:locked", "true");
        } else {
            $guide->setAttribute("inkscape:locked", "false");
        }
        if (defined $guide_name) {
            $guide->setAttribute("inkscape:label", $guide_name);
        }
        if (defined $color) {
            $guide->setAttribute("inkscape:color", $color);
        }
        if ($is_horizontal) {
            $guide->setAttribute("orientation", "0,1");
        } else {
            $guide->setAttribute("orientation", "1,0");
        }
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
