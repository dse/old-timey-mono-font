#!/usr/bin/env perl
use warnings;
use strict;
use Unicode::UCD qw(charinfo);
use Getopt::Long;
use File::Basename qw(fileparse dirname basename);
use String::ShellQuote qw(shell_quote);
our $force;
our $git;
Getopt::Long::Configure(qw(gnu_getopt));
Getopt::Long::GetOptions(
    'f|force' => \$force,
    'g|git' => \$git,
);
foreach my $filename (@ARGV) {
    next unless $filename =~ m{\.svg$}i;
    my ($dirname, $basename) = (dirname($filename), basename($filename));
    local $_ = $basename;
    if (!s{^([0-9A-Fa-f]+)\b}{}) {
        warn("$filename: hex codepoint not found\n");
        next;
    }
    my $codepoint = hex($1);
    my $charname = eval { charinfo($codepoint)->{name} };
    if (!defined $charname) {
        warn("$filename: charname for U+%04X not defined\n", $codepoint);
        next;
    }
    $charname =~ s{^[^0-9A-Za-z]+}{};
    $charname =~ s{[^0-9A-Za-z]+$}{};
    $charname =~ s{[^0-9A-Za-z]+}{-}g;
    $charname = lc($charname);
    my $suffix = s{(?:--.*)*\.svg$}{} ? $& : undef;
    my $new_filename = sprintf("%s/%04x-%s%s", $dirname, $codepoint, $charname, $suffix);
    if ($filename eq $new_filename) {
        next;
    }
    my @cmd = ("git", "mv", $filename, $new_filename);
    if (!$git) {
        shift(@cmd);
    }
    system(@cmd);
    my $cmd = join(" ", map { shell_quote($_) } @cmd);
    if ($?) {
        warn("$cmd\n");
        die("    failed to execute: $!\n") if $? < 0;
        die(sprintf("    died with signal %d, %s coredump\n",
                    ($? & 127), ($? & 128) ? 'with' : 'without')) if $? & 127;
        die(sprintf("    exited with value %d\n", $? >> 8));
    }
}
