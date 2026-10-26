#!/usr/bin/env perl
use warnings;
use strict;
use File::Find;
use Getopt::Long;
use Unicode::UCD qw(charinfo);

my $general_categories = Unicode::UCD::general_categories();

Getopt::Long::Configure(qw(gnu_getopt));

Getopt::Long::GetOptions(
    "C|chdir=s" => sub { chdir($_[1]); },
) or die(":-(\n");

File::Find::find(sub {
                     if (!scalar(stat($_))) {
                         return;
                     }
                     if (!-f _) {
                         return;
                     }
                     if (!/^(?<codepoint>[0-9A-Fa-f]+)(?:[-.]+(?<variant>.+))?\.svg$/) {
                         return;
                     }
                     my $codepoint = hex($+{codepoint});
                     my $variant = $+{variant};
                     my $charinfo = charinfo($codepoint);
                     my $gc = defined $charinfo ? $charinfo->{category} : undef;
                     my $charname = defined $charinfo ? $charinfo->{name} : undef;
                     my $type;
                     if (!defined $gc) {
                         $type = "none";
                     } elsif ($gc eq "Ll") {
                         $type = "lower";
                     } elsif ($gc eq "Lu") {
                         $type = "upper";
                     } elsif ($gc eq "Lt") {
                         $type = "upper";
                     } elsif ($gc eq "Nd") {
                         $type = "upper";
                     } elsif ($gc eq "Sm") {
                         $type = "lower";
                     } else {
                         $type = "upper?";
                     }
                     my $general_category = $general_categories->{$gc};
                     printf("%-8s  %-24s  %s -- U+%04X %s\n",
                            $type,
                            $general_category,
                            $File::Find::name,
                            $codepoint, $charinfo->{name} // "<none>");
                 }, "src/upright");
