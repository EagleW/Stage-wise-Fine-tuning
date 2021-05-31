# Wikipedia Graph-to-Text Dataset

## Overview
This repository contains data used for the Wikipedia fine-tuning stage for paper Stage-wise Fine-tuning for Graph-to-Text Generation. [Dataset](https://drive.google.com/file/d/18N8xgAftgoV7D03G643EDp1BfQXzPOTH/view?usp=sharing)

## Dataset

The data folder contains 166 JSON files which include graph-to-text pairs related to 15 categories (Astronaut, University, Monument, Building, ComicsCharacter, Food, Airport,
SportsTeam, WrittenWork, Athlete, Artist, City, MeanOfTransportation, CelestialBody, Politician)
that appear in the WebNLG dataset. The file name is the Wikidata instance.

Each line in a file represents the dictionary instance of a graph-to-text pair stored in JSON format. The dictionary contains 5 keys: "triples" contains all triples provided by the corresponding to a Wikipedia page, "type" represents the type of the instance, "txt" represents a paragraph where sentences that contains the triple entities, "covered" represents how many triples are covered by the text, and "total" represents the total number of triples. Each triple contains 4 elements: subject, relation, object, a True/False flag whether this triple is contained in the paragraph. For this paper, we filtered out those triples that don't appear in the corresponding paragraph.

## License
Creative Commons — Attribution 4.0 International — CC BY 4.0
