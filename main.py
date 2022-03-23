import abstractive

from_audio = """And also, uh, as we discussed about the probability concept, the probability is one of the major concept over here. Randy, so this is basically called as the basic process of conditional probability that probability of a given B, that is the thing which we are trying to identify sometime we might have some additional information. Let's say we have, let's say, apart from the cavity and all, we have something called as weather is sunny, so the traditional information may be relevant, may not be relevant, is not mandatory, that water the information you're catching at a particular point of time because we all are dealing with partially observable system that I already told you in my last class."""

summary = abstractive.summarize(from_audio)

print(summary)