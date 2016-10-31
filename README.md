Musip

Set-Up
https://github.com/MTG/essentia

You might need to install ipython to run the program

To install ipython
sudo pip install --user ipython

To run a file
python -m IPython <filename>

To solve warnings (Matplotlib is building the font cache using fc-list. This may take a moment.)
cd ~/.cache/matplotlib/
rm fontList.cache

Run the code and the warning will again be issue.
Run the code again, no more warnings.
