# Graphic Card Trading Simulation
## Overview
This project simulates a market for trading graphic cards, where multiple agents participate by buying and selling based on different strategies. The simulation aims to model market dynamics and agent behaviors over many iterations. In reality, it's an exercise to show, at least to some extent, coding performance and good practices.

I will now give an explanation of my decision process.

Regarding the directory tree, the use of /src allows to easily distinguish between application code and other files such as configuration or tests. It also prevents namespace conflicts. The /agents, /markets and /simulators folders follow domain naming, just like most of the modules they contain, to have the correct meaning in it's context and avoid general words. The /tests folder mirrors the structure of the /src folder to facilitate tracking which modules test which, and be able to quickly jump between each other.

Module and class division have followed modularity and single responsibility, so each context is self-contained and dependencies are minimized. When these dependencies exist between classes, each one has defined an interface that encapsulates internal changes. An example of this is the buy operation that links the agents with the market. Instead of heavily coupling the agent class with the market class by making market changes on the buy method of the agent, a buy method in the market class is called and the agent class allows the market class to know what buying something implies to it. A Mediator pattern has also been applied with the Simulator class, to aggregate the relations that might superseed and entangle the market and the agents, such as for example the iteration management. Inheritance is used in the agents domain, as core behavior can be extracted from each of the specific agents into a base class, preventing code duplication and promoting reusability. If the specification was extended in the future, other base classes could be extracted from the CardMarket and the Simulator, but following the YAGNI principle, we shouldn't anticipate these facts as they may never occur, plus it's not obvious which ones could be the common parts. In addition to that, more child classes could follow, respecting the open/closed principle. Composition is used in the Simulator class, as it is composed by market and agents classes. Also, the way Simulator interfaces with the parent BaseAgent class allows for polymorphism when calling the perform_action method.

Testing is crucial, as it guarantees specification compliance and enables refactoring. Without it, we wouldn't be able to know if the real behavior of the system matches the expected one. Also, any future changes to the code could mean breaking the previous solution and thus be avoided, something that would inevitably imply code deterioration up to an unsustainable point.

Using a virtual environment and a package manager is almost taken for granted nowadays, which is good news, but we shouldn't forget of it's importance. In order to ensure that the application can work from scratch, and that no very particular state of affairs in a certain machine is what allows it to do so, virtual environments allow to fix the application dependencies and encapsulate them, making it easy to reproduce the necessary context elsewhere.

Typing prevents errors and helps define better interfaces, while making development easier along the way. Licensing is also encouraged for legal protection and promotes clarity of contribution, if expected.

A non-exhaustive summary of several good practices in this project:
- Encapsulation
- Inheritance
- Polymorphism
- Composition
- Single responsibility
- Error handling
- Testing. With high coverage and test isolation.
- Logging
- Performance. For both the application and tests.
- Tooling. For standardize style, format, linting and security.
- Version control with Git
- Tpying annotation
- Docstring documentation at the module, class and method level
- Licensing
- Dependency management with both open and fixed versions
- Project configuration standardization with .toml file
- README file

The project could be extended with e.g.:
- Dockerization
- Pre-commit hooks
- Doit or Makefile tasks
- .env file for certain variables extraction
- Further parametrization
- Versioning, with a CHANGELOG file
- Simulation data visualization
- Improved custom agent algorithm

## Project Structure
The project is organized as follows:

**agents/**: Contains all the agent classes representing different trading behaviors.

**markets/**: Contains the market where the stock and price is tracked and on which agents trade. 

**simulators/**: Contains the simulator to run the market-agents iterations. Over each iteration agents are first shuffled and then all perform an operation sequentially.

**tests/**: Contains unit tests for all major components of the project.

## Setup
### Prerequisites
Python 3.11 or higher

pipenv for managing Python packages

## Installation

### Clone the repository
git clone https://github.com/jmirallesdemiguel/card-market-simulator
### Create a Virtual Environment and install the dependencies:
pipenv install

## Usage
Navigate to the project root directory and run the main simulation script:

python src/main.py

## Understanding the Classes
### Markets

- **CardMarket**: Manages the stock and pricing of graphic cards, with methods to handle buying and selling.

### Agents

- **BaseAgent**: Base class defining the core functionality of an agent.

- **CustomAgent**: Implements a strategy that adjusts its actions based on market trends to maximize final cash balance.

- **RandomAgent**: Chooses randomly whether to buy, sell, or do nothing.

- **TrendContrarianAgent**: Buys when the price is dropping and may sell or do nothing otherwise.

- **TrendFollowerAgent**: Buys when the price is rising and may sell or do nothing otherwise.

### Simulators

- **Simulator**: Aggregates a market and a list of agents and performs a trading simulation over a certain number of iterations. In each iteration the agent list is shuffled and then each agent performs it's action sequentially. Keeps track of the previous iteration final price and informs the market.

## Testing
To run the unit tests, ensure you are in the project root directory and use pytest.

This will execute all the tests under the tests/ directory and provide a summary of the results.

Please ensure your code adheres to the project’s coding standards and includes relevant tests.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

