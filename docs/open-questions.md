# Open Questions

## Market

1. What exact customer has the strongest willingness to pay?
2. CPO, eMSP, OEM, fleet, developer, or consumer?
3. Which country has the best initial integration economics?
4. What regulatory requirements apply to the chosen transaction model?

## Network

5. Which providers expose usable APIs?
6. Which providers permit third-party transaction initiation?
7. Which providers require commercial contracts?
8. Which roaming hubs provide the broadest useful coverage?
9. Where are direct integrations superior to hub integrations?

## Payments

10. Can Enigma legally intermediate funds in each target market?
11. Should Enigma use licensed payment providers rather than become a regulated payment intermediary?
12. How should refunds and disputes work?
13. How should taxes and invoices be represented?
14. How should cross-border settlement work?

## Identity

15. What is the canonical identity of a vehicle?
16. How should one user control multiple vehicles?
17. How should fleets delegate authorization to drivers?
18. How should OEM identities map to Enigma identities?
19. What privacy boundaries are required?

## Reliability

20. How can provider-reported availability be independently validated?
21. Can transaction outcomes produce a reliable network health signal?
22. How should stale data be detected?
23. How should conflicting provider data be resolved?

## Architecture

24. Which operations require synchronous APIs?
25. Which should be event-driven?
26. What must be idempotent?
27. How should provider-specific semantics be normalized?
28. How should versioning work when external standards evolve?

## Expansion

29. Which adjacent service has the strongest reuse of the charging architecture?
30. When should parking, tolls, maintenance, fleets, and energy be introduced?
31. What common primitives can serve all of them?

## Competitive

32. What can Hubject-like roaming hubs already solve?
33. What can Indian aggregators already solve?
34. What do OEM platforms solve internally?
35. Which gap remains after combining existing standards and providers?

## Strategic test

The most important question is:

**If existing roaming hubs, eMSPs, OEMs, and aggregators were connected together tomorrow, what valuable problem would still remain?**

Enigma should be built around the answer, not around the existence of fragmentation alone.