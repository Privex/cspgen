# Privex Content Security Policy Generator (CSP Gen)

[![Build Status](https://travis-ci.com/Privex/cspgen.svg?branch=master)](https://travis-ci.com/Privex/cspgen) 
[![Codecov](https://img.shields.io/codecov/c/github/Privex/cspgen)](https://codecov.io/gh/Privex/cspgen)  
[![PyPi Version](https://img.shields.io/pypi/v/privex-cspgen.svg)](https://pypi.org/project/privex-cspgen/)
![License Button](https://img.shields.io/pypi/l/privex-cspgen) 
![PyPI - Downloads](https://img.shields.io/pypi/dm/privex-cspgen)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/privex-cspgen) 
![GitHub last commit](https://img.shields.io/github/last-commit/Privex/cspgen)

A Python tool for generating Content Security Policies without constantly repeating yourself.

```
+===================================================+
|                 © 2021 Privex Inc.                |
|               https://www.privex.io               |
+===================================================+
|                                                   |
|   CSPGen - Python Content Sec Policy Generator    |
|   License: X11/MIT                                |
|                                                   |
|        Core Developer(s):                         |
|                                                   |
|          (+)  Chris (@someguy123) [Privex]        |
|          (+)  Kale (@kryogenic) [Privex]          |
|                                                   |
+===================================================+

CSPGen - A Python tool for generating Content Security Policies without constantly repeating yourself.
Copyright (c) 2021    Privex Inc. ( https://www.privex.io )

```

## Quickstart

```sh
# Install/Upgrade CSPGen using python3 pip as root
sudo -H python3 -m pip install -U privex-cspgen
# Or if you don't have root access / don't trust installing as root, you can install
# as a normal user, as long as $HOME/.local/bin is in your $PATH
python3 -m pip install --user -U privex-cspgen 
# Use the 'rehash' command to rescan PATH for new executables, for tab completion to work reliable
rehash

# Use --example to create an INI file using our example.ini template, which you can
# then adjust to your own CSP needs
csp-gen --example > my_csp.ini
# Open up my_csp.ini in your favourite editor, and adjust to your specific needs (e.g. nano)
nano my_csp.ini
# Parse my_csp.ini into browser Content-Security-Policy header format, outputting the result to my_header.txt
csp-gen my_csp.ini | tee -a my_header.txt
# NOTE: If something is wrong with the binary, you can run cspgen via the Python module instead
python3 -m privex.cspgen my_csp.ini | tee -a my_header.txt
# If you have some sort-of INI auto-generation, or simply want to do some pre-processing of your INI with unix tools,
# then you can simply pipe an INI config into csp-gen
cat my_csp.ini | csp-gen | tee -a my_header.txt

# If you wanted to make the CSP header more readable - assuming the web server you're gonna use it on allows newlines,
# you can use --section-sep to separate each CSP section (img-src, media-src etc.) with a newline
csp-gen --section-sep "\n" my_csp.ini
```

## Docker Quickstart

**Our DockerHub image:** `privex/cspgen`

Our image is based on `python:3.9-alpine` to ensure the smallest image size, since CSPGen doesn't require any special
libraries that would require a full debian-based image.

```sh
# Alias the docker run command to 'cspgen' for convenience
alias cspgen="docker run --rm -i privex/cspgen"
# Generate an example .ini file
cspgen --example > my_csp.ini
# Adjust the INI file to your CSP needs
nano my_csp.ini
# Once your INI file is ready to be converted, pipe it in via STDIN
# (docker cannot access your files unless you mount a volume onto /data)
cspgen < my_csp.ini
# If you wanted to make the CSP header more readable - assuming the web server you're gonna use it on allows newlines,
# you can use --section-sep to separate each CSP section (img-src, media-src etc.) with a newline
cspgen --section-sep "\n" < my_csp.ini
```

## Install

### From pip3

CSPGen can easily be installed from PyPi, using the standard `pip3` package manager.

```sh
# Install/Upgrade CSPGen using pip3 as root
sudo -H pip3 install -U privex-cspgen
# Or if you don't have root access / don't trust installing as root, you can install
# as a normal user, as long as $HOME/.local/bin is in your $PATH
pip3 install --user -U privex-cspgen 
# If you have problems using pip3, then use python3 / python3.x to call the pip module
python3.7 -m pip install --user -U privex-cspgen
```

### From repo source code

```sh
# Install pipenv if you don't already have it installed.
# Ideally install it using whatever the latest version of python is - on your system
python3.8 -m pip install -U pipenv

git clone https://github.com/Privex/cspgen.git
cd cspgen
# Create a virtualenv + install required deps + development deps
pipenv install --dev
# Activate the virtualenv (use 'exit' to deactivate a pipenv virtualenv)
pipenv shell
# Use run.py to run the CLI from the repo directly
./run.py --example > my_csp.ini
./run.py my_csp.ini
```

### From Docker (DockerHub)

```sh
###
# You can run privex/cspgen directly, and docker should auto download it from Docker Hub.
# Use the image just like you would the normal csp-gen EXE
###
docker run --rm -i privex/cspgen --example > my_csp.ini
docker run --rm -i privex/cspgen < my_csp.ini
###
# You can use 'docker pull' to manually download, or update the cspgen image
###
docker pull privex/cspgen
###
# You can re-tag our image to an easier to type image name
###
docker tag privex/cspgen cspgen
docker run --rm -i cspgen < my_csp.ini
```


### From Docker (building image from repo Dockerfile)

```sh
git clone https://github.com/Privex/cspgen.git
cd cspgen
docker build -t cspgen .
docker run --rm -i cspgen < my_csp.ini
```


## Usage

### Example INI File

Once you've installed CSPGen, you can begin creating CSP template files, in INI format in any folder you like.

Here is a basic example INI template, which covers most of the basics:

```ini
[groups]
# First we define cdn, onions, and i2p
cdn = https://cdn.privex.io cdn.privex.i2p files.privex.i2p files.privex.io https://www.privex.io
onions = privex3guvvasyer6pxz2fqcgy56auvw5egkir6ykwpptferdcb5toad.onion privexqvhkwdsdnjofrsm7reaixclmzpbpveefiu4uctfm2l4mycnwad.onion
i2p = privex.i2p www.privex.i2p pay.privex.i2p
# Now we can add our main websites, PLUS the onions, and i2p variables
websites = https://www.privex.io https://pay.privex.io https://privex.io {{onions}} {{i2p}}
# While defaultsrc will contain 'self' + websites + cdn
defaultsrc = 'self' {{websites}} {{cdn}}

images = https://i.imgur.com https://ipfs.io https://cloudflare-ipfs.com
video = https://youtube.com https://vimeo.com
media = {{video}} {{images}}

[default-src]
# For default-src, we can simply set zones to use the defaultsrc var
zones = {{defaultsrc}}
# Enable unsafe-inline and disable unsafe-eval for default-src
unsafe-inline = true
unsafe-eval = false

[img-src]
zones = {{defaultsrc}} {{images}} {{trustpilot}}

[media-src]
zones = {{defaultsrc}} {{media}}

[flags]
# Special header 'flags'. We can set the independent CSP flag 'upgrade-insecure-requests' here.
flags = upgrade-insecure-requests
```

### Loading INI files

Assuming we saved this file as `my_csp.ini`, it could be loaded in two different ways:

#### As command line arguments

You can pass one or more filenames as positional CLI arguments to `csp-gen`. For now we'll just pass one:

```sh
csp-gen my_csp.ini
# NOTE: If something is wrong with the binary, you can run cspgen via the Python module instead
python3 -m privex.cspgen my_csp.ini
```

#### Piped via STDIN

In compliance with UNIX standards, the tool can also accept a config via STDIN, and will output the generated
CSP config via STDOUT. Any logging (if logging is even enabled by setting env `LOG_LEVEL=DEBUG`) is sent to STDERR
by default, to prevent getting mixed with the config printed via standard output.

```sh
cat my_csp.ini | csp-gen | tee -a output.txt
```

You can also set the filename to `-`, as you would with `gzip`, `tar`, and other UNIX/Linux programs, to force
reading from STDIN:

```sh
cat my_csp.ini | csp-gen - | tee -a output.txt
```

### Customising Output Format

Currently there are just two customisation options available:

 - `--section-sep` - The separator used between each "section" like default-src, img-src, media-src etc.
   
   Defaults to `' '` (one space)
 - `--file-sep` - The separator used between each INI file's outputted config. This only matters if you're passing
   more than one INI config file to `csp-gen` at a time.
   
   Defaults to: `'\n\n'` (two newline characters.)

Note that you don't need to pass literal newline/carriage return/tab characters, as the script will automatically
convert `\n` `\r` and `\t` in text format, into their real single character versions.

Example:

```sh
csp-gen --section-sep "\t" --file-sep "\n\n--NEXT--\n\n\t" my_csp.ini example.ini
```

This would result in the output (line breaks were added to the output after copying, to make it more readable):

```
default-src: 'self' https://www.privex.io https://pay.privex.io https://privex.io 
privex3guvvasyer6pxz2fqcgy56auvw5egkir6ykwpptferdcb5toad.onion 
privexqvhkwdsdnjofrsm7reaixclmzpbpveefiu4uctfm2l4mycnwad.onion privex.i2p www.privex.i2p pay.privex.i2p https://cdn.privex.io 
cdn.privex.i2p files.privex.i2p files.privex.io 'unsafe-inline'; img-src: 'self' https://www.privex.io https://pay.privex.io 
https://privex.io privex3guvvasyer6pxz2fqcgy56auvw5egkir6ykwpptferdcb5toad.onion 
privexqvhkwdsdnjofrsm7reaixclmzpbpveefiu4uctfm2l4mycnwad.onion privex.i2p www.privex.i2p pay.privex.i2p https://cdn.privex.io 
cdn.privex.i2p files.privex.i2p files.privex.io https://i.imgur.com https://ipfs.io 
https://cloudflare-ipfs.com;   media-src: 'self' https://www.privex.io https://pay.privex.io https://privex.io 
privex3guvvasyer6pxz2fqcgy56auvw5egkir6ykwpptferdcb5toad.onion 
privexqvhkwdsdnjofrsm7reaixclmzpbpveefiu4uctfm2l4mycnwad.onion privex.i2p www.privex.i2p pay.privex.i2p https://cdn.privex.io 
cdn.privex.i2p files.privex.i2p files.privex.io https://youtube.com https://vimeo.com https://i.imgur.com 
https://ipfs.io https://cloudflare-ipfs.com;   upgrade-insecure-requests;

--NEXT--

    default-src: 'self' https://www.privex.io https://pay.privex.io https://privex.io 
privex3guvvasyer6pxz2fqcgy56auvw5egkir6ykwpptferdcb5toad.onion 
privexqvhkwdsdnjofrsm7reaixclmzpbpveefiu4uctfm2l4mycnwad.onion privex.i2p www.privex.i2p pay.privex.i2p https://cdn.
privex.io cdn.privex.i2p files.privex.i2p files.privex.io 'unsafe-inline'; style-src: 'self' https://www.privex.io 
https://pay.privex.io https://privex.io privex3guvvasyer6pxz2fqcgy56auvw5egkir6ykwpptferdcb5toad.onion 
privexqvhkwdsdnjofrsm7reaixclmzpbpveefiu4uctfm2l4mycnwad.onion privex.i2p www.privex.i2p pay.privex.i2p https://cdn.
privex.io cdn.privex.i2p files.privex.i2p files.privex.io https://widget.trustpilot.com https://trustpilot.com 
https://fonts.gstatic.com https://fonts.googleapis.com 'unsafe-inline';     script-src: 'self' https://www.privex.io 
https://pay.privex.io https://privex.io privex3guvvasyer6pxz2fqcgy56auvw5egkir6ykwpptferdcb5toad.onion  
privexqvhkwdsdnjofrsm7reaixclmzpbpveefiu4uctfm2l4mycnwad.onion privex.i2p www.privex.i2p pay.privex.i2p 
https://cdn.privex.io cdn.privex.i2p files.privex.i2p files.privex.io https://widget.trustpilot.com  
https://trustpilot.com 'unsafe-inline';   font-src: 'self' https://www.privex.io https://pay.privex.io  
https://privex.io privex3guvvasyer6pxz2fqcgy56auvw5egkir6ykwpptferdcb5toad.onion 
privexqvhkwdsdnjofrsm7reaixclmzpbpveefiu4uctfm2l4mycnwad.onion privex.i2p www.privex.i2p pay.privex.i2p 
https://cdn.privex.io cdn.privex.i2p files.privex.i2p files.privex.io https://widget.trustpilot.com 
https://trustpilot.com https://fonts.gstatic.com https://fonts.googleapis.com;      img-src: 'self' 
https://www.privex.io https://pay.privex.io https://privex.io 
privex3guvvasyer6pxz2fqcgy56auvw5egkir6ykwpptferdcb5toad.onion 
privexqvhkwdsdnjofrsm7reaixclmzpbpveefiu4uctfm2l4mycnwad.onion privex.i2p www.privex.i2p 
pay.privex.i2p https://cdn.privex.io cdn.privex.i2p files.privex.i2p files.privex.io 
https://i.imgur.com https://ipfs.io https://cloudflare-ipfs.com https://widget.trustpilot.com 
https://trustpilot.com;      media-src: 'self' https://www.privex.io https://pay.privex.io 
https://privex.io privex3guvvasyer6pxz2fqcgy56auvw5egkir6ykwpptferdcb5toad.onion 
privexqvhkwdsdnjofrsm7reaixclmzpbpveefiu4uctfm2l4mycnwad.onion privex.i2p www.privex.i2p pay.privex.i2p 
https://cdn.privex.io cdn.privex.i2p files.privex.i2p files.privex.io https://youtube.com https://vimeo.com 
https://i.imgur.com https://ipfs.io https://cloudflare-ipfs.com;   object-src: 'self' https://www.privex.io 
https://pay.privex.io https://privex.io privex3guvvasyer6pxz2fqcgy56auvw5egkir6ykwpptferdcb5toad.onion 
privexqvhkwdsdnjofrsm7reaixclmzpbpveefiu4uctfm2l4mycnwad.onion privex.i2p www.privex.i2p pay.privex.i2p 
https://cdn.privex.io cdn.privex.i2p files.privex.i2p files.privex.io https://youtube.com https://vimeo.com 
https://i.imgur.com https://ipfs.io https://cloudflare-ipfs.com;  form-action: 'self' https://www.privex.io 
https://pay.privex.io https://privex.io privex3guvvasyer6pxz2fqcgy56auvw5egkir6ykwpptferdcb5toad.onion 
privexqvhkwdsdnjofrsm7reaixclmzpbpveefiu4uctfm2l4mycnwad.onion privex.i2p www.privex.i2p pay.privex.i2p 
https://cdn.privex.io cdn.privex.i2p files.privex.i2p files.privex.io https://hived.privex.io;       
connect-src: 'self' https://www.privex.io https://pay.privex.io https://privex.io 
privex3guvvasyer6pxz2fqcgy56auvw5egkir6ykwpptferdcb5toad.onion 
privexqvhkwdsdnjofrsm7reaixclmzpbpveefiu4uctfm2l4mycnwad.onion privex.i2p www.privex.i2p pay.privex.i2p 
https://cdn.privex.io cdn.privex.i2p files.privex.i2p files.privex.io 
https://hived.privex.io;       upgrade-insecure-requests;

```

### Compiling the repo into a self-contained PYZ (ZIP) executable file

#### Requirements + Compiling

Once finished, you'll have a fully self-contained Python application at `dist/csp-gen.pyz`, which 
can be executed on any Linux/Unix/macOS system as a normal executable, and the user only needs Python 3
installed, no need for pip3 install, since all dependencies are packaged inside of the .PYZ file.

Required to compile:

- A Linux / UNIX(-like) operating system. Should work on:
   - Linux Distros: Ubuntu 18.04+, Debian 10+ (Buster or newer), Fedora (30+), CentOS (6+), RHEL, Oracle, probably most others
   - BSD Distros: FreeBSD, OpenBSD, NetBSD, and most others
   - macOS: Probably any version in the past 10 years. I'd recommend no older than Mavericks (10.9).
- The Linux/UNIX `zip` CLI application (`apt install -y zip`, `dnf install -y zip`, `brew install zip`)
- The `bash` shell, to execute the compile.sh script. May not be compatible with `bash` versions prior to 4.0
- Python 3.6+ (maybe 3.7+) and `pip3` (the `pip` python3 module)

```sh
git clone https://github.com/Privex/cspgen.git
cd cspgen
./compile.sh
```

You should now have a fully self-contained Python application at `dist/csp-gen.pyz` :)

#### Using the PYZ file

The easiest way to use the PYZ file is to simply copy it into `/usr/local/bin/csp-gen`, like so:

```sh
# By using 'install', it will ensure 'csp-gen' has the correct perms to be read and ran by all users.
sudo install dist/csp-gen.pyz /usr/local/bin/csp-gen
```

Now you should be able to run `csp-gen` like normal. The benefit of the PYZ, is that you can distribute
the PYZ like a static binary, it contains all dependencies required for the application to run - inside of the
singular file. 

It doesn't require the user to `pipenv install`, setup virtualenvs, or anything like that. They
simply just need to make sure Python 3.6 or newer is installed.

```sh
user@host $ csp-gen -V

    Content Security Policy (CSP) Generator
        
        Version: v0.5.0
        Github:  https://github.com/Privex/cspgen
        License: X11 / MIT
        
        (C) 2021 Privex Inc. ( https://www.privex.io )


```

## License

CSPGen is released under the X11 / MIT License.

Please see the file `LICENSE.txt` or `LICENSE` for full license text.

# Thanks for reading!

**If this project has helped you, consider [grabbing a VPS or Dedicated Server from Privex](https://www.privex.io) -**
**prices start at as little as $0.99/mo USD (we take cryptocurrency!)**


