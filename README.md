# :pizza: Comprehensive Food Database
This repository includes all of the necessary files for a comprehensive database of foods in the United States. 

Included are both grocery store foods and restaurant foods. MySQL files, images for foods, and scripts are also included. The scripts are mainly for scraping the web for images of the foods. The web-scraping involves threaded processing to make it faster.

#### Arxiv Link:
For more information on this project, [here](https://ieeexplore.ieee.org/document/10216759) is the link to the paper on IEEExplore.

The paper above was published in the 2022 International Conference on Computational Science and Computational Intelligence (CSCI). If you use this dataset, please site with

L. Whalen, B. Turner-McGrievy, M. McGrievy, A. Hester and H. Valafar, "On Creating a Comprehensive Food Database," 2022 International Conference on Computational Science and Computational Intelligence (CSCI), Las Vegas, NV, USA, 2022, pp. 1610-1614, doi: 10.1109/CSCI58124.2022.00288. keywords: {Costs;Databases;Scientific computing;Soft sensors;Eating disorders;Fats;Reliability;MySQL;Table Design;USDA;Food Database},

# Why?
The USDA food database can be quite confusing to deal with. It has many tables with relations between them that are not well defined, leading to issues in using it for any real project. We have decided to tackle this problem, creating a simple database containing all the foods present in the USDA database, alongside with images for each food.

## UPDATE: 10/16/2023 (mm/dd/yyyy):
Due to Git storage limits, we have decided to move the files for the project onto the file storage platform MEGA. The link to zip files of the database files and images can be found [here](https://mega.nz/folder/0elAXR6L#QuC3C95Od8wn_j0jcn-d4A).

[Here](https://github.com/lxaw/UofSCSWITCHStudy) is an example website using this database. It is relatively simple, but should give a general idea of how the database can be used in a project.

Furthermore, we would like to thank [@jpoles1](https://github.com/jpoles1) for a creating a great tutorial on how to potentially use this database. See their posts [here](https://blog.jpoles1.com/archives/277).

## Database information:

### Menustat:
- 96 Restaurants
- 193,369 food items
- 105,077 image files
### USDA Branded:
- 17,619 Brands
- 991,665 Foods
- 322,401 image files
### USDA Non-Branded:
- 50,254 Foods
- 7 data types:
-  SR Legacy Food
-   Sample Food
-   Sub Sample Food
-   Foundation Food
-   Agricultural Acquisition Food
-   Survey FNDDS Food
- 26,028 image files
### Menuwithnutrition
- 205,000 foods

#### Note: 
- The discrepancy between the number of foods and the number of images is due to the fact that many foods do not have a particular image for them.


## Special Thanks 
The Comprehensive Food Database team would like to especially thank those users who have provided more data or tools related to the project to the community.

### Users:
- Username: jpoles1
- GitHub: https://github.com/jpoles1
- Contribution: Noticed issue with LFS storage, added Canadian food data, provided helpful scripts and tutorials. Please check out his blog [here](https://blog.jpoles1.com/archives/277) where you can find helpful tips about the food database and other interesting posts.


## ❤️ How to Support ❤️
- If this code or anyother I have written has helped you, feel free to make a donation at https://www.buymeacoffee.com/whalenlexn.
