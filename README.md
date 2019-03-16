FiNePPL (aka this group) was created as a trial for an idea, that FiNePPL can make better financial decisions together.

## goals

- Help educate FiNePPL around latest financial tools and mechanisms.
- Help FiNePPL reach their personal financial goals.
- Grow FiNePPL.

## rules

- **equality.** we treat members with respect and as equals.
    - _when 50%+1 members of the group agree and every group member is aware of the decision, they can add new members to the group_
    - _when 100% members of the group agree, they can change this README_
    - _when 100%-1 members of the group agree on termination decision, they can terminate the one who disagrees_
- **contribute.** everyone needs to contribute in order to benefit.
    - _termination after 1 month with no contributions to FiNe_
- **security.** keep artifacts of FiNe private and secure.
    - _termination, if violation was done consciously_
- **privacy.** FiNePPL is a private group, shouldn't be discussed outside of FiNe (except with direct family members).
    - _immediate termination_

## projects

- [Bet] FiNeBet: https://bitbucket.org/fineppl/fine-bets
- [Emo] Sentiment Analysis: https://bitbucket.org/fineppl/fine-sentiment
- [Algo] Algorithmic Trading: https://bitbucket.org/fineppl/fine-algos


## cross-cutting

### prioritized commodities

Commodity could be a stock unit, option of the following companies.

> stated here as a point of reference, intended to be used in multiple projects.

- Amazon
- Microsoft
- Alphabet
- Apple
- Facebook

### signal aggregation across projects

if trading decision of various projects tracked in the same data format, like

```
- project id
- financial commodity id
- timestamp
- decision sell / buy
- confidence level
```

we can train a statistical model, that would assign weights to specific FiNe projects.
and would be making a aggregated sell/buy decision, when overall model confidence reaches predetermined threshold.

they you give this model a certain budget a let it trade.
goal for the model could be to beat SP500 for a given month.

trading data that model produces can be also re-annotated and fed back to the training set.

## setup

```
mkdir fine && cd fine &&
git clone git@bitbucket.org:fineppl/fine.git &&
git clone git@bitbucket.org:fineppl/fine-algos.git &&
git clone git@bitbucket.org:fineppl/fine-bets.git &&
git clone git@bitbucket.org:fineppl/fine-sentiment.git
```
