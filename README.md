# Mariolike Markov Level Generation
An example of using a Markov chain to generate levels like those from Super Mario Bros. based on the Markov chain given on the right side of Figure 6.7

Scripts:

- `train.py`: code that trains a Markov chain on the levels from Super Mario Bros. 1 and 2 (The Lost Levels)
- `generate.py`: code that generates a new level from the trained Markov chain, overwriting the existing level
- `visualize.py`: code that visualizes the generated level with assets from Kenney's Platformer Asset Pack

To run the code take the following steps: 

1. Install Python 3.9 (but tweaking it for other versions should be simple) and the 'pickle' library
2. Run `train.py`, which will train a Markov chain represented as a dictionary of dictionaries based on the levels from Super Mario Bros. (SMB) and Super Mario Bros.: The Lost Levels (SMB2)
3. Run `generate.py`, which will generate a level in a tile representation to `Generated Levels/output.txt` (Warning: this will overwrite any previous generated levels)
4. (Optionally) run `visualize.py`, which will visualize the generated level using Kenney's Pixel Platformer assets.
5. Make alterations to `train.py` to alter the state representation of the Markov chain, `generate.py` to alter the sampling procedure, or `visualize.py` to alter the visualization procedure including the constructive rules, rereun steps 2-4 to see the impact of these changes


## MarkovMario Scraper Addition
A web scraper added in order to improve the dataset size of mario levels. Uses the `requests` and `beautifulsoup` library and some simple image processing to scrape
a set of mario level images, extract the unique blocks from them, and store their representations.

If you want to run the code yourself, start a new environment and run `pip install -r requirements.txt` to install the dependencies.

- `scraper.py`: Downloads the set of mario level images from the internet using simple scraping techniques
- `preprocess.py`: Preprocesses images into blocks, and stores the unique blocks seen at least once across all levels as sprite pngs
- `mapper.py`: Encoding represents maps as indices into the sprite array for a particular set of maps.
  - Note a choice has been made in the preprocess step to remove blocks unique to a certain level, we choose to replace with the most similar block here. Sometimes this has weird results. Otherwise we would not have been able to use a uint8 representation.

After dataset has been scraped, you can run the code to generate new levels:

1. Run `train_index_repr.py` to generate the Markov Chain on the scraped levels. For best results choose an exemplar level to test. For pandemonium, try with all levels.
2. Run `generate_index_repr.py` to create a new level. Adjust the code slightly to change the paths in order to specify SMB1 or SMB2 assets, and choose the tile to use when no other tile is found, this will majorly affect the output.