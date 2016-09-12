#!/usr/bin/perl
use strict;
use warnings;
use Data::Dumper;

my @images = ();
while (my $line = <>) {
	$line =~ s/\s//gsm;
	my ($file, $score) = split /,/, $line;
	my ($name) = $file =~ /\/([^\/]+)_\d+\.jpg$/;
	my $tmp = "/tmp/${score}-$name";
	`cp $file $tmp`;
	`convert $tmp -resize !224x!224 $tmp.jpg`;
	push @images, $tmp . ".jpg";
	last if $#images == 19;
}
my $imagelist = join " ", @images;
my $rnd = rand();
`montage -label %f -size 896x1120 -tile 4x5 -coalesce -quality 100 -geometry 224x224+0+0 $imagelist /tmp/montage-$rnd.jpg`;
`aws s3 cp /tmp/montage-$rnd.jpg s3://pg-image-search/montages/ --grants read=uri=http://acs.amazonaws.com/groups/global/AllUsers`;

print "https://s3-us-west-2.amazonaws.com/pg-image-search/montages/montage-$rnd.jpg\n";
exit;
