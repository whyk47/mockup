git add .
git commit -m '.'
git push
aws ecr get-login-password --region ap-southeast-1 | docker login --username AWS --password-stdin 980921716072.dkr.ecr.ap-southeast-1.amazonaws.com
docker build -t yk47/mockup .
docker tag yk47/mockup:latest 980921716072.dkr.ecr.ap-southeast-1.amazonaws.com/yk47/mockup:latest
docker push 980921716072.dkr.ecr.ap-southeast-1.amazonaws.com/yk47/mockup:latest