This project was part a multi-geography programme where Global tools produced the data in the form of JSON Semi-structured format.
The whole content of the JSON was the outcome of an event driven architechture that produced polices to "Bill" in servicing platforms for each local country.
I helped with the adoption of these logics by using this file in Spain, Portugal and Italy ( where I was the Data Analyst in charge of analyzing and coding the Python Parser);
as well as help later countries like Netherlands, Ireland, Germany with the logics successfully implemented in the 3 countries above.

The content of the Python Parser, helps decript the JSON structure by understanding the structure needed by the Servicing Platforms of Policy data and organizing that content in the scenario of:
 - New Business Polices
    -  Coinsurance - Leader & Followers
    -  Multiple Risks
    -  Multiple Layers
    -  Grouped/Combined Risks
 - Renewals Tacit and Marketing
 - Cancelations upon renewal
 - Mid Term Adjustments (MTAs)

This python file also helped to retrived key data for the company to identify Carriers, Clients, Products, etc...
The complexity of this document is also noticeable in the way the iterations are produced in orders to build and compare negotiations to calculate deltas of ammounts (MTAs).
