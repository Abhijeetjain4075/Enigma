# Open-Source Competitive Audit — 2026-09-30

## SteVe
Established open-source OCPP server/CSMS demonstrating that basic OCPP control infrastructure is not inherently proprietary.
https://github.com/steve-community/steve

## CitrineOS
Modular open-source OCPP 2.0.1 CSMS with separated modules and message-broker architecture.
https://github.com/citrineos/citrineos

## OpenCPO
Open-source charging platform combining OCPP 1.6/2.0.1 CSMS, admin, driver PWA, charger simulator, tester, PKI and OCPI roaming.
https://github.com/opencpo/opencpo

## EVtivity
Publicly describes OCPP 1.6/2.1, OCPI 2.2.1/2.3.0, ISO 15118 Plug & Charge, REST APIs and operational AI.
https://github.com/EVtivity/evtivity-csms

## gocpp
Public Go library covering OCPP 1.6, 2.0.1 and 2.1 with typed APIs and schema validation.
https://github.com/shiv3/gocpp

## Strategic implication

Enigma's implementation moat cannot simply be:
- OCPP server
- CSMS
- OCPI server
- charger simulator
- driver app
- billing dashboard

These are already available from commercial and/or public implementations. Enigma should consume such infrastructure where appropriate and focus engineering effort on its experimentally validated residual workflow.