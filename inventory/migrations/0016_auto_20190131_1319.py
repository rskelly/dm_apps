# Generated by Django 2.1.4 on 2019-01-31 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0015_section_region'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='distribution_format',
            field=models.CharField(blank=True, choices=[('AAC', 'AAC'), ('AI', 'AI'), ('AIFF', 'AIFF'), ('AMF', 'AMF'), ('ASCII Grid', 'ASCII Grid'), ('AVI', 'AVI'), ('Android', 'Android'), ('BMP', 'BMP'), ('BWF', 'BWF'), ('Blackberry', 'Blackberry'), ('CCT', 'CCT'), ('CDED ASCII', 'CDED ASCII'), ('CDF', 'CDF'), ('CDR', 'CDR'), ('CSV', 'CSV'), ('DBD', 'DBD'), ('DBF', 'DBF'), ('DICOM', 'DICOM'), ('DNG', 'DNG'), ('DOC', 'DOC'), ('DOCX', 'DOCX'), ('DXF', 'DXF'), ('E00', 'E00'), ('ECW', 'ECW'), ('EDI', 'EDI'), ('EMF', 'EMF'), ('EPS', 'EPS'), ('EPUB2', 'EPUB2'), ('EPUB3', 'EPUB3'), ('ESRI REST', 'ESRI REST'), ('EXE', 'EXE'), ('FGDB/GDB', 'FGDB/GDB'), ('Flat raster binary', 'Flat raster binary'), ('GIF', 'GIF'), ('GML', 'GML'), ('GRIB1', 'GRIB1'), ('GRIB2', 'GRIB2'), ('GeoJSON', 'GeoJSON'), ('GeoPDF', 'GeoPDF'), ('GeoPackage', 'GeoPackage'), ('GeoRSS', 'GeoRSS'), ('GeoTIF', 'GeoTIF'), ('HDF', 'HDF'), ('HTML', 'HTML'), ('IATI', 'IATI'), ('IOS', 'IOS'), ('JAR', 'JAR'), ('JFIF', 'JFIF'), ('JPEG 2000', 'JPEG 2000'), ('JPEG2', 'JPEG2'), ('JPG', 'JPG'), ('JSON', 'JSON'), ('JSON Lines', 'JSON Lines'), ('JSON-LD', 'JSON-LD'), ('KML', 'KML'), ('KMZ', 'KMZ'), ('LAS', 'LAS'), ('LYR', 'LYR'), ('MOV', 'MOV'), ('MP3', 'MP3'), ('MPEG', 'MPEG'), ('MPEG-1', 'MPEG-1'), ('MXD', 'MXD'), ('MXF', 'MXF'), ('MapInfo', 'MapInfo'), ('NetCDF', 'NetCDF'), ('ODP', 'ODP'), ('ODS', 'ODS'), ('ODT', 'ODT'), ('PDF', 'PDF'), ('PDF/A-1', 'PDF/A-1'), ('PDF/A-2', 'PDF/A-2'), ('PNG', 'PNG'), ('PPT', 'PPT'), ('RDF', 'RDF'), ('RDF Turtle', 'RDF Turtle'), ('RDF n-triples', 'RDF n-triples'), ('RDF/XML', 'RDF/XML'), ('RDFa', 'RDFa'), ('RSS', 'RSS'), ('SAR', 'SAR'), ('SAV', 'SAV'), ('SEGY', 'SEGY'), ('SHP', 'SHP'), ('SQL', 'SQL'), ('SQL Lite', 'SQL Lite'), ('SVG', 'SVG'), ('TAB', 'TAB'), ('TIFF', 'TIFF'), ('TRiG', 'TRiG'), ('TRiX', 'TRiX'), ('TXT', 'TXT'), ('VPF', 'VPF'), ('WAV', 'WAV'), ('WFS', 'WFS'), ('WMS', 'WMS'), ('WMTS', 'WMTS'), ('WMV', 'WMV'), ('WPS', 'WPS'), ('Web App', 'Web App'), ('XLS', 'XLS'), ('XLSM', 'XLSM'), ('XML', 'XML'), ('ZIP', 'ZIP')], max_length=255, null=True),
        ),
    ]