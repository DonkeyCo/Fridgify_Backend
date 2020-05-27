# Fridgify_Backend
Fridgify's Backend repository

![Code coverage](coverage/coverage.svg?) 

![Docker hub builds](https://img.shields.io/docker/cloud/build/fridgify/fridgify)
![Docker hub automated builds](https://img.shields.io/docker/cloud/automated/fridgify/fridgify)

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/a12a694e4db141db8ad32441a7a89dce)](https://www.codacy.com/gh/Fridgify/Fridgify_Backend?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Fridgify/Fridgify_Backend&amp;utm_campaign=Badge_Grade)

| Production   |      Development |
|:----------:|:-------------:|
| ![Docker image size production server](https://img.shields.io/docker/image-size/fridgify/fridgify/latest) |  ![Docker image size develop server](https://img.shields.io/docker/image-size/fridgify/fridgify/develop-latest)  |
| ![Docker version production server](https://img.shields.io/docker/v/fridgify/fridgify/latest?color=blue) | ![Docker version production server](https://img.shields.io/docker/v/fridgify/fridgify/develop-latest?color=blue) |
| ![Teamcity build production](https://img.shields.io/teamcity/build/e/Fridgify_DeployFridgifyProduction?server=https%3A%2F%2Ffridgify-tc.donkz.dev) |    ![Teamcity build production](https://img.shields.io/teamcity/build/e/Fridgify_DeployFridgifyDevelopment?server=https%3A%2F%2Ffridgify-tc.donkz.dev)   |
| [![Teamcity build production](https://img.shields.io/website?label=documentation&url=https%3A%2F%2Ffridgapi-dev.donkz.dev%2F)](https://fridgapi.donkz.dev/) |    [![Teamcity build production](https://img.shields.io/website?label=documentation&url=https%3A%2F%2Ffridgapi-dev.donkz.dev%2F)](https://fridgapi-dev.donkz.dev/)   |

### Notes for Development
When using Behave, you have to navigate to the tests folder and run *behave* in the
console window to ensure everything working correctly. This has to be thought of when
automating testing. (That is actually stupid. But hey, who am I to say something is
stupid.)