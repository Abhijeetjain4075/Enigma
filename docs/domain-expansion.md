# Enigma Domain Expansion Matrix

## Purpose

Expansion should be driven by primitive reuse, transaction value and residual fragmentation.

| Domain | Existing Enigma primitives | Key operations | New risks |
|---|---|---|---|
| EV charging | Provider, Asset, Capability, Identity, Authorization, Session, Transaction, Money | discover, quote, authorize, start, stop, bill | physical action, energy measurement |
| Parking | Provider, Asset, Availability, Reservation, Authorization, Transaction | discover, reserve, enter, exit, pay | location, reservation conflicts |
| Tolls | Provider, Vehicle, Identity, Authorization, Money | identify, charge, dispute | legal/tolling rules |
| Maintenance | Provider, Service, Reservation, Transaction | quote, book, fulfil, invoice | service quality/liability |
| Roadside assistance | Provider, Identity, Vehicle, Journey, Service | request, dispatch, fulfil | emergency/safety |
| Battery swapping | Provider, Asset, Capability, Session, Money | reserve, authorize, swap, bill | inventory/asset identity |
| Home energy | Asset, Capability, Authorization, Money, Journey | schedule, optimize, settle | energy regulation |
| V2G/DER | Vehicle, Asset, Capability, Authorization, Session, Money | dispatch, meter, settle | grid rules, energy measurement |

## Addition gate

A domain is eligible only when:

1. core primitives can represent it without semantic distortion;
2. provider permissions are available;
3. the transaction has measurable value;
4. legal responsibility is understood;
5. failure recovery is possible;
6. economics support integration cost.

## Anti-pattern

Do not expand merely because an API exists.
