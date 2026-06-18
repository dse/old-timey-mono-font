#!/usr/bin/env perl
use warnings;
use strict;
use XML::LibXML;
use XML::LibXML::XPathContext;
use Getopt::Long;
use List::Util qw(max);
use Math::Trig qw(pi);

our $NEW_SVG;

use constant COLOR_GREEN    => "#009900";
use constant COLOR_GREEN_20 => "#ff9900";
use constant COLOR_BLACK    => "#000000";
use constant COLOR_BLUE     => "#0000ff";
use constant COLOR_RED      => "#ff0000";
use constant COLOR_ORANGE   => "#ff9900";
use constant COLOR_ORANGE__FEINT => "#ffcc80";

use constant COLOR_IS_BROWN => "#986a44";
use constant COLOR_IS_BLUE  => "#0099e5"; # 26, 4d
use constant COLOR_IS_RED   => "#ff0000"; # 7f

use constant COLOR_GRID_BLUE           => "#b3b3ff";
use constant COLOR_GRID_GREEN          => "#5aff5a";
use constant COLOR_GRID_RED            => "#ff9e9e";
use constant COLOR_GRID_GRAY           => "#bbbbbb";
use constant COLOR_GRID_ORANGE         => "#ffab57";
use constant COLOR_GRID_MAGENTA        => "#ff8cff";
use constant COLOR_GRID_CYAN           => "#1cffff";
use constant COLOR_GRID_YELLOW         => "#ffff00"; # higher luminance
use constant COLOR_GRID_BLACK          => "#000000";
use constant COLOR_GRID_WHITE          => "#ffffff";
use constant COLOR_GRID_NON_REPRO_BLUE => "#95c9d7";

use constant COLOR_OVERSHOOT  => COLOR_GRID_GREEN;
use constant COLOR_EX_CENTER  => COLOR_GRID_RED;
use constant COLOR_CAP_CENTER => COLOR_GRID_BLACK;
use constant COLOR_ACCENT     => COLOR_ORANGE;
use constant COLOR_ACCENT__FEINT => COLOR_ORANGE__FEINT;

our $DESCENDER_C2C    = 300; # amount below baseline, CENTER-TO-CENTER
our $ASCENDER_C2C     = 960; # amount above baseline, CENTER-TO-CENTER
our $OVERSHOOT        = 20;
our $EX_HEIGHT_C2C    = 660; # amount above baseline, CENTER-TO-CENTER
our $CAP_HEIGHT_C2C   = 960; # amount above baseline, CENTER-TO-CENTER
our $STROKE_WIDTH     = 96;

our $WIDTH            = 1008;
our $HEIGHT           = 1680;

our $ASCENT           = 1344;
our $DESCENT          = $HEIGHT - $ASCENT;
our $ACCENT_SEPARATOR = $STROKE_WIDTH;
our $BASELINE_CENTER  = $DESCENT + $STROKE_WIDTH / 2;
our $ITALIC_ANGLE     = -12;

our %NS;
BEGIN {
    %NS = (
        inkscape => "http://www.inkscape.org/namespaces/inkscape",
        sodipodi => "http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd",
        svg      => "http://www.w3.org/2000/svg",
    );
}

our $in_place = 0;
our $delete_guides = 0;
our $small_caps = 0;
our $accents = 0;
our $tall = 0;

Getopt::Long::Configure("gnu_getopt");
Getopt::Long::GetOptions(
    "i|in-place" => \$in_place,
    "d|delete-guides" => \$delete_guides,
    "s|small-caps" => \$small_caps,
    "a|accents" => \$accents,
    "t|tall" => \$tall,
) or die(":-(");

if ($tall) {
    $HEIGHT = 2016;
    $ASCENT = $HEIGHT - ($HEIGHT - $CAP_HEIGHT_C2C - $STROKE_WIDTH) / 2;
    $DESCENT = $HEIGHT - $ASCENT;
    $BASELINE_CENTER = $DESCENT + $STROKE_WIDTH / 2;
}

if ($small_caps) {
    my $dh = ($ASCENDER_C2C - $EX_HEIGHT_C2C) / 2;
    $ASCENDER_C2C -= $dh;
    $CAP_HEIGHT_C2C -= $dh;
}

local $/ = undef;
my $thingy;
while (<>) {
    printf STDERR ("Read $ARGV\n");
    $thingy = My::Thingy->new();
    $thingy->load_xml($_);
    $thingy->delete_guides();
    if (!$delete_guides) {

        $thingy->create_guide($BASELINE_CENTER - $DESCENDER_C2C - $STROKE_WIDTH/2, name => "descender");
        $thingy->create_guide($BASELINE_CENTER - $DESCENDER_C2C,                   name => "descender-B");
        $thingy->create_guide($BASELINE_CENTER - $DESCENDER_C2C + $STROKE_WIDTH/2, name => "descender-C");
        $thingy->create_guide($BASELINE_CENTER - $DESCENDER_C2C - $STROKE_WIDTH/2 - $OVERSHOOT, color => COLOR_OVERSHOOT, name => "descender");
        $thingy->create_guide($BASELINE_CENTER - $DESCENDER_C2C                   - $OVERSHOOT, color => COLOR_OVERSHOOT, name => "descender-B");
        $thingy->create_guide($BASELINE_CENTER - $DESCENDER_C2C + $STROKE_WIDTH/2 - $OVERSHOOT, color => COLOR_OVERSHOOT, name => "descender-C");

        $thingy->create_guide($BASELINE_CENTER - $STROKE_WIDTH/2, name => "baseline");
        $thingy->create_guide($BASELINE_CENTER,                   name => "baseline-B");
        $thingy->create_guide($BASELINE_CENTER + $STROKE_WIDTH/2, name => "baseline-C");
        $thingy->create_guide($BASELINE_CENTER - $STROKE_WIDTH/2 - $OVERSHOOT, color => COLOR_OVERSHOOT, name => "baseline");
        $thingy->create_guide($BASELINE_CENTER                   - $OVERSHOOT, color => COLOR_OVERSHOOT, name => "baseline-B");
        $thingy->create_guide($BASELINE_CENTER + $STROKE_WIDTH/2 - $OVERSHOOT, color => COLOR_OVERSHOOT, name => "baseline-C");

        $thingy->create_guide($BASELINE_CENTER + $CAP_HEIGHT_C2C/2, color => COLOR_CAP_CENTER, name => "cap-center");

        if (!$small_caps) {
            $thingy->create_guide($BASELINE_CENTER + $EX_HEIGHT_C2C + $STROKE_WIDTH/2, name => "ex-height");
            $thingy->create_guide($BASELINE_CENTER + $EX_HEIGHT_C2C, name => "ex-height-B");
            $thingy->create_guide($BASELINE_CENTER + $EX_HEIGHT_C2C - $STROKE_WIDTH/2, name => "ex-height-C");
            $thingy->create_guide($BASELINE_CENTER + $EX_HEIGHT_C2C + $STROKE_WIDTH/2 + $OVERSHOOT, color => COLOR_OVERSHOOT, name => "ex-height");
            $thingy->create_guide($BASELINE_CENTER + $EX_HEIGHT_C2C                   + $OVERSHOOT, color => COLOR_OVERSHOOT, name => "ex-height-B");
            $thingy->create_guide($BASELINE_CENTER + $EX_HEIGHT_C2C - $STROKE_WIDTH/2 + $OVERSHOOT, color => COLOR_OVERSHOOT, name => "ex-height-C");
        }

        $thingy->create_guide($BASELINE_CENTER + $CAP_HEIGHT_C2C + $STROKE_WIDTH/2, name => "ascender");
        $thingy->create_guide($BASELINE_CENTER + $CAP_HEIGHT_C2C, name => "ascender-B");
        $thingy->create_guide($BASELINE_CENTER + $CAP_HEIGHT_C2C - $STROKE_WIDTH/2, name => "ascender-C");
        $thingy->create_guide($BASELINE_CENTER + $CAP_HEIGHT_C2C + $STROKE_WIDTH/2 + $OVERSHOOT, color => COLOR_OVERSHOOT, name => "ascender");
        $thingy->create_guide($BASELINE_CENTER + $CAP_HEIGHT_C2C                   + $OVERSHOOT, color => COLOR_OVERSHOOT, name => "ascender-B");
        $thingy->create_guide($BASELINE_CENTER + $CAP_HEIGHT_C2C - $STROKE_WIDTH/2 + $OVERSHOOT, color => COLOR_OVERSHOOT, name => "ascender-C");

        if (!$small_caps) {
            $thingy->create_guide($BASELINE_CENTER + $EX_HEIGHT_C2C/2, color => COLOR_EX_CENTER, name => "ex-center/oper-center");
        }

        $thingy->create_guide($WIDTH/2, orientation => "vertical");
        $thingy->create_guide($STROKE_WIDTH/2,  orientation => "vertical");
        $thingy->create_guide($WIDTH - $STROKE_WIDTH/2, orientation => "vertical");

        if ($accents) {
            my $accent_above__bottom = $BASELINE_CENTER + max($ASCENDER_C2C, $CAP_HEIGHT_C2C) + $STROKE_WIDTH / 2 + $ACCENT_SEPARATOR;
            my $accent_above__top    = $HEIGHT;
            my $accent_above__center = ($accent_above__bottom + $accent_above__top) / 2;
            $thingy->create_guide($accent_above__center, name => "accent-above--center", color => COLOR_ACCENT);
            $thingy->create_guide($accent_above__top,    name => "accent-above--top",    color => COLOR_ACCENT);
            $thingy->create_guide($accent_above__bottom, name => "accent-above--bottom", color => COLOR_ACCENT);
            my $accent_below__top    = $BASELINE_CENTER - $STROKE_WIDTH/2 - $ACCENT_SEPARATOR;
            my $accent_below__bottom = 0;
            my $accent_below__center = ($accent_below__top + $accent_below__bottom) / 2;
            $thingy->create_guide($accent_below__center, name => "accent-below--center", color => COLOR_ACCENT);
            $thingy->create_guide($accent_below__top,    name => "accent-below--top",    color => COLOR_ACCENT);
            $thingy->create_guide($accent_below__bottom, name => "accent-below--bottom", color => COLOR_ACCENT);
        }

        my $cap_center = $BASELINE_CENTER + $CAP_HEIGHT_C2C / 2;
        my $ex_center  = $BASELINE_CENTER + $EX_HEIGHT_C2C / 2;
        my $mid_center = ($cap_center + $ex_center) / 2;

        $thingy->create_guide_2(
            x => $WIDTH / 2,
            y => $cap_center,
            angle => $ITALIC_ANGLE,
            name => "ital center cap",
        );
        $thingy->create_guide_2(
            x => $WIDTH / 2,
            y => $mid_center,
            angle => $ITALIC_ANGLE,
            name => "ital center mid",
        );
        $thingy->create_guide_2(
            x => $WIDTH / 2,
            y => $ex_center,
            angle => $ITALIC_ANGLE,
            name => "ital center ex",
        );
    }
} continue {
    if (eof && $in_place && $ARGV ne "-") {
        my $fh;
        my $ARGVTMP = $ARGV . ".tmp";
        open($fh, ">", $ARGVTMP) or die("$ARGVTMP: $!\n");
        print $fh $thingy->to_string() or die("$ARGVTMP: $!\n");
        close($fh) or die("$ARGVTMP: $!\n");
        rename($ARGVTMP, $ARGV) or die("$ARGV => $ARGVTMP: $!\n");
        print STDERR ("Wrote $ARGV\n");
    } else {
        print $thingy->to_string();
    }
}

package My::Thingy {
    use Math::Trig qw(pi);
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

        my $width  = $svg->getAttribute("width");
        my $height = $svg->getAttribute("height");

        my @view_box = split(" ", $svg->getAttribute("viewBox") // "");
        my ($view_box_xmin, $view_box_ymin, $view_box_width, $view_box_height) = @view_box;

        $view_box_xmin //= 0;
        $view_box_ymin //= 0;
        $width  //= $view_box_width  //= $width;
        $height //= $view_box_height //= $height;

        my $view_box_xmax = $view_box_xmin + $view_box_width;
        my $view_box_ymax = $view_box_ymin + $view_box_height;

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
            # print("$pos_x, $pos_y => $pos_x_svg, $pos_y_svg\n");
        }
    }
    sub delete_guides {
        my ($self) = @_;
        foreach my $guide ($self->{xpc}->findnodes("//sodipodi:guide")) {
            $guide->parentNode->removeChild($guide);
        }
    }
    sub create_guide_2 {
        my ($self, %args) = @_;
        my $x          = $args{x} // ($WIDTH / 2);
        my $y          = $args{y} // 0;
        my $angle      = $args{angle} // 0;
        my $name       = $args{name};
        my $color      = $args{color};
        my $horizontal = $args{horizontal};
        my $vertical   = $args{vertical};
        my $locked     = $args{locked};
        if (defined $angle && defined $horizontal && defined $vertical) {
            die("create_guide_2: supplying angle, horizontal, and vertical makes no sense");
        } elsif (defined $angle && defined $horizontal) {
            die("create_guide_2: supplying angle and horizontal makes no sense");
        } elsif (defined $angle && defined $vertical) {
            die("create_guide_2: supplying angle and vertical makes no sense");
        } elsif (defined $horizontal && defined $vertical) {
            die("create_guide_2: supplying horizontal and vertical makes no sense");
        }
        if ($vertical) {
            $angle = 0;
            undef $vertical;
        } elsif ($horizontal) {
            $angle = 90;
            undef $vertical;
        }
        $angle *= pi / 180 if defined $angle;
        my $guide = $self->{doc}->createElement("sodipodi:guide");
        my $xx = $self->x_svg_to_view_box($x);
        my $yy = $self->y_svg_to_view_box($y);
        $guide->setAttribute("position", sprintf("%f,%f", $xx, $yy));
        $guide->setAttribute("inkscape:locked", $args{locked} ? "true" : "false");
        $guide->setAttribute("inkscape:label", $name) if defined $name;
        $guide->setAttribute("inkscape:color", $color) if defined $color;
        $guide->setAttribute("orientation", sprintf("%f,%f", -cos($angle), -sin($angle)));
        my ($namedview) = $self->{xpc}->findnodes("//sodipodi:namedview");
        if (!$namedview) {
            die("no namedview element\n");
        }
        $namedview->appendChild($guide);
    }
    sub create_guide {
        my ($self, $new_pos_svg, %args) = @_;

        my $orientation = (delete $args{orientation}) // "horizontal";
        if ($orientation eq "horizontal") {
            $args{angle} = 270;
            $args{x} = 0;
            $args{y} = $new_pos_svg;
        } else {
            $args{angle} = 0;
            $args{x} = $new_pos_svg;
            $args{y} = 0;
        }
        $self->create_guide_2(%args);

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
        # printf STDERR ("%f | %f %f | %f %f\n", $coord, $from_1, $from_2, $to_1, $to_2);
        my $a = ($coord - $from_1) / ($from_2 - $from_1);
        my $b = $to_1 + $a * ($to_2 - $to_1);
        return $b;
    }
}

BEGIN { $NEW_SVG = <<"EOF"; }
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!-- Created with Inkscape (http://www.inkscape.org/) -->
<svg xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
     xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
     xmlns="http://www.w3.org/2000/svg"
     xmlns:svg="http://www.w3.org/2000/svg"
     width="1008"
     height="1680"
     viewBox="0 0 63 105"
     version="1.1"
     id="svg5"
     xml:space="preserve"
     inkscape:version="1.2.2 (b0a8486541, 2022-12-01)"
     sodipodi:docname="blank-char.svg">
    <sodipodi:namedview id="namedview7"
                        pagecolor="#ffffff"
                        bordercolor="#666666"
                        borderopacity="1.0"
                        inkscape:showpageshadow="2"
                        inkscape:pageopacity="0.0"
                        inkscape:pagecheckerboard="0"
                        inkscape:deskcolor="#d1d1d1"
                        inkscape:document-units="px"
                        showgrid="true"
                        inkscape:current-layer="layer1"
                        showguides="true"
                        inkscape:lockguides="false">
        <inkscape:grid type="xygrid"
                       id="grid1382"
                       spacingx="0.125"
                       spacingy="0.125"
                       empspacing="12"
                       originx="0"
                       originy="0"
                       units="px"
                       visible="true"/>
    </sodipodi:namedview>
    <defs id="defs2"/>
    <g inkscape:groupmode="layer"
       id="layer3"
       inkscape:label="Layer 3"
       style="display:inline;opacity:0.5;stroke-width:3.60000001;stroke-dasharray:none"
       transform="matrix(0.83333333,0,0,0.83333333,-157.97619,-173.09626)"/>
    <g inkscape:groupmode="layer"
       id="layer2"
       inkscape:label="Layer 2"
       style="display:inline"/>
    <g inkscape:label="Layer 1"
       inkscape:groupmode="layer"
       id="layer1"
       style="display:inline"/>
</svg>
EOF
