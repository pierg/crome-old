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
          echo "-c,                       launch clustering with default input"
          echo "-m,                       launch mapping with default input"
          exit 0
          ;;
        -c)
          echo "Launching CROME..."
          echo "Copying custom input file if exists..."
          cp /home/crome_specifications.py /home/cogomo/
          echo "Launching clustering..."
          python3 ./run_crome.py
          echo "Process finished, results avilable"
          echo "Clustering finished, exiting..."
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
