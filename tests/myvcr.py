import vcr

my_vcr = vcr.VCR(
        serializer='json',
        cassette_library_dir='tests/fixtures/cassettes',
        record_mode='once',
        match_on=['host', 'method', 'port', 'path'],
    )
