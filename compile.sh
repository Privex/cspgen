#!/usr/bin/env bash
#############################################################
# Python Self-contained ZIP Executable (PYZ) Compiler
#
# (C) 2020 Privex Inc. - https://www.privex.io
#     + Someguy123 ( https://github.com/Someguy123 )
#
#  * Copies the folder this script is contained within, excluding certain files, into a temporary folder.
#  * Copies the entrypoint Python file 'USE_CMD' to the file '__main__.py' - ran when the PYZ is ran.
#  * Installs the Python requirements from the requirements file REQUIREMENTS_FILE into the temporary folder.
#  * Zips up the temporary folder into ZIP_OUTDIR/ZIP_NAME
#  * Adds a '#!/usr/bin/env python3' shebang to the start of the zip file, and sets it as +x (executable)
#
# Once finished, you'll have a fully self-contained Python application at ZIP_OUTDIR/ZIP_NAME, which
# can be executed on any Linux/Unix/macOS system as a normal executable, and the user only needs Python 3
# installed, no need for pip3 install, since all dependencies are packaged inside of the .PYZ file.
#
#############################################################

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

source "${DIR}/.bash_colors"

: ${PYTHON_EXE="python3"}
: ${USE_CMD="bin/csp-gen"}
: ${ZIP_NAME="csp-gen.pyz"}
: ${ZIP_OUTDIR="${DIR}/dist"}
: ${ZIP_LEVEL=9}
: ${PKG_OUT_DIR="./"}
: ${REQUIREMENTS_FILE="base_requirements.txt"}

comp_temp="$(mktemp -d)"
tmp_proj="${comp_temp%/}/cspgen/"
RS_ARGS=('-avh' '--progress')

RS_EXCLUDE=(
    '*.pyz'
    '*.pyc'
    "${DIR}/.git"
    "${DIR}/.idea"
    "${DIR}/*/__pycache__"
    "${DIR}/__pycache__"
    "${DIR}/.env"
    "${DIR}/dist"
)

ZIP_EXCLUDE=(
    ".idea/*"
    ".vscode/*"
    ".git/*"
    "data/*"
    ".env"
    ".dist/*"
    "*/__pycache__/*"
    "*.pyc"
    "*.pyz"
    "*.ini"
    "*.zip"
    "*.log"
)

#for x in "${RS_EXCLUDE[@]}"; do
#    RS_ARGS+=('--exclude' "$x")
#done
RS_ARGS+=("--exclude-from=\"${DIR}/.rsync_exclude\"")

msg bold yellow " >>> Syncing project dir ${DIR} into temp dir $tmp_proj"
msg yellow " >>> Rsync args: ${RS_ARGS[*]}" "${DIR%/}/" "$tmp_proj"
rsync "${RS_ARGS}" "${DIR%/}/" "$tmp_proj"

msg bold yellow " >>> Entering $tmp_proj"
cd "$tmp_proj"

msg bold yellow " >>> Copying command file '${USE_CMD}' to __main__.py "
if [[ -f "__main__.py" ]]; then
    msg red "     !!! __main__.py exists already. removing __main__.py so it can be replaced with ${USE_CMD} ..."
    rm -vf "__main__.py"
fi
cp -v "${USE_CMD}" '__main__.py'

msg bold yellow " >>> Installing PIP requirements from file: ${REQUIREMENTS_FILE}"

"$PYTHON_EXE" -m pip install -r "${REQUIREMENTS_FILE}" --target "$PKG_OUT_DIR"

#msg bold yellow " >>> Moving up to temp container folder $comp_temp"
#cd ..

msg bold yellow " >>> Zipping up folder $comp_temp into ../${ZIP_NAME}.zip"
zip -v "-${ZIP_LEVEL}" -r "../${ZIP_NAME}.zip" . -x "${ZIP_EXCLUDE[@]}"

cd ..
[[ ! -d "$ZIP_OUTDIR" ]] && mkdir -p "$ZIP_OUTDIR"

msg bold yellow " >>> Adding shebang to ${ZIP_NAME}.zip via concat into ${ZIP_OUTDIR}/${ZIP_NAME}"
echo '#!/usr/bin/env python3' | cat - "${ZIP_NAME}.zip" | pv > "${ZIP_OUTDIR}/${ZIP_NAME}"
msg bold yellow " >>> Setting +x executable flag on ${ZIP_OUTDIR}/${ZIP_NAME}"
chmod -v +x "${ZIP_OUTDIR}/${ZIP_NAME}"

msg bold yellow " >>> Exiting and cleaning up temp dir: $comp_temp"
cd "$DIR"
sleep 2
rm -rvf "$comp_temp"
msg bold green " [+++] Finished. ZIP Binary is at: ${ZIP_OUTDIR}/${ZIP_NAME}"
