# co-occurrence analysis algorithm
This algorithm was implemented in python to do co-ocurrence analysis using geolocalizated data, which can be available in the Global Biodiversity Information Facility (GBIF), using the methodology propoused by (Silva et al., 2016). 

Two parameters are needed to create a transactions file, the geo-located data (with next structure: specie_name, latitude, longitude) and distance in meters. First step of the algorithm is create a folder named DE_results, where are saved the output files (transaction, all_rules, positive/negative rules), reading all records in data file, one by one and calculating the distance between the one registry and the rest, using its latitude and longitude through Haversine Formula (Chopde & Nichat, 2013). If the distance is lower than the parameter, a transaction is created and stored in the transaction file, each transaction has the name of the species which their separation were not farther than distance in parameter, concatenated with comma.

The second step is to define basic values of parameters such as minimum support, minimum confidence, negative minimum lift, positive minimum lift, then rules are generated through apriori algorithm presented in Agrawal & Srikant, (1994), using transaction file created previously, this algorithm creates a set of rules, where each rule containes antecedent and consequent elements and confidence value, in addition is necessary to calculate the frequency of each element of the rule using the function chi square from scipy.stats python package. This function calculates the chi-square and p-value for the rule. We calculated support and lift values from definitions presented in (Silva et al., 2016). Finally some conditions are evaluated to identify if the rule is positive or negative, only the rules that has p-value equal to ~0 in positive cases and p-value equal to ~1 in negative cases, are stored in database-final file. Also all rules generated are stored in all-rules file.

# Prerequisites
- Python 2.7
- numpy python package

# How to install
- Install all prerequisites
- clone this repository with:
  git clone https://github.com/simonorozcoarias/co-ocurrence_analysis.git

# How to run
python disespAlgor.py file_with_data.txt distance_en_meters

# References 
Agrawal, R., & Srikant, R. (1994). Fast algorithms for mining association rules. Proceeding VLDB ’94 Proceedings of the 20th International Conference on Very Large Data Bases, 1215, 487–499. https://doi.org/10.1.1.40.6757

Chopde, N., & Nichat, M. (2013). Landmark Based Shortest Path Detection by Using A* and Haversine Formula. GH Raisoni College of Engineering and …, 1(2), 298–302.

Silva, L. A. E., Siqueira, M. F., Pinto, F. D. S., Barros, F. S. M., Zimbrão, G., & Souza, J. M. (2016). Applying data mining techniques for spatial distribution analysis of plant species co-occurrences. Expert Systems with Applications, 43, 250–260. https://doi.org/10.1016/j.eswa.2015.08.031

# Citation

If you use this algorithm in your research please cite as following:

Orozco-Arias S, Núñez-Rincón AM, Tabares-Soto R, López-Álvarez D. 2019. Worldwide co-occurrence analysis of 17 species of the genus Brachypodium using data mining. PeerJ 6:e6193 DOI 10.7717/peerj.6193
