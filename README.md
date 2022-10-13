# csvToolkit
Simple project to handle and present csv (comma separate values) files.
## Features
With this program, you can preview, edit and save changes to csv files.  
Feature list:
- preview csv file as table view
- add new and remove columns
- add new and remove rows
- change row values
- search values
- fill empty (NaN) values
- delete rows with empty values
- generate static and interactive plots
## Dependencies (libraries)
Below each name of library is shown installation command using package installer for Python (pip):
- [tkinter](https://docs.python.org/3/library/tkinter.html)
```bash
pip install tk
```
- [pandas](https://pandas.pydata.org/)
```bash
pip install pandas
```
## Usage
1. Make sure that delimiter character is correct to particular file.  
2. Click "open csv file" button and select csv file to open. After a while, content file should be visible in program.
### Preview tab
1. To see specific item (row), select record and click "Show/edit item" button or double click LMB (left mouse button).
2. To search value, enter the value next to label "Search:" and click "Start search" or press **Enter**. After a while,
   (when file is large) result will be shown below search bar.
3. To clear result and back to whole file, press **Rest search** button.
## License
Project is under [MIT License](LICENSE.md).