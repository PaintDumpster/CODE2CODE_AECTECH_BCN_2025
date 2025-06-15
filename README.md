<img src="data/img/Code  2 code.png" width="300">

# *CODE*2**CODE**

> This hackathon project aims to adress the age old problem of allowing designers to quickly check if their BIM models are code compliant with their local or foreign regulations. This is usually a tedious process that requires external consultancy and, if not properly done, can result in serious delays or even project cancelations.
Therefore, the project is a web page that allows the user to simply upload the model, along with a documment of the regulation to specify, and throug prompting wit an llm, understand if the model is correctly implementing these regulations.
To do this, we generate graph databases of the IFC model and the regulatory documentation. This allows to establish concrete relationships between documentation parameters and bim objects, both expressed as nodes.
We used langchain to create a graphRAG that allows the LLM to be aware of the graph, retrieve data and even generate queries. Langchain allows the user to write a natural language prompt as the llm translates it to graph query language.

## HOW TO USE THIS REPO

1. check the branches. everything is currently in development, hehe.
2. download the repo and input the .cypher files into a neo4j aura database instance.
3. input yourOpenAI api key into the vue llm file.
4. start the vue server
5. connect your langchain instance to the database and to the llm.
6. Enjoy the bursting feeling of querying through a documentation and seeing reflected in your ifc model (if you dont mind an endless amount of bugs <3).