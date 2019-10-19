# Anatomy of the pubmed abstract ETL

Filenames are stored in data_load table.

1. we extract the next packet to process from data_load were downloaded_ind
is the false dual. Done.

2. we download the gz-compressed archive file from the pubmed FTP site.

Downloading process is pubmed_gz_downloader which downloads file f from the
pubmed ftp site and decompresses it as an (XML) string.

The XML string is scanned by pubmed_xml_gz_scanner. We need to store each
abstract as raw XML into the abstract_stg table with the data_load packet id.

After we process a packet, set the processed_ind and downloaded_ind to the
true dual and set the downloaded_dttm to now in the data_load table at the
packet id.

Voilà

### ... and then

After we have one packet processed, add a notification loop to process the
next packet.
