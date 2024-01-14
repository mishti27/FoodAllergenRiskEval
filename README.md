This Python program uses the Open AI API to evaluate restaurants menus for risk of specific allergens. 
Details can be found in my medium blog at My first Generative AI project: Evaluating restaurant menus for allergen safety @ https://medium.com/@mishti27/food-safety-algorithm-part-2-developing-the-program-49b750410fb9

Installation and use
1) Your Python project folder should look like this.
   basedir
     - src
     - data
         - input
 
2) Download the following files and place them in the src folder:
•	foodAllergyRiskEvalFunctions.py
•	foodAllergyRiskEvalMain.py
•	menuData_format.JSON
•	menu_analysis_response_format.JSON

3) In the file foodAllergyRiskEvalMain.py, set the following:
•	Your Open AI API key.
•	Your base directory (your Python project folder)

4) In the data\input folder, place your menu data files. These can be text dumps of restaurant website menus, or files created by a screen scrapers. 

5) Go back to foodAllergyRiskEvalMain.py and set the following:
•	The allergens of interest.
•	The menu data file name.

6) Execute the program.  
 
Potential improvements
•	Loop thru multiple menu files in the data\input folder.
•	Alternatively, read HTTP data from a list of restaurant websites returned by a search.
•	Graphical user interface that presents scoring and ranking of multiple restaurants.
