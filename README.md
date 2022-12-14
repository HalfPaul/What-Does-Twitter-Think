# What does Twitter think?
"What does Twitter think?" provides user Twitter's general sentiment about certain topic.
## How to run frontend
``` 
cd app 
docker build -t twitter_think_client .
docker run -p 3000:3000 twitter_think_client
```

## How to run API
``` 
cd api 
docker build -t twitter_think_api .
docker run -p 8000:8000 twitter_think_api
```

![Project Image](img.png)