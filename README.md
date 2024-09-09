# CooKin

Autonomous agent that takes a city as input and gives a recipe in french based on the weather and the location.

Using LangChain and basic LangGraph

The weather API used is https://wttr.in/

## Docker
```
docker build -t streamlit .
docker run --name CooKin -p 8501:8501 streamlit
```

Then open your browser to http://localhost:8501/ and follow the steps.

## Running without docker

```
pip install -r requirements
```

### Without Streamlit

Use the .env.template to create your .env

Run :
```
python agent.py
```

Then you can write your text

### With Streamlit

```
streamlit run streamlit_app.py
```

Then open your browser to http://localhost:8501/ and follow the steps.

