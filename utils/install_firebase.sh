#!/bin/bash
# Script to install a specific version of firebase tools
# The code for this is borrowed from the script at https://firebase.tools
# The main difference is that it allows for the install of a specific
# firestore version.
#
# to install a specific version: install_firebase.sh v[firestore tools release]
# i.e.
# $ install_firebase.sh v13.2.1
#
# to uninstall run: uninstall=true install_firebase.sh

# If the user asked for us to uninstall firebase, then do so.
if [ "$uninstall" = "true" ]; then

    echo "-- Removing binary file..."
    sudo rm $(which firebase)
    echo "-- Removing emulator runtimes..."
    rm -rf ~/.cache/firebase/emulators
    echo "-- Removing npm cache..."
    rm -rf ~/.cache/firebase/tools
    echo "-- Removing firebase runtime..."
    rm -rf ~/.cache/firebase/runtime

    echo "-- firebase-tools has been uninstalled"
    echo "-- All Done!"

    exit 0
fi

# We need to ensure that we don't mess up an existing "firebase"
# install, so before doing anything we check to see if this system
# has "firebase" installed and if so, we exit out.
echo "-- Checking for existing firebase-tools on PATH..."
HAS_FIREBASE_TOOLS=$(which firebase)

if [ ! -z "$HAS_FIREBASE_TOOLS" ]; then
    INSTALLED_FIREBASE_VERSION=$(firebase --version)

    # In the case of a corrupt firebase-tools install, we wont be able to
    # retrieve a version number, so to keep the logs correct, we refer to
    # your existing install as either the CLI version or as a "corrupt install"
    if [ ! -z "$INSTALLED_FIREBASE_VERSION" ]; then
        FIREBASE_TOOLS_NICKNAME="firebase-tools@$(firebase --version)"
    else
        FIREBASE_TOOLS_NICKNAME="a corrupted firebase-tools binary"
    fi

    # We are only capable of upgrading installs of the standalone binary version of firebase-tools
    # To detect if the version of firebase-tools installed is the binary version, we pass a hidden
    # flag which returns a JSON response from the binary or an error on a regular install.
    if [[ "$(firebase --tool:setup-check 2>&1)" == error* ]]; then
        # If the install isn't a binary (i.e. it was installed via npm) then we can't help, so we exit.
        echo "Your machine already has $FIREBASE_TOOLS_NICKNAME installed. Nothing to do."
        echo "-- All done!"

        exit 0
    else
        # If the user didn't pass upgrade=true, then we print the command to do an upgrade and exit
        if [ ! "$upgrade" = "true" ]; then
            echo "Your machine has $FIREBASE_TOOLS_NICKNAME installed."
            echo "If you would like to upgrade your install run: curl -sL firebase.tools | upgrade=true bash"

            exit 0
        else
            # If the user did pass upgrade=true, then we allow the script to continue and overwrite the install.
            echo "-- Your machine has $FIREBASE_TOOLS_NICKNAME, attempting upgrade..."
        fi

    fi
fi


INSTALL_DIR="/usr/local/bin"

# We use "tr" to translate the uppercase "uname" output into lowercase
UNAME=$(uname -s | tr '[:upper:]' '[:lower:]')

# Then we map the output to the names used on the Github releases page
case "$UNAME" in
    linux*)     MACHINE=linux;;
    darwin*)    MACHINE=macos;;
esac

# If we never define the $MACHINE variable (because our platform is neither Mac
# or Linux), then we can't finish our job, so just log out a helpful message
# and close.
if [ -z "$MACHINE" ]
then
    echo "Your operating system is not supported."
    exit 0
fi

if [ $# -eq 0 ]; then
  VERSION="latest"
elif [ "$1" == "--help" ]; then
  echo "This script takes an optional argument (version)."
  echo "Usage: $0 [version]"
  exit 0
else  
  VERSION="$1"
fi
echo "-- Installing firestore tools version $VERSION"

DOWNLOAD_URL="https://firebase.tools/bin/$MACHINE/$VERSION"

INSTALL_DIR="/usr/local/bin"

#
# Perform install
#

# We need to ensure that the INSTALL_DIR exists.
# On some platforms like the Windows Subsystem for Linux it may not.
# We create it using a non-destructive mkdir command.
sudo mkdir -p "$INSTALL_DIR"

echo "-- Downloading binary from $DOWNLOAD_URL"

# We use "curl" to download the binary with a flag set to follow redirects
# (Github download URLs redirect to CDNs) and a flag to show a progress bar.
sudo curl -o "$INSTALL_DIR/firebase" -L --progress-bar $DOWNLOAD_URL

# Once the download is complete, we mark the binary file as readable
# and executable (+rx).
echo "-- Setting permissions on binary..."
sudo chmod +rx "$INSTALL_DIR/firebase"

# If all went well, the "firebase" binary should be located on our PATH so
# we'll run it once, asking it to print out the version. This is helpful as
# standalone firebase binaries do a small amount of setup on the initial run
# so this not only allows us to make sure we got the right version, but it
# also does the setup so the first time the developer runs the binary, it'll
# be faster.
VERSION=$("$INSTALL_DIR/firebase" --version)

# If no version is detected then clearly the binary failed to install for
# some reason, so we'll log out an error message and report the failure
# to headquarters via an analytics event.
if [ -z "$VERSION" ]
then
    echo "Something went wrong, firebase has not been installed."
    echo "Please file a bug with your system information on Github."
    echo "https://github.com/firebase/firebase-tools/"
    echo "-- All done!"

    exit 1
fi

# In order for the user to be able to actually run the "firebase" command
# without specifying the absolute location, the INSTALL_DIR path must
# be present inside of the PATH environment variable.

echo "-- Checking your PATH variable..."
if [[ ! ":$PATH:" == *":$INSTALL_DIR:"* ]]; then
    echo ""
    echo "It looks like $INSTALL_DIR isn't on your PATH."
    echo "Please add the following line to either your ~/.profile or ~/.bash_profile, then restart your terminal."
    echo ""
    echo "PATH=\$PATH:$INSTALL_DIR"
    echo ""
    echo "For more information about modifying PATHs, see https://unix.stackexchange.com/a/26059"
    echo ""
fi

# Since we've gotten this far we know everything succeeded. We'll just
# let the developer know everything is ready and take our leave.
echo "-- firebase-tools@$VERSION is now installed"

echo "-- running emulator setup"
firebase setup:emulators:firestore

echo "-- All Done!"

exit 0

