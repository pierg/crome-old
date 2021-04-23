# Generate Files
if [ $# -eq 0 ]
  then
    echo "No parameters provided. Launching bash"
    bash
else
    while test $# -gt 0; do
      case "$1" in
        -h|--help)
          echo "options:"
          echo "-h, --help                show brief help"
          echo "-e,                       do not launch anything"
          echo "-m,                       launch web-server"
          exit 0
          ;;
        -e)
          echo "Waiting for commands..."
          break
          ;;
         -w)
          echo "Launching the web-server..."
          python3 ./web/webapp.py
          ;;
        *)
          break
          ;;
      esac
    done
fi
