Ennigaldi
=========

A lightweight set of Django applications for managing and exporting
collection assets, such as museum object records and their associated metadata.


Rationale
---------

The idea behind **Ennigaldi** is to provide a standards-compliant,
open-source data model for cultural collection assets.
The main goal is to have full compatibility with the
Object Information Group in [Spectrum 4.0](http://collectionstrust.org.uk/spectrum/)
as well as the [VRA Core 4](https://www.loc.gov/standards/vracore/)
XML representation.
A long-term aim is to build, on top of this, simple procedure registers
for management actions upon these objects.

The name **Ennigaldi** comes from a
[late Babylonian priestess](https://en.wikipedia.org/wiki/Ennigaldi)
said to have organized the world's earliest museum.

The project aims to implement some of the functionality currently found
in other proprietary or open-source software, while prioritizing
the following aspects:

- Full standards compliance: the data model can be exported to
  various standard representations with minimal loss of information.
- Single setup and configuration: unlike other systems, which rely
  on complex interactions among a hodgepodge of software,
  requiring script-based installation and a dedicated virtual machine,
  we are looking to keep everything under a single piece of software
  and database to afford the systems administrator full control
  over the install and configuration process.
- Pluggable structure: by leveraging the flexibility of Django,
  the project can be customized and extended in various ways;
  for example, the built-in accession number generator can be
  replaced with a different rule, or skipped altogether.


Features
--------

**Ennigaldi** is currently in early development stage, but already provides
a minimally functional implementation of:

- Object register entry, including a single title, basic information,
  dimensions and inscriptions.
- Automatic accession number generation following the
  [Re-org](https://ceroart.revues.org/2112) standard
  promoted by the [École du Patrimoine Africain](http://www.epa-prema.net/).
- Output of a simple HTML detail page for each object,
  modeled after the [SICG](http://sicg.iphan.gov.br/sicg/pesquisarBem)
  system created by the Brazilian national heritage institute,
  [IPHAN](http://www.iphan.gov.br).


Roadmap
-------

The following features are required before **Ennigaldi** can be considered
suitable for alpha release:

- Complete the Object Production and Description groups (Spectrum)
  implementation.
- Provide a web-based interface for starting accession batches,
  which currently must be done in the Python shell.
- Provide some sort of digital asset implementation for the objects,
  at the very least the ability to add a set of photographs
  with the proper metadata.
- Provide simple user registration and management, including
  versioning, possibly with [Django-reversion](https://django-reversion.readthedocs.io/).

Further improvements in the future might include:

- Spectrum Procedure support.
- Internationalization of the interface and of content.
- Geolocation support by means of PostGIS.
- API to integrate with various related systems, such as
  [Tainacan](https://github.com/medialab-ufg/tainacan) or
  [Mapas culturais](https://github.com/culturagovbr/mapasculturais-br).
