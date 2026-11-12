# Example project

The billing service reads its rate table from `rates.csv`. A nightly job from another team drops that file, and no code in this repo mentions how it arrives. If its columns ever change, tell finance before changing the parser.
