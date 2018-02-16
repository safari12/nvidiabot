# Strategies

- `gagpu`
    - name: `get available gpu`
    - description: `Notify users by email if nvidia gpus are in stock`
    - sources: 
        - `nvidia website`
    - params:
        - `emails`
            - list, seperated by comma
            - require
    - duration:
        - `morning - 8:00am`
            - `every 30 min`
        - `afternoon - 12:00pm`
            - `every hour`
        - `nighttime - 12:00am`
            - `every 2 hour`
