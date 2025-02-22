# github-user-activity

## Project URL for roadmap.sh project
https://roadmap.sh/projects/github-user-activity

## Setup

1. Clone repository:

    ```bash
    git clone https://github.com/Anele-e/github-user-activity.git

2. Navigate to the project directory:

    ```bash
    cd github-user-activity
    ```

3. Install the 'virtualenv' package in python if you do not have one.

    ```bash
    pip install virtualenv
    ```

4. Create a virtual environment. 'venv' is an optional name

    ```bash
    virtualenv venv
    ```

    Python 3.3 or newer 

    ```bash
    python -m venv venv
    ```
5. Activate the virtual environment

    On Powershell
    ```bash
     .\venv\Scripts\Activate.ps1

    ```
    On Unix or MacOS:

    ```bash
     source venv\Scripts\activate

    ```

## To run program

In the command line/Terminal run the command below with your github username

```bash
python user_activity.py <username>

```

To get an output similar to the one below

```bash
Output:
- Pushed 3 commits to kamranahmedse/developer-roadmap
- Opened a new issue in kamranahmedse/developer-roadmap
- Starred kamranahmedse/developer-roadmap
- ...
```

