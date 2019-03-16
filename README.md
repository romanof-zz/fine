FiNePPL (aka this group) was created as a trial for an idea, that FiNePPL can make in better financial decisions together.

## Goals

- Help educate FiNePPL around latest financial tools and mechanisms.
- Help FiNePPL reach their personal financial goals.
- Grow FiNePPL.

## Rules

- **Privacy** FiNePPL is a private group, shouldn't be discussed outside of FiNe (except with direct family members).
    - _immediate termination_
- **Security** keep artifacts of FiNe private and secure.
    - _termination, if violation was done consciously_
- **Contribute** everyone needs to contribute in order to benefit.
    - _termination after 1 month with no contributions to FiNe_
- **Equality** we treat members with respect and as equals.
    - _when 50%+1 members of the group agree and every group member is aware of the decision, they can add new members to the group_
    - _when 100% members of the group agree, they can change this README_
    - _when 100%-1 members of the group agree on termination decision, they can terminate the one who disagrees_

## Project Tracking

FiNePPL would likely work on multiple projects simultaneously. I don't think it makes sense to track them in separate Trello boards (at least while group is small). So lets use one in this project, and tag each individual project with tags listed bellow in **[...]**

### Projects

- [Bet] FiNeBet: https://bitbucket.org/fineppl/fine-bets/src
- [Emo] Sentiment Analysis: https://bitbucket.org/fineppl/fine-sentiment/src
- [Algo] Algorithmic Trading: https://bitbucket.org/fineppl/fine-algos/src

## Cross-cutting ideas

### Signal Aggregation across projects.

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

## Setup

```
mkdir fine && cd fine &&
git clone git@bitbucket.org:fineppl/fine.git &&
git clone git@bitbucket.org:fineppl/fine-algos.git &&
git clone git@bitbucket.org:fineppl/fine-bets.git &&
git clone git@bitbucket.org:fineppl/fine-sentiment.git
```
