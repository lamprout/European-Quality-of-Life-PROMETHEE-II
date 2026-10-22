# Quality of Life in Europe — PROMETHEE II Analysis (2014–2023)

## Project overview

This project was done due to the motivation I had from both a personal and academic interest in the factors that play vital role in **Quality of Life**. Personal interest derived from the fact that I want to pursue a professional career abroad, therefore a study showing results about the well-being of several European Countries would help me make a more data-driven decision. My academic interest on the other hand emerged due to how complex Quality of Life has become nowadays and its many aspects. The tool used in this research, PROMETHEE II method, is extremely significant in exploring Quality of Life and its indicators. 

Quality of Life is compared across **20 European Union countries** using **13 indicators** from Eurostat each with its own significancy. For the python implementation, **2 scenarios** were introduced. The first one involves an **aggregated analysis** using the average values for each criterion across the 10-year range for every country. The second consists of a **yearly evaluation** where each country will be compared even with itself but for different year, for example Denmark of 2020 with Denmark of 2019 etc.

The goal is to examine how countries compare across a wide variety of indicators, reflecting several aspects of well-being such as economic performance, housing quality, social vulnerability and others.  

**Period:** 2014–2023  
**Countries:** Austria (AT), Belgium (BE), Croatia (HR), Czechia (CZ), Denmark (DK), Finland (FI), France (FR), Germany (DE), Greece (EL), Hungary (HU), Ireland (IE), Italy (IT), Luxembourg (LU), Netherlands (NL), Poland (PL), Portugal (PT), Romania (RO), Slovakia (SK), Spain (ES), Sweden (SE).  
**Tools:** Python, pandas, NumPy, Matplotlib, openpyxl, Eurostat API and Excel.

## Research Questions
1. For the **average scenario**, which EU countries **rank** the **highest, lowest**? 
2. For the **yearly scenario**, which EU countries **rank** the **highest, lowest**? 
3. What was the **best and worst year for every country**? Is there any 
particular year that seems for every country was a downfall?  
4. Which **countries** showed the **most improvement or decline**?  
5. Are there countries that overall perform extremely low at some 
indicators but excel in others?  
6. Which countries are the **best, worst across all indicators**?
7. How **sensitive** are the rankings to the choice of PROMETHEE **preference function and weights**?

## Indicators direction and weights

| Criterion | Direction | Weight |
|---|---|---:|
| Median income | **Maximize** | 0.15 |
| GDP per capita | **Maximize** | 0.04 |
| Great Difficulty making ends meet | Minimize | 0.11 |
| Bad Housing quality | Minimize | 0.09 |
| Housing overcrowding | Minimize | 0.06 |
| Unemployment rate | Minimize | 0.14 |
| Inability to face unexpected expenses | Minimize | 0.12 |
| Arrears | Minimize | 0.08 |
| Perceived criminality | Minimize | 0.07 |
| Perceived pollution | Minimize | 0.04 |
| Average weekly working hours | Minimize | 0.05 |
| Tertiary educational attainment | **Maximize** | 0.02 |
| Road fatalities | Minimize | 0.03 |

**Note:** These are analyst-assigned weights, based on my own preference. Results depend on the selected indicators, their directions, the weights and the preference function chosen.

## Methodology

In this section the methodology we used is explained. For a more analytical describing of it, different weight scenarios and preference functions used can be seen in a previous research done using 10 countries and 10 indicators in : [`Previous Analytical Report 10 Countries 10 Indicators`](Previous%20Analytical%20Report%2010%20Countries%2010%20Indicators/Quality_Of_Life.pdf)

1. **Data collection:** Annual data for 20 European Union countries are retrieved from Eurostat. The period chosen is 2014-2023, using 13 indicators related to Quality of Life. 
2. **Data preparation:** Filtering the dataset dimensions, merging the dataset and organizing the observations by country-year. This creates a dataset with 200 country-year observations.
3. **Missing values:** Some indicators in Eurostat have missing values for some years. This makes us replace missing values with the corresponding country's mean for the corresponding indicator across the years of our analysis. 
4. **Average Scenario:** The average value of each indicator for every country over 2014-2023 is calculated, introducing as to a dataset of 20 alternatives for the overall country comparison in the 10 year range. 
5. **Criterion directions and weights:** Our Promethee II methodology needs to know which indicators need to be maximized or minimized to define, using the differences of the observations, if a difference > 0 is better for evaluating Quality of Life. Each criterion is defined as either maximized or minimized, depending on whether higher or lower values represent better Quality of Life. A specific weight vector is assigned representing the importance each indicator has for us. Different weights can be used, according to the corresponding analysts opinion in the significancy of each weight, with all weights summing to 1 though. 
6. **PROMETHEE II:** The PROMETHEE II Multi-Criteria Decision Analysis (MCDA) method is used to evaluate the alternatives through pairwise comparisons. For every indicator, the difference in performance between each pair of alternatives is calculated. We take into account if the criterion should be maximized or minimized. After this, using the preference functions, these differences are transformed into preference degrees, showing how strongly one alternative is preferred over another. After this, the netflows are calculated. The positive flow (Φ⁺), indicates how strongly one alternative is preferred over the others, while the negative flow (Φ⁻) indicates how strongly it is outranked by them. Their difference Φ⁺ − Φ⁻, produces the unicriterion netflows Φ (Φ = Φ⁺ − Φ⁻). These net flows are the final rankings we have but without using the weights that indicate how significant we think each criterion is. By multiplying the unicriterion netflows with their corresponding weights and summing them up, we obtain the global netflows, representing each alternative's overall relative performance.

7. **Preference functions:** The implementation supports six preference functions: 
- **Usual**: This criterion requires no parameters q, p, or s to fix 
indicating that even the smallest deviation among a pair of actions is taken into account in the final ranking. The preference degree takes either the value of 0 or 1. In case of 0 there is indifference 
between the actions showing that they are both considered equally preferred. In case of 1 there is an absolute preference of one action over the other. This criterion is the simplest but also useful 
when the decision maker can’t decide for the p and q values. Using this criterion made the PROMETHEE method fully comparable with TOPSIS and VIKOR since it does not require in this case the definition of the additional variables we introduced (q, p, or s).

- **U-Shape**: This criterion requires only the parameter q. The decision maker is able to create a value for the indifference threshold. As we said before, below this threshold, actions are indifferent to the decision maker. However, even the smallest value above the q parameter is crucial since the preference function instantly takes the value of 1. The function acts like a binary variable taking either 0 or 1. 

- **V-Shape**: This criterion requires only the parameter q. The decision maker is able to create a value for the indifference threshold. As we said before, below this threshold, actions are indifferent to the decision maker. However, even the smallest value above the q parameter is crucial since the preference function instantly takes the value of 1. The function acts like a binary variable taking either 0 or 1.

- **Level**: This criterion requires both p and q parameters. When the deviation is below q the preference degree is 0 and when its greater than p it is equal to 1. Any value between the thresholds means that the preference degree is equal to 0.5. Therefore, the preference function can only take the values 0, 0.5, 1. 

- **Linear**: This criterion is the same with the Level criterion but with the difference that the preference degree does not have a fixed value between the thresholds, being a Linear function acquiring any value between 0 and 1. 

- **Gaussian**: This criterion needs the decision maker to fix only the parameter s. If the deviation is less than or equal to 0, then the preference degree is 0. If on the other hand its greater than 0 then the preference degree has the value of 1-e((-d^2)/(2s^2)).

A single preference function is selected and applied across all 13 criteria for each execution. In our case the **Linear** function is mostly used and some differences are seen with the **Usual** one. For functions requiring thresholds, the indifference (q), preference (p), and Gaussian (s) parameters are calculated using the standard deviation of each criterion, with coefficients of 0.25, 0.75, and 0.45, respectively.

8. **Country ranking:** The 20 countries are ranked according to their global net flows, from highest to lowest. Higher netflows indicate stronger relative performance across the indicators chosen to represent Quality of Life.

9. **Yearly analysis:** The methodology used hear is the same used for the average scenario but now instead of 20 observations its done for 200 (country-year). This approach compares individual observations across the entire time range (2014-2023) providing additional insights over the decade. Here each country is compared even with it self but for a different year, for example Greece 2014 with Greece 2015. 

10. **Results and visualization:** An excel file, including final rankings for both scenarios is produced. Inside exist seperate sheets with each criterion (using the average scenario) with the difference,preference matrices and the unicriterion and weighted flows each indicator has. For the yearly scenario these matrices are big to visualize and interpret so only for 1 criterion is outputed (unemployment) only to have the methodology and each step printed for sensitivity analysis. In the final excel files (1 is for Linear method and the other for the Usual), 2 sheets have been made with visualizations for either the average or yearly scenario. Using our python script, indicator profiles for all 20 countries are generated to show their performance across all 13 criteria, alongside criterion-ranking charts to highlight differences between countries.


## Research Question Findings

The findings below are based on the outputs from the PROMETHEE II workbooks. The **Linear** scenario is used for detailed temporal and criterion-specific comparisons, with **Usual** as a preference-function sensitivity check. 

### RQ1 — Highest- and lowest-ranked countries (average scenario)

#### Country rankings — Usual preference function

![Usual Preference Function - Average Scenario](figures/Usual-Linear/Usual%20Function%20Average%20Scenario.png)

#### Country rankings — Linear preference function

![Linear Preference Function - Average Scenario](figures/Usual-Linear/Linear%20Function%20Average%20Scenario.png) 

As seen in the outputs above:

**Using the Linear Preference Function** in the first position is Denmark with a global net flow of 0.4620 with some difference from the countries in the following ranks. Austria (0.3988), Sweden (0.3773) and Luxembourg (0.3672) rank 2,3,4. The lowest-ranked countries are Croatia (−0.4140), Romania (−0.4532), and Greece (−0.7509).

**Using the Usual Preference Function** the first positions are more near to each other. Austria ranks first with a global net flow of 0.4905, closely followed by the Netherlands (0.4784), Denmark (0.4779) and Sweden (0.4747). The lowest-ranked countries remain Croatia (−0.4842), Romania (−0.5432), and Greece (−0.7442).

What we observe is that the highest-ranked countries change positions depending on the preference function (the reason will be explained further bellow), while the three lowest-ranked countries remain unchanged. Notably, Greece consistently ranks last, with a considerable gap from Romania in 19th place, indicating substantially weaker relative performance across the selected quality-of-life indicators. Using the Linear function, the first position becomes more "dominant" than using the Usual one in which the first positioned countries have more similar values.


### RQ2 — Highest- and lowest-ranked country-year observations (yearly scenario)

 #### Top 10 and Bottom 10 — Usual preference function

![Usual - Best and Worst Country-Year Observations](figures/Usual-Linear/Usual%20Function-Best-Worst-Yearly%20Scenario.png)

#### Top 10 and Bottom 10 — Linear preference function

![Linear - Best and Worst Country-Year Observations](figures/Usual-Linear/Linear%20Function-Best-Worst-Yearly%20Scenario.png)

As seen in the outputs above:

**Using the Linear Preference Function**, Denmark in 2022 achieves the highest global net flow of 0.4956, followed by Denmark in 2021 (0.4756) and 2023 (0.4736). On the other hand, Greece in 2014 records the lowest global net flow of −0.7425. Looking at the ten highest-ranked observations, Denmark appears 4 times, with no other country having more than 2 entries, while Greece occupies 9 of the last 10 positions, demonstrating its consistently weak relative performance.

**Using the Usual Preference Function**, the Netherlands in 2022 ranks first with a global net flow of 0.5941, followed by the Netherlands in 2023 (0.5857) and 2021 (0.5704). The lowest-ranked observation is Hungary in 2014, with a global net flow of −0.7655. Among the ten highest-ranked observations, the Netherlands appears 4 times, Austria 3 times and Denmark twice, while Greece appears again many times (7)   among the last 10 positions.

Overall, although the highest- and lowest-ranked observations differ between the two preference functions, Greece consistently dominates the bottom of the rankings, while Denmark, the Netherlands and Austria demonstrate strong performance across multiple years.

### RQ3 — Best and worst years by country

As seen in the individual country evolution charts in [`figures/Countries 2014-2023/`](figures/Countries%202014-2023/)

The following years correspond to the highest and lowest **global net flow for each country under the preference function chosen from the analyst (Linear)**.

| Country | Best year | Worst year |
|---|---:|---:|
| Austria | 2020 | 2015 |
| Belgium | 2023 | 2015 |
| Croatia | 2023 | 2014 |
| Czechia | 2023 | 2014 |
| Denmark | 2022 | 2014 |
| Finland | 2022 | 2015 |
| France | 2019 | 2014 |
| Germany | 2019 | 2014 |
| Greece | 2023 | 2014 |
| Hungary | 2023 | 2014 |
| Ireland | 2022 | 2014 |
| Italy | 2023 | 2014 |
| Luxembourg | 2023 | 2015 |
| Netherlands | 2022 | 2014 |
| Poland | 2023 | 2014 |
| Portugal | 2020 | 2014 |
| Romania | 2023 | 2014 |
| Slovakia | 2023 | 2014 |
| Spain | 2017 | 2014 |
| Sweden | 2023 | 2020 |

**2014 is the lowest-performing year for 15 of 20 countries** under Linear, whereas **2023 is the best for 11/20**. This suggests a general shift toward stronger relative scores in later years, although some countries peak earlier (for example, France and Germany in 2019 and Spain in 2017). 

It is **important to note** that the **yearly comparisons** are based on **a single PROMETHEE II analysis containing all 200 country-year alternatives** (20 countries × 10 years), rather than separate analyses conducted for each year. Consequently, the global net flows are calculated within the same evaluation framework, allowing comparisons of countries' relative performance across different years.


### RQ4 — Largest improvements or declines in the decade 

To examine changes in Quality of Life of the countries from 2014 to 2023 we will evaluate the difference of their global netflows in 2023 and 2014 **(ΔΦ(country) = Φ(2023) − Φ(2014))**. Under the preference function used (Linear) and while observing the visualizations in  [`figures/Countries 2014-2023/`](figures/Countries%202014-2023/):

| Country | ΔΦ (2014–2023) |
|---|---:|
| Hungary | +0.633 |
| Poland | +0.630 |
| Italy | +0.602 |
| Czechia | +0.570 |
| Croatia | +0.496 |
| Ireland | +0.484 |
| Portugal | +0.429 |
| Romania | +0.378 |
| Slovakia | +0.370 |
| Belgium | +0.343 |
| Netherlands | +0.283 |
| Austria | +0.226 |
| Denmark | +0.209 |
| Luxembourg | +0.196 |
| Spain | +0.150 |
| Greece | +0.112 |
| Germany | +0.102 |
| Finland | +0.083 |
| Sweden | +0.076 |
| France | +0.027 |

As seen above, Hungary, Poland, Italy and Czechia have the greatest improvements in our research between 2014 and 2023. In our study, **none of the 20 countries has a decline** over the decade. The smallest improvements though, belong to France, Sweden and Finland.

Overall, the findings suggest a general improvement in **relative Quality of Life performance** between 2014 and 2023, although the magnitude of improvement differs considerably across countries, since some countries even after huge improvement as a whole still score low in total rankings.

The overall improvement observed between 2014 and 2023 may partly reflect the economic recovery of several European countries following
the financial crises of the preceding years. This explanation though remains a hypothesis, since our methodology identifies differences in relative performance rather than establishing causal relationships. As we mentioned Quality of Life is multi dimensional and even 13 indicators are not enough to evaluate exactly its definition.


### RQ5 — Strengths and weaknesses

Using the visualizations bellow, we can examine how the 20 countries perform across the Quality of Life indicators chosen, under the Linear Preference Function.

1) [`figures/criterion_rankings/`](figures/Criteria%20Profiles%20Across%20Countries/)
2) [`figures/Country Profiles Across Indicators/`](figures/Country%20Profiles%20Across%20Indicators/)


| Country | Strong Performance | Weak Performance |
|---|---|---|
| **Netherlands** | Working hours (1st), unexpected expenses (1st), housing overcrowding (2nd) | Perceived criminality (20th), pollution (16th) |
| **Germany** | Difficulty making ends meet (1st), unemployment (2nd), arrears (3rd) | Perceived pollution (20th), criminality (16th) |
| **Croatia** | Perceived criminality (1st), pollution (1st) | Unexpected expenses (20th), arrears (19th), median income (18th) |
| **Luxembourg** | Median income (1st), GDP per capita (1st), tertiary education (2nd) | Perceived pollution (18th) |
| **Czechia** | Unemployment (1st), arrears (1st), housing deprivation (4th) | Tertiary education (18th), working hours (17th) |
| **Ireland** | Tertiary education (1st), housing overcrowding (1st), GDP per capita (2nd) | Unexpected expenses (16th), arrears (16th) |
| **Poland** | Perceived criminality (2nd), unemployment (4th) | Housing overcrowding (19th), working hours (19th), road fatalities (18th) |
| **Slovakia** | Housing deprivation (2nd), perceived criminality (3rd) | Housing overcrowding (17th), median income (16th), tertiary education (16th) |
| **Belgium** | Housing overcrowding (3rd), tertiary education (5th) | Housing deprivation (17th), perceived criminality (17th) |
| **Hungary** | Unemployment (3rd) | Median income (19th), housing deprivation (19th), GDP per capita (17th) |
| **Spain** | Housing overcrowding (4th), road fatalities (5th) | Unemployment (19th), housing deprivation (16th) |

The results reveal considerable differences in performance across individual Quality of Life criteria.


Overall, these results show that even if a country excels in some indicators it isnt evidence for believing they dont perform poorly in others. This highlights the importance of using an MCDA method such as PROMETHEE II, to evaluate countries by considering multiple economic, social, environmental and more indicators rather than relying only in common ones. Every country except Greece (ranks last in every indicator), ranks good in some indicators and poorly in others. This is also big evidence to how much the indicators affect the final ranking. Difference in the weights assignment would give also different weighted final netflows. For example imagine a country that excels in 2 indicators based on our research that we given weights w1,w2 but performs poorly in 3 others that we give weights w3,w4,w5 . If we made w1,w2 significantly smaller and w3,w4,w5 this would decrease a lot this countrys final ranking. This shows how important choosing the indicators is and also how sensitive our analysis can be when choosing weights and preference functions.

### RQ6 — Best and worst countries for each indicator
Using the visualization in [`figures/criterion_rankings/`](figures/Criteria%20Profiles%20Across%20Countries/), we constructed a table with the best and worst country in each criterion.
The table reports the highest and lowest **unicriterion net flows under Linear**, not necessarily the highest or lowest raw Eurostat value.

| Indicator | Best | Worst |
|---|---|---|
| Median income | Luxembourg | Romania |
| GDP per capita | Luxembourg | Romania |
| Difficulty making ends meet | Germany | Greece |
| Housing deprivation | Finland | Portugal |
| Housing overcrowding | Ireland | Romania |
| Unemployment | Czechia | Greece |
| Unexpected expenses | Netherlands | Croatia |
| Arrears | Czechia | Greece |
| Perceived criminality | Croatia | Netherlands |
| Perceived pollution | Croatia | Germany |
| Working hours | Netherlands | Greece |
| Tertiary education | Ireland | Romania |
| Road fatalities | Sweden | Romania |

No single country leads across all 13 Quality of Life indicators, which is understandable given the multidimensional nature of Quality of Life. As shown in the previous research question, each country has its strengths and weaknesses. 

### RQ7 — Sensitivity analysis in Preference Functions and Weights

Choosing a preference function plays a vital role in the PROMETHEE II methodology, since this is how the differences between the countries we compare, are translated into preference degrees. 

The **Usual Preference Function** assigns full preference provided that one alternative performs better than the other. This happens even when the difference is extremely small.

In contrast, the **Linear Preference Function** uses thresholds to evaluate the significance of these differences. If the difference is smaller than the threshold q we choose, there is no preference of the one alternative over the other. If its between the thresholds q,p then there is partial preference (equal to (d-q)/(p-q) ). If the difference is bigger than the threshold p then there is full preference.

Comparing the results obtained using these two functions reveals several differences in the final rankings:

- **Denmark** ranks 1st under Linear but 3rd under Usual.

- **Austria** ranks 2nd under Linear but 1st under Usual.

- **The Netherlands** ranks 6th under Linear but 2nd under Usual.

- In the yearly scenario, **Denmark–2022** achieves the highest global net flow under Linear, while **Netherlands–2022** ranks first under Usual.

In the average scenario the **same ten countries** occupy the first ten positions, while the **same three countries** occupy the bottom three positions. This shows that changing the preference function might change the general rankings but not in ways that for example the 1st country in one scenario will be made 10th in the other one.

PROMETHEE II provides 6 commonly used preference functions as we mentioned. The main one used in this research was the Linear one as it provided a more flexible and gradual evaluation of the differences between countries. The Usual function was used as a comparison to demonstrate how changing the preference functiion can influence the final rankings, while also identifying results that remain relatively consistent.

Another important component of our PROMETHEE II methodology is **selecting criterion weights**. In this study, the weights were chosen depending on how important the analyst things each of them is. Higher values for weights give greater influence to the corresponding criteria, while lower reduces the influence to the overall evaluation. Changing the weights can affect the final rankings, since different combinations represent different perspectives in the significancy of each criteria and how much the final netflows are weighted. These findings highlight that **PROMETHEE II rankings depend not only on the data used but also in the choices made from the analyst**. This includes preference functions, thresholds, indicators and their weighting.

## Repository structure

```text
europe-quality-of-life-promethee-complete
├── Analysis.md
├── requirements.txt
├── Python File/
│   └── PROMETHEE-II-Quality-Of-Life-Final.py
├── Previous Analytical Report 10 Countries 10 Indicators/
│   └── Quality_Of_Life.pdf
├── figures/
│   ├── Countries 2014-2023/
│   ├── Country Profiles Across Indicators/
│   ├── Criteria Profiles Across Countries/
│   └── Usual-Linear/
└── results/
    ├── Quality_Of_Life_EU_Linear_Function.xlsx
    └── Quality_Of_Life_EU_Usual_Function.xlsx
```

The source code and figures are included in the folders shown above.

## How to run

1. Install Python and the required packages listed in `requirements.txt`.
2. The included main script uses pandas, NumPy, Matplotlib, openpyxl and the `eurostat` package.
3. Run the analysis script from the project root:

   ```bash
   Python File/PROMETHEE-II-Quality-Of-Life-Final.py
   ```

4. Choose a preference function when prompted. The script retrieves data from Eurostat, calculates the rankings and generates the configured outputs.


## Conclusion

This research was done to observe and compare Quality of Life across several European Union countries over a 10-year period (2014-2023). A Multi-Criteria Decision Analysis method (PROMETHEE II) was performed. For the analysis, 2 scenarios were compiled. One for aggregated data using the mean values of every criterion over the 10-year period so that we could compare the overall average performance of each country and the other for a yearly comparison using every country in every year of this decade. While comparing the countries performance, six difference preference functions are available from which one was chosen as the main one (Linear), while a second one was used for sensitivity analysis. Weights were assigned according to the researcher doing this project, while if wanted they can change for further analysis. 
The findings demonstrated that countries such as Denmark, Austria Sweden and Luxembourg are consistent among the first places in the final ranking while Greece, Romania and Hungary rank most of the times the lowest. A tough year for most of the countries was 2014 since most of them had their lowest well-being scores in this year and a crucial observation was that Hungary, despite starting from the lowest ranking in 2014, had the most improvement in the decade. By using 2 different preference functions, we saw that rankings are affected. This happened because the Usual function takes into account even the smallest difference between 2 criteria when computing the preference between 2 countries while this doesn't happen in the other functions (for example the Linear one we used) because thresholds exist above/bellow which a difference is statistically significant. The weights used came from the researchers view. By choosing different ones there are differences on the outputs and this happens because by evaluating each indicator differently, the final rankings are affected since we proved that there are countries that excel in some indicators but perform poorly in others. This also showed why it is important to use a multidimensional approach when evaluating Quality of Life but also being careful in how each indicator is weighted depending on what criteria we think is most crucial in well-being.  
Overall, this research shows the value of the PROMETHEE II methodology in handling complex concepts such as Quality of Life. 

## Limitations

- **Country selection:** The analysis includes 20 EU member states, meaning the results should not be generalized to all European countries. However, since the project is flexible, the users can expand the analysis by adding more countries to the Python script and running it again to generate new outputs, provided the required Eurostat data exist. 

- **Criteria, weights, and preference functions:** The results of our analysis depend as we mentioned in the indicators, the weights we assign and the preference function chosen. Different choices may lead to different rankings. Users can experiment with alternative preference functions by selecting from our Python script a different one, or adjust the indicator weights of preference according to their own liking, ensuring though that their sum remains equal to 1. 

- **Subjective indicators:** Crime and Pollution indicators, show people's perception of them rather than objective measurements of these criteria.

- **Average-Yearly:** Using the average scenario over 2014-2023 we tried to create an overall look of the country over the 10 years and compare each one with the rest. To see how individual countries perform over the decade each year, we created the yearly scenario. However, this approach increased the number of alternatives 10 times (20->200), making the visualizations and comparisons used in the average scenario more complex. 

- **Relative rankings:** Our PROMETHEE II global netflows represent relative performance among the alternatives included in the research. They should not be interpreted as absolute measures of Quality of Life . Adding or removing countries can change the final rankings.

## Recommendations

1.	Different Weight Determination
Future studies should conduct a large-scale survey questioning the significancy of each of the indicators. Doing this, a greater number of participants could take place and this would allow for a more representative result in creating weights for each of the indicators. This could give a different approach than this research showing how multi-dimensional the concept of Quality of Life, and PROMETHEE II MCDA method is.
2.	More expanding Set of Indicators
This study used 13 indicators focused on economic, material, criminality and pollution aspects. It would be wise to expand the criteria to include more dimensions, such as physical health, mental well-being, access to services and more. As we mentioned in the limitations, Quality of Life is so complex that even our 13 criteria are not enough to describe it as a concept. By having more indicators and from different dimensions, this would broaden our view in Quality of Life since we saw how multi-dimensional it is.
3.	Include all EU Countries 
This research used 20 different European Union countries that scored differently across the indicators chosen. It could be scaled up to cover all members of the European Union to observe the overall Quality of Life ranking in Europe.
4.	PROMETHEE vs Other MCDA Methods
It would be wise to extend this research in using other MCDA methods such as TOPSIS, ELECTRE and the others we mentioned so that we could compare the results and see the differences between them.
5. Extension of the Time Period
The present analysis covers the period from 2014 to 2023. Future studies could extend the dataset to include more recent years as new Eurostat observations become available.
This would allow researchers to investigate whether the improvements observed in several countries continue over time and whether their relative Quality of Life rankings change.



## Data source

**Eurostat** — European statistical data: https://ec.europa.eu/eurostat

For reproducibility, document the exact Eurostat dataset codes, dimensions and units used for each criterion in the source code or a separate data dictionary.

## Project purpose

This is a personal data analytics portfolio project demonstrating data acquisition, preprocessing, multi-criteria decision analysis, sensitivity analysis, visualization and interpretation using Python and Excel.

## Included Files
1) The charts used for visualising both scenarios for Quality of Life are available in [`figures/Usual-Linear/`](figures/Usual-Linear/)
2) Individual country evolution charts are in [`figures/Countries 2014-2023/`](figures/Countries%202014-2023/)
3) The complete set of 20 country profiles across indicators is available in [`figures/Country Profiles Across Indicators/`](figures/Country%20Profiles%20Across%20Indicators/)
4) The complete set of 13 Criteria Profiles Across Countries is available in [`figures/criterion_rankings/`](figures/Criteria%20Profiles%20Across%20Countries/)
5) The 2 excel files for Linear and Usual preference are available in [`results`](results/Quality_Of_Life_EU_Linear_Function.xlsx)
[`results`](results/Quality_Of_Life_EU_Usual_Function.xlsx)
6) The python script used is available in [`Python File`](Python%20File/PROMETHEE-II-Quality-Of-Life-Final.py)
7) The analytical report used in a previous research for more understanding of the theoritical part of our analysis is available in [`Previous Analytical Report 10 Countries 10 Indicators`](Previous%20Analytical%20Report%2010%20Countries%2010%20Indicators/Quality_Of_Life.pdf)


**Note:** The Excel workbook is provided as an existing export. The preference comparison images were supplied separately and are not generated automatically by the included script in one run; choose `u` for Usual function or `li` for Linear, for separate runs.
