First of all build image localy

```
docker build -t homework1 .
```

Then we can run container with port mapping

```
docker run -p 8000:80 homework1
```

Tag image 

```
docker tag <imageId> nikfedoseev/microservice-architecture-homeworks:homework1
```

Push image 

```
docker push nikfedoseev/microservice-architecture-homeworks:homework1    
```

After push to docker hub we can run container like this

```
docker run -p 8000:80 nikfedoseev/microservice-architecture-homeworks:homework1
```