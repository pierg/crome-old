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
          echo "-w,                       launch web-server"
          exit 0
          ;;
        -w)
          echo "Deploy the web server without rebuilding..."
          python3 ./web/backend/app.py
          ;;
        -s)
          echo "Going to scripts folder..."
          cd scripts
          ;;
        -d)
          echo "Build and deploy..."
          cd ./web/frontend
          npm run deploy
          cd ../backend
          python3 app.py
          ;;
        *)
          break
          ;;
      esac
    done
fi
