git pull
docker build -t phone .
docker rm -f phone
docker run -v /mnt/usb:/mnt/usb --privileged --restart unless-stopped -d -h "phone" --name "phone" phone
