Idea is to find correlation between different informational sources, that could influence the market and stock price changes.

## data mining

### stock tickers

- 5 min market tickets for following commodities https://bitbucket.org/fineppl/fine/src/master/#markdown-header-prioritized-commodities

### twitter feed bot

To start create an account and follow a list of X predefined news makers accounts.

- process 1 (every 5 min):
    - check feed and search for terms denoting the commodity from the list.
    - if found -> store the tweet with timestamp and account id and commodity id.
- process 2 (every month):
    - if no tweet observed for a month -> unfollow account.
- process 3 (every 1d) (optional):
    - check every following account's followers.
    - check their feed and see if last 50 tweets contained data about any of the commodities.
    - if found: subscribe.

## analysis

### analysis1

- do tf/idf on terms in the stored tweet => cluster => get top 10 excluding stop-words.
- check the corresponding ticket change for a commodity.
- associate change in price as a positive/negative weight of the terms.
- to this analysis for a month of data -> check top positive and top negative terms.
