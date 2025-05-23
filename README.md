# WeSave Backend Challenge - iSave

## Requirements

- `python` version 3.8
- `sqlite3`

## Intro

Welcome to the WeSave Tech Challenge! Your task is to build the backend of a web app, iSave, that helps clients manage their investments based on their financial goals. The core of this application is based on portfolio management and financial indicators.

## Submission Instructions

- Clone this repo (do not fork it)
- Implement the features described above.
- Solve the levels in ascending order
- Write tests to cover the implemented functionality.
- Ensure your code is well-documented. It is expected that you provide information on how to start off the application and to use the API.
- You can do as many commits as you would like for each level. Every commit should follow the [Conventional Commit Standard](https://www.conventionalcommits.org/en/v1.0.0/), i.e:

```txt
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

example:

```txt
chore(Init): this is the first commit

Add the basic requirements to the application

Level-1
```

## Evaluation Criteria

Your submission will be evaluated based on:

- Functionality: How well does the backend meet the requirements?
- Code Quality: Is the code well-organized, commented, and maintainable?
- Testing: Are there adequate tests to ensure the functionality is correct and reliable?

## Sending Your Results

Once you are done, please send your results to your correspondent from WeSave. You can send your Github / Gitlab / Bitbucket project link or zip your directory and send it via email. If you do not use Github / Gitlab / Bitbucket, do nit forget to attach your `.git` folder.

## The Challenge

In the `LEVELS.md` file, you will find 5 levels, each giving you a task to achieve by writing code, with increasing difficulty.

Your goal is to do as many levels as possible within the given time frame and showcase your hacker skills.

## Pointers

You can have a look at the higher levels, but please do the simplest thing that could work for the level you're currently solving.

The levels become more complex over time, so you will probably have to re-use some code and adapt it to the new requirements.
A good way to solve this is by using OOP, adding new layers of abstraction when they become necessary and possibly write tests so you don't break what you have already done.

Don't hesitate to write shameless code at first, and then refactor it in the next levels.

For higher levels we are interested in seeing code that is clean, extensible and robust, so don't overlook edge cases, use exceptions where needed, ...

Please also note that:

- Authentication is not necessary in this application.
- You are allowed to use any publicly available gems.
- All amounts are to be stored as decimal.
- All asset prices are defined in the same currency.

**Good luck!**

## Setup and run the app

1. Clone the repository:
   ```sh
   git clone https://github.com/CamilleClipet/wesave_test
   cd wesave_test
   ```

2. Start the application using Docker Compose:
    ```sh
    docker-compose up --build
    ```

3. Open a shell in the Docker container
    ```sh
    docker-compose exec web sh
    ```
4. Load the json data
    ```sh
    python -m app.scripts.load_json
    ```

## Level 1

Visit http://localhost:5001/portfolios/

## Notes

Thank you for giving me the chance to do this test.

I tried to not spend too much time on it and it stops at level 2. Because it was on such short notice I picked Flask / SQLalchemy over Ruby, I hope you don't mind. It took me a little while to respawn a containerized Flask project as I don't create projects from scratch in my day-to-day. I helped myself with ChatGPT for that.
I took the liberty of changing the json data because the amounts didn't add up (amount in portfolio != sum of investments amounts).

Now, for what's missing that I'm aware of:
- typing
- end-to-end tests
- automatic linting / reformatting (I tried to do it as I go)
- some refactoring to put come code / methods in common in the business logic such as making sure the investment exists, checking the amount against the investment's amount...
- I realised mid-test I was confusing a contract with a portfolio (and assumed there was only 1 portfolio), hopefully there shouldn't be residual issues / mistakes from that.
- I don't know if you expected more views? Btw I went with port 5001 because my own port 5000 was unavailable due to processes I couldn't kill.
- I probably could have managed the project with uv to save me some hassle but I thought of it mid-test
- Of course the whole logic changes if there are several customers

Thank you in advance for reading.
