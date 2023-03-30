use LWP::UserAgent;
use HTTP::Request::Common;

# Endpoint URLs
my $predict_text_url = 'http://localhost:5000/predict_text';
my $predict_file_url = 'http://localhost:5000/predict_file';

# Test GET request
my $ua = LWP::UserAgent->new();
my $text = 'I am feeling stressed';
my $url = "$predict_text_url?text=$text";
my $response = $ua->get($url);

if ($response->is_success()) {
    my $content = $response->decoded_content();
    print "GET request test passed: $content\n";
} else {
    print "GET request test failed: " . $response->status_line() . "\n";
}

# Test POST request
my $file_path = 'test_file.csv';
my $csv_content = "text\nI am feeling stressed\nI am not feeling stressed\n";
open(my $fh, '>', $file_path) or die "Could not open file '$file_path': $!";
print $fh $csv_content;
close($fh);

my $file = [ $file_path ];
my $response = $ua->request(POST $predict_file_url, Content_Type => 'form-data', Content => [ file => $file ]);

if ($response->is_success()) {
    my $content = $response->decoded_content();
    print "POST request test passed: $content\n";
} else {
    print "POST request test failed: " . $response->status_line() . "\n";
}

# Clean up test file
unlink $file_path or warn "Could not unlink $file_path: $!";
