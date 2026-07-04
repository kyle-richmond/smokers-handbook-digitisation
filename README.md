Extract structured price tables from scans of The Smokers' Handbook using the OpenAI Responses API. 

Developed as part of research into the British tobacco industry in the 1950s and 1960s.

Original copies of the Smoker's Handbook can be found on-site at the Bristol Archives (see bristolmuseums [dot] org [dot] uk / bristol-archives)

## Workflow

1. Photograph handbook pages.
2. Sort pages into yearly folders for each edition of the handbook.
3. Remove non-price pages e.g. photos of advertisements within handbook, cover pages, etc.
4. Manual pre-processing e.g. rotate and/or crop images where necessary.
5. Resize images to reduce API input token usage and processing costs.
6. Run the extraction scripts by year.
7. Combine yearly outputs.
8. Manually validate and correct the extracted data against images and original hand-digitized subsample.